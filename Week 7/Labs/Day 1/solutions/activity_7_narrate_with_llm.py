"""Activity 7: narrate the anomaly finding with an LLM, then fact-check it."""

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Narrate with an LLM", layout="wide")

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


def build_facts(series: pd.Series, flags: pd.Series, z: pd.Series, window: int) -> str:
    """Build a plain-text facts block from computed values only.

    This is the boundary the model is not allowed to cross. The model
    never sees `series`, `flags`, or `z` as data structures, only the
    strings this function writes. If a number is not in this text, the
    model has no way to know it.
    """
    lines = [
        f"Series: NYC daily taxi rides, {series.index.min().date()} to {series.index.max().date()}.",
        f"Mean daily rides: {series.mean():,.0f}. Smoothing window in use: {window} days.",
        "Anomalies detected with a trailing 28-day z-score, threshold 3:",
    ]
    for date, value in flags.items():
        lines.append(f"  {date.date()}: {value:,.0f} rides, z = {z[date]:.2f}")
    return "\n".join(lines)


@st.cache_data(show_spinner=False)
def draft_narrative(facts: str) -> str:
    """Ask the model to narrate the facts block, and nothing else.

    `@st.cache_data` keys on the `facts` argument, so asking twice for the
    same facts returns the cached answer instead of calling the API again.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content":
             "You write short analyst notes. Use ONLY the facts given. Do not invent numbers."},
            {"role": "user", "content":
             facts + "\n\nWrite three sentences for an operations manager."},
        ],
        max_tokens=250,
        temperature=0.2,
    )
    return response.choices[0].message.content


st.title("Narrate with an LLM")

st.markdown(
    "This app hands the model a **facts block built entirely from computed "
    "values**, the output of Activity 6's anomaly detector. The model never "
    "sees the raw series and never performs any analysis. It only writes "
    "sentences about numbers the code already computed."
)

series = load_taxi(str(DATA))
window = 28
threshold = 3.0

baseline = series.shift(1).rolling(window)
z = (series - baseline.mean()) / baseline.std()
flags = series[z.abs() > threshold]

st.subheader("The facts block")
st.caption("This is the ONLY thing the model receives. Not the DataFrame, not the series, not the chart.")
facts = build_facts(series, flags, z, window)
st.code(facts, language="text")

st.subheader("Draft a narrative")
st.caption(
    "The call costs a fraction of a cent. It runs on a button, not on every "
    "rerun, so widening a chart elsewhere on the page never spends a key by "
    "accident. `@st.cache_data` also means pressing the button twice for "
    "the same facts block does not call the API a second time."
)

if st.button("Draft the narrative"):
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("No OPENAI_API_KEY found. Check your .env at the repository root.")
    else:
        with st.spinner("Drafting..."):
            st.write(draft_narrative(facts))

st.subheader("Fact-check it")
st.markdown(
    """
The paragraph above is a first draft, not the deliverable. Run it against this checklist,
then write your own corrected version underneath:

1. Every number in the paragraph appears in the facts block.
2. No date is mentioned that was not flagged.
3. No flagged date is omitted.
4. Superlatives are correct. If it says "the largest drop", confirm that date really has
   the most extreme z-score in the facts block.
5. No causal claim is made that the data does not support.

Model output varies between runs, so there is nothing here to compare your paragraph
against. Check it against the five items above and against the facts block itself,
not against what you expect to see.
"""
)

st.text_area(
    "Your corrected paragraph, plus the list of what the draft got wrong (or confirmation it held up):",
    height=200,
)
