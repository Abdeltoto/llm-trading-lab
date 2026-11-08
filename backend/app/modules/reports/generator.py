from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Campaign, Competitor, DecisionLog, EquitySnapshot
from app.modules.analytics.benchmarks import BenchmarkCalculator
from app.modules.analytics.metrics import cumulative_return, max_drawdown


def build_campaign_report_html(db: Session, campaign_id: UUID) -> str:
    settings = get_settings()
    campaign = db.get(Campaign, campaign_id)
    if not campaign:
        raise ValueError("Campagne introuvable")

    competitors = db.query(Competitor).filter(Competitor.campaign_id == campaign_id).all()
    bench = BenchmarkCalculator()
    rows_html = []

    for c in competitors:
        snaps = (
            db.query(EquitySnapshot)
            .filter(EquitySnapshot.competitor_id == c.id)
            .order_by(EquitySnapshot.as_of)
            .all()
        )
        decisions = db.query(DecisionLog).filter(DecisionLog.competitor_id == c.id).count()
        eq_series = [s.equity for s in snaps]
        final = snaps[-1].equity if snaps else campaign.initial_capital
        cum = cumulative_return(campaign.initial_capital, final)
        dd = max_drawdown(eq_series)
        rows_html.append(
            f"<tr><td>{c.name}</td><td>{c.provider}/{c.model_id}</td>"
            f"<td>{cum:.2%} if cum else 'N/A'</td><td>{dd:.2%} if dd else 'N/A'</td>"
            f"<td>{decisions}</td><td>${c.ai_cost_usd}</td></tr>".replace(
                "{cum:.2%} if cum else 'N/A'", f"{cum:.2%}" if cum is not None else "N/A"
            ).replace("{dd:.2%} if dd else 'N/A'", f"{dd:.2%}" if dd is not None else "N/A")
        )

    generated = datetime.now(timezone.utc).isoformat()
    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"/>
<title>Rapport — {campaign.name}</title>
<style>
body{{font-family:system-ui,sans-serif;margin:2rem;}}
.banner{{background:#b45309;color:#fff;padding:.5rem 1rem;font-weight:600;}}
table{{border-collapse:collapse;width:100%;margin-top:1rem;}}
th,td{{border:1px solid #ccc;padding:.5rem;text-align:left;}}
</style></head><body>
<div class="banner">SIMULATION — ARGENT FICTIF</div>
<h1>Rapport de campagne</h1>
<p><strong>{campaign.name}</strong> — mode {campaign.mode} — moteur {campaign.execution_engine}</p>
<p>Généré : {generated} — version {settings.app_version} — commit {settings.git_commit}</p>
<p>Capital initial par concurrent : ${campaign.initial_capital} (fictif). Budget IA : ${campaign.ai_budget_usd}.</p>
<h2>Classement</h2>
<table>
<tr><th>Concurrent</th><th>Modèle</th><th>Rendement cumulé</th><th>Drawdown max</th><th>Décisions</th><th>Coût IA</th></tr>
{''.join(rows_html)}
</table>
<p><em>Les rendements courts ne doivent pas être extrapolés annualisés sans prudence.</em></p>
</body></html>"""


def build_campaign_report_json(db: Session, campaign_id: UUID) -> dict:
    campaign = db.get(Campaign, campaign_id)
    if not campaign:
        raise ValueError("Campagne introuvable")
    settings = get_settings()
    out = {
        "campaign_id": str(campaign_id),
        "name": campaign.name,
        "mode": campaign.mode,
        "execution_engine": campaign.execution_engine,
        "app_version": settings.app_version,
        "git_commit": settings.git_commit,
        "competitors": [],
    }
    for c in db.query(Competitor).filter(Competitor.campaign_id == campaign_id):
        snaps = (
            db.query(EquitySnapshot)
            .filter(EquitySnapshot.competitor_id == c.id)
            .order_by(EquitySnapshot.as_of)
            .all()
        )
        final = snaps[-1].equity if snaps else campaign.initial_capital
        out["competitors"].append(
            {
                "id": str(c.id),
                "name": c.name,
                "provider": c.provider,
                "model_id": c.model_id,
                "cumulative_return": str(
                    cumulative_return(campaign.initial_capital, final) or Decimal("0")
                ),
                "ai_cost_usd": str(c.ai_cost_usd),
                "decisions": db.query(DecisionLog).filter(DecisionLog.competitor_id == c.id).count(),
            }
        )
    return out
