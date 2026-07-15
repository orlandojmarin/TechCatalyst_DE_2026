# Week 4 Day 2 Student Resources: Keys, Relationships, and Joins

> **AI-Free Zone (Weeks 1 to 4).** Do not use Copilot, ChatGPT, or another AI assistant to write your SQL. Read documentation, inspect tables, predict row counts, and write the joins yourself. That is how you learn to verify a result later.

## Core Documentation

| Resource | Why it helps |
|---|---|
| [BigQuery Sandbox](https://cloud.google.com/bigquery/docs/sandbox) | Official setup and no-cost Sandbox limits. Checked July 13, 2026. |
| [BigQuery public datasets](https://cloud.google.com/bigquery/public-data) | How public data is hosted and accessed through `bigquery-public-data`. Checked July 13, 2026. |
| [GoogleSQL query syntax: joins](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#join_operation) | Official inner, left, right, and full join behavior in GoogleSQL. Checked July 13, 2026. |
| [DBeaver SQL Editor](https://dbeaver.com/docs/dbeaver/SQL-Editor/) | Run the local SQL in DBeaver and inspect the result grid. |
| [Python `sqlite3` URI guide](https://docs.python.org/3/library/sqlite3.html#how-to-work-with-sqlite-uris) | Open the copied SQLite databases in read-only mode. Checked July 14, 2026. |
| [pandas `read_sql_query`](https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html) | Send SQL through a `sqlite3` connection and receive a DataFrame. Checked July 14, 2026. |
| [Snowflake TPC-H sample data](https://docs.snowflake.com/en/user-guide/sample-data-tpch) | Schema context for the read-only Activity 3 sample data. Checked July 14, 2026. |
| [Snowflake date and time functions](https://docs.snowflake.com/en/sql-reference/functions-date-time) | Reference for `DATE_TRUNC` and `DATEDIFF` in the Snowflake drills. Checked July 14, 2026. |

## Quick Patterns

Match only records that have a lookup row:

```sql
SELECT trips.trip_id, stations.name
FROM trips
INNER JOIN stations
  ON trips.start_station_id = stations.station_id;
```

Keep every trip, including trips with a missing lookup:

```sql
SELECT trips.trip_id, stations.name
FROM trips
LEFT JOIN stations
  ON trips.start_station_id = stations.station_id;
```

Prove that a supposed lookup key is unique:

```sql
SELECT
  COUNT(*) AS rows_in_lookup,
  COUNT(DISTINCT station_id) AS distinct_keys
FROM stations;
```

Count real matches after preserving lookup rows:

```sql
SELECT stations.name, COUNT(trips.trip_id) AS trip_count
FROM stations
LEFT JOIN trips
  ON stations.station_id = trips.start_station_id
GROUP BY stations.name;
```

Send SQLite SQL through Python and return a DataFrame:

```python
from contextlib import closing
import sqlite3
import pandas as pd

with closing(sqlite3.connect("file:crime_database.db?mode=ro", uri=True)) as connection:
    result = pd.read_sql_query("SELECT 1 AS connection_ok;", connection)

result
```

Set the Snowflake sample-data context before querying:

```sql
USE DATABASE SNOWFLAKE_SAMPLE_DATA;
USE SCHEMA TPCH_SF1;
SHOW TABLES;
```

## Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| `no such table` in DBeaver | You opened the wrong SQLite file | Reconnect to your copy in `student-work/week4/day2/` |
| `ModuleNotFoundError: pandas` in the notebook | VS Code selected the wrong Jupyter kernel, or the root project was not synchronized | From the repository root run `uv sync`, then select `<repo-root>/.venv/bin/python` as the kernel |
| Notebook cannot find a database | One or more `.db` files were not copied into the Day 2 workspace | Copy all three databases using the README commands |
| `no such table` in the notebook | The query was sent to the wrong database key | Check the notebook section's database key and table list |
| `Column name ... is ambiguous` | Both tables have a column with that name | Qualify it with an alias, such as `trips.trip_id` |
| Output has more rows than expected | A key matched more than one row | Check key uniqueness and explain the fan-out |
| Zero-trip station shows `1` | You used `COUNT(*)` after a left join | Use `COUNT(trips.trip_id)` |
| BigQuery cannot access a table | Wrong project, missing Sandbox setup, or an organizational restriction | Confirm your Sandbox project, then ask the instructor to check the class account |
| BigQuery estimates more bytes than expected | Query is inspecting too many columns or rows | Select specific columns and add `LIMIT` while exploring |
| Snowflake says no active warehouse | The optional transfer needs the instructor-provided warehouse | Select the named warehouse in Workspaces, then rerun the context commands |
| Snowflake cannot find `CUSTOMER` or `ORDERS` | The current database or schema is wrong | Run the provided `USE DATABASE` and `USE SCHEMA` commands, then confirm the current context |
| Snowflake sample data is missing | The class role does not have imported privileges or the shared database is not attached | Stop and ask the instructor to check the class account. Do not create a replacement database. |

## Lab Deliverable Checklist

| Done | Deliverable |
|---|---|
| [ ] | Pre-class quiz completed |
| [ ] | Day 2 workspace created under `student-work/week4/day2/` |
| [ ] | Three SQLite databases, the companion notebook, and the three starter files copied into the workspace |
| [ ] | Repository-root dependencies synchronized and `<repo-root>/.venv/bin/python` selected as the notebook kernel |
| [ ] | Activity 0 queries completed and 4, 1,000, 1,002 left-join, 4 to 3 to 1 checkpoints explained |
| [ ] | Companion notebook connection tests passed and at least one query from each Day 1 activity transferred |
| [ ] | Day 2 join queries run or replayed through the companion notebook; four reflection responses completed |
| [ ] | Case-close evidence-chain table completed and briefing presented |
| [ ] | Activity 1 validation comments completed in GoogleSQL |
| [ ] | Activity 2 core tier, Q1 through Q6, completed with plain-English result comments |
| [ ] | Stretch tier attempted if time allowed |
| [ ] | Snowflake Tier A, Drills 1 through 5, completed if the instructor opened the extension |
| [ ] | Snowflake Tier B, Drills 6 through 10, completed as the core extension target |
| [ ] | Snowflake Tier C and Tier D attempted if time allowed |
| [ ] | Post-class quiz completed |
