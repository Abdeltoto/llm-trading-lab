from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json

from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.models import (
    AuditEvent,
    Competitor,
    DecisionLog,
    EquitySnapshot,
    FillRow,
    OrderRow,
    PositionRow,
)
from app.modules.data.demo_provider import UNIVERSE, DemoDataProvider
from app.modules.execution.local_engine import LocalCanonicalExecutionEngine
from app.modules.ledger.portfolio import PortfolioState, Position
from app.modules.llm.demo_provider import DemoDeterministicStrategy
from app.modules.risk.engine import RiskEngine
from app.schemas.decision import DecisionContract


PROMPT_V1 = "allocation-etf-v1"


def prompt_hash() -> str:
    return hashlib.sha256(PROMPT_V1.encode()).hexdigest()[:16]


class ExperimentRunner:
    def __init__(self, db: Session, settings: Settings | None = None) -> None:
        self.db = db
        self.settings = settings or get_settings()
        self.data = DemoDataProvider()
        self.execution = LocalCanonicalExecutionEngine(self.settings)
        self.risk = RiskEngine()

    def _load_portfolio_state(self, competitor: Competitor) -> PortfolioState:
        state = PortfolioState(cash=competitor.cash)
        for row in competitor.positions:
            state.positions[row.symbol] = Position(
                symbol=row.symbol, quantity=row.quantity, avg_cost=row.avg_cost
            )
        return state

    def _persist_positions(self, competitor: Competitor, state: PortfolioState) -> None:
        existing = {p.symbol: p for p in competitor.positions}
        seen = set()
        for sym, pos in state.positions.items():
            seen.add(sym)
            if sym in existing:
                existing[sym].quantity = pos.quantity
                existing[sym].avg_cost = pos.avg_cost
            else:
                self.db.add(
                    PositionRow(
                        competitor_id=competitor.id,
                        symbol=sym,
                        quantity=pos.quantity,
                        avg_cost=pos.avg_cost,
                    )
                )
        for sym, row in existing.items():
            if sym not in seen:
                self.db.delete(row)
        competitor.cash = state.cash

    def run_decision_cycle(self, competitor: Competitor, as_of: datetime) -> DecisionLog:
        ordered = (
            self.db.query(Competitor)
            .filter(Competitor.campaign_id == competitor.campaign_id)
            .order_by(Competitor.name)
            .all()
        )
        idx = next(i for i, c in enumerate(ordered) if c.id == competitor.id)
        strategy = DemoDeterministicStrategy(self.data, variant=idx % 3)

        t0 = datetime.now(timezone.utc)
        decision = strategy.propose(as_of, competitor.name)
        latency = int((datetime.now(timezone.utc) - t0).total_seconds() * 1000)

        bars = self.data.bars_as_of(as_of, UNIVERSE)
        latest = bars["event_time"].max().to_pydatetime()
        if latest.tzinfo is None:
            latest = latest.replace(tzinfo=timezone.utc)

        held = {p.symbol for p in competitor.positions}
        verdict = self.risk.validate_decision(
            decision, latest_bar_time=latest, held_symbols=held
        )

        snap_hash = self.data.snapshot_hash(as_of, UNIVERSE)
        log = DecisionLog(
            competitor_id=competitor.id,
            as_of=as_of,
            contract=decision.model_dump(mode="json"),
            validation_ok=verdict.approved,
            rejection_reason=verdict.reason,
            data_snapshot_hash=snap_hash,
            latency_ms=latency,
            cost_usd=Decimal("0"),
        )
        self.db.add(log)
        self.db.flush()

        if not verdict.approved:
            self._audit("decision_rejected", {"competitor": str(competitor.id), "reason": verdict.reason})
            return log

        if decision.abstain:
            return log

        state = self._load_portfolio_state(competitor)
        marks = self.data.latest_close_marks(as_of, UNIVERSE)
        prior_equity = state.equity(marks)
        self.risk.update_equity_guards(prior_equity, prior_equity)

        targets = {t.symbol: t.target_weight for t in decision.targets}
        targets_cash = decision.cash_weight

        exec_day = self.data.next_trading_day(as_of)
        if exec_day <= as_of:
            exec_day = self.data.next_trading_day(as_of.replace(hour=23, minute=59))

        open_prices = self.data.open_on_date(exec_day.date(), UNIVERSE)
        state, fills = self.execution.rebalance_to_targets(
            state,
            targets,
            marks,
            exec_day.date(),
            open_prices,
        )
        self._persist_positions(competitor, state)

        idem_base = f"{competitor.id}:{log.id}"
        for f in fills:
            key = f"{idem_base}:{f.symbol}:{f.side}:{f.quantity}:{f.trade_date}"
            order = OrderRow(
                competitor_id=competitor.id,
                decision_id=log.id,
                idempotency_key=hashlib.sha256(key.encode()).hexdigest(),
                symbol=f.symbol,
                side=f.side,
                quantity=f.quantity,
                status="filled",
                execution_date=f.trade_date,
                assumptions_label="estimation",
            )
            self.db.add(order)
            self.db.flush()
            self.db.add(
                FillRow(
                    order_id=order.id,
                    price=f.price,
                    commission=f.commission,
                    slippage_cost=f.slippage_cost,
                )
            )

        new_marks = self.data.latest_close_marks(as_of, UNIVERSE)
        eq = state.equity(new_marks)
        self.db.add(
            EquitySnapshot(
                competitor_id=competitor.id,
                as_of=as_of,
                equity=eq,
                cash=state.cash,
            )
        )
        return log

    def _audit(self, event_type: str, payload: dict) -> None:
        self.db.add(AuditEvent(event_type=event_type, payload=payload))

    def run_demo_campaign_step(self, campaign_id, as_of: datetime) -> list[DecisionLog]:
        competitors = (
            self.db.query(Competitor).filter(Competitor.campaign_id == campaign_id).all()
        )
        logs = []
        for c in competitors:
            logs.append(self.run_decision_cycle(c, as_of))
        self.db.commit()
        return logs
