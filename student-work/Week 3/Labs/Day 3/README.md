# Week 3 Day 3: DataFrames Close-Out and the Medallion ETL Mini-Capstone

Today closes the Python and DataFrame foundation before the week turns to SQL and
warehousing. The morning fills the last Python gap (comprehensions), finishes the
core pandas moves, and gives a first, gentle look at Polars. The afternoon puts it
all together in a small, real bronze-to-silver pipeline you run on your own machine.

The goal is not speed. The goal is that every student leaves able to write a
comprehension, reshape a DataFrame with confidence, and explain how raw data
becomes a clean, typed silver table.

> **Schedule note.** This day was originally planned as "SQL by hand on BigQuery."
> SQL moved to **Day 4** (fundamentals) and **Day 5** (on BigQuery) so the class
> could finish the DataFrame foundation first. The old SQL starter files and the
> 2025 SQL reference material now live in `Week 3/Labs/Day 4/`.

## Learning Objectives

By the end of today, you will be able to:

1. Write list, dictionary, and set comprehensions, and say when a comprehension is
   clearer than a `for` loop or `map`/`filter`.
2. Select, filter, group, and summarize a DataFrame with pandas without guessing.
3. Map pandas filtering and joins to their SQL twins: `.query()` and boolean masks
   (`&`/`|`/`~`) to `WHERE`/`AND`/`OR`/`NOT`, `.between()` to `BETWEEN`, `.isin()`
   to `IN`/`NOT IN`, and `merge`/`concat`/`.join` to `JOIN`/`UNION`.
4. Translate a small pandas workflow into Polars and name one API difference.
4. Explain the medallion pattern: raw, bronze (immutable), and silver (clean, typed).
5. Build a bronze-to-silver pipeline in `--local` mode and prove pandas and Polars
   agree on the row count.
6. Explain three cleaning decisions and why each one changes the row count.

## Lab Index

### Provided Files

| File or folder | Source | Purpose |
|---|---|---|
| `README.md` | This file | Day plan, setup, deliverables, and success criteria. |
| `Student_Resources.md` | This folder | Curated documentation and quick references for today. |
| `Activity_0_Comprehensions.ipynb` | This folder | New: short, single-concept drills on list, dict, and set comprehensions. Fills the Day 1 gap. |
| `DataFrame_Fundamentals_Walkthrough.ipynb` | This folder | Instructor-led guided walkthrough of pandas fundamentals (read, select, filter, group, summarize) plus a short "your turn." Students keep it as a reference. |
| `Instructor Notes/Day 3 Demo - Pandas to SQL.ipynb` | Instructor Notes | Fully-worked demo of the Pandas→SQL bridge. Teach from it, then release as the reference for Activity 2. |
| `Activity_2_Pandas_to_SQL.ipynb` | This folder | New: the pandas patterns that map directly to SQL: `.query()` and boolean filtering (`&`/`|`/`~`), `BETWEEN`, `IN`/`NOT IN`, exclude, and joins (`merge`, `concat`, `.join`). The bridge into Day 5 SQL. |
| `Activity_3_Pandas_Data_Cleaning/` | 2025 reference, modernized | Optional extra pandas practice: CSV inspection, missing data profiling, currency string conversion, `fillna`, `dropna`, and sector-level aggregation. |
| `Activity_4_Crowdfunding_Cleanup/` | 2025 reference, modernized | Optional extra pandas practice: column selection, filtering, derived columns, staff-pick outcome summary, and business interpretation. |
| `Activity_5_Groupby_Time_Series/` | 2025 reference, modernized | Optional extra pandas practice: date parsing, time-series cleanup, `groupby`, monthly summaries, and range-based comparison. |
| `Activity_6_Search_For_The_Worst/` | 2025 reference, modernized | Optional confidence rep: category inspection, boolean filtering, sorting, reset index, and top-row selection. |
| `Activity_7_Comic_Books_CSV_Cleanup/` | 2025 reference, modernized | Optional extra pandas practice: large CSV cleanup, column pruning, renaming, string cleanup, numeric coercion, and CSV output. |
| `Activity_8_Comic_Books_Summary/` | 2025 reference, modernized | Optional extra pandas practice: `nunique`, min/max year, summary DataFrame construction, and frequency counts. |
| `Activity_9_Concat_Dataframes/` | 2025 reference, modernized | Optional extra pandas practice: reading multiple CSVs, row-wise `concat`, key preservation, `merge`, and grouped balance checks. |
| `Activity_10_Duplicate_Key_Quality/` | This folder | New: duplicate detection, business-key cleanup, lookup key checks, and join row-count validation. |
| `Activity_11_Pivot_Crosstab_Melt/` | This folder | New: worked examples plus practice for `pivot_table`, `crosstab`, and `melt`. |
| `Activity_12_Rolling_Window_Signals/` | This folder | New: worked examples plus practice for rolling averages, `shift`, percent change, and trend flags. |
| `Activity_13_Pandas3_Safe_Assignment/` | This folder | New: pandas 3 safe assignment practice with `.copy()` and `.loc`. |
| `../Day 1/Activity_2_Pandas_Polars_Quick_Drills.ipynb` | Day 1 pointer | Short pandas-and-Polars quick drills. Optional Polars intro if time allows. Copy it, do not move it. |
| `Mini_Project_Medallion_ETL/` | This folder | Afternoon mini-capstone. Start with its `README.md`, then the guided notebook. |
| `Dataset/` | 2025 reference | SQLite `.db` files kept for the SQL days. Not used today. |
| `solutions/` | This folder | Instructor references. Do not copy from it. |
| `quiz/Quiz_1_ThreeWeek_Review.md` | This folder | **New.** 10 Q (40s each): OLTP/OLAP, warehouse vs operational, ETL/ELT, lakehouse, file vs table format, built-in modules, Pathlib, collections, unpacking, functions vs lambda. Bias-audited. |
| `quiz/Quiz_2_Pandas_Concepts.md` | This folder | **New.** 8 Q on pandas: Series vs DataFrame, filtering, `.query()`, `.loc`, groupby, merge `how=`, `fillna`, `object` dtype. Bias-audited. |
| `quiz/Pre_Quiz.md`, `quiz/Day_3_Knowledge_Check.md` | This folder | Original Markdown Mash quizzes (kept; the two new ones above are preferred given the Day 3 changes). |

