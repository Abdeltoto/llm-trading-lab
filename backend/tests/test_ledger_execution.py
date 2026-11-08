from datetime import date
from decimal import Decimal

from app.modules.ledger.portfolio import PortfolioState, FillRecord
from app.modules.execution.local_engine import LocalCanonicalExecutionEngine
from app.config import Settings, TradingMode


def test_ledger_conservation_with_fees():
    state = PortfolioState(cash=Decimal("10000"))
    fill = FillRecord(
        symbol="SPY",
        side="buy",
        quantity=10,
        price=Decimal("100"),
        commission=Decimal("1"),
        slippage_cost=Decimal("0.5"),
        trade_date=date(2024, 1, 3),
    )
    state.apply_fill(fill)
    assert state.cash == Decimal("10000") - Decimal("1000") - Decimal("1.5")
    assert state.positions["SPY"].quantity == 10


def test_execution_uses_open_not_decision_close():
    settings = Settings(TRADING_MODE=TradingMode.DEMO)
    engine = LocalCanonicalExecutionEngine(settings)
    state = PortfolioState(cash=Decimal("100000"))
    marks = {"SPY": Decimal("100")}
    open_prices = {"SPY": Decimal("101")}
    targets = {"SPY": Decimal("0.5")}
    state, fills = engine.rebalance_to_targets(
        state, targets, marks, date(2024, 1, 4), open_prices
    )
    assert fills
    assert fills[0].price != Decimal("100")
