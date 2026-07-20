# Week 4 Day 4: Snowflake Objects, Stages, and Reliable Loads

**Format:** Individual SQL work, partner validation, and a team design defense  
**Platforms:** Snowflake Snowsight Workspaces, instructor-provisioned warehouse and schema  
**Datasets:** Small synthetic customer and order tables for SQL and pandas mastery; NYC Taxi Parquet for the Snowflake stage load; traffic-accident CSV for pandas ETL practice

## Purpose

You already know that SQL transfers across SQLite, BigQuery, and Snowflake. Today begins by completing the unfinished Day 3 sequence, then rebuilding SQL and CTE confidence with a tiny predictable dataset in your assigned Snowflake schema. You will solve the same transformations in pandas so the connection between SQL intermediate results and DataFrames becomes visible. The remaining activities show what makes a warehouse operational: context, object lifetimes, stages, repeatable loads, and validated publishing.

This is an AI-Free Zone day. Write and explain your own SQL. Use the provided documentation, the lab starter, and partner discussion, not an AI assistant.

## Learning Objectives

By the end of the day, you can:

1. Set and verify Snowflake role, warehouse, database, and schema context.
2. Choose between temporary, transient, and permanent tables for a stated need.
3. Use CTAS, a view, and a zero-copy clone for different purposes.
4. Create an external S3 stage that uses an instructor-provided storage integration, without embedding cloud credentials.
5. Inspect a Parquet schema, load a table with `COPY INTO`, and validate the result.
6. Explain why a stage and a file format are separate objects.
7. Build a pandas ETL pipeline that publishes validated analytical tables to Snowflake.
8. Plan a multi-step business question as named intermediate results, then reproduce those results in pandas.

## Carryover Labs

Day 3 included continued Day 2 work, a pandas refresher, and the first CTE lesson. The three Day 3 activities below remain in their original folders. Complete unfinished work before moving into the Day 4 mastery circuit.

| Original activity | Why it carried over | Completion point today |
|---|---|---|
| [Day 3 Activity 1: GTFS SQL Warm-up](../Day%203/Activity_1_GTFS_SQL_Warmup.md) | Prior-day work reduced the available practice block. | Complete the required warm-ups and explain the grain of the CTE result. |
| [Day 3 Activity 2: BigQuery Public Taxi CTE Drills](../Day%203/Activity_2_BigQuery_Public_Taxi_CTEs.md) | Students need more time to build and inspect the required CTEs. | Complete the assigned core drills and validate each intermediate grain. |
| [Day 3 Activity 3: BigQuery Taxi Business Challenge](../Day%203/Activity_3_BigQuery_Taxi_Business_Challenge.md) | The CTE foundation needs reinforcement before the team explanation. | Complete the team query, evidence check, and presentation deliverable. |

## Today's Arc

| Sequence | Activity | Learner outcome |
|---|---|---|
| 1 | Activity 0 and context check | Set up a safe workspace and set role, warehouse, database, and schema. |
| 2 | Lesson 1, DDL journey | Build two tables from scratch: data types, INSERT, table types, views, CTAS, UPDATE, DELETE, DROP. |
| 3 | Lesson 2, SQL practice | Query the warehouse you built with SELECT, JOIN, GROUP BY, and CTEs. |
| 4 | Lesson 3, table and view types | Choose permanent, transient, or temporary tables and standard, materialized, or secure views on purpose. |
| 5 | Activity 4 | Full pandas ETL to Snowflake: the recreated 2025 activity, built as chainable pipeline steps. |
| 6 | Activity 5, SQL and pandas | CTE ladder in SQL, then the pandas mirror, proving parity. |
| 7 | Activity 6, retail parallels | Repeat the CTE ladder on a new domain, then map each SQL window to its pandas twin. |
| 8 | CTE Grain Game | Run the Markdown Mash grain game to lock in "what does one row represent?" |
| 9 | Activity 2 | Create a stage and file format, infer a Parquet schema, load it, and validate the load. |
| 10 | Activity 1 or Activity 3 | Optional deep dives: table type and clone lab, or the TPC-H SQL transfer drills. |
| 11 | Group activity and knowledge check | Defend a warehouse-object design, then explain object choice, loading, and grain decisions. |
| Carryover | Day 3 Activities 1 through 3 | Finish any unfinished Day 3 SQL sequence in its original folder, if it carried over. |

