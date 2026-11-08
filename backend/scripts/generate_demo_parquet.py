"""Génère data/demo/daily_bars.parquet (séries synthétiques reproductibles)."""

from datetime import timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

UNIVERSE = ["SPY", "QQQ", "IWM", "DIA", "TLT", "GLD"]
SEED = 42


def main() -> None:
    rng = np.random.default_rng(SEED)
    root = Path(__file__).resolve().parents[2] / "data" / "demo"
    root.mkdir(parents=True, exist_ok=True)

    start = pd.Timestamp("2024-01-02", tz="UTC")
    days = pd.bdate_range(start, periods=280, freq="C")

    rows = []
    base_prices = {"SPY": 470, "QQQ": 400, "IWM": 195, "DIA": 380, "TLT": 92, "GLD": 185}
    state = dict(base_prices)

    for day in days:
        for sym in UNIVERSE:
            shock = float(rng.normal(0, 0.008))
            state[sym] = max(10.0, state[sym] * (1 + shock))
            close = state[sym]
            open_px = close * (1 + float(rng.normal(0, 0.002)))
            high = max(open_px, close) * (1 + abs(float(rng.normal(0, 0.003))))
            low = min(open_px, close) * (1 - abs(float(rng.normal(0, 0.003))))
            event_time = day.to_pydatetime()
            # disponible après la clôture (16:00 US simplifié → 21:00 UTC)
            available_at = (day + timedelta(hours=21)).to_pydatetime().replace(tzinfo=timezone.utc)
            rows.append(
                {
                    "symbol": sym,
                    "event_time": event_time.replace(tzinfo=timezone.utc),
                    "available_at": available_at,
                    "open": round(open_px, 4),
                    "high": round(high, 4),
                    "low": round(low, 4),
                    "close": round(close, 4),
                    "volume": int(rng.integers(1_000_000, 5_000_000)),
                }
            )

    df = pd.DataFrame(rows)
    out = root / "daily_bars.parquet"
    df.to_parquet(out, index=False)
    print(f"Écrit {out} ({len(df)} lignes)")


if __name__ == "__main__":
    main()
