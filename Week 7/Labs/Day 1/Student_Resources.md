# Week 7 · Day 1 - Student Resources: From Notebook Charts to a Data App

> **AI coding tools note:** AI allowed, review required. Week 7 is past the AI-Free Zone that applied to Weeks 1 through 4. You can use an AI assistant while building today's charts and Streamlit apps, but you must be able to explain every line you submit, including why a chart type was chosen, why a caching decorator sits where it does, and why the anomaly detector uses a trailing window instead of a centered one. If you cannot explain a line, do not submit it.

---

## Core Documentation

| Resource | Why It Helps |
| :--- | :--- |
| [pandas chart visualization](https://pandas.pydata.org/docs/user_guide/visualization.html) | Reach for this when you want the full tour of what `.plot` can do beyond a basic line or bar, including subplots and secondary axes |
| [pandas.DataFrame.plot API](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html) | Reach for this when you need the exact keyword for a specific `.plot` call, such as `kind`, `figsize`, or `title`, in Activity 1 |
| [hvPlot user guide](https://hvplot.holoviz.org/user_guide/index.html) | Reach for this when the one-line `.hvplot` upgrade in Activity 2 needs a chart type or option `.plot` does not have, like linked hover across subplots |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Reach for this when you need a Plotly chart type or styling option in Activity 3, or the `px.scatter` and `go.Scatter` calls in Activities 5 and 6 |
| [Streamlit API reference](https://docs.streamlit.io/develop/api-reference) | Reach for this any time you need a widget or layout call you have not used yet, such as `st.sidebar.radio`, `st.metric`, or `st.expander`, across Activities 4 through 7 |
| [Streamlit caching](https://docs.streamlit.io/develop/concepts/architecture/caching) | Reach for this when `@st.cache_data` behaves unexpectedly, for example when a cached function still seems to rerun after you changed an unrelated part of the script |
| [statsmodels ExponentialSmoothing](https://www.statsmodels.org/stable/generated/statsmodels.tsa.holtwinters.ExponentialSmoothing.html) | Reach for this when you need to confirm what `trend`, `seasonal`, and `seasonal_periods` actually control in the Activity 6 forecast |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | Reach for this when wiring the `chat.completions.create` call in Activity 7, the same client you built in Week 6 |
| [yfinance documentation](https://ranaroussi.github.io/yfinance/) | Reach for this when `yf.download` in Activity 5 returns a shape you were not expecting, or you need a parameter beyond `start`, `end`, and `multi_level_index` |

---

## The `.plot` formatting keywords

`.plot` is a thin wrapper over matplotlib. A handful of keywords cover most of what Activity 1 needs:

```python
claims.groupby("Provider State")["ratio"].mean().sort_values().plot(
    kind="barh",       # chart type: line, bar, barh, hist, box, scatter, pie
    figsize=(8, 6),    # width, height in inches
    title="Charge-to-payment ratio by state",
    xlabel="Ratio",
    legend=False,
)
```

`kind` picks the chart type. Everything else is layout and labeling, and none of it changes the underlying data.

## The one-line hvPlot upgrade

hvPlot does not replace `.plot`, it sits next to it. The only change is a second import:

```python
import pandas as pd
import hvplot.pandas  # registers .hvplot on every DataFrame and Series

claims.groupby("Provider State")["ratio"].mean().sort_values().hvplot.barh(
    title="Charge-to-payment ratio by state"
)
```

Same data, same `groupby`, same keyword names in most cases. What changes is the output: a chart you can hover and zoom instead of a static image.

## The Streamlit rerun model and `@st.cache_data`

A Streamlit script is not a program that runs once and waits. It reruns from line 1 on every interaction: a slider move, a button click, an expander opening.

```python
@st.cache_data
def load_taxi(path: str) -> pd.Series:
    return pd.read_csv(path, parse_dates=["timestamp"]).set_index("timestamp")["value"].resample("D").sum()

daily = load_taxi(str(DATA))  # runs once per unique argument, then reads from cache
```

Without `@st.cache_data`, `load_taxi` re-reads and re-resamples the whole file on every single rerun, even if all that happened was opening an expander. With it, the expensive work happens once per distinct input and every later rerun reuses the cached result.

## The yfinance `multi_level_index=False` gotcha

By default, `yf.download(...)` returns a DataFrame with MultiIndex columns shaped like `('Close', 'AAPL')`, not a flat `'Close'` column. That means `frame["Close"]` returns a DataFrame, not a Series, and any call that expects a Series, such as `.rolling()` or `.iloc[-1]`, either fails or silently misbehaves.

```python
frame = yf.download("AAPL", start=start, end=end, auto_adjust=True, multi_level_index=False)
prices = frame["Close"]  # now a plain Series, because multi_level_index=False flattened the columns
```

Forget the two keyword arguments together, and Activity 5's `load_prices` will look correct, run without an error, and still hand the rest of the app the wrong shape.

## Why the LLM in Activity 7 receives facts, not raw data

Activity 7's `build_facts` function turns the anomaly results into a plain text string, the date range, the mean, and each flagged date with its value and z-score, and that string is the only thing sent to the model:

```python
def build_facts(series: pd.Series, flags: pd.Series, z: pd.Series, window: int) -> str:
    lines = [f"Series: NYC daily taxi rides, {series.index.min().date()} to {series.index.max().date()}."]
    for date, value in flags.items():
        lines.append(f"  {date.date()}: {value:,.0f} rides, z = {z[date]:.2f}")
    return "\n".join(lines)
```

The model never sees the DataFrame. It is good at turning a short list of facts into readable prose, and it is not a reliable source of new numbers or new analysis. If a number is not printed into that string, the model has no way to know it exists, so any number in the paragraph that is not in the facts block was invented, not computed. That is why the deliverable is your fact-checked correction, not the generated paragraph.

---

## Lab Deliverable Checklist

| Requirement | Description | Status |
| :--- | :--- | :--- |
| **Environment** | Six packages installed to the root `.venv` via `uv add`, `student-work/week7/day1/data/` populated | ☐ |
| **Pandas plots** | Static charts built with `.plot` on hospital claims and closing price data | ☐ |
| **hvPlot rebuild** | Same charts rebuilt with `.hvplot`, one import added, nothing else changed | ☐ |
| **Chart choice and titles** | Chart-choice rules applied, label titles rewritten as conclusion titles | ☐ |
| **First Streamlit app** | Metrics, line chart, and table working; rerun experiment completed with and without `@st.cache_data` | ☐ |
| **Demand Explorer** | Switchable source (taxi CSV or live ticker) working; bad ticker and empty date range both show `st.error`, never a traceback | ☐ |
| **Forecast** | Holt-Winters forecast implemented and checked against the standalone verification values | ☐ |
| **Anomaly detector** | Centered-window bug reproduced and explained, then fixed with a trailing window; all six flagged dates matched and interpreted | ☐ |
| **LLM narration** | Narration button working, generated paragraph checked against all five checklist items, corrected paragraph and notes written in the app | ☐ |
| **Group activity** | Chart Clinic diagnosis, redesign, and six-step arc completed and presented | ☐ |
| **Exit ticket** | Completed `quiz/Day1_Quiz.md` | ☐ |
