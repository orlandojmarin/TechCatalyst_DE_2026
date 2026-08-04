"""Activity 6: forecast and anomaly detection, built on the Demand Explorer."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Demand Explorer", layout="wide")

# This lets the same file run both from the repo (data is one level up, in
# ../data/) and from a student-work/ folder (data is a sibling, in ./data/).
HERE = Path(__file__).parent
DATA = HERE / "data" / "nyc_taxi.csv"
if not DATA.exists():
    DATA = HERE.parent / "data" / "nyc_taxi.csv"


@st.cache_data
def load_taxi(path: str) -> pd.Series:
    """Load the taxi CSV and return daily ride counts.

    Returns a pandas Series with a DatetimeIndex, one value per day,
    summed from the half-hourly readings in the raw file.
    """
    raw = pd.read_csv(path, parse_dates=["timestamp"], index_col="timestamp")
    return raw["value"].resample("D").sum()


@st.cache_data
def load_prices(ticker: str, start: str, end: str) -> pd.Series:
    """Download daily closing prices for `ticker` between `start` and `end`.

    Returns a pandas Series of closing prices indexed by date. Passing
    auto_adjust=True and multi_level_index=False is required: without them,
    yfinance returns MultiIndex columns shaped like ('Close', 'AAPL')
    instead of a flat 'Close' column, and frame["Close"] would return a
    DataFrame instead of a Series.
    """
    frame = yf.download(
        ticker, start=start, end=end, progress=False,
        auto_adjust=True, multi_level_index=False,
    )
    return frame["Close"]


st.title("Demand Explorer")

source = st.sidebar.radio("Data source", ["NYC taxi demand", "Live ticker"])

if source == "NYC taxi demand":
    series = load_taxi(str(DATA))
    label = "Daily rides"
else:
    ticker = st.sidebar.text_input("Ticker", "AAPL")
    start = st.sidebar.date_input("Start", pd.Timestamp("2023-01-01"))
    end = st.sidebar.date_input("End", pd.Timestamp.today())
    try:
        series = load_prices(ticker, str(start), str(end))
        label = f"{ticker} closing price"
    except Exception:
        st.error("Could not fetch that ticker. Check the symbol, or switch to NYC taxi demand.")
        st.stop()

if series.empty:
    st.error("That query returned no rows. Widen the date range, check the ticker symbol, or switch sources.")
    st.stop()

window = st.sidebar.slider("Smoothing window (days)", 1, 30, 7)
smoothed = series.rolling(window).mean()

a, b, c = st.columns(3)
a.metric("Latest", f"{series.iloc[-1]:,.0f}")
b.metric("Average", f"{series.mean():,.0f}")
c.metric("Peak", f"{series.max():,.0f}")

chart = pd.DataFrame({label: series, f"{window}-day average": smoothed})
st.plotly_chart(
    px.line(chart, title=f"{label}, smoothed over {window} days"),
    width="stretch",
)

st.subheader("Forecast")
horizon = st.sidebar.slider("Forecast horizon (days)", 7, 60, 30)

# TODO: fit a Holt-Winters model on `series` and forecast `horizon` steps
# ahead:
#   fit = ExponentialSmoothing(series, trend="add", seasonal="add",
#                               seasonal_periods=7).fit()
#   future = fit.forecast(horizon)
# `seasonal_periods=7` encodes a weekly cycle, which is correct for daily
# taxi data. Keep that in mind if you switch to the live ticker: markets do
# not have a clean 7-day cycle, so the seasonal component means much less
# for stock prices.
#
# The line below is a placeholder so the app can boot before you finish
# this. Replace it.
future = series.tail(horizon)

combined = pd.DataFrame({"actual": series, "forecast": future})
st.plotly_chart(
    px.line(combined, title=f"Actual demand and a {horizon}-day Holt-Winters forecast"),
    width="stretch",
)

st.subheader("Anomalies")
threshold = st.sidebar.slider("Anomaly threshold (z)", 2.0, 5.0, 3.0, step=0.5)

# This is the obvious first attempt at a rolling baseline: a centered
# window. It is intentionally the wrong tool here. A centered window of 28
# days needs 14 days of data on BOTH sides of each point, so the most
# recent 14 days in the series get a NaN baseline, and NaN never exceeds
# `threshold`. That silently hides the most recent anomalies, which are
# exactly the ones a live monitoring system needs to catch.
#
# TODO: once you have confirmed the problem, replace this with a trailing
# window that only looks backward, so every day (including the most recent)
# gets a real baseline:
#   baseline = series.shift(1).rolling(28)
baseline = series.rolling(28, center=True)

# TODO: compute the z-score of each day against `baseline`, then keep the
# days whose z-score magnitude exceeds `threshold`:
#   z = (series - baseline.mean()) / baseline.std()
#   flags = series[z.abs() > threshold]
#
# The two lines below are placeholders so the app can boot before you
# finish this. Replace them.
z = pd.Series(0.0, index=series.index)
flags = series.iloc[0:0]

st.write(f"{len(flags)} days exceed {threshold} standard deviations.")

fig = px.line(series.to_frame("value"), title="Demand with anomalies marked")
# TODO: add a scatter trace marking the flagged anomalies on top of the
# line:
#   fig.add_scatter(x=flags.index, y=flags.values, mode="markers",
#                    marker={"size": 11, "color": "red"}, name="anomaly")
st.plotly_chart(fig, width="stretch")

st.dataframe(pd.DataFrame({"value": flags, "z": z[flags.index].round(2)}))
