# Week 4 - SQL Foundations to Cloud Warehouse

**TechCatalyst DE 2026 · July 13-17 · The Hartford**

Theme: the SQL week. Monday opens with a fun Markdown Mash recap of Weeks 1 to 3, then SQL starts small and local (SQLite in DBeaver), grows relational (joins), learns to organize logic (subqueries and CTEs) at cloud scale (BigQuery Sandbox, plus DuckDB as a local query engine), and lands on Snowflake, the focus platform for the rest of the course. Everything is written by hand: the AI-Free Zone still applies this week.

## Day map

| Day | Topic | Hands-on |
| :--- | :--- | :--- |
| 1 | Kickoff Mash (Weeks 1-3 recap) + SQL foundations on SQLite | `Labs/Day 1/`: pandas-to-SQL warmup drill, DBeaver setup, SELECT/WHERE/ORDER BY (LeBron stats), aggregates and GROUP BY/HAVING (call center), the crime investigation opener. Optional evening homework: BigQuery transfer drills |
| 2 | Keys, relationships, and joins | `Labs/Day 2/`: close the murder mystery with SQLite joins; inner vs left joins and row-count validation on BigQuery bikeshare data; team case-close briefings |
| 3 | Subqueries, CTEs, and OLTP vs OLAP | `Labs/Day 3/`: GTFS warmup, NYC Taxi drills and business challenge on the public BigQuery dataset, subquery-to-CTE rewrites, DuckDB as a file query engine (Parquet from local, GitHub URLs, S3); SQL Question Review Board |
| 4 | Snowflake foundations, CTAS, and views | `Labs/Day 4/`: Snowsight and DBeaver orientation, TPCH sample-data drills, CTAS vs views, table and view types, the NorthWind Traders case presented to the CSO |
| 5 | Loading Snowflake from S3 + the week end to end | `Labs/Day 5/`: external stage on S3, file formats, COPY INTO for CSV/JSON/Parquet, cumulative load-transform-persist-validate pipeline; XYZ Retail team case kickoff (presentations Monday) |

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
- DuckDB appears on Day 3 as a local OLAP engine to make the OLTP vs OLAP conversation concrete before Snowflake.
- Window functions, QUALIFY, and query tuning are deliberately absent this week; they open Week 5 on Snowflake.
