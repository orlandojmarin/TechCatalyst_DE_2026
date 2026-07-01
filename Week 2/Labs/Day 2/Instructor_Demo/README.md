# Instructor Demo: Python Foundations (notebook to script)

**Audience:** Week 2 Day 2, before the drills
**Environment:** VS Code with the Jupyter extension, Python 3.13, UV
**Files:** `Python_Foundations_Demo.ipynb` (47 cells), `claims.csv`, `demo_pipeline.py`
**Estimated time:** 50 to 70 minutes (modular: skip any section your group already has)

## Purpose

Teach the day's Python live in a notebook, from the **basics to modern Python
3.7+**, covering every concept the drills practice, framed by the data engineering
flow (ingest, inspect, transform, analyze, output). Then move the same logic into a
`.py` script so students are ready for the script-based drills and homework and
know how to run them. The notebook is intentionally comprehensive so it doubles as
a reference; skip or skim sections the group is already comfortable with.

## Setup

1. Open this `Instructor_Demo/` folder in VS Code.
2. Open `Python_Foundations_Demo.ipynb`.
3. Click **Select Kernel** and choose your project `.venv` (the one in
   `student-work/week2/day2/.venv`, or any UV project `.venv`). Run a cell to
   confirm the kernel works.
4. Keep `demo_pipeline.py` open in a second tab; you will switch to it at the end.

The notebook reads `claims.csv` from this folder, so run it with this folder as the
working directory (the default when you open the notebook here).

## Flow and talking points

The notebook has four parts. Run a cell, ask the prediction question, then run it.

**Part 1: Basics** (types, f-strings, strings, collections, control flow,
functions, exceptions)
- Map each cell to its drill (types/f-strings -> 01, conditionals -> 02, loops ->
  04/07, lists -> 05, dicts -> 06, functions -> 08).
- Pause points: "What breaks if `reserve` stays a string?" and "Why is a set the
  right tool for distinct policy types?"

**Part 2: Data I/O** (text, CSV, JSON, SQLite)
- This is the ingest/output of the DE flow, and the bridge to Day 4 (pandas) and
  the SQL weeks. The CSV cell defines `claims`, reused below.
- Pause point: "JSON is what an API returns tomorrow; how is it different from the
  flat CSV?"

**Part 3: Modern Python 3.7+** (comprehensions, lambdas/map/filter, generators,
walrus, match/case, classes, dataclasses + type hints)
- This is the Advanced Track material. Emphasize these are everyday professional
  Python, not exotic tricks.
- Pause points: "Read this comprehension as a sentence", "Why is a claim a class
  but `loss_ratio` a function?", and "What did `@dataclass` write for us?"

**Part 4: Put it together** (a small aggregate pipeline, then notebook -> script)
- Pause point: "Which policy type is running hot, and what would you tell
  underwriting?"

## The notebook to script transition (do this live)

This is the bridge to the homework.

1. Show the last two markdown cells: notebooks are for exploring; `.py` files are
   how pipelines ship and how the drills and homework are structured.
2. Switch to `demo_pipeline.py`. Point out it is the same ingest, transform,
   analyze, output, now wrapped in functions and a `main()`.
3. Run it from the terminal so they see script execution:

   ```bash
   uv run python demo_pipeline.py
   ```

4. Then walk the student workflow live (this sets up Activity 0):
   - Create `student-work/week2/day2/` at the repo root and `cd` into it.
   - `uv init`, and note the `.venv` is created right there.
   - Select that `.venv` as the interpreter.
   - Copy a drill's `Unsolved` scaffold (and any `Resources/`) into the folder.
   - Run it with `uv run python ...`.

## Expected observations

- Loss ratio by policy type prints `auto: 45.6%`, `liability: 44.5%`,
  `property: 83.9%`.
- Open claims: `CLM-D01, CLM-D03, CLM-D05, CLM-D06, CLM-D07, CLM-D08`.
- The notebook and `demo_pipeline.py` produce the same numbers. That is the point:
  same logic, two delivery forms.

## Cleanup

The output `loss_ratio_report.json` is generated; delete it before committing if
you do not want it tracked.

## Troubleshooting

- Notebook cannot find `claims.csv`: the working directory is wrong. Open the
  notebook from this folder, or `cd` here first.
- Imports or kernel errors: confirm the selected kernel is a project `.venv`, not a
  system Python.
- A cell depends on an earlier cell: run the notebook top to bottom. If you jump
  around, restart the kernel and run all.
