# Week 7 · Day 1: From Notebook Charts to a Data App

Week 6 closed with you deciding when a problem needs AI at all and defending that call in front of your team. This week turns to a different kind of judgment: how you show anyone what you found. Today starts with the same hospital claims and closing price data from earlier weeks, plotted three ways (`.plot`, hvPlot, Plotly Express), so you feel exactly what an interactive chart buys you over a static one. Then you stop making charts and start building an app: a Streamlit page that reruns itself on every click, a switchable data source with a real failure mode to handle, a forecast and an anomaly detector you have to debug before it tells the truth, and a narration button that hands an LLM computed facts instead of raw data.

By the end of the day you will have shipped a small, real Streamlit app, not just a notebook, and you will have practiced the habit this course keeps coming back to: name the decision a chart supports before you pick its type, and never let a smoothing window or a forecast quietly delete the finding you actually care about.

---

## Daily Sequence Arc

| Arc Block | Topic | Focus |
| :--- | :--- | :--- |
| Block 1 | Pandas Plot Fundamentals | Static charts straight off `.plot`, no new import, on hospital claims and closing price data ([Activity 1](./Activity_1_Pandas_Plot_Fundamentals.ipynb)) |
| Block 2 | Interactive Charts with hvPlot | The one-line upgrade from `.plot` to `.hvplot`, and what hover, zoom, and a linked dropdown add ([Activity 2](./Activity_2_Interactive_With_hvPlot.ipynb)) |
| Block 3 | Charts That Argue | Chart-choice rules, label titles versus conclusion titles, and the six-step decision arc, all against the same claims data ([Activity 3](./Activity_3_Charts_That_Argue.ipynb)) |
| Block 4 | Your First Streamlit App | Run-and-read first: resampling and metric formatting worked in a notebook with visible output ([Concepts notebook](./Activity_4_Concepts_Resampling_and_Metrics.ipynb)). Then build a small NYC taxi app with metrics, a line chart, and a direct look at the Streamlit rerun model and `@st.cache_data` ([Activity 4](./Activity_4_First_Streamlit_App.md)) |
| Block 5 | The Demand Explorer | Run-and-read first: the `yfinance` MultiIndex trap and rolling smoothing worked in a notebook with visible output ([Concepts notebook](./Activity_5_Concepts_yfinance_and_Smoothing.ipynb)). Then build a switchable data source (bundled CSV or a live `yfinance` ticker), a smoothing control, and graceful handling of a bad ticker ([Activity 5](./Activity_5_Demand_Explorer.md)) |
| Block 6 | Forecast and Anomalies | Run-and-read first: `.fit()` and `.forecast()` on a Holt-Winters model worked in a notebook with visible output ([Concepts notebook](./Activity_6_Concepts_Holt_Winters.ipynb)). Then build a Holt-Winters forecast and a rolling z-score anomaly detector, including a centered-window bug you are meant to hit before you fix it ([Activity 6](./Activity_6_Forecast_and_Anomalies.md)) |
| Block 7 | Narrate With an LLM | Run-and-read first: `max_tokens` and `temperature` worked against a real LLM call with visible output ([Concepts notebook](./Activity_7_Concepts_Tokens_and_Temperature.ipynb)). Then build a button that asks an LLM to draft an analyst paragraph from computed facts only, then a required fact-check and correction ([Activity 7](./Activity_7_Narrate_With_LLM.md)) |
| Block 8 | Chart Clinic | Diagnosing a bad claims dashboard, redesigning it, and presenting and defending the redesign in teams ([Group Activity](./Group_Activity_Chart_Clinic.md)) |

Students who finish early can continue with the optional [Deploy Stretch](./Deploy_Stretch_Streamlit_Cloud.md), which puts a finished app on a public URL.

---

## Core Learning Objectives

1. **Chart Selection:** Match a question's shape (comparison, trend, relationship, distribution, part-to-whole) to the chart type that answers it, and name the chart type that would mislead instead.
2. **Chart Escalation:** Move the same finding from a static `.plot` chart, to an interactive hvPlot chart, to an interactive Plotly Express chart, and explain when interactivity earns its place and when it is noise.
3. **The Streamlit Rerun Model:** Explain why a Streamlit script reruns from the top on every interaction, and use `@st.cache_data` to keep an expensive load or call from repeating unnecessarily.
4. **Resilient Apps:** Build an app that switches data sources cleanly and fails with a readable `st.error` message, never a traceback, when a live source misbehaves.
5. **Honest Analysis:** Debug a smoothing window and an anomaly detector that run without errors and quietly produce the wrong answer, and keep an LLM narration grounded in computed facts instead of raw data.

---

## Setup Instructions

Start with [Activity 0](./Activity_0_UV_Viz_Setup.md). It adds six packages to the shared root environment: `hvplot`, `streamlit`, `plotly`, `yfinance`, `statsmodels`, and `jupyter-bokeh` (the last one renders hvPlot's Bokeh charts inside Jupyter; skip it and Activity 2's charts come out blank with no error). Run `uv add hvplot streamlit plotly yfinance statsmodels jupyter-bokeh` from the repository root, create `student-work/week7/day1/`, and copy the `data/` folder into it. Everything today uses the single root `.venv`; there is no second environment this week.

---

## Lab Index

