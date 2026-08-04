"""Activity 4: your first Streamlit app."""

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Taxi Demand", layout="wide")

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


daily = load_taxi(str(DATA))

st.title("NYC taxi demand")
st.write(f"{len(daily):,} days, {daily.index.min().date()} to {daily.index.max().date()}")

left, right = st.columns(2)
left.metric("Busiest day", f"{daily.max():,.0f}", help=str(daily.idxmax().date()))
right.metric("Quietest day", f"{daily.min():,.0f}", help=str(daily.idxmin().date()))

st.line_chart(daily)

with st.expander("See the raw daily numbers"):
    st.dataframe(daily.to_frame("rides"))
