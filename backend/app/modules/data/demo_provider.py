from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pandas as pd

UNIVERSE = ["SPY", "QQQ", "IWM", "DIA", "TLT", "GLD"]


class DemoDataProvider:
    """Données synthétiques reproductibles (seed fixe)."""

    def __init__(self, data_dir: Path | None = None) -> None:
        root = data_dir or Path(__file__).resolve().parents[4] / "data" / "demo"
        self.parquet_path = root / "daily_bars.parquet"
        self._df: pd.DataFrame | None = None

    def load(self) -> pd.DataFrame:
        if self._df is None:
            if not self.parquet_path.exists():
                raise FileNotFoundError(
                    f"Jeu démo manquant : {self.parquet_path}. Exécutez scripts/generate_demo_parquet.py"
                )
            self._df = pd.read_parquet(self.parquet_path)
            self._df["event_time"] = pd.to_datetime(self._df["event_time"], utc=True)
            self._df["available_at"] = pd.to_datetime(self._df["available_at"], utc=True)
        return self._df

    def bars_as_of(self, as_of: datetime, symbols: list[str] | None = None) -> pd.DataFrame:
        df = self.load()
        symbols = symbols or UNIVERSE
        mask = (df["available_at"] <= as_of) & (df["symbol"].isin(symbols))
        return df.loc[mask].sort_values(["symbol", "event_time"])

    def latest_close_marks(self, as_of: datetime, symbols: list[str]) -> dict[str, Decimal]:
        bars = self.bars_as_of(as_of, symbols)
        marks: dict[str, Decimal] = {}
        for sym in symbols:
            sub = bars[bars["symbol"] == sym]
            if sub.empty:
                continue
            row = sub.iloc[-1]
            marks[sym] = Decimal(str(row["close"]))
        return marks

    def open_on_date(self, trade_date, symbols: list[str]) -> dict[str, Decimal]:
        df = self.load()
        d = pd.Timestamp(trade_date).tz_localize("UTC")
        out: dict[str, Decimal] = {}
        day = df[df["event_time"].dt.normalize() == d]
        for sym in symbols:
            sub = day[day["symbol"] == sym]
            if not sub.empty:
                out[sym] = Decimal(str(sub.iloc[0]["open"]))
        return out

    def snapshot_hash(self, as_of: datetime, symbols: list[str]) -> str:
        bars = self.bars_as_of(as_of, symbols)
        payload = bars[["symbol", "event_time", "close"]].tail(len(symbols) * 5).to_csv(
            index=False
        )
        import hashlib

        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def next_trading_day(self, after: datetime) -> datetime:
        df = self.load()
        dates = sorted(df["event_time"].dt.normalize().unique())
        after_norm = pd.Timestamp(after).tz_convert("UTC").normalize()
        for d in dates:
            if d > after_norm:
                return d.to_pydatetime().replace(tzinfo=timezone.utc)
        return after
