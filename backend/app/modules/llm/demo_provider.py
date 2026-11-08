from decimal import Decimal
from uuid import uuid4

from app.modules.data.demo_provider import UNIVERSE, DemoDataProvider
from app.schemas.decision import DecisionContract, TargetWeight


class DemoDeterministicStrategy:
    """Agents déterministes : rotations fixes selon momentum 5j (calcul code)."""

    NAMES = ("Momentum-A", "EqualWeight-B", "Defensive-C")

    def __init__(self, data: DemoDataProvider, variant: int) -> None:
        self.data = data
        self.variant = variant

    def propose(self, as_of, competitor_name: str) -> DecisionContract:
        bars = self.data.bars_as_of(as_of, UNIVERSE)
        weights: dict[str, Decimal] = {s: Decimal("0") for s in UNIVERSE}
        if self.variant == 0:
            # top 3 momentum
            scores = []
            for sym in UNIVERSE:
                sub = bars[bars["symbol"] == sym].tail(6)
                if len(sub) >= 2:
                    ret = Decimal(str(sub.iloc[-1]["close"])) / Decimal(
                        str(sub.iloc[0]["close"])
                    ) - Decimal("1")
                    scores.append((sym, ret))
            scores.sort(key=lambda x: x[1], reverse=True)
            for sym, _ in scores[:3]:
                weights[sym] = Decimal("0.20")
            cash = Decimal("1") - sum(weights.values())
        elif self.variant == 1:
            n = Decimal(len(UNIVERSE))
            w = (Decimal("1") / n).quantize(Decimal("0.000001"))
            for i, sym in enumerate(UNIVERSE):
                weights[sym] = w if i < len(UNIVERSE) - 1 else (Decimal("1") - w * (n - 1))
            cash = Decimal("0")
        else:
            weights["TLT"] = Decimal("0.40")
            weights["GLD"] = Decimal("0.20")
            cash = Decimal("0.40")

        targets = [
            TargetWeight(symbol=s, target_weight=weights[s], evidence_ids=["price-snapshot-1"])
            for s in UNIVERSE
            if weights[s] > 0
        ]
        return DecisionContract(
            decision_id=uuid4(),
            as_of=as_of,
            targets=targets,
            cash_weight=cash,
            rationale_summary=f"DEMO {competitor_name} variante {self.variant}",
            abstain=False,
        )
