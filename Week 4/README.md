# Week 4 - SQL Foundations to Cloud Warehouse

**TechCatalyst DE 2026 · July 13-17 · The Hartford**

Theme: the SQL week. Monday opens with a fun Markdown Mash recap of Weeks 1 to 3, then SQL starts small and local (SQLite in DBeaver), grows relational (joins), learns to organize logic (subqueries and CTEs) at cloud scale (BigQuery Sandbox, plus DuckDB as a local query engine), and lands on Snowflake, the focus platform for the rest of the course. Everything is written by hand: the AI-Free Zone still applies this week.

## Python environment rule

Week 4 uses the existing repository-root Python project:

- `.venv` is always at the repository root.
- `pyproject.toml` and `uv.lock` stay at the repository root.
- Run `uv sync`, `uv add`, `uv run`, or `uv pip install` from the repository root.
- Use `uv add <package>` when the package should be recorded in your root `pyproject.toml`.
- Use `uv pip install --python .venv/bin/python <package>` only when an activity explicitly calls for a temporary install that should not change `pyproject.toml`.
- Do not run `uv init` or create another default `.venv`, `pyproject.toml`, `uv.lock`, or `.gitignore` inside `student-work/`.
- Student-authored notebooks, SQL, databases, screenshots, and other work still belong under `student-work/week4/dayX/`.
- Activity-specific `.env` or `.cfg` files belong beside the activity files under `student-work/` and are ignored by the one repository-root `.gitignore`.

If a future activity has a real dependency-version conflict, its instructions will explicitly offer a named root environment or a local activity environment and explain why the exception is needed.

## Day map

| Day | Topic | Hands-on |
| :--- | :--- | :--- |
| 1 | Kickoff Mash (Weeks 1-3 recap) + SQL foundations on SQLite | `Labs/Day 1/`: pandas-to-SQL warmup drill, DBeaver setup, SELECT/WHERE/ORDER BY (LeBron stats), aggregates and GROUP BY/HAVING (call center), the crime investigation opener. Optional evening homework: BigQuery transfer drills |
| 2 | Keys, relationships, and joins | `Labs/Day 2/`: close the murder mystery with SQLite joins; inner vs left joins and row-count validation on BigQuery bikeshare data; team case-close briefings |
| 3 | Subqueries, CTEs, and persisting results | `Labs/Day 3/`: GTFS temporary-table warm-up, Chicago Taxi CTE drills and business challenge in BigQuery, SQLite DDL fast-finisher, read-only Snowflake TPC-H transfer lab, and SQL Question Review Board |
| 4 | Snowflake objects, secure loading, and pandas ETL | `Labs/Day 4/`: Snowflake context, table lifecycles, CTAS, views, clones, one controlled Parquet stage and load, TPC-H drills, and a full pandas ETL pipeline that publishes four analytical tables |
| 5 | Snowflake loading patterns and the week end to end | `Labs/Day 5/`: extend external stages and `COPY INTO` across CSV, JSON, and Parquet; build a cumulative load-transform-persist-validate pipeline; begin the XYZ Retail team case for Monday presentations |

## Contents

| Folder | What's in it |
| :--- | :--- |
| `Labs/Day 1-5/` | Daily README, reading, activities, starters, solutions, and `quiz/` (pre and post Markdown Mash) |
| `SlidesPDF/` | PDF exports of the day decks as they are finalized |

## Weekly deliverables

- Day 3: taxi business challenge queries with bytes-scanned evidence.
- Day 5: the end-to-end SQL pipeline (stage, COPY INTO, CTE transform, CTAS, view, validation).
- Weekend: the pandas-vs-SQL homework (same transformations, two tools); XYZ Retail team proposal, presented Monday of Week 5.

## Notes

- BigQuery is used only as a free SQL engine (Sandbox plus public datasets). GCP as a platform is out of scope for 2026; AWS remains the taught cloud.
- SQLite provides the safe Day 3 DDL surface because BigQuery Sandbox does not support DML.
- Window functions, QUALIFY, and query tuning are deliberately absent this week; they open Week 5 on Snowflake.
