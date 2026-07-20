# Week 5 Day 1: Stages, Window Functions, and Snowpark

**Format:** Notebook drills, individual SQL work in Snowsight, an instructor code-along, and partner validation
**Platform:** Snowflake Snowsight, plus the repository-root `.venv` for the notebook work
**Datasets:** NYC Taxi Parquet, NYC taxi zone CSV, a course JSON manifest, small hand-checkable stock and claims tables, and TPC-H sample data

## Purpose

Week 4 gave you Snowflake objects, SQL, CTEs, and a pandas load. Today you finish the loading story, add the analytical tool you will use constantly (window functions), and meet Snowpark, the DataFrame API that runs inside Snowflake. The day opens with retention drills that prove SQL and pandas are the same thinking, and it closes by announcing the Week 5 mini-capstone. Everything today sets up the move to Databricks and PySpark tomorrow.

This is an AI-allowed week (review required). You may use an assistant to explain or draft, but you must read, run, and be able to defend every line you submit.

## Learning Objectives

By the end of the day, you can:

1. Translate between SQL and pandas for filtering, grouping, `HAVING`, `LAG`, moving averages, ranking, and `CASE`.
2. Create file formats and a stage, and load CSV, JSON, and Parquet with explicit contracts.
3. Inspect staged files before loading them, and keep raw JSON in a `VARIANT` column.
4. Rank, compare, and accumulate with window functions, within partitions, including `QUALIFY` for clean top-N filters.
5. Explain what Snowpark is, run DataFrame code that executes inside Snowflake, and say where the laptop-versus-warehouse boundary sits.
6. Describe the Week 5 mini-capstone and what your team will present on Day 5.

## Today's Arc

| Sequence | Activity | Learner outcome |
|---|---|---|
| 1 | Group activity: From PoC to Production | Open the day as architects: scale last week's pandas ETL PoC on paper, in teams. (`Week 4/Labs/Day 4/Group_Activity_From_PoC_to_Production.md`) |
| 2 | Monday Markdown Mash | Warm up with a Week 4 recap quiz. |
| 3 | Activity 0 | Confirm your Snowflake context and Week 5 work folder. |
| 4 | Activity 1 | Kickoff drills: run each query in Snowflake, then make pandas match it exactly; today's window functions make their first cameo. |
| 5 | Lesson 1 | Follow the stages walkthrough on the weather data: peek, load three ways, and see the rerun surprise. |
| 6 | Activity 2 | Load Parquet and CSV taxi files from a stage, check for duplicates, and cross-validate row counts. |
| 7 | Activity 3 | Refine what you loaded: RAW to CLEAN to FINAL with date features, consolidated pricing, and reconciliation checks. |
| 8 | Activity 4 | Rank, compare, and accumulate with window functions on a stock table, then a TPC-H stretch. |
| 9 | Activity 5 | Write the demo's window moves yourself, in SQL, on the shared stock and milk tables. |
| 10 | Activity 6 | Activity 5's twin: the exact same questions, same tables, now in pandas; answers must agree. |
| 11 | Snowpark code-along | Follow the instructor through Snowpark basics: sessions, lazy evaluation, pushdown. |
| 12 | Activity 7 | Fly solo in Snowpark: build a tiny claims table, hit known checkpoints, write a table back. |
| 14 | Mini-capstone announcement | Meet the Million Song Lakehouse project you will present on Day 5. |
| 15 | Knowledge check | Closing quiz on stages, formats, and window functions. |

Your instructor will tell you which blocks are core today and which are optional or carry into tomorrow; the `Polars Lab.ipynb` stays available as extra retention practice.

## Lab Index

### Provided Files

