from datetime import timezone

from app.modules.analytics.benchmarks import BenchmarkCalculator
from app.modules.data.demo_provider import DemoDataProvider


def test_benchmark_spy_same_convention():
    data = DemoDataProvider()
    dates = sorted(data.load()["event_time"].dt.normalize().unique())
    start = dates[20].to_pydatetime().replace(tzinfo=timezone.utc)
    end = dates[40].to_pydatetime().replace(tzinfo=timezone.utc)
    calc = BenchmarkCalculator(data)
    r = calc.spy_buy_hold_return(start, end)
    assert r is not None
