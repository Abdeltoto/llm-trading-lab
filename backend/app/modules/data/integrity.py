from datetime import datetime

import pandas as pd


def filter_point_in_time(df: pd.DataFrame, as_of: datetime) -> pd.DataFrame:
    """Retire toute ligne dont available_at est postérieur à as_of."""
    if "available_at" not in df.columns:
        raise ValueError("Colonne available_at requise")
    as_of_ts = pd.Timestamp(as_of).tz_convert("UTC") if as_of.tzinfo else pd.Timestamp(as_of, tz="UTC")
    return df[df["available_at"] <= as_of_ts]
