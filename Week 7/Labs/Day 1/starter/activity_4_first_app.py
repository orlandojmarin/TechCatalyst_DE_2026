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
    # TODO: read the CSV at `path` with pd.read_csv, parsing the "timestamp"
    # column as dates and using it as the index (parse_dates=["timestamp"],
    # index_col="timestamp"). Then take the "value" column, resample it to
    # daily totals with .resample("D").sum(), and return that Series.
    # Result: a Series with a DatetimeIndex, 215 daily values, running from
    # 2014-07-01 to 2015-01-31.
    #
    # The line below is a placeholder so the app can boot before you finish
    # this function. Replace it with your real return statement.
    return pd.Series(dtype="float64", index=pd.DatetimeIndex([], name="timestamp"))


daily = load_taxi(str(DATA))

st.title("NYC taxi demand")
st.write(f"{len(daily):,} days, {daily.index.min().date()} to {daily.index.max().date()}")

left, right = st.columns(2)
# TODO: call left.metric(...) for the busiest day: label "Busiest day",
# value f"{daily.max():,.0f}", and help=str(daily.idxmax().date()) so the
# date shows on hover. Then call right.metric(...) the same way for the
# quietest day, using daily.min() and daily.idxmin(). Result: two metric
# tiles side by side, one showing the busiest day's ride count and one
# showing the quietest.

# TODO: call st.line_chart(daily) to plot the daily ride counts. Result: a
# line chart of NYC taxi demand from 2014-07-01 to 2015-01-31, with a
# visible dip around the January 2015 blizzard.

with st.expander("See the raw daily numbers"):
    st.dataframe(daily.to_frame("rides"))
