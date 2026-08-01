# Activity 0: Environment Setup for Visualization and Streamlit

**Module:** Week 7 Day 1
**Estimated Time:** 20 minutes
**Difficulty:** Beginner
**Format:** Individual
**Prerequisites:** Repo cloned, VS Code open at the repo root, the repo-root UV environment already created

## Objective

Today builds interactive visualizations with hvPlot and Plotly, then wraps them into a small Streamlit app. This activity adds the six packages the day needs to your shared environment and gets your work folder ready.

## Install the visualization packages

Run this from the repository root:

```bash
uv add hvplot streamlit plotly yfinance statsmodels jupyter-bokeh
```

This records the six packages in the root `pyproject.toml`, the same file every other week has been using. There is one UV project for the whole class, so everyone installs into the same `pyproject.toml` and the same `.venv`, and `uv sync` reproduces it for anyone who pulls the repo.

`jupyter-bokeh` is the one that is not obvious. hvPlot draws with Bokeh, and Bokeh needs that package to render inside Jupyter. Without it your hvPlot charts come out blank in Activity 2, with no error to tell you why.

## Create your work folder

From the repository root:

```bash
mkdir -p student-work/week7/day1
```

## Copy the data

Copy the provided data folder into your work folder. Do not edit the files under `Week 7/Labs/Day 1/` in place.

```bash
cp -R "Week 7/Labs/Day 1/data" student-work/week7/day1/
```

The reason: the instructor pushes new files to `Week 7/Labs/...` over the rest of the course. If you edit a provided file directly, your next `git pull` can conflict with that update. Working only inside `student-work/` keeps your changes out of the instructor's path.

## Select the interpreter

In VS Code and in Jupyter, select `<repo-root>/.venv/bin/python` as the interpreter or kernel:

- VS Code: open the command palette, run **Python: Select Interpreter**, and choose the one whose path ends in `.venv/bin/python` at the repo root.
- Jupyter: click **Select Kernel** at the top right of a notebook and choose the same repo-root `.venv`.

If you pick the wrong interpreter, the symptom is `ModuleNotFoundError: No module named 'hvplot'` even though `uv add` reported success. That means the notebook or script is running against a different Python than the one you just installed into.

## Fix a `VIRTUAL_ENV` mismatch warning

If a terminal shows:

```text
warning: `VIRTUAL_ENV=...` does not match the project environment path `.venv` and will be ignored
```

a different project's environment is still active in that shell. Fix it:

```bash
deactivate
```

Then return to the repository root and, if you want the prompt to show the active environment, optionally run:

```bash
source .venv/bin/activate
```

## Confirm the install

Run this from the repository root:

```bash
uv run python -c "
import pandas, hvplot, streamlit, statsmodels, plotly, yfinance, matplotlib
import hvplot.pandas
print(pandas.__version__, hvplot.__version__, streamlit.__version__, statsmodels.__version__)
"
```

Expected output:

```text
3.0.3 0.12.2 1.60.0 0.14.6
```

Your exact version numbers may differ slightly if packages have updated since this was written, but the command must run with no `ImportError`, and the first number (pandas) must start with `3.`.

## Success Criteria

- `uv add hvplot streamlit plotly yfinance statsmodels jupyter-bokeh` completed with no errors, run from the repository root.
- The import check above runs cleanly and pandas starts with `3.`.
- `student-work/week7/day1/data/` contains `hospital_claims.parquet`, `closing_price.csv`, and `nyc_taxi.csv`.
- Your notebooks and scripts use the repo-root `.venv` interpreter, not a different environment.
- No new `.venv` or `pyproject.toml` exists inside `student-work/`.
