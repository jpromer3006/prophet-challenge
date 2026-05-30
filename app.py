"""Forecasting Net Prophet — a public Streamlit app.

Explores MercadoLibre Google-search-trend seasonality and forecasts near-term
popularity with Prophet. Built for a general audience: every chart is paired
with a plain-language takeaway.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import analysis
from data_loader import load_combined, load_search_trends
from model import forecast, load_model

st.set_page_config(
    page_title="Forecasting Net Prophet",
    page_icon="📈",
    layout="wide",
)


# --------------------------------------------------------------------------- #
# Cached data + model (computed once per server, not per page load)
# --------------------------------------------------------------------------- #
@st.cache_data
def get_trends():
    return load_search_trends()


@st.cache_data
def get_combined():
    return load_combined()


@st.cache_resource
def get_model():
    return load_model()


@st.cache_data
def get_forecast(periods: int):
    # _model is excluded from the cache key by leading underscore convention;
    # we pass periods so each horizon is cached separately.
    return forecast(get_model(), periods=periods)


# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
st.title("📈 Forecasting Net Prophet")
st.markdown(
    "How popular is **MercadoLibre** — Latin America's biggest e-commerce "
    "platform — on Google, and where is interest headed next? This app mines "
    "hourly Google search data for patterns and forecasts the near-term trend."
)

trends = get_trends()

with st.expander("ℹ️ What am I looking at?"):
    st.markdown(
        "- **Search Trends** is Google's relative measure of how often people "
        "searched for MercadoLibre each hour (0–100 scale).\n"
        "- The forecast uses **Prophet**, an open-source time-series model from "
        "Meta, trained on data from "
        f"**{trends.index.min():%b %Y}** to **{trends.index.max():%b %Y}**.\n"
        "- This is an educational demo, **not financial advice.**"
    )

tab_forecast, tab_seasonality, tab_stock = st.tabs(
    ["🔮 Forecast", "🗓️ When are people searching?", "💹 Search vs. stock"]
)


# --------------------------------------------------------------------------- #
# Tab 1: Forecast
# --------------------------------------------------------------------------- #
with tab_forecast:
    st.subheader("Forecast future search interest")
    days = st.slider(
        "How many days ahead should we forecast?",
        min_value=7,
        max_value=90,
        value=30,
        step=1,
        help="Forecasting too far beyond the data gets unreliable, so we cap it at 90 days.",
    )

    view = st.radio(
        "Chart view",
        ["🔍 Forecast & recent weeks", "🌐 Full history (daily average)"],
        horizontal=True,
        help="Zoom in on the upcoming forecast, or smooth the whole history into a "
        "daily trend line. (The raw data is hourly, so the full range looks busy "
        "unless it's averaged.)",
    )

    with st.spinner("Crunching the forecast…"):
        fc = get_forecast(periods=days * 24)

    history = trends["Search Trends"]
    split = history.index.max()
    fc_idx = fc.set_index("ds")
    future = fc_idx[fc_idx.index > split]

    def add_band(fig, x, lower, upper):
        """Shade the confidence interval as a filled band."""
        fig.add_trace(go.Scatter(
            x=x, y=upper, mode="lines", line=dict(width=0),
            showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(
            x=x, y=lower, mode="lines", line=dict(width=0), fill="tonexty",
            fillcolor="rgba(0,120,255,0.15)", name="Likely range", hoverinfo="skip"))

    fig = go.Figure()
    if view.startswith("🔍"):
        # Zoom: recent hourly history + the upcoming forecast only.
        window = max(days, 14)
        recent = history[history.index >= split - pd.Timedelta(days=window)]
        add_band(fig, future.index, future["yhat_lower"], future["yhat_upper"])
        fig.add_trace(go.Scatter(
            x=future.index, y=future["yhat"], mode="lines",
            line=dict(color="#0078ff"), name="Forecast"))
        fig.add_trace(go.Scatter(
            x=recent.index, y=recent.values, mode="lines",
            line=dict(color="#9aa0a6", width=1.5), name="Actual (history)"))
        subtitle = f"Last {window} days of actual data + {days}-day forecast"
    else:
        # Smoothed: whole history as a daily average + future daily forecast.
        hist_daily = history.resample("D").mean()
        fut_daily = future[["yhat", "yhat_lower", "yhat_upper"]].resample("D").mean()
        add_band(fig, fut_daily.index, fut_daily["yhat_lower"], fut_daily["yhat_upper"])
        fig.add_trace(go.Scatter(
            x=fut_daily.index, y=fut_daily["yhat"], mode="lines",
            line=dict(color="#0078ff"), name="Forecast (daily avg)"))
        fig.add_trace(go.Scatter(
            x=hist_daily.index, y=hist_daily.values, mode="lines",
            line=dict(color="#9aa0a6", width=1.5), name="Actual (daily avg)"))
        subtitle = "Daily average across the full history"

    fig.update_layout(
        height=460, xaxis_title="Date", yaxis_title="Search interest", title=subtitle,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=60),
    )
    st.plotly_chart(fig, use_container_width=True)

    future_avg = future["yhat"].mean()
    recent_avg = history.tail(days * 24).mean()
    delta = (future_avg - recent_avg) / recent_avg * 100
    direction = "higher" if delta >= 0 else "lower"
    st.success(
        f"Over the next **{days} days**, average search interest is projected at "
        f"**{future_avg:.0f}** — about **{abs(delta):.1f}% {direction}** than the "
        f"most recent {days}-day average. The shaded band shows the likely range."
    )


# --------------------------------------------------------------------------- #
# Tab 2: Seasonality
# --------------------------------------------------------------------------- #
with tab_seasonality:
    st.subheader("When do people search the most?")

    by_hour = analysis.traffic_by_hour(trends)
    by_weekday = analysis.traffic_by_weekday(trends)
    by_week = analysis.traffic_by_week_of_year(trends)

    peak_hour = int(by_hour.idxmax())
    peak_day = by_weekday.idxmax()
    low_week = int(by_week.idxmin())

    c1, c2, c3 = st.columns(3)
    c1.metric("⏰ Busiest hour", f"{peak_hour:02d}:00")
    c2.metric("📅 Busiest day", peak_day)
    c3.metric("📉 Quietest week of year", f"Week {low_week}")

    st.plotly_chart(
        px.line(by_hour, markers=True, title="Average traffic by hour of day")
        .update_layout(showlegend=False, yaxis_title="Search interest"),
        use_container_width=True,
    )
    st.plotly_chart(
        px.bar(by_weekday, title="Average traffic by day of week")
        .update_layout(showlegend=False, yaxis_title="Search interest"),
        use_container_width=True,
    )
    st.plotly_chart(
        px.line(by_week, title="Average traffic by week of the year")
        .update_layout(showlegend=False, yaxis_title="Search interest"),
        use_container_width=True,
    )
    st.info(
        f"**Takeaway:** interest peaks around **{peak_hour:02d}:00** and is "
        f"strongest on **{peak_day}** — useful timing for marketing campaigns."
    )


# --------------------------------------------------------------------------- #
# Tab 3: Search vs. stock
# --------------------------------------------------------------------------- #
with tab_stock:
    st.subheader("Does search interest predict the stock price?")
    combined = get_combined()

    norm = combined[["close", "Search Trends"]].copy()
    norm = (norm - norm.min()) / (norm.max() - norm.min())
    norm.columns = ["Stock price (scaled)", "Search interest (scaled)"]
    st.plotly_chart(
        px.line(norm, title="Search interest vs. stock price (both scaled 0–1)")
        .update_layout(yaxis_title="Scaled value", legend_title=""),
        use_container_width=True,
    )

    corr = analysis.correlation_table(combined)
    st.plotly_chart(
        px.imshow(
            corr, text_auto=".2f", color_continuous_scale="RdBu", zmin=-1, zmax=1,
            title="Correlation between search, volatility, and returns",
        ),
        use_container_width=True,
    )
    st.warning(
        "**Takeaway:** the correlation between lagged search interest and stock "
        "returns is near zero. Search trends reveal real consumer interest, but "
        "on their own they are **not** a reliable predictor of stock moves. "
        "This is a demo, not investment advice."
    )

st.caption(
    "Data originally from the edX AI bootcamp dataset mirror · "
    "Forecasts by Prophet · Built with Streamlit"
)