| Order | File | Purpose |
|---|---|---|
| Reading | `Reading_Stages_Windows_and_Snowpark.md` | Explainer: stages and file formats, window functions, and Snowpark. |
| Lesson | `Lesson_1_Stages_and_Loading.md` | The guided stages walkthrough on the weather dataset: peek from a stage, DDL plus `COPY INTO`, the rerun surprise, CTAS, and `INFER_SCHEMA`. |
| Resources | `Student_Resources.md` | Current documentation, patterns, and the deliverable checklist. |
| Dataset A | NYC Taxi Parquet and CSV files in `stages/` | `yellow_tripdata_2026-01.parquet`, `yellow_tripdata_2026-02.parquet`, `yellow_tripdata_2026-01.csv`, `yellow_tripdata_2026-02.csv`. |
| Dataset W | Course S3 files: `raw/weather/weather_raw.csv`, `.parquet`, `.json` | Twenty messy weather rows in three formats, the Lesson 1 walkthrough data. |
| Dataset C | TPC-H `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1` | Read-only sample data for the window-function stretch and the Snowpark code-along. |
| 0 | `Activity_0_Snowflake_Context_Check.md` | Confirm role, warehouse, database, schema, and Week 5 work folder. |
| 1 | `Activity_1_Week5_Kickoff_Drills.ipynb` | Snowflake-first drills on a small claims table: run the SQL, match it in pandas, meet `shift`, `rolling`, and `rank` through taught mini-examples. |
| 2 | `Activity_2_Stage_Infer_Schema_and_Copy_Into.md` | Stage, load Parquet and CSV taxi files, duplicate detection, cross-format validation. SQL inline. |
| 3 | `Activity_3_Raw_to_Clean.md` | RAW to CLEAN to FINAL: types, date features, consolidated pricing, reconciliation. SQL inline. |
| 4 | `Activity_4_Window_Functions.md` | Ranking, `LAG`/`LEAD`, running totals, and moving averages. SQL inline. |
| 5 | `Activity_5_Time_Series_Window_Drills.md` | `PARTITION BY`, `QUALIFY`, `UNPIVOT`, and seasonality on the shared `STOCKS` tables. SQL inline. |
| 6 | `Activity_6_Windows_in_Pandas.ipynb` | Activity 5's twin in pandas: guided walkthrough, then solo, answers must match the SQL grids. |
| Code-along | `Code_Along_Snowpark_Basics.ipynb` | Instructor-led: sessions, lazy evaluation, pushdown, writing back. Keep as your Snowpark reference. |
| 7 | `Activity_7_Snowpark_First_Flight.ipynb` | Solo Snowpark on a tiny claims table you create: known checkpoints, then write a table back. |
| Mini-capstone | `Mini_Capstone_Announcement.md` | The Million Song Lakehouse project brief preview. |
| Drills | `Polars Lab.ipynb` | Polars review lab (kept for retention). |
| Quiz | `quiz/W5D1_Monday_Markdown_Mash.md` | Warm-up review quiz. |
| Quiz | `quiz/W5D1_Stages_and_Windows_Check.md` | Closing knowledge check on stages, formats, and window functions. |

Solutions for Activities 1 through 7 are in `solutions/`, in the matching format (notebooks for notebooks, markdown with inline SQL for SQL activities).

### Deliverables

| Deliverable | Evidence |
|---|---|
| Kickoff drills | All seven drills produce identical results in Snowsight and pandas; checkpoints match in your copied notebook. |
| Single-file and multi-file load | Stage listing, `COPY INTO` results, before/after row counts proving no duplicates, Parquet vs. CSV row-count match. |
| Raw to clean | `clean_yellow_taxi` with zero rule violations and `daily_taxi_summary` reconciling exactly with CLEAN. |
| Window functions | Activity 4 checkpoints matched; Activity 5 checkpoints matched (1512 rows, 3 NULLs, top 3 per symbol via `QUALIFY`, January 1963 = 589). |
| Pandas translation | Activity 6: melt reshape done, exactly 3 partition NaNs explained, top 3 per symbol, 12-month YoY, wrap-up questions answered. |
| Snowpark | Activity 7 checkpoints matched, `W5D1_CLAIMS_ENRICHED` written and verified in Snowsight, wrap-up questions answered. |

## Carryover Labs

- `Week 4/Labs/Day 4/Activity_5_SQL_CTE_and_Pandas_Mastery_Circuit.md` and `Activity_6_Retail_SQL_and_Pandas_Parallel_Circuit.md` were published as optional and remain so. They are excellent extra reps of exactly what Activity 1 warms up. Complete them any evening this week if you want more.
- `Week 4/Labs/Day 5/Group_Activity_Insurance_Analytics_Architecture_Brief.md` was not run in Week 4. It stays on the plan: your instructor will schedule it this week alongside the mini-capstone design work.

## Classroom Contract

The instructor provisions the role, warehouse, database, schema, and storage integration. Create objects only in your assigned schema (`TECHCATALYST.<your_name>`). Do not paste AWS keys into SQL. Use `USE ROLE DE; USE WAREHOUSE COMPUTE_WH; USE DATABASE TECHCATALYST; USE SCHEMA TECHCATALYST.<your_name>;` to set context. Keep your password in `snow.cfg` only, never in a notebook or worksheet.

## Success Criteria

- All authored work is under `student-work/week5/day1/`.
- Your loads name exact files, never a whole bucket prefix, and use the storage integration.
- Your window-function answers match the provided checkpoints, and Activities 6 and 7 agree with each other.
- You can explain, in plain language, when to use a stage load, a window function, `QUALIFY`, and Snowpark, and you can say in one sentence what moves where: Snowpark moves the code to the data; pandas moves the data to the code.