### Provided Files

| File | Purpose |
| :--- | :--- |
| `Reading_Charts_That_Argue.md` | Student reading: chart choice, label versus conclusion titles, honest smoothing and forecasting, and the six-step arc |
| `Student_Resources.md` | Documentation links, code concepts, and the lab deliverable checklist |
| `Activity_0_UV_Viz_Setup.md` | Installing the six visualization packages and preparing your `student-work/` folder |
| `Activity_1_Pandas_Plot_Fundamentals.ipynb` | Static charts with `.plot` on hospital claims and closing price data |
| `Activity_2_Interactive_With_hvPlot.ipynb` | The same charts rebuilt with `.hvplot`, hover, zoom, and a linked dropdown |
| `Activity_3_Charts_That_Argue.ipynb` | Chart-choice rules and title rewrites (label versus conclusion) on the same claims data |
| `Activity_4_Concepts_Resampling_and_Metrics.ipynb` | Run-and-read: `.resample()`, `.max()`/`.idxmax()`, and f-string number formatting, fully worked before you open Activity 4's `.py` |
| `Activity_4_First_Streamlit_App.md` | A first Streamlit app on NYC taxi data, plus the rerun-model experiment with `@st.cache_data` |
| `Activity_5_Concepts_yfinance_and_Smoothing.ipynb` | Run-and-read: the `yfinance` MultiIndex-versus-flat-columns trap and rolling-window smoothing, fully worked before you open Activity 5's `.py` |
| `Activity_5_Demand_Explorer.md` | Switchable data source (bundled CSV or live `yfinance` ticker), a smoothing slider, and bad-ticker handling |
| `Activity_6_Concepts_Holt_Winters.ipynb` | Run-and-read: exponential smoothing, `.fit()` versus `.forecast()`, fully worked before you open Activity 6's `.py` |
| `Activity_6_Forecast_and_Anomalies.md` | Holt-Winters forecasting and a rolling z-score anomaly detector, including the centered-window trap |
| `Activity_7_Concepts_Tokens_and_Temperature.ipynb` | Run-and-read: `max_tokens` and `temperature` against a real LLM call, fully worked before you open Activity 7's `.py` |
| `Activity_7_Narrate_With_LLM.md` | An LLM narration button fed computed facts only, plus a required fact-check and correction |
| `Deploy_Stretch_Streamlit_Cloud.md` | Optional: deploying a finished app to Streamlit Community Cloud with a public URL |
| `Group_Activity_Chart_Clinic.md` | Diagnosing and redesigning a bad claims dashboard, presented and defended in teams |
| `quiz/Day1_Quiz.md` | Knowledge check and exit ticket (Markdown Mash) |
| `data/hospital_claims.parquet` | Medicare hospital billing data used in Activities 1 through 3 |
| `data/closing_price.csv` | Stock closing price data used in Activities 1 through 3 |
| `data/nyc_taxi.csv` | Daily NYC taxi ride counts used in Activities 4 through 7 |
| `starter/activity_4_first_app.py` | Starter script for Activity 4 |
| `starter/activity_5_demand_explorer.py` | Starter script for Activity 5 |
| `starter/activity_6_forecast_anomalies.py` | Starter script for Activity 6 |
| `starter/activity_7_narrate_with_llm.py` | Starter script for Activity 7 |
| `solutions/` | Completed notebooks and scripts for Activities 1 through 7, for instructor and self-check use |

### Deliverables

The four Concepts notebooks for Activities 4 through 7 are run-and-read references, not deliverables. Run each one before opening the matching `.py` starter, but do not submit it and do not expect a checkbox for it below; only the app file for each activity is graded.

| Deliverable File | Target Location | Purpose |
| :--- | :--- | :--- |
| Pandas Plot Notebook | `student-work/week7/day1/Activity_1_Pandas_Plot_Fundamentals.ipynb` | Completed static charts on claims and price data |
| hvPlot Notebook | `student-work/week7/day1/Activity_2_Interactive_With_hvPlot.ipynb` | Completed interactive rebuild with hvPlot |
| Charts That Argue Notebook | `student-work/week7/day1/Activity_3_Charts_That_Argue.ipynb` | Completed chart-choice and title rewrite exercises |
| First Streamlit App | `student-work/week7/day1/activity_4_first_app.py` | Working taxi metrics app, rerun experiment completed |
| Demand Explorer App | `student-work/week7/day1/activity_5_demand_explorer.py` | Working switchable-source app with bad-ticker and empty-result handling |
| Forecast and Anomalies App | `student-work/week7/day1/activity_6_forecast_anomalies.py` | Working forecast and anomaly detector, trailing window fix applied, six flagged dates interpreted |
| LLM Narration App | `student-work/week7/day1/activity_7_narrate_with_llm.py` | Working narration button, generated paragraph fact-checked and corrected in the app's text box |
| Group Activity Worksheet | `student-work/week7/day1/Group_Activity_Chart_Clinic.md` | Completed diagnosis, redesign, and six-step arc for the assigned dashboard |
| Exit Ticket | `quiz/Day1_Quiz.md` | Completed knowledge check |
| PR Description | GitHub Pull Request | Summary of your chart-choice rewrites, your Activity 6 anomaly interpretation, and your Activity 7 fact-check corrections |
