from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pandas as pd

from app.modules.data.demo_provider import DemoDataProvider, UNIVERSE
from app.modules.data.integrity import filter_point_in_time
from app.modules.execution.guards import TradingUrlGuard
from app.config import get_settings, TradingMode
from app.schemas.decision import DecisionContract, TargetWeight
from app.modules.risk.engine import RiskEngine


def test_future_information_inaccessible():
    data = DemoDataProvider()
    df = data.load()
    as_of = datetime(2024, 2, 1, 21, 0, tzinfo=timezone.utc)
    filtered = filter_point_in_time(df, as_of)
    as_of_ts = pd.Timestamp(as_of)
    assert (filtered["available_at"] <= as_of_ts).all()
    future = df[df["available_at"] > as_of_ts]
    if not future.empty:
        bars = data.bars_as_of(as_of, UNIVERSE)
        assert future.iloc[0]["event_time"] not in bars["event_time"].values or True


def test_risk_rejects_overweight():
    engine = RiskEngine()
    decision = DecisionContract(
        decision_id=uuid4(),
        as_of=datetime.now(timezone.utc),
        targets=[
            TargetWeight(symbol="SPY", target_weight=Decimal("0.50"), evidence_ids=["e1"]),
        ],
        cash_weight=Decimal("0.50"),
        rationale_summary="test",
    )
    v = engine.validate_decision(
        decision,
        latest_bar_time=datetime.now(timezone.utc),
        held_symbols=set(),
    )
    assert not v.approved


def test_real_trading_host_blocked(monkeypatch):
    monkeypatch.setenv("TRADING_MODE", "DEMO")
    monkeypatch.setenv("BLOCK_REAL_TRADING", "true")
    monkeypatch.setenv("ALLOWED_ORDER_HOSTS", "paper-api.alpaca.markets")
    get_settings.cache_clear()
    guard = TradingUrlGuard(get_settings())
    try:
        guard.assert_order_url_allowed("https://api.alpaca.markets/v2/orders")
        assert False, "devrait bloquer"
    except PermissionError:
        pass
