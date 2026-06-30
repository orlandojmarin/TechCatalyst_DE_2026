# Week 2: Developer Foundations and Python

**TechCatalyst DE 2026, June 29 to July 2, The Hartford**

Theme: data engineers write, version, review, and run code by hand. The week builds one continuous pipeline, ending in a hand-written **medallion ETL** (raw S3 source to GCS bronze to silver).

## How the days connect

The days use different datasets on purpose (variety keeps the practice fresh and matches the dataset policy), but the **skills stack into one pipeline**. The dataset changes; the pipeline stage you are learning is the throughline.

| Day | Pipeline stage | You learn to... | Carries into |
|---|---|---|---|
| 1 | Environment | handle raw files, search, and version code in the terminal + Git | every later day (run scripts, submit by PR) |
| 2 | Language | read, clean, and model records in Python by hand (collections, datetime, JSON I/O, error handling) | Day 3 parsing/retries; Day 4 "by hand, then by library" |
| 3 | Ingestion | pull JSON from a live API, paginate, handle failures, write a clean CSV | Day 4 raw landing |
| 4 | Transformation + cloud | land bronze, refine to silver with pandas/Polars, ship to GCS | Week 3 BigQuery and the capstone |

A concrete handoff to point out to students: on Day 2 they sum groups with `collections` and parse dates with `datetime` themselves; on Day 4 `pandas.groupby` and `pd.to_datetime` do the same work at scale. Same idea, less code.

## Contents

| Folder | What is in it |
| :--- | :--- |
| `Slides/` | W2D1 to W2D4 decks and visual prompts |
| `Instructor Notes/` | Per-day guides with demo scripts, timing, answer keys, pitfalls, and fallback plans |
| `Labs/Day 1-4/` | Daily labs, starter material, resources, and solution support where appropriate |
| `Audits/` | Day-level readiness and acceptance reports |

## Day Map

| Day | Topic | Hands-on work |
| :--- | :--- | :--- |
| 1, Monday | Linux CLI, pipes, grep, find, cron, Git collaboration | CLI scavenger hunt, Git relay with pull requests and merge conflicts |
| 2, Tuesday | Python foundations: types, collections, control flow, functions, tracebacks | 2025 Python drill blocks, modernized for local Linux and UV where package setup is needed |
| 3, Wednesday | Intermediate Python: exceptions, file I/O, OOP for reading, HTTP and requests | Three-level API ingestion lab using NYC Open Data |
| 4, Thursday | pandas core, Polars comparison, medallion bronze/silver, cross-cloud S3 to GCS | Week 2 deliverable: medallion ETL mini-project (S3 raw to GCS bronze to silver) |

## Carried Over From 2025

- Python drills A and B for Day 2, used as proven practice material after modernization.
- pandas instructor demos, student activities, and Yellow Taxi analysis for Day 4.
- Terminal walkthrough concepts for Day 1, rewritten for Linux terminal and VS Code.

Reference material is not treated as current truth. Commands, environment assumptions, package behavior, and platform workflows must be checked before reuse.

## Ground Rules

- AI-free zone for code generation during Weeks 1 to 4.
- Type commands by hand during live practice.
- Use Linux terminal, VS Code, Chrome, and Colab only where each tool fits the lesson.
- Do not assume a browser-hosted development environment.
- Submit work through pull requests with peer review.
- Use UV for local Python setup when a lab requires a Python project.

## Companion Resources

- DataTalksClub Zoomcamp dlt ingestion workshop, after-hours reading: <https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/workshops/dlt.md>
- Python Tutor, visualize execution: <https://pythontutor.com>
- explainshell, inspect shell commands: <https://explainshell.com>
