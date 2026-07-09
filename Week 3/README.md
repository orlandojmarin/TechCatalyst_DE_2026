# Week 3: Warehousing, BigQuery, SQL, Ingestion, and Governance

**TechCatalyst DE 2026, July 6 to July 10, The Hartford**

Theme: finish the Python and DataFrame foundation, then move into modern warehousing with BigQuery and hand-written SQL. Deliverable: an end-to-end mini-pipeline (medallion silver + BigQuery warehouse + SQL evidence) with optimization evidence.

> **Realignment (updated July 8).** The class needed two full days of Python and pandas review, so the week was rescheduled. Days 1–2 became Python/pandas; Day 3 closes DataFrames and runs the medallion mini-capstone; Day 4 is a Python/terminal/pandas recap plus a SQL kickoff on BigQuery public data; Day 5 is SQL depth, the business challenge, and the deliverable. SQL **stays in Week 3** because Week 4 Day 2 (advanced SQL) and Day 3 (dbt) assume it. Event ingestion (Pub/Sub, Beam, Dataflow) is **parked** in `_Parked_and_Optional/` for the capstone; orchestration/governance is **demoted to reading + demo** and returns as a full lab in Week 4 Day 5 and Week 8. Unused Python/engine bonus labs are offered as **after-hours self-study** (see `_Parked_and_Optional/INDEX.md`). The Day map below reflects **actual delivery**, not the original plan.

## Contents

| Folder | What's in it |
|---|---|
| `Slides/` | Week 3 decks, visual prompts, and speaker notes |
| `SlidesPDF/` | PDF exports for active Week 3 decks |
| `Instructor Notes/` | Per-day guides, demo scripts, cost guards, and rubrics |
| `Labs/Day 1-5/` | Activities, benchmark lab, SQL drills, ingestion lab files, and governance lab |
| `Audits/` | Day acceptance reports |

## Day Map

| Day | Topic (as delivered) | Hands-on |
|---|---|---|
| 1 | Python review + intro to pandas | Python drills (data structures, methods, lambda, map/filter, unpacking, built-in modules); start pandas |
| 2 | DataFrames intro + pandas overview + labs/drills | Pandas overview, pandas drills, Yellow Taxi Analysis |
| 3 | DataFrames close-out + medallion ETL | Comprehensions, DataFrame fundamentals, Pandas→SQL bridge, then the medallion mini-capstone in local mode |
| 4 | Recap (Python/terminal/pandas) + SQL fundamentals kickoff | Morning recap and medallion catch-up; afternoon GTFS warm-up + first taxi SQL drills (SELECT/WHERE/GROUP BY) on public data |
| 5 | More SQL fundamentals + business challenge + deliverable | Joins, grouped aggregates, HAVING; a plain business challenge with bytes; partition cost demo; Week 3 deliverable (governance demoted to reading + demo) |

> **SQL scope:** Week 3 teaches SQL **fundamentals only** (SELECT/WHERE/GROUP BY/HAVING/ORDER BY/basic JOINs). **CTEs, window functions, and tuning are Week 4 Day 2.** SQL is a new skill for many students, so the pace is deliberately slow.

## Cost Guards

- Set budget alerts before cloud work.
- Avoid `SELECT *` in BigQuery benchmarks.
- Use dry-run estimates before benchmark queries.
- Remember that `LIMIT` is not a cost-control strategy for broad scans.
- Stop active Dataflow jobs before leaving class.
- Use one shared orchestration demo environment, not one per student.

## Carried Over From Prior Years

`Labs/Day 4/` contains the SQL drills, SQL mini-project, and SQLite datasets from prior cohorts (used on Day 5). Treat them as reference input and modernize syntax and platform assumptions before teaching.

## Naming Note

Use Knowledge Catalog terminology for governance content. Use GoogleSQL for BigQuery content.

## Companion Resources

- [DataTalksClub Data Engineering Zoomcamp Module 3](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse)
- [DataTalksClub Data Engineering Zoomcamp Module 2](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration)
- BigQuery public data explorer: `bigquery-public-data.new_york_taxi_trips`
