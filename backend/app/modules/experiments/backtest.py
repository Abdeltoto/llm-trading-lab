from datetime import timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Campaign, Competitor, EquitySnapshot
from app.modules.data.demo_provider import UNIVERSE, DemoDataProvider
from app.modules.experiments.runner import ExperimentRunner


class BacktestService:
    """BACKTEST : parcours historique avec horloge simulée."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.data = DemoDataProvider()
        self.runner = ExperimentRunner(db)

    def run(self, campaign_id, max_days: int = 30) -> int:
        df = self.data.load()
        dates = sorted(df["event_time"].dt.normalize().unique())
        count = 0
        for d in dates[:max_days]:
            as_of = d.to_pydatetime().replace(hour=21, minute=0, tzinfo=timezone.utc)
            self.runner.run_demo_campaign_step(campaign_id, as_of)
            count += 1
        return count
