from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Literal


@dataclass
class Position:
    symbol: str
    quantity: int
    avg_cost: Decimal


@dataclass
class FillRecord:
    symbol: str
    side: Literal["buy", "sell"]
    quantity: int
    price: Decimal
    commission: Decimal
    slippage_cost: Decimal
    trade_date: date


@dataclass
class PortfolioState:
    cash: Decimal
    positions: dict[str, Position] = field(default_factory=dict)

    def equity(self, marks: dict[str, Decimal]) -> Decimal:
        pos_val = sum(
            Decimal(pos.quantity) * marks.get(sym, Decimal("0"))
            for sym, pos in self.positions.items()
        )
        return self.cash + pos_val

    def apply_fill(self, fill: FillRecord) -> None:
        notional = Decimal(fill.quantity) * fill.price
        fees = fill.commission + fill.slippage_cost
        if fill.side == "buy":
            self.cash -= notional + fees
            pos = self.positions.get(fill.symbol)
            if pos:
                new_qty = pos.quantity + fill.quantity
                pos.avg_cost = (
                    (pos.avg_cost * pos.quantity + notional) / new_qty
                    if new_qty
                    else Decimal("0")
                )
                pos.quantity = new_qty
            else:
                self.positions[fill.symbol] = Position(
                    symbol=fill.symbol, quantity=fill.quantity, avg_cost=fill.price
                )
        else:
            pos = self.positions.get(fill.symbol)
            if not pos or pos.quantity < fill.quantity:
                raise ValueError("Vente impossible : quantité insuffisante")
            self.cash += notional - fees
            pos.quantity -= fill.quantity
            if pos.quantity == 0:
                del self.positions[fill.symbol]
