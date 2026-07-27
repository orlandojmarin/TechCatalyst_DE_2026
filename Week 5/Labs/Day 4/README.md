# Week 5 Day 4: dbt Core with Snowflake

**Format:** Self-paced, end-to-end individual project in VS Code  
**Platform:** dbt Core with the Snowflake adapter  
**Dataset:** Shared Airbnb raw tables in `AIRBNB.RAW`  
**Output:** Student-owned objects in `TECHCATALYST.<STUDENTNAME>`

## Purpose

You already know how to write a SQL transformation. Today the focus is how a team manages many transformations as one reliable system.

Across five connected activities, you will build a small analytics project and learn why each dbt feature exists. The journey moves from a single model to a dependency graph, then to a small star schema, data quality gates, historical tracking, and generated documentation.

This is an AI-allowed week, with review required. You may use an assistant to explain or draft, but you must read, run, and be able to defend every line you submit.

## The project you will build

```text
AIRBNB.RAW
  RAW_LISTINGS ----> SRC_LISTINGS ----> DIM_LISTINGS_CLEANSED ---+
                                                                 +--> DIM_LISTINGS_W_HOSTS
  RAW_HOSTS -------> SRC_HOSTS -------> DIM_HOSTS_CLEANSED ------+

  RAW_REVIEWS -----> SRC_REVIEWS -----> FCT_REVIEWS -------------+
                                                                 +--> MART_FULLMOON_REVIEWS
  full moon CSV ----------------------> SEED_FULL_MOON_DATES -----+
```

The core analytical shape is a small star:

- `FCT_REVIEWS` stores review events, one row per review.
- `DIM_LISTINGS_W_HOSTS` stores descriptive context, one row per listing.
- Analysts join them by `listing_id`.

## Learning Objectives

By the end of the sequence, you can:

1. Install dbt Core and connect it to Snowflake without putting credentials in the repository.
2. Explain the difference between raw inputs, staging models, dimensions, facts, and marts.
3. Use `ref()` and `source()` to create dependencies and lineage.
4. Explain when a CTE improves a model and when it is unnecessary.
5. Read Jinja as template logic that dbt compiles into Snowflake SQL.
6. Choose view, table, and incremental materializations deliberately.
7. Load a seed and distinguish it from a source.
8. Write generic and singular data tests.
9. Explain a small star schema and the grain of its fact and dimension.
10. Use snapshots, generated docs, and a package macro.

## Today's Arc

| Sequence | Activity | The question you should be able to answer |
|---|---|---|
| 0 | dbt Core setup | How do the project, profile, adapter, and Snowflake connection fit together? |
| 1 | First models | How does a SQL `SELECT` become a managed view? |
| 2 | Core models | How do `ref()`, Jinja, materializations, facts, and dimensions create a DAG and a star? |
| 3 | Sources, seeds, and tests | How does a project declare origins, reference data, and quality contracts? |
| 4 | Snapshots, docs, and packages | How does dbt preserve history, explain itself, and reuse trusted logic? |
| 5 | Mini-capstone block | How will your team apply the same ideas to its bronze and silver work? |

Complete Activities 0 through 3 in order. Activity 4 is stretch work after `dbt build` passes.

## Lab Index

### Provided Files

| Order | File | Purpose |
|---|---|---|
| 0 | `Activity_0_dbt_Core_Setup.md` | Install dbt Core, create the project and profile, configure aliases and materializations. |
| 1 | `Activity_1_First_Models.md` | Build staging views, inspect output, and read compiled SQL. |
| 2 | `Activity_2_Materializations_and_Core_Models.md` | Build dimensions and an incremental fact, inspect the DAG, and explain the star schema. |
| 3 | `Activity_3_Sources_Seeds_and_Tests.md` | Declare sources, load a seed, build a mart, and create data quality gates. |
| 4 | `Activity_4_Snapshots_Docs_and_Packages.md` | Preserve controlled history, generate docs, and use `dbt_utils`. |
| Data | `AIRBNB.RAW` in Snowflake | Shared raw listings, reviews, and hosts. |
| Seed | [seed_full_moon_dates.csv](https://dbt-datasets.s3.us-east-2.amazonaws.com/seed_full_moon_dates.csv) | Small reference dataset used by the mart. |
| Capstone | `../Mini_Capstone/README.md` | Team project work after the dbt sequence. |

Solutions for Activities 1 through 4 are in `solutions/`. Use them after attempting the solo tasks.

### Deliverables

| Deliverable | Evidence |
|---|---|
| Working project | `dbt debug` passes from `student-work/week5/day4/airbnb`. |
| Staging layer | Three views read `AIRBNB.RAW` through declared sources. |
| Core layer | Three dimensions and one incremental fact build in `TECHCATALYST.<STUDENTNAME>`. |
| Mart | The full moon review mart joins the fact to a seed. |
| Quality | Eight generic tests and one singular test pass. |
| End-to-end build | `dbt build` completes successfully. |
| Explanation | You can narrate the grain, dependencies, materializations, and purpose of each layer. |

## Classroom Contract

- Work only in `student-work/week5/day4/airbnb`.
- Use the repository's root `.venv`. Do not create another UV project or `.venv` in the day folder.
- Keep credentials only in `~/.dbt/profiles.yml`.
- Read shared input from `AIRBNB.RAW`.
- Activity 2 permits one additive, username-tagged review insert for the incremental demonstration. Do not update or delete shared raw rows.
- Create and replace only objects in `TECHCATALYST.<STUDENTNAME>` that carry your username prefix.
- Deny any Duo push that you did not trigger.

## How to study, not just follow

At every checkpoint, stop and answer three questions:

1. What changed in the warehouse?
2. Which dbt file or command caused that change?
3. Why is this safer or clearer than a disconnected SQL worksheet?

If you cannot answer one, return to the explanation above the command before moving on.

## Success Criteria

- `dbt build` is green.
- Eight dbt models exist after Activity 3: three staging models, three dimensions, one fact, and one mart.
- Every model-to-model dependency uses `ref()`, and every raw-table dependency uses `source()`.
- You can explain model, materialization, grain, dimension, fact, mart, source, seed, test, snapshot, and package in plain language.
- You can answer the framing question: what does dbt give a data team that a folder of SQL worksheets does not?

## Currentness Check

Commands and syntax were checked on July 27, 2026 against the official dbt documentation for dbt Core data tests, YAML snapshots, packages, and documentation commands. This lab intentionally uses dbt Core only.