### Deliverables

| # | Deliverable | Format | Due |
|---|---|---|---|
| 0 | Pre quiz | Markdown Mash quiz response | Start of day |
| 1 | Day 3 setup proof | `student-work/week3/day3/` folder with copied files and pandas version | During Activity 0 |
| 2 | Comprehension drills | Completed `Activity_0_Comprehensions.ipynb` | Before DataFrame fundamentals |
| 3 | DataFrame fundamentals | Worked through `DataFrame_Fundamentals_Walkthrough.ipynb` (walkthrough + "your turn") | Before the SQL bridge |
| 4 | Pandas-to-SQL bridge | Completed `Activity_2_Pandas_to_SQL.ipynb` (all challenges) | Before the mini-capstone |
| 5 | Polars quick drills (optional) | Completed copy of `Activity_2_Pandas_Polars_Quick_Drills.ipynb` | If time allows |
| 6 | Extra pandas review drills (optional) | Completed one or more copied `Activity_3` through `Activity_13` folders | During catch-up or stretch time |
| 7 | Medallion ETL mini-capstone | `--local` run with pandas silver = 14 rows, plus 3 cleaning notes (Polars translation is optional stretch) | End of day or instructor-approved follow-up |
| 8 | Closing quiz | Markdown Mash quiz response | End of day |

## Pacing Lanes

Use the lane that fits your current confidence. Changing lanes during the day is normal.

| Lane | Best fit | Required path |
|---|---|---|
| Support lane | Comprehensions or pandas still feel shaky. | Finish Activity 0, Activity 1, and Activity 2 (the SQL bridge). Pair on the medallion notebook and stay in `--local` mode. Skip the optional Polars drills. |
| Core lane | You can write pandas but want more reps. | Finish Activities 0, 1, and 2, then complete the medallion notebook in `--local` mode with both pandas and Polars. |
| Stretch lane | You are already comfortable. | Finish the notebooks including the optional Polars drills, convert the medallion notebook into `medallion_etl.py`, then attempt the optional cloud path with ADC. |

## Schedule

| Time | Block | Output |
|---|---|---|
| 8:00-8:25 | Pre quiz and Day 2 recall | Pre quiz response and a shared list of pandas questions to close today. |
| 8:25-9:00 | Comprehensions | Instructor demo, then Activity 0 drills. |
| 9:00-10:00 | DataFrame fundamentals | Activity 1: read, select, filter, group, summarize. |
| 10:15-11:30 | Pandas-to-SQL bridge | Activity 2: `.query()`, boolean filtering (`&`/`|`/`~`), `BETWEEN`, `IN`/`NOT IN`, and joins. Name the SQL twin for each. |
| 11:30-12:00 | Medallion framing | Instructor walkthrough of raw, bronze, and silver; open the mini-capstone README. |
| 1:00-2:45 | Medallion build (local) | Work the guided notebook cell by cell to pandas silver = 14 rows. Polars (Part 6) is optional stretch. |
| 2:45-3:30 | Cleaning debrief | Explain three cleaning decisions and why each changed the row count. |
| 3:30-4:30 | Stretch or catch-up | Optional pandas review drills, optional Polars drills, script conversion, or finish the notebooks. |
| 4:30-5:00 | Closing quiz and Day 4 preview | Closing quiz response and a preview of warehousing and SQL. |

## Setup

The course uses one shared UV environment at the repo root. Today you verify it,
add what is new, and create a clean work folder. Do not run `uv init` inside
`student-work/`.

From the repo root:

