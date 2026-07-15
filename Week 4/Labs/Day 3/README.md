# Week 4 Day 3: Readable SQL and Reusable Results

Day 3 moves from one-statement SQL into named steps and reusable results. You will inspect tiny transit data, build CTEs against public taxi data, then compare SQLite and Snowflake object behavior.

This is an AI-Free Zone. Write and explain your own SQL. Use documentation, notes, and partner discussion.

## Learning Objectives

By the end of the day, you can:

1. Choose among a subquery, CTE, temporary table, view, and CTAS table.
2. Use BigQuery session mode to retain temporary tables across query entries.
3. Explain BigQuery `STRUCT` and `UNNEST` and compare them with Snowflake `VALUES`.
4. Build and verify multi-step CTE queries against a fixed public-data window.
5. Create tables, insert rows, build CTAS snapshots, and create views in SQLite and Snowflake.
6. Compare common view and table types in BigQuery and Snowflake.

## Lab Index

### Provided files

| Order | File | Purpose |
|---|---|---|
| 0 | `Activity_0_SQL_Workspace_Setup.md` | Prepare the Day 3 work folder and copy starters. |
| 1 | `Activity_1_GTFS_SQL_Warmup.md` | Enable a BigQuery session, understand GTFS, and complete six verified warm-ups. |
| 2 | `Activity_2_BigQuery_Public_Taxi_CTEs.md` | Complete five guided CTE drills and seven extensions with a fixed 2023 window. |
| 3 | `Activity_3_BigQuery_Taxi_Business_Challenge.md` | Build one equally scoped team query, visualize its five-row result, and defend the business story. |
| 4 | `Activity_4_SQLite_DDL_Fast_Finisher.md` | Run the same DDL, insert, CTAS, and view workflow in SQLite and Snowflake. |
| 5 | `Activity_5_Snowflake_SQL_Transfer_Lab.md` | Use TPC-H joins and CTEs, then save results as temporary tables, views, and CTAS tables. |
| Group | `Group_Activity_SQL_Question_Review_Board.md` | Defend one cost-aware SQL answer as business evidence. |
| Reading | `Reading_SQL_By_Hand_BigQuery.md` | Compare query structures, sessions, and reusable database objects. |
| Dataset | [Chicago Taxi Trips](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew/about_data) | Public source represented in BigQuery. |
| Starter | `starter/` | Editable SQL scaffolds and review template. |
| Resources | `Student_Resources.md` | Official documentation and decision guide. |
| Quiz | `quiz/` | Pre-check and closing knowledge check. |

### Deliverables

| Deliverable | Evidence |
|---|---|
| GTFS warm-up | Six queries whose outputs match the posted results. |
| Public taxi CTE drills | Five core queries using the fixed 2023 window and required CTE names. |
| Business challenge | One two-CTE query, five-row result check, manual bar chart, interpretation, recommendation, limitation, and next validation. |
| DDL comparison | SQLite and Snowflake evidence showing snapshot-versus-view behavior. |
| Snowflake transfer | Drills 1 through 6 plus an object-choice explanation. |
| Review board | Three-minute team defense. |

## Suggested learning arc

| Sequence | Work |
|---|---|
| Launch | Activity 0, instructor demo of sessions and temporary objects. |
| Guided practice | Activity 1 GTFS warm-up. |
| Core practice | Activity 2 Drills 1 through 5. |
| Application | Activity 3 and Group Review Board. |
| Persistence transfer | Activity 4 SQLite, then Snowflake. |
| Additional practice | Activity 2 extensions and Activity 5 Snowflake drills. |

## What you write

| Starter | Provided | You write |
|---|---|---|
| `day3_gtfs_setup.sql` | Tiny temporary tables | Nothing; run it in session mode. |
| `day3_gtfs_warmup.sql` | Six blank work areas | Six SQL answers. |
| `day3_public_taxi_cte_drills.sql` | Fixed dates and named-step hints | Five core queries and selected extensions. |
| `day3_public_taxi_business_challenge.sql` | Two-CTE planning, validation, visualization, and story headings | One full query, chart evidence, and team defense. |
| `day3_sqlite_ddl_fast_finisher.sql` | SQLite table and seed rows | CTAS, view, checks, and explanation. |
| `day3_snowflake_ddl_mirror.sql` | Snowflake table and seed rows | CTAS, view, checks, and explanation. |
| `w4d3_snowflake_tpch_transfer.sql` | Context and ten drill prompts | Drills 1 through 6, then selected extensions. |

## Success Criteria

- All work remains under `student-work/week4/day3/`.
- The one repository-root `.gitignore` is used. No nested ignore file is created.
- BigQuery session mode is enabled before GTFS temporary tables are created.
- Taxi queries use GoogleSQL and `2023-12-25` through `2023-12-31`.
- Created Snowflake objects are confined to the assigned `TECHCATALYST` schema.
- You can justify whether a result belongs in a CTE, temporary table, view, or stored table.
