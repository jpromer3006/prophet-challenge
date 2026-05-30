"""Load and clean the cached MercadoLibre datasets.

Data is read from the local ``data/`` folder (committed to the repo) so the
public app never depends on a remote host being online. The raw CSVs were
originally sourced from the edX AI bootcamp dataset mirror.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

TRENDS_CSV = DATA_DIR / "google_hourly_search_trends.csv"
STOCK_CSV = DATA_DIR / "mercado_stock_price.csv"


def load_search_trends() -> pd.DataFrame:
    """Return hourly Google search-trend data indexed by datetime.

    The cached CSV stores dates as ``M/D/YY H:MM`` (e.g. ``6/1/16 0:00``),
    so we parse that format explicitly rather than relying on inference.
    """
    df = pd.read_csv(TRENDS_CSV)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%y %H:%M")
    df = df.set_index("Date").sort_index()
    return df


def load_stock_price() -> pd.DataFrame:
    """Return hourly MercadoLibre closing-price data indexed by datetime."""
    df = pd.read_csv(STOCK_CSV, parse_dates=["date"]).dropna()
    df = df.set_index("date").sort_index()
    return df


def load_combined() -> pd.DataFrame:
    """Join search trends and stock price on their shared hourly timestamps."""
    trends = load_search_trends()
    stock = load_stock_price()
    combined = pd.concat([stock, trends], axis=1).dropna()
    return combined
