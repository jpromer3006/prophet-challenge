"""Pure analysis functions extracted from the original notebook.

Each function takes a DataFrame and returns a DataFrame/Series so the web
layer can render the results however it likes (charts, tables, metrics).
"""

import pandas as pd

DAY_NAMES = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}


def traffic_by_hour(trends: pd.DataFrame) -> pd.Series:
    """Average search traffic for each hour of the day (0-23)."""
    s = trends.groupby(trends.index.hour)["Search Trends"].mean()
    s.index.name = "Hour of day"
    return s


def traffic_by_weekday(trends: pd.DataFrame) -> pd.Series:
    """Average search traffic for each day of the week, labelled Mon-Sun."""
    s = trends.groupby(trends.index.isocalendar().day)["Search Trends"].mean()
    s.index = s.index.map(DAY_NAMES)
    s.index.name = "Day of week"
    return s


def traffic_by_week_of_year(trends: pd.DataFrame) -> pd.Series:
    """Average search traffic for each ISO week of the year (1-52)."""
    s = trends.groupby(trends.index.isocalendar().week)["Search Trends"].mean()
    s.index.name = "Week of year"
    return s


def median_vs_month(trends: pd.DataFrame, year: int, month: int) -> dict:
    """Compare one month's total traffic against the all-time monthly median."""
    monthly_totals = trends.groupby(
        [trends.index.year, trends.index.month]
    )["Search Trends"].sum()
    month_total = monthly_totals.get((year, month))
    median_total = monthly_totals.median()
    ratio = month_total / median_total if month_total is not None else None
    return {
        "month_total": month_total,
        "median_total": median_total,
        "ratio": ratio,
    }


def correlation_table(combined: pd.DataFrame) -> pd.DataFrame:
    """Build the lagged-search / volatility / return correlation matrix."""
    df = combined.copy()
    df["Lagged Search Trends"] = df["Search Trends"].shift(1)
    df["Hourly Stock Return"] = df["close"].pct_change()
    df["Stock Volatility"] = df["close"].pct_change().rolling(4).std()
    cols = ["Stock Volatility", "Lagged Search Trends", "Hourly Stock Return"]
    return df[cols].corr()
