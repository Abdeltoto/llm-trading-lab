from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from app.schemas.decision import DecisionContract


@dataclass
class RiskLimits:
    max_positions: int = 6
    max_weight_per_symbol: Decimal = Decimal("0.25")
    allowed_symbols: frozenset[str] = frozenset({"SPY", "QQQ", "IWM", "DIA", "TLT", "GLD"})
    max_daily_loss_pct: Decimal = Decimal("0.03")
    max_drawdown_pct: Decimal = Decimal("0.10")
    data_staleness_hours: int = 72


@dataclass
class RiskVerdict:
    approved: bool
    reason: str | None = None


class RiskEngine:
    def __init__(self, limits: RiskLimits | None = None) -> None:
        self.limits = limits or RiskLimits()
        self._paused = False
        self._peak_equity: Decimal | None = None

    @property
    def paused(self) -> bool:
        return self._paused

    def update_equity_guards(self, equity: Decimal, prior_equity: Decimal | None) -> None:
        if self._peak_equity is None or equity > self._peak_equity:
            self._peak_equity = equity
        if prior_equity and prior_equity > 0:
            daily_loss = (prior_equity - equity) / prior_equity
            if daily_loss >= self.limits.max_daily_loss_pct:
                self._paused = True
        if self._peak_equity and self._peak_equity > 0:
            dd = (self._peak_equity - equity) / self._peak_equity
            if dd >= self.limits.max_drawdown_pct:
                self._paused = True

    def validate_decision(
        self,
        decision: DecisionContract,
        *,
        latest_bar_time: datetime,
        held_symbols: set[str],
    ) -> RiskVerdict:
        if self._paused:
            return RiskVerdict(False, "Campagne en pause (perte quotidienne ou drawdown)")

        if decision.as_of.tzinfo is None:
            return RiskVerdict(False, "as_of doit être timezone-aware (UTC)")

        stale_limit = decision.as_of - timedelta(hours=self.limits.data_staleness_hours)
        if latest_bar_time < stale_limit:
            return RiskVerdict(False, "Données de marché trop anciennes")

        if decision.abstain:
            return RiskVerdict(True)

        active = [t for t in decision.targets if t.target_weight > 0]
        if len(active) > self.limits.max_positions:
            return RiskVerdict(False, f"Plus de {self.limits.max_positions} positions")

        for t in decision.targets:
            if t.symbol not in self.limits.allowed_symbols:
                return RiskVerdict(False, f"Instrument non autorisé : {t.symbol}")
            if t.target_weight > self.limits.max_weight_per_symbol:
                return RiskVerdict(False, f"Poids max dépassé pour {t.symbol}")

        for t in decision.targets:
            if t.target_weight > 0 and t.target_weight < Decimal("0"):
                return RiskVerdict(False, "Poids négatif interdit (pas de short V1)")

        # Long only: cannot target weight on symbol not held if reducing below 0 handled elsewhere
        for t in decision.targets:
            if t.target_weight == 0 and t.symbol in held_symbols:
                continue

        return RiskVerdict(True)
