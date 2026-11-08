from decimal import Decimal
from typing import Sequence


def max_drawdown(equity_series: Sequence[Decimal]) -> Decimal | None:
    if len(equity_series) < 2:
        return None
    peak = equity_series[0]
    max_dd = Decimal("0")
    for v in equity_series:
        if v > peak:
            peak = v
        if peak > 0:
            dd = (peak - v) / peak
            if dd > max_dd:
                max_dd = dd
    return max_dd


def cumulative_return(initial: Decimal, final: Decimal) -> Decimal | None:
    if initial <= 0:
        return None
    return final / initial - Decimal("1")
