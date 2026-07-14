# Week 4 Day 2: Keys, Relationships, and Joins

**Module:** Week 4, Day 2  
**Difficulty:** Beginner to Intermediate  
**Format:** Individual query work, partner validation, then team briefing  
**Platforms:** SQLite in DBeaver or Python with pandas, then BigQuery Sandbox with GoogleSQL. Optional transfer: Snowflake sample data in Snowsight Workspaces.

## Purpose

Yesterday you asked one table careful questions. Today you connect tables and prove that the connection is trustworthy. A join is not just syntax. It is a claim that two columns describe the same business thing. If that claim is wrong, a query can run perfectly and still multiply or lose records.

You will first close the Sequel City investigation in SQLite. You can send the same SQLite SQL through DBeaver or through Python and pandas. Then you will use BigQuery Sandbox and public Austin bikeshare data to practice the same habits on a cloud warehouse.

## Scope

Use these ideas today:

- Primary keys, foreign keys, and relationship shapes
- Inner joins and left joins
- Join conditions, table aliases, and two lookups to the same table
- Row-count validation and join fan-out
- `COUNT(trips.trip_id)` versus `COUNT(*)` after a left join
- `sqlite3` connections and `pd.read_sql_query()` as another interface for the same SQLite SQL
- GoogleSQL table references in BigQuery Sandbox
- Optional extension: complete a 15-drill Snowflake progression on read-only TPC-H sample data

Do not use these yet:

- Subqueries or `WITH` CTEs. These begin on Day 3.
- `CREATE TABLE`, CTAS, or creating views (Day 4)
- Window functions such as `ROW_NUMBER` (Week 5)
- AI assistants to write SQL. Week 4 is an AI-Free Zone.

## Today's Arc

| Sequence | Activity | Story |
|---|---|---|
| 1 | Pre-class quiz and cold open | Revisit the Day 1 suspect board, the `AgentID = -1` orphan, and decide which tables need a relationship |
| 2 | Keys and relationship demo | Predict row preservation, then learn primary keys, foreign keys, and one-to-many fan-out |
| 3 | Activity 0 | Reopen the Sequel City case, validate joins, and close it with an evidence chain |
| 4 | SQLite interface bridge | Run the same Day 1 and Day 2 SQLite SQL through Python and receive DataFrames with pandas |
| 5 | Group activity | Deliver a three-minute case-close briefing and defend one validation choice |
| 6 | Cloud transition | Connect the local join habit to BigQuery Sandbox and public Austin bikeshare tables |
| 7 | Activity 1 | Practice inner and left joins, row preservation, and validation anchors |
| 8 | Activity 2 | Answer business questions with joins and aggregates. Complete the stretch tier only after the core tier |
| 9 | Optional Activity 3 | Progress through 15 Snowflake TPC-H drills, from one-table retrieval to multi-step analysis, without creating objects |
| 10 | Post-class quiz | Check that keys, join choice, nulls, and fan-out are clear |

## Datasets

