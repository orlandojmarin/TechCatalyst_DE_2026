# Activity 0: Environment Check and File Copy

**Module:** Week 3 Day 1
**Estimated Time:** 25 minutes
**Difficulty:** Beginner
**Format:** Individual, then pair check
**Prerequisites:** Repo cloned, VS Code open at the repo root, the Week 2 Day 3 repo-root environment already created

## Objective

Confirm the shared repo-root environment still works after the long weekend, add the two packages Week 3 Day 1 needs, and copy today's starter files into `student-work/week3/day1/`.

## Background

In Week 2 Day 3 you created one UV project at the repo root. That is still the plan: one environment at the root of the folder VS Code has open, so the interpreter and notebook kernel are auto-detected, and one place where every `uv add` lands.

Keep the two ideas separate, same as before:

- **The environment** (`pyproject.toml`, `uv.lock`, `.venv/`) lives at the repo root. It is generated and gitignored, so `git pull` never touches it.
- **Your work** (copied notebooks, scripts, and data) lives under `student-work/week3/day1/`. The instructor only ships files outside `student-work/`, so a `git pull` never conflicts with what you wrote.

Today you do not run `uv init` and you do not create a new `.venv`. You reuse the environment you already have and only add what is new.

## Instructions

1. Open a terminal in VS Code and confirm you are at the repo root.

   ```bash
   pwd
   # should end with the cloned repo folder, for example .../TechCatalyst_DE_2026
   ls -a
   # you should see .venv, pyproject.toml, and uv.lock from Week 2
   ```

   If `.venv` or `pyproject.toml` is missing (you missed Week 2 Day 3 or re-cloned), rebuild the root project first:

   ```bash
   uv init
   uv add requests httpx python-dotenv boto3 google-genai pandas polars ipykernel
   ```

2. Add today's new packages from the repo root:

   ```bash
   uv add pyarrow google-cloud-storage
   ```

   Everything else Day 1 needs (pandas, Polars, boto3, ipykernel) is already in the environment from Week 2.

3. Confirm the environment and check the pandas version:

   ```bash
   uv run python -c "import pandas, polars, pyarrow; print('env ok, pandas', pandas.__version__)"
   ```

   Expected: `env ok, pandas 3.0.x`. Week 3 content assumes pandas 3. If you see a 2.x version, run `uv add "pandas>=3.0"`. If that fails with a Python version error, ask the instructor: pandas 3 requires Python 3.11 or newer, and the fix is usually `uv python pin 3.12` followed by `uv sync`.

4. Create your Day 1 work folder and copy today's files into it. Work on the copies, never on the provided originals.

   ```bash
   mkdir -p student-work/week3/day1
   cp "Week 3/Labs/Day 1/Activity_1_Python_Refresh_Drills.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Activity_2_Pandas_Polars_Quick_Drills.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Activity_3_DataFrame_Cleaning_Lab.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Activity_4_Automation_Drills.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/starter/taxi_review.py" student-work/week3/day1/
   cp -R "Week 3/Labs/Day 1/data" student-work/week3/day1/
   ```

   Optional bonus labs, if you plan to work on them after class:

   ```bash
   cp "Week 3/Labs/Day 1/Bonus_Lab_Parquet_vs_CSV.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Bonus_Dask_Intro.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Bonus_Modin_Intro.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Bonus_FireDucks_Intro.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Bonus_Lab_Engine_Probes.md" student-work/week3/day1/
   ```

5. Copy the carryover medallion notebook, script scaffold, and data:

   ```bash
   cp "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/Medallion_ETL_Mini_Project.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/starter/medallion_etl.py" student-work/week3/day1/
   cp -R "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/data/raw" student-work/week3/day1/data/
   ```

6. List what you have:

   ```bash
   find student-work/week3/day1 -maxdepth 3 -type f | sort
   ```

7. Open one of your copied notebooks and confirm the kernel. Click **Select Kernel** at the top right and pick the repo-root environment, shown as **.venv (Python 3.x.x)**. It is the same kernel you used all of Week 2, so it usually stays selected.

8. Scripts run from your work folder with `uv run`, which walks up and finds the repo-root environment automatically:

   ```bash
   cd student-work/week3/day1
   uv run python taxi_review.py
   ```

## Installing Packages Later

If a notebook cell fails with `ModuleNotFoundError` during the day, you have two options:

- From any terminal: `uv add <package>` run at the repo root, then restart the notebook kernel.
- From inside the notebook: run `!uv pip install <package>` in a cell, then restart the kernel. This installs into the same repo-root `.venv` but does not record the package in `pyproject.toml`, so prefer `uv add` when you can.

One exception today: do not install Modin or FireDucks into the shared environment. They have their own dependency stacks and may pull a different pandas version than the required labs use. The `Bonus_Lab_Engine_Probes.md` lab shows the safe pattern: a second environment with a different name.

## Expected Output

```text
env ok, pandas 3.0.x
```

Your work folder should contain:

```text
student-work/week3/day1/
  Activity_1_Python_Refresh_Drills.ipynb   (your copy)
  Activity_2_Pandas_Polars_Quick_Drills.ipynb   (your copy)
  Activity_3_DataFrame_Cleaning_Lab.ipynb   (your copy)
  Activity_4_Automation_Drills.ipynb   (your copy)
  taxi_review.py   (your copy)
  medallion_etl.py   (your copy)
  data/taxi_trip_review.csv
  data/raw/weather_raw.csv
```

Extra files are fine. The key is that your editable copies are inside `student-work/week3/day1/` and no new `.venv` was created there.

## Success Criteria

- `uv run python -c "import pandas, polars, pyarrow; print('env ok')"` prints `env ok` from the repo root.
- `pandas.__version__` starts with `3.`.
- No `.venv` exists inside `student-work/week3/day1/`. The only project environment is the repo-root `.venv`.
- The four Day 1 activity notebooks, `taxi_review.py`, `medallion_etl.py`, and `data/` exist in your work folder.
- Your notebooks use the repo-root **.venv** kernel.
- You can explain why you are not editing files directly under `Week 3/Labs/Day 1/`.

## Hints

<details>
<summary>I see `VIRTUAL_ENV does not match the project environment`</summary>

A leftover environment from another project is active in your shell. Run:

```bash
deactivate
uv run python --version
```

</details>

<details>
<summary>I accidentally ran `uv init` inside student-work/week3/day1</summary>

Stop and ask the instructor before deleting anything. The fix is usually removing the generated `pyproject.toml`, `.python-version`, and `.venv` from that folder so `uv run` resolves to the repo root again.

</details>

<details>
<summary>The kernel picker does not show the repo-root .venv</summary>

Confirm `.venv` exists at the repo root (`ls -a`) and that `ipykernel` is installed (`uv add ipykernel`). Then click **Select Kernel** again. Fallback: **Enter interpreter path** with `.venv/bin/python`.

</details>

## Stretch Goals

- Add a `README.md` in `student-work/week3/day1/` that records your Python version, pandas version, and copied files. You will extend it all day with findings.
- Help one teammate verify their kernel selection.
