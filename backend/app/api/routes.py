from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.auth import verify_credentials
from app.config import TradingMode, get_settings
from app.db import get_db
from app.models import Campaign, Competitor, DecisionLog, EquitySnapshot, OrderRow
from app.modules.data.demo_provider import UNIVERSE, DemoDataProvider
from app.modules.experiments.runner import ExperimentRunner, prompt_hash
from app.modules.reports.generator import build_campaign_report_html, build_campaign_report_json

router = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_credentials)])


class CampaignCreate(BaseModel):
    name: str = "Campagne démo LLM Trading Lab"
    mode: TradingMode = TradingMode.DEMO


class RunStepRequest(BaseModel):
    as_of: datetime | None = None


@router.get("/health")
def health():
    s = get_settings()
    return {
        "status": "ok",
        "trading_mode": s.trading_mode.value,
        "execution_engine": s.execution_engine,
        "version": s.app_version,
        "simulation_banner": "SIMULATION — ARGENT FICTIF",
    }


@router.get("/data/universe")
def universe():
    data = DemoDataProvider()
    df = data.load()
    return {
        "symbols": UNIVERSE,
        "rows": len(df),
        "from": df["event_time"].min().isoformat(),
        "to": df["event_time"].max().isoformat(),
    }


@router.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)):
    items = db.query(Campaign).order_by(Campaign.created_at.desc()).all()
    return [
        {
            "id": str(c.id),
            "name": c.name,
            "mode": c.mode,
            "status": c.status,
            "initial_capital": str(c.initial_capital),
            "execution_engine": c.execution_engine,
        }
        for c in items
    ]


@router.post("/campaigns")
def create_campaign(body: CampaignCreate, db: Session = Depends(get_db)):
    settings = get_settings()
    if body.mode != settings.trading_mode:
        raise HTTPException(400, "TRADING_MODE serveur incompatible avec la campagne demandée")
    camp = Campaign(
        name=body.name,
        mode=body.mode.value,
        initial_capital=Decimal("100000"),
        ai_budget_usd=Decimal("50"),
        execution_engine=settings.execution_engine,
        config={
            "universe": UNIVERSE,
            "max_positions": 6,
            "max_weight": "0.25",
            "prospective_weeks": 8,
        },
    )
    db.add(camp)
    db.flush()
    ph = prompt_hash()
    for i, label in enumerate(("Momentum-A", "EqualWeight-B", "Defensive-C")):
        db.add(
            Competitor(
                campaign_id=camp.id,
                name=label,
                provider="demo",
                model_id=f"deterministic-{i}",
                cash=Decimal("100000"),
                prompt_hash=ph,
            )
        )
    db.commit()
    db.refresh(camp)
    return {"id": str(camp.id), "name": camp.name}


@router.post("/campaigns/{campaign_id}/run-step")
def run_step(campaign_id: UUID, body: RunStepRequest, db: Session = Depends(get_db)):
    camp = db.get(Campaign, campaign_id)
    if not camp:
        raise HTTPException(404, "Campagne introuvable")
    as_of = body.as_of or datetime.now(timezone.utc)
    if as_of.tzinfo is None:
        as_of = as_of.replace(tzinfo=timezone.utc)
    runner = ExperimentRunner(db)
    logs = runner.run_demo_campaign_step(campaign_id, as_of)
    return {"decisions": len(logs), "as_of": as_of.isoformat()}


@router.get("/campaigns/{campaign_id}/arena")
def arena(campaign_id: UUID, db: Session = Depends(get_db)):
    camp = db.get(Campaign, campaign_id)
    if not camp:
        raise HTTPException(404, "Campagne introuvable")
    competitors = db.query(Competitor).filter(Competitor.campaign_id == campaign_id).all()
    out = []
    for c in competitors:
        snaps = (
            db.query(EquitySnapshot)
            .filter(EquitySnapshot.competitor_id == c.id)
            .order_by(EquitySnapshot.as_of)
            .all()
        )
        curve = [{"t": s.as_of.isoformat(), "equity": float(s.equity)} for s in snaps]
        out.append(
            {
                "id": str(c.id),
                "name": c.name,
                "provider": c.provider,
                "model_id": c.model_id,
                "equity_curve": curve,
                "cash": float(c.cash),
                "ai_cost_usd": float(c.ai_cost_usd),
            }
        )
    return {"campaign_id": str(campaign_id), "competitors": out, "engine": camp.execution_engine}


@router.get("/campaigns/{campaign_id}/decisions")
def decisions(campaign_id: UUID, db: Session = Depends(get_db)):
    comps = db.query(Competitor).filter(Competitor.campaign_id == campaign_id).all()
    ids = [c.id for c in comps]
    logs = (
        db.query(DecisionLog)
        .filter(DecisionLog.competitor_id.in_(ids))
        .order_by(DecisionLog.as_of.desc())
        .limit(100)
        .all()
    )
    return [
        {
            "id": str(d.id),
            "competitor_id": str(d.competitor_id),
            "as_of": d.as_of.isoformat(),
            "validation_ok": d.validation_ok,
            "rejection_reason": d.rejection_reason,
            "contract": d.contract,
            "data_snapshot_hash": d.data_snapshot_hash,
            "cost_usd": float(d.cost_usd),
        }
        for d in logs
    ]


@router.get("/campaigns/{campaign_id}/orders")
def orders(campaign_id: UUID, db: Session = Depends(get_db)):
    comps = db.query(Competitor).filter(Competitor.campaign_id == campaign_id).all()
    ids = [c.id for c in comps]
    rows = db.query(OrderRow).filter(OrderRow.competitor_id.in_(ids)).order_by(OrderRow.created_at.desc()).limit(200).all()
    return [
        {
            "id": str(o.id),
            "symbol": o.symbol,
            "side": o.side,
            "quantity": o.quantity,
            "status": o.status,
            "execution_date": o.execution_date.isoformat() if o.execution_date else None,
            "assumptions_label": o.assumptions_label,
        }
        for o in rows
    ]


@router.post("/campaigns/{campaign_id}/backtest")
def run_backtest(campaign_id: UUID, db: Session = Depends(get_db), days: int = 20):
    from app.modules.experiments.backtest import BacktestService

    camp = db.get(Campaign, campaign_id)
    if not camp:
        raise HTTPException(404, "Campagne introuvable")
    if camp.mode != "BACKTEST" and get_settings().trading_mode.value != "BACKTEST":
        # Autorisé en DEMO pour exploration étiquetée
        pass
    svc = BacktestService(db)
    steps = svc.run(campaign_id, max_days=days)
    return {"steps": steps, "exploratory": True, "note": "Backtest LLM exploratoire — voir methodology.md"}


@router.get("/campaigns/{campaign_id}/report")
def report(campaign_id: UUID, format: str = "json", db: Session = Depends(get_db)):
    if format == "html":
        html = build_campaign_report_html(db, campaign_id)
        return Response(content=html, media_type="text/html; charset=utf-8")
    return build_campaign_report_json(db, campaign_id)