| Dataset | File or table | Why we use it today |
|---|---|---|
| Sequel City investigation | `data/crime_database.db` | A small local database where the evidence trail makes relationship mistakes visible |
| Day 1 SQLite review | `data/bron.db` and `data/call_center_database2.db` | Local copies used to replay the Day 1 basketball and call-center SQL through Python and pandas |
| Austin bikeshare | `bigquery-public-data.austin_bikeshare.bikeshare_trips` and `bigquery-public-data.austin_bikeshare.bikeshare_stations` | A public, cloud-hosted event table and lookup table for realistic join practice. Source: [BigQuery public datasets](https://cloud.google.com/bigquery/public-data) |
| Snowflake TPC-H sample, optional | `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1` | Shared read-only relational sample data for a full SQL-transfer drill progression. Source: [Snowflake sample data](https://docs.snowflake.com/en/user-guide/sample-data-tpch) |

## Lab Index

### Provided Files

| # | File | Focus |
|---|---|---|
| Reading | `Reading_Joins_and_Relationships.md` | Explainer: keys, row preservation, fan-out, and validation |
| Resources | `Student_Resources.md` | Curated documentation, quick patterns, and deliverable checklist |
| 0 | `Activity_0_SQLite_Murder_Mystery_Joins.md` | Close the investigation with local SQLite joins and count checkpoints |
| Companion | `SQLite_Python_Pandas_Companion.ipynb` | Answer-free notebook for sending the Day 1 and Day 2 SQLite queries through Python and pandas |
| 1 | `Activity_1_BigQuery_Join_Foundations.md` | BigQuery Sandbox, inner joins, left joins, and relationship validation |
| 2 | `Activity_2_BigQuery_Join_Business_Drills.md` | Business questions with joins and aggregates, with a stretch tier |
| 3 | `Activity_3_Snowflake_TPCH_Optional_Transfer.md` | Optional read-only Snowflake transfer: 15 drills from retrieval through intermediate multi-step analysis |
| Group | `Group_Activity_Case_Close_Briefing.md` | Three-minute evidence-chain briefing and defense |
| Starter | `starter/w4d2_murder_mystery_joins.sql` | SQLite query scaffold |
| Starter | `starter/w4d2_bikeshare_join_drills.sql` | GoogleSQL query scaffold |
| Starter | `starter/w4d2_snowflake_tpch_transfer.sql` | Answer-free Snowflake scaffold with 15 ordered drill sections |
| Quiz | `quiz/W4D2_Pre_Quiz.md` | Day 1 retrieval practice |
| Quiz | `quiz/W4D2_Post_Quiz.md` | Keys, joins, nulls, and fan-out check |

### Deliverables

| # | Deliverable | Format |
|---|---|---|
| 0 | Pre-class quiz | Markdown Mash responses |
| 1 | Investigation evidence trail | `w4d2_murder_mystery_joins.sql` with six queries and the final evidence comment |
| 2 | Case-close briefing | One evidence-chain table and a three-minute team presentation |
| 3 | SQLite interface bridge | Copied companion notebook with at least one Day 1 query from each activity, the Day 2 join work, and four reflections |
| 4 | BigQuery join foundations | `w4d2_bikeshare_join_drills.sql`, Activity 1 answers plus validation comments |
| 5 | Business join drills | Core Activity 2 answers, then stretch work if time permits |
| 6 | Optional Snowflake transfer | Completed Snowflake drill tiers and a three-part portable-SQL reflection |
| 7 | Post-class quiz | Markdown Mash responses |

## Student Workspace

Keep your work in your personal student folder, never inside this provided lab folder. Start at the repository root:

```bash
mkdir -p student-work/week4/day2
cp "Week 4/Labs/Day 2/data/bron.db" student-work/week4/day2/
cp "Week 4/Labs/Day 2/data/call_center_database2.db" student-work/week4/day2/
cp "Week 4/Labs/Day 2/data/crime_database.db" student-work/week4/day2/
cp "Week 4/Labs/Day 2/SQLite_Python_Pandas_Companion.ipynb" student-work/week4/day2/
cp "Week 4/Labs/Day 2/starter/w4d2_murder_mystery_joins.sql" student-work/week4/day2/
cp "Week 4/Labs/Day 2/starter/w4d2_bikeshare_join_drills.sql" student-work/week4/day2/
cp "Week 4/Labs/Day 2/starter/w4d2_snowflake_tpch_transfer.sql" student-work/week4/day2/
cd student-work/week4/day2
uv init
uv add pandas ipykernel
uv run python --version
```

`uv init`, `uv add`, and `uv run` must happen after you enter `student-work/week4/day2`. `uv add pandas ipykernel` creates or updates this day's `.venv` in this folder and records the notebook dependencies. Running those commands from the repository root would place the project files in the wrong location and cause interpreter or kernel confusion. `uv run` uses this `.venv` automatically. Keep `.venv`, `__pycache__`, and generated local files gitignored.

Optional: if `student-work/week4/day1/warmup_claims.db` still exists, copy it into `student-work/week4/day2/`. The companion notebook will detect it and open the six Day 1 warmup SQL slots. The notebook works without this optional file.

In VS Code, select `student-work/week4/day2/.venv/bin/python` as the interpreter. Open your copied `SQLite_Python_Pandas_Companion.ipynb` and select the same `.venv` as its Jupyter kernel. If you see `VIRTUAL_ENV does not match the project environment`, run `deactivate`, then run the command again. You may optionally activate the correct environment with `source .venv/bin/activate`.

Complete the copied starter files in this folder. For local SQLite, you may open `crime_database.db` in DBeaver or send the same SQL through the companion notebook. The notebook also includes sections for replaying the Day 1 basketball, call-center, and investigation queries. In BigQuery, paste or upload only your personal `w4d2_bikeshare_join_drills.sql`; do not edit the provided starter in place. If your instructor opens the Snowflake extension, use only your copied `w4d2_snowflake_tpch_transfer.sql` file.

## Check Yourself Culture

Counts are evidence. Before trusting a joined result, state the grain of each input, check whether the key is unique on the lookup side, and compare the output count to the input count you expected to preserve. A surprising count is useful information, not a reason to edit the query until it looks familiar.

## Success Criteria

- You can identify the primary key and foreign key in a relationship.
- You can choose an inner or left join and explain which rows it preserves.
- You validate a join with a row count or uniqueness check before interpreting the result.
- You can explain why a left join from people to Sequel City events grows from 1,000 to 1,002 rows.
- You can use `COUNT(trips.trip_id)` rather than `COUNT(*)` when counting matches after a left join.
- You can explain that DBeaver and pandas are two interfaces sending SQL to the same SQLite engine.
- You can use a read-only `sqlite3` connection and `pd.read_sql_query()` to return a SQL result as a DataFrame.
- You write only GoogleSQL in BigQuery and do not use AI assistants.
- If you complete the optional transfer, you can solve progressively harder questions on Snowflake and identify the SQL that moved unchanged.
