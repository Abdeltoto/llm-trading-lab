from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_DOWN

from app.config import Settings
from app.modules.ledger.portfolio import FillRecord, PortfolioState


@dataclass
class ExecutionAssumptions:
    commission_bps: Decimal
    spread_bps: Decimal
    slippage_bps: Decimal
    label: str = "estimation"


class LocalCanonicalExecutionEngine:
    """Moteur V1 : open du jour d'exécution, hypothèses déclarées."""

    def __init__(self, settings: Settings) -> None:
        self.assumptions = ExecutionAssumptions(
            commission_bps=Decimal(str(settings.execution_commission_bps)),
            spread_bps=Decimal(str(settings.execution_spread_bps)),
            slippage_bps=Decimal(str(settings.execution_slippage_bps)),
        )

    def _adjust_price(self, open_price: Decimal, side: str) -> tuple[Decimal, Decimal]:
        bps = (self.assumptions.spread_bps + self.assumptions.slippage_bps) / Decimal(
            "10000"
        )
        if side == "buy":
            fill = open_price * (Decimal("1") + bps)
        else:
            fill = open_price * (Decimal("1") - bps)
        slippage_cost = abs(fill - open_price)
        return fill, slippage_cost

    def _commission(self, notional: Decimal) -> Decimal:
        return notional * self.assumptions.commission_bps / Decimal("10000")

    def rebalance_to_targets(
        self,
        state: PortfolioState,
        targets: dict[str, Decimal],
        marks: dict[str, Decimal],
        execution_date: date,
        open_prices: dict[str, Decimal],
    ) -> tuple[PortfolioState, list[FillRecord]]:
        equity = state.equity(marks)
        fills: list[FillRecord] = []

        desired_value = {s: equity * w for s, w in targets.items() if w > 0}
        for symbol, target_val in desired_value.items():
            price = marks.get(symbol, Decimal("0"))
            if price <= 0:
                continue
            target_qty = int((target_val / price).to_integral_value(rounding=ROUND_DOWN))
            current_qty = state.positions.get(symbol, None)
            current = current_qty.quantity if current_qty else 0
            delta = target_qty - current
            if delta == 0:
                continue
            open_px = open_prices.get(symbol)
            if open_px is None or open_px <= 0:
                continue
            side = "buy" if delta > 0 else "sell"
            qty = abs(delta)
            if side == "sell":
                held = state.positions.get(symbol)
                if not held or held.quantity < qty:
                    qty = held.quantity if held else 0
                if qty == 0:
                    continue
            fill_price, slip_unit = self._adjust_price(open_px, side)
            notional = Decimal(qty) * fill_price
            commission = self._commission(notional)
            slippage_cost = slip_unit * Decimal(qty)
            fill = FillRecord(
                symbol=symbol,
                side=side,
                quantity=qty,
                price=fill_price,
                commission=commission,
                slippage_cost=slippage_cost,
                trade_date=execution_date,
            )
            state.apply_fill(fill)
            fills.append(fill)

        # Sell positions not in targets
        for symbol, pos in list(state.positions.items()):
            if symbol not in targets or targets.get(symbol, Decimal("0")) == 0:
                open_px = open_prices.get(symbol)
                if not open_px:
                    continue
                fill_price, slip_unit = self._adjust_price(open_px, "sell")
                notional = Decimal(pos.quantity) * fill_price
                commission = self._commission(notional)
                slippage_cost = slip_unit * Decimal(pos.quantity)
                fill = FillRecord(
                    symbol=symbol,
                    side="sell",
                    quantity=pos.quantity,
                    price=fill_price,
                    commission=commission,
                    slippage_cost=slippage_cost,
                    trade_date=execution_date,
                )
                state.apply_fill(fill)
                fills.append(fill)

        return state, fills
