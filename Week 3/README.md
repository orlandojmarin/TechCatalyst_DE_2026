# Week 3: Warehousing, BigQuery, SQL, Ingestion, and Governance

**TechCatalyst DE 2026, July 6 to July 10, The Hartford**

Theme: rebuild the Python and DataFrame foundation, then move into modern warehousing with BigQuery, hand-written SQL, event ingestion, orchestration, and governance. Deliverable: an end-to-end mini-pipeline with optimization evidence and applied security.

## Contents

| Folder | What's in it |
|---|---|
| `Slides/` | Week 3 decks, visual prompts, and speaker notes |
| `SlidesPDF/` | PDF exports for active Week 3 decks |
| `Instructor Notes/` | Per-day guides, demo scripts, cost guards, and rubrics |
| `Labs/Day 1-5/` | Activities, benchmark lab, SQL drills, ingestion lab files, and governance lab |
| `Audits/` | Day acceptance reports |

## Day Map

| Day | Topic | Hands-on |
|---|---|---|
| 1 | Python review, terminal automation overview, pandas, Polars, and medallion ETL carryover | New Python drills, stepwise DataFrame library lab, and carryover medallion local mode |
| 2 | Warehouse foundations plus BigQuery architecture, table types, pricing, partitioning, and clustering | Load taxi data, create table variants, run a 9-cell benchmark, and defend warehouse readiness |
| 3 | SQL by hand: execution order, grouping, joins, CASE, dates, and CTEs | GTFS warm-up, taxi SQL drills, business challenge, and query review board |
| 4 | Pub/Sub semantics, Beam model, and Dataflow templates | Publish events and run a GCS-to-BigQuery template |
| 5 | Orchestration and governance: Cloud Composer, access layers, Knowledge Catalog, and PII masking | Pipeline, benchmarks, queries, and masking proof |

## Cost Guards

- Set budget alerts before cloud work.
- Avoid `SELECT *` in BigQuery benchmarks.
- Use dry-run estimates before benchmark queries.
- Remember that `LIMIT` is not a cost-control strategy for broad scans.
- Stop active Dataflow jobs before leaving class.
- Use one shared orchestration demo environment, not one per student.

## Carried Over From Prior Years

`Labs/Day 3/` contains SQL drills, a SQL mini-project, and datasets from prior cohorts. Treat them as reference input and modernize syntax and platform assumptions before teaching.

## Naming Note

Use Knowledge Catalog terminology for governance content. Use GoogleSQL for BigQuery content.

## Companion Resources

- [DataTalksClub Data Engineering Zoomcamp Module 3](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse)
- [DataTalksClub Data Engineering Zoomcamp Module 2](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration)
- BigQuery public data explorer: `bigquery-public-data.new_york_taxi_trips`
