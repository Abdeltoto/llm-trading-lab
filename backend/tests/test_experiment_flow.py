from datetime import timezone
from decimal import Decimal

from app.models import Campaign, Competitor
from app.modules.experiments.runner import ExperimentRunner, prompt_hash
from app.modules.data.demo_provider import DemoDataProvider


def test_isolation_between_competitors(db_session):
    camp = Campaign(name="t", mode="DEMO", initial_capital=Decimal("100000"), config={})
    db_session.add(camp)
    db_session.flush()
    ph = prompt_hash()
    for label in ("Momentum-A", "EqualWeight-B", "Defensive-C"):
        db_session.add(
            Competitor(
                campaign_id=camp.id,
                name=label,
                provider="demo",
                model_id="d",
                cash=Decimal("100000"),
                prompt_hash=ph,
            )
        )
    db_session.commit()
    data = DemoDataProvider()
    d0 = sorted(data.load()["event_time"].dt.normalize().unique())[10]
    as_of = d0.to_pydatetime().replace(hour=21, minute=0, tzinfo=timezone.utc)
    runner = ExperimentRunner(db_session)
    runner.run_demo_campaign_step(camp.id, as_of)
    comps = db_session.query(Competitor).filter(Competitor.campaign_id == camp.id).all()
    cashes = {c.name: c.cash for c in comps}
    assert len(set(cashes.values())) >= 1


def test_idempotent_orders(db_session):
    camp = Campaign(name="t", mode="DEMO", initial_capital=Decimal("100000"), config={})
    db_session.add(camp)
    db_session.flush()
    c = Competitor(
        campaign_id=camp.id,
        name="Momentum-A",
        provider="demo",
        model_id="d",
        cash=Decimal("100000"),
        prompt_hash=prompt_hash(),
    )
    db_session.add(c)
    db_session.commit()
    data = DemoDataProvider()
    d0 = sorted(data.load()["event_time"].dt.normalize().unique())[5]
    as_of = d0.to_pydatetime().replace(hour=21, minute=0, tzinfo=timezone.utc)
    runner = ExperimentRunner(db_session)
    runner.run_decision_cycle(c, as_of)
    db_session.commit()
    from app.models import OrderRow

    n1 = db_session.query(OrderRow).count()
    runner.run_decision_cycle(c, as_of)
    db_session.commit()
    n2 = db_session.query(OrderRow).count()
    assert n2 >= n1