```bash
mkdir -p student-work/week3/day3
uv add pandas polars pyarrow
uv run python -c "import pandas, polars, pyarrow; print('env ok, pandas', pandas.__version__)"
```

Expected: `env ok, pandas 3.0.x`. Select the repo-root `.venv` as your VS Code
interpreter and your Jupyter kernel. If you see
`VIRTUAL_ENV does not match the project environment`, run `deactivate`, then
`uv run python --version`.

## Copy Today's Activity Files

From the repo root:

```bash
cp "Week 3/Labs/Day 3/Activity_0_Comprehensions.ipynb" student-work/week3/day3/
cp "Week 3/Labs/Day 3/DataFrame_Fundamentals_Walkthrough.ipynb" student-work/week3/day3/
cp "Week 3/Labs/Day 3/Activity_2_Pandas_to_SQL.ipynb" student-work/week3/day3/
# optional Polars intro, if time allows:
cp "Week 3/Labs/Day 1/Activity_2_Pandas_Polars_Quick_Drills.ipynb" student-work/week3/day3/
```

Optional extra pandas practice folders:

```bash
cp -R "Week 3/Labs/Day 3/Activity_3_Pandas_Data_Cleaning" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_4_Crowdfunding_Cleanup" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_5_Groupby_Time_Series" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_6_Search_For_The_Worst" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_7_Comic_Books_CSV_Cleanup" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_8_Comic_Books_Summary" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_9_Concat_Dataframes" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_10_Duplicate_Key_Quality" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_11_Pivot_Crosstab_Melt" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_12_Rolling_Window_Signals" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Activity_13_Pandas3_Safe_Assignment" student-work/week3/day3/
```

Suggested order if you only have time for a few:

1. `Activity_3_Pandas_Data_Cleaning`
2. `Activity_7_Comic_Books_CSV_Cleanup`
3. `Activity_8_Comic_Books_Summary`
4. `Activity_9_Concat_Dataframes`
5. `Activity_10_Duplicate_Key_Quality`
6. `Activity_11_Pivot_Crosstab_Melt`
7. `Activity_12_Rolling_Window_Signals`
8. `Activity_13_Pandas3_Safe_Assignment`

Use `Activity_6_Search_For_The_Worst` as a quick confidence rep for filtering
and sorting. Use `Activity_4_Crowdfunding_Cleanup` and
`Activity_5_Groupby_Time_Series` when students need more practice with derived
columns, groupby, and time-stamped data. Use `Activity_10` through `Activity_13`
when the concept is new and students need a worked example before independent
practice.

For the mini-capstone, copy the notebook, the starter script, and the data from
the project folder:

```bash
cp "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/Medallion_ETL_Mini_Project.ipynb" student-work/week3/day3/
cp "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/starter/medallion_etl.py" student-work/week3/day3/
cp -R "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/data" student-work/week3/day3/
```

Work only on your copies under `student-work/week3/day3/`. Never copy from any
`solutions/` folder. Weeks 1 to 4 are still an AI-Free Zone.

## Medallion Mini-Capstone

The full how-to, checkpoints, and hints are in
`Mini_Project_Medallion_ETL/README.md`. Two rules for today:

- **Run `--local` mode.** Local mode reads and writes plain files and needs no
  cloud login, so the whole class can finish the graded work. The optional cloud
  path (public S3 read, GCS write) is a stretch step and uses
  `gcloud auth application-default login`, never a downloaded key file.
- **Notebook first, script second.** Work the guided notebook to the expected
  checkpoint, then, only if you are in the stretch lane, move your code into
  `medallion_etl.py` and run it from the terminal.

```bash
cd student-work/week3/day3
uv run python medallion_etl.py --local
```

## Expected Output

Comprehension and DataFrame notebooks should run cleanly on the repo-root kernel.

The medallion mini-capstone in `--local` mode should print:

```text
silver rows: 14
```

pandas silver is 14 rows (6 dropped: one missing date, duplicates on
`(station, date)`, and rows missing `tmax` or `tmin`). The Polars translation
(Part 6) is an optional stretch; if you attempt it, its count should also be 14.

## Success Criteria

- Your work lives under `student-work/week3/day3/`.
- The only project environment is the repo-root `.venv`, running pandas 3.
- You can write a list, dict, and set comprehension and read one aloud in plain English.
- Your DataFrame fundamentals notebook runs top to bottom.
- (Optional) You explored the pandas-and-Polars quick drills and can name one Polars API difference.
- The medallion mini-capstone runs in `--local` mode with pandas silver = 14 rows (Polars translation optional).
- Bronze data is byte-identical to raw; silver is cleaned, typed, and written as parquet.
- Your notes explain at least three cleaning decisions and why each changed the row count.
- You did not use AI assistants to write or complete code. Weeks 1 to 4 are still an AI-Free Zone.
- If you attempted optional pandas review drills, you copied the whole activity folder into `student-work/week3/day3/` and worked only on your copy.
