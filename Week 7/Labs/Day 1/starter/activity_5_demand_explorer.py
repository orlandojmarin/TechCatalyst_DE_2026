"""Activity 5: the Demand Explorer, with a switchable data source."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

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

    Returns a pandas Series of closing prices indexed by date.
    """
    # TODO: call yf.download(ticker, start=start, end=end, progress=False,
    # auto_adjust=True, multi_level_index=False) and store the result in a
    # variable called `frame`. Both keyword arguments are required: without
    # them, yfinance returns MultiIndex columns shaped like ('Close', 'AAPL')
    # instead of a flat 'Close' column, and frame["Close"] below would
    # return a DataFrame instead of a Series. Then return frame["Close"].
    #
    # The line below is a placeholder so the app can boot before you finish
    # this function. Replace it with your real return statement.
    return pd.Series(dtype="float64")


st.title("Demand Explorer")

# TODO: replace the line below with
# source = st.sidebar.radio("Data source", ["NYC taxi demand", "Live ticker"])
# Result: a radio control in the sidebar that lets you switch between the
# bundled taxi data and a live ticker lookup.
source = "NYC taxi demand"

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

# TODO: replace the two placeholder lines below with
# window = st.sidebar.slider("Smoothing window (days)", 1, 30, 7)
# smoothed = series.rolling(window).mean()
# Result: a sidebar slider that controls how smooth the second line on the
# chart below is.
window = 7
smoothed = series.rolling(window).mean()

a, b, c = st.columns(3)
a.metric("Latest", f"{series.iloc[-1]:,.0f}")
b.metric("Average", f"{series.mean():,.0f}")
c.metric("Peak", f"{series.max():,.0f}")

chart = pd.DataFrame({label: series, f"{window}-day average": smoothed})
# TODO: call st.plotly_chart(...) passing a px.line(chart, title=f"{label},
# smoothed over {window} days") figure, with use_container_width=True.
# Result: a Plotly line chart with two series, the raw values and the
# smoothed average.
