from datetime import timezone
from decimal import Decimal

from app.models import Campaign, Competitor
from app.modules.data.demo_provider import DemoDataProvider
from app.modules.experiments.runner import ExperimentRunner, prompt_hash


def test_reproducible_accounting_known_seed(db_session):
    """Scénario déterministe : deux exécutions identiques → même cash final."""
    camp = Campaign(name="replay", mode="DEMO", initial_capital=Decimal("100000"), config={})
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
    d0 = sorted(data.load()["event_time"].dt.normalize().unique())[12]
    as_of = d0.to_pydatetime().replace(hour=21, minute=0, tzinfo=timezone.utc)
    runner = ExperimentRunner(db_session)
    runner.run_decision_cycle(c, as_of)
    db_session.commit()
    cash1 = float(c.cash)

    camp2 = Campaign(name="replay-2", mode="DEMO", initial_capital=Decimal("100000"), config={})
    db_session.add(camp2)
    db_session.flush()
    c2 = Competitor(
        campaign_id=camp2.id,
        name="Momentum-A",
        provider="demo",
        model_id="d",
        cash=Decimal("100000"),
        prompt_hash=prompt_hash(),
    )
    db_session.add(c2)
    db_session.commit()
    runner.run_decision_cycle(c2, as_of)
    db_session.commit()
    assert float(c2.cash) == cash1


def test_worker_recovery_idempotent_key_unique(db_session):
    from app.models import OrderRow
    from sqlalchemy.exc import IntegrityError

    camp = Campaign(name="w", mode="DEMO", initial_capital=Decimal("100000"), config={})
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
    o = OrderRow(
        competitor_id=c.id,
        idempotency_key="same-key",
        symbol="SPY",
        side="buy",
        quantity=1,
        status="filled",
    )
    db_session.add(o)
    db_session.commit()
    db_session.add(
        OrderRow(
            competitor_id=c.id,
            idempotency_key="same-key",
            symbol="SPY",
            side="buy",
            quantity=1,
            status="filled",
        )
    )
    try:
        db_session.commit()
        assert False
    except IntegrityError:
        db_session.rollback()
