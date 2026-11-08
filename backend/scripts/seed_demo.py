"""Crée une campagne démo si aucune n'existe et exécute quelques pas."""

from datetime import timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db import SessionLocal, engine
from app.models import Base, Campaign, Competitor
from app.modules.data.demo_provider import DemoDataProvider, UNIVERSE
from app.modules.experiments.runner import ExperimentRunner, prompt_hash


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        existing = db.query(Campaign).first()
        if existing:
            print("Campagne existante, seed ignoré.")
            return

        camp = Campaign(
            name="Campagne démo par défaut",
            mode="DEMO",
            initial_capital=Decimal("100000"),
            ai_budget_usd=Decimal("50"),
            execution_engine="local_canonical",
            config={"universe": UNIVERSE, "prospective_weeks": 8},
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

        data = DemoDataProvider()
        df = data.load()
        dates = sorted(df["event_time"].dt.normalize().unique())[:15]
        runner = ExperimentRunner(db)
        for d in dates:
            as_of = d.to_pydatetime().replace(hour=21, minute=0, tzinfo=timezone.utc)
            runner.run_demo_campaign_step(camp.id, as_of)
        print(f"Campagne démo {camp.id} initialisée ({len(dates)} pas).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
