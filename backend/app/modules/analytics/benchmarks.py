from decimal import Decimal

from app.modules.data.demo_provider import UNIVERSE, DemoDataProvider


class BenchmarkCalculator:
    def __init__(self, data: DemoDataProvider | None = None) -> None:
        self.data = data or DemoDataProvider()

    def spy_buy_hold_return(self, start_as_of, end_as_of) -> Decimal | None:
        bars = self.data.bars_as_of(end_as_of, ["SPY"])
        start_bars = self.data.bars_as_of(start_as_of, ["SPY"])
        if bars.empty or start_bars.empty:
            return None
        end_px = Decimal(str(bars.iloc[-1]["close"]))
        start_px = Decimal(str(start_bars.iloc[-1]["close"]))
        if start_px == 0:
            return None
        return end_px / start_px - Decimal("1")

    def equal_weight_return(self, start_as_of, end_as_of) -> Decimal | None:
        rets = []
        for sym in UNIVERSE:
            end_b = self.data.bars_as_of(end_as_of, [sym])
            start_b = self.data.bars_as_of(start_as_of, [sym])
            if end_b.empty or start_b.empty:
                continue
            end_px = Decimal(str(end_b.iloc[-1]["close"]))
            start_px = Decimal(str(start_b.iloc[-1]["close"]))
            if start_px > 0:
                rets.append(end_px / start_px - Decimal("1"))
        if not rets:
            return None
        return sum(rets) / Decimal(len(rets))