## Lab Index

### Provided Files

| Order | File | Purpose |
|---|---|---|
| Reading | `Reading_Snowflake_Objects_and_Loading.md` | Explainer: context, object lifetimes, stages, and trustworthy loads. |
| Resources | `Student_Resources.md` | Current documentation, patterns, troubleshooting, and checklist. |
| Dataset A | [NYC Taxi January 2026 Parquet](https://techcatalyst-de-2026.s3.amazonaws.com/nyc-taxi/yellow-tripdata/yellow_tripdata_2026-01.parquet) | Single approved source file for the Snowflake stage load. |
| Dataset B | [Traffic accident CSV](https://techcatalyst-de-2026.s3.amazonaws.com/raw/accidents/accidents_2017_to_2023_english.csv) | Public S3 source for the pandas ETL activity. |
| 0 | `Activity_0_Snowflake_Workspace_Setup.md` | Create the Day 4 workspace and `snow.cfg`, and verify Snowflake context. |
| Lesson 1 | `Lesson_1_DDL_Data_Types_and_Snowflake_Objects.md` | Guided DDL journey: data types, CREATE and INSERT, table types, views, CTAS, UPDATE, DELETE, DROP. SQL inline. |
| Lesson 2 | `Lesson_2_SQL_Practice_CTEs_Joins_GroupBy.md` | Ten practice problems on the Lesson 1 tables (SELECT, JOIN, GROUP BY, CTEs). SQL inline, with expected results. |
| Lesson 3 | `Lesson_3_Snowflake_Table_and_View_Types.md` | Table and view types, Time Travel, and how to choose. SQL inline. |
| 1 | `Activity_1_Table_Types_CTAS_Views_and_Clones.md` | Optional deep dive: table types, CTAS, views, and zero-copy clones. SQL scaffold inline. |
| 2 | `Activity_2_Stage_Infer_Schema_and_Copy_Into.md` | Load the January 2026 Taxi Parquet file from an S3 stage. SQL scaffold inline. |
| 3 | `Activity_3_Snowflake_SQL_Transfer_Drills.md` | Four core and eight extension SQL drills on shared TPC-H data. SQL scaffold inline. |
| 4 | `Activity_4_Pandas_ETL_to_Snowflake.md` and `Activity_4_Pandas_ETL_to_Snowflake.ipynb` | Full pandas ETL pipeline and four Snowflake analytical tables. Notebook. |
| 5 | `Activity_5_SQL_CTE_and_Pandas_Mastery_Circuit.md` and `Activity_5_Pandas_Mirror.ipynb` | Nine SQL CTE drills (inline) and eight pandas mirror drills (notebook). |
| 6 | `Activity_6_Retail_SQL_and_Pandas_Parallel_Circuit.md` and `Activity_6_Pandas_Parallel.ipynb` | Second CTE ladder (inline) plus a SQL-and-pandas window parallel circuit (notebook). |
| Group | `Group_Activity_Taxi_Ingestion_Design_Defense.md` | Defend a warehouse-object design to a stakeholder. |
| Template | `day4_load_review_template.md` | Copy into your work folder as `day4_load_review.md` and record your evidence. |
| Quiz | `quiz/W4D4_Snowflake_Objects_and_Loads_Knowledge_Check.md` | Closing Markdown Mash knowledge check. |
| Game | `quiz/W4D4_CTE_Grain_Markdown_Mash.md` | Fast "what does one row represent?" grain game in Markdown Mash format. |

### Deliverables

| Deliverable | Evidence |
|---|---|
| DDL warehouse | Two tables built in your schema, a live view, a CTAS snapshot, and evidence you can explain view versus CTAS. |
| SQL practice | Ten worked query answers, including the LEFT JOIN that finds Finn and the Problem 10 CTE that returns Cara and Ben. |
| Context check | Your current role, warehouse, database, and schema recorded in `day4_load_review.md`. |
| Object lifecycle | Result grids proving the snapshot, view, and clone behave differently. |
| Load review | Stage listing, `COPY INTO` outcome, row count, date range, and one data-quality check. |
| Design defense | One-page object decision table and a three-minute team presentation. |
| Optional drills | Four core SQL queries, then selected extension queries and plain-language comments if time permits. |
| Pandas ETL pipeline | Completed notebook, data-quality evidence, four analysis DataFrames, four Snowflake tables, and row-count reconciliation. |
| SQL and pandas mastery | Nine SQL answers, eight pandas mirror results, grain comments, and a passing SQL-to-pandas parity check. |
| Retail parallel circuit | Activity 6 CTE ladder answers, seven window drills, pandas twins, and a passing above-benchmark parity check returning D then B. |

## What You Write

The instructions are the starter. SQL activities give you the context and labeled tasks inline, so you copy the scaffold into a Snowsight worksheet and complete it. Pandas activities are notebooks with the setup provided and TODOs to complete. Nothing provides finished answers.

| Activity | Provided for you | You write |
|---|---|---|
| Activity 1 (inline SQL) | Session context and nine labeled tasks | Table DDL, inserts, CTAS, view, clone, update, and recovery checks |
| Activity 2 (inline SQL) | Session context, exact source, and seven labeled tasks | File format, stage, schema inference, table, `COPY INTO`, and validation SQL |
| Activity 3 (inline SQL) | Read-only context and twelve prompts | Four core queries with grain comments, then selected extensions |
| Activity 4 (notebook) | Imports, source read, rename requirements, progressive examples, IQR implementation, config loader, and prompts | Rename mapping, guided cleaning, quality interpretation, features, four analyses, three target DDL statements, writes, and reconciliation |
| Activity 5 (inline SQL and notebook) | Tiny dataset setup, nine CTE prompts with planning frames and a wrong-grain query; a pandas notebook with connector setup and assertions | SQL queries and grain explanations; DataFrame filters, merges, groups, comparisons, and parity lists |
| Activity 6 (inline SQL and notebook) | Retail dataset setup, a CTE ladder, a wrong-grain repair, seven window prompts; a pandas notebook with setup and assertions | Store-to-region CTEs and window functions; pandas twins using groupby, rolling, shift, rank, and apply |

## Classroom contract

The instructor provisions the role, warehouse, database, schema, and storage integration before class. Students create tables, views, stages, and file formats only within their assigned schema. Do not create warehouses, integrations, roles, or databases unless the instructor explicitly grants that task. This is intentional least-privilege design, not a missing step.

The single source file for Activity 2 is:

```text
s3://techcatalyst-de-2026/nyc-taxi/yellow-tripdata/yellow_tripdata_2026-01.parquet
```

The stage points to the containing prefix. The load command names the one required file, so students do not accidentally load a different month.

## Success Criteria

- Your work is under `student-work/week4/day4/`, not inside this lab folder.
- You can identify which Snowflake context setting controls permissions, compute, and object location.
- You create a stage through a storage integration, never by pasting AWS keys into SQL or a notebook.
- Your `COPY INTO` load has a documented result and at least two validation checks.
- You can recommend a table type and defend the trade-off.
- You can explain how pandas transformations, the Snowflake connector, a temporary stage, and `COPY INTO` form one pipeline.
- You can explain each CTE as a named intermediate result and map it to an equivalent pandas DataFrame.
- You do not use AI assistants to write the work.
