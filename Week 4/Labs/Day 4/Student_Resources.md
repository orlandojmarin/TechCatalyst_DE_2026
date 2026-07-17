# Week 4 Day 4 Student Resources: Snowflake Objects and Loads

> **AI-Free Zone (Weeks 1 to 4).** Do not use Copilot, ChatGPT, or another AI assistant to write SQL or complete the lab. Use documentation, your starter scripts, and partner discussion.

## Core Documentation

| Resource | Why it helps |
|---|---|
| [Snowflake Workspaces](https://docs.snowflake.com/en/user-guide/ui-snowsight/workspaces) | The current Snowsight SQL editing surface. Legacy Worksheets are no longer the default learning path. Checked July 14, 2026. |
| [Virtual warehouses](https://docs.snowflake.com/en/user-guide/warehouses-overview) | Understand compute, auto-suspend, and why a warehouse must be selected to run a query or load. |
| [CREATE STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage) | Named internal and external stages, URLs, file formats, and supported cloud storage locations. |
| [S3 storage integrations](https://docs.snowflake.com/en/user-guide/data-load-s3-config-storage-integration) | Why the instructor supplies the integration and the privileges required to create a stage with it. |
| [INFER_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) | Inspect staged Parquet column definitions before creating the target table. |
| [COPY INTO table](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table) | Load files, match Parquet columns by name, and interpret load behavior. |
| [Temporary and transient tables](https://docs.snowflake.com/en/user-guide/tables-temp-transient) | Compare persistence, Time Travel, and Fail-safe trade-offs. |
| [Snowflake Connector for Python API](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api) | Use `write_pandas` and understand its row-count return values. |

## Current Snowflake Object Map

These official references extend the Day 4 core objects. Dynamic tables, pipes, streams, and tasks are a pipeline preview. Interactive tables, semantic views, and Cortex Search are awareness topics for later lessons.

| Resource | What to look for |
|---|---|
| [CREATE DYNAMIC TABLE](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table) | A materialized query result that Snowflake refreshes toward a target-lag freshness goal. |
| [CREATE INTERACTIVE TABLE](https://docs.snowflake.com/en/sql-reference/sql/create-interactive-table) | A specialized table for low-latency, high-concurrency workloads with regional availability limits. |
| [Semantic views](https://docs.snowflake.com/en/user-guide/views-semantic/overview) | Governed metrics, dimensions, facts, and relationships defined as a schema object. |
| [Snowpipe and pipes](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro) | Automated file ingestion driven by a pipe that contains a `COPY` statement. |
| [Streams](https://docs.snowflake.com/en/user-guide/streams-intro) | Change data capture through an offset on a source object, without storing a second copy of the rows. |
| [Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro) | Scheduled or event-triggered SQL and procedure execution. |
| [Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) | Low-latency hybrid vector and keyword search over text data. |

## Context before SQL

Every Snowflake action happens under a context. Run this before you create an object:

```sql
SELECT
  CURRENT_ROLE() AS active_role,
  CURRENT_WAREHOUSE() AS active_warehouse,
  CURRENT_DATABASE() AS active_database,
  CURRENT_SCHEMA() AS active_schema;
```

| Setting | Controls | Common confusion |
|---|---|---|
| Role | What you are allowed to do. | A warehouse being visible does not mean your role can create a stage. |
| Warehouse | Compute used to run queries and loads. | A warehouse does not store the table data. |
| Database and schema | Where new objects are named. | A schema is not a folder on your laptop. |

## Core loading pattern

```sql
CREATE OR REPLACE FILE FORMAT taxi_parquet_ff
  TYPE = PARQUET
  USE_LOGICAL_TYPE = TRUE;

CREATE OR REPLACE STAGE taxi_stage
  URL = 's3://techcatalyst-de-2026/nyc-taxi/yellow-tripdata/'
  STORAGE_INTEGRATION = <INSTRUCTOR_STORAGE_INTEGRATION>
  FILE_FORMAT = (FORMAT_NAME = 'taxi_parquet_ff');

LIST @taxi_stage;
```

The stage is a named pointer to file storage. The file format tells Snowflake how to interpret the file. They are deliberately separate because one stage can support multiple loading patterns, and a file format can be reused.

## Pandas ETL and Snowflake

Activity 4 uses pandas for row-level cleaning, data-quality profiling, feature engineering, and grouped analysis. Snowflake stores the four analytical outputs. The notebook pre-creates transient target tables so their schema and lifecycle are intentional.

`write_pandas` saves a DataFrame into Parquet chunks, uploads the chunks to a temporary Snowflake stage, and runs `COPY INTO` for the target table. Its return values include success, chunk count, and written row count. Reconcile those values with both `len(dataframe)` and `COUNT(*)` in Snowflake. [Python connector API](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api), [connector authentication](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-example#connecting-using-the-default-authenticator)

Keep credentials outside your code. Activity 0 has you create `student-work/week4/day4/snow.cfg` with a `[DEV]` section containing your own `account`, `user`, and `password`, plus `role = DE`, `warehouse = COMPUTE_WH`, `database = TECHCATALYST`, and your `schema`. The password lives in `snow.cfg` only; never paste it into a notebook or script, and never commit an AWS key or token.

The repository-root `.gitignore` already ignores `**/snow.cfg`, so your populated file remains local. Do not create another `.gitignore` inside the day folder.

The notebook reads the section into a regular Python dictionary and passes the dictionary to the connector:

```python
from configparser import ConfigParser

config = ConfigParser()
config.read("snow.cfg")
params = dict(config["DEV"])

conn = snowflake.connector.connect(**params)
```

The `**` operator unpacks the dictionary into named arguments. For example, `params["warehouse"]` becomes the connector's `warehouse=...` argument. This keeps environment-specific values out of notebook cells while making the connection code short and reusable.

## SQL and pandas mastery references

| Resource | What to use it for |
|---|---|
| [Working with CTEs](https://docs.snowflake.com/en/user-guide/queries-cte) | Confirm that a CTE is a named query result available within one statement. Use that definition while thinking of each CTE as the intermediate table the business question needs. |
| [Snowflake `WITH` clause](https://docs.snowflake.com/en/sql-reference/constructs/with) | Check the syntax for defining multiple CTEs that later CTEs and the final query can reference. |
| [Using pandas DataFrames with the Python connector](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-pandas) | Load a Snowflake `SELECT` result with `fetch_pandas_all()` and compare SQL transformations with DataFrame transformations. |

Use this sequence when a query feels too large:

1. State what one final row represents.
2. Name the metric that does not exist yet.
3. Create one intermediate result at the grain required for that metric.
4. Inspect that result with the final `SELECT`.
5. Add the next business transformation only after the current grain is correct.

## Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| `No active warehouse selected` | The context block did not run, or the selected warehouse is suspended. | Select the instructor-provided warehouse in Workspaces and rerun the context block. |
| `Insufficient privileges` when creating a stage | Your role lacks `CREATE STAGE` on the schema or `USAGE` on the integration. | Stop and show the exact error to the instructor. Do not switch to an admin role or add credentials. |
| `LIST` returns no files | The S3 path or integration is wrong. | Confirm the stage definition and the single expected filename with the instructor. |
| `COPY INTO` reports zero loaded rows | The file was already loaded into that target table, or the file path is wrong. | Check the copy result. Do not add `FORCE = TRUE` unless the instructor asks you to repeat a controlled load. |
| Values are null after the load | Target columns did not match the file, or types are incompatible. | Review `INFER_SCHEMA` output and use `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE`. |
| `write_pandas` cannot find a column | DataFrame and target identifiers do not match. | Confirm uppercase DataFrame columns and the explicit target schema. |
| S3 CSV access fails in Activity 4 | The runtime cannot reach the approved source through its configured access. | Stop and show the exact error. Do not add cloud keys to the notebook. |
| `snow.cfg was not found` | The example file was not copied into the day workspace, or the notebook is running from a different folder. | Confirm that the notebook and `snow.cfg` are both in `student-work/week4/day4/`, then check the notebook kernel and working directory. |
| `Missing [DEV] section` or placeholder error | The section name changed, or one or more values were not completed. | Keep the section name exactly `[DEV]` and replace every angle-bracket placeholder with the instructor-provided value. |
| The connection is refused or authentication fails | The `account`, `user`, or `password` is wrong, or a value still has a placeholder. | Recheck the four fixed values (`role = DE`, `warehouse = COMPUTE_WH`, `database = TECHCATALYST`, your `schema`) and your login, then show the error to the instructor. Keep the password in `snow.cfg` only. |

## Lab Deliverable Checklist

| Done | Deliverable |
|---|---|
| [ ] | Day 4 workspace created under `student-work/week4/day4/` |
| [ ] | Context block ran and values recorded |
| [ ] | Temporary and transient behavior compared |
| [ ] | CTAS snapshot, live view, and clone evidence captured |
| [ ] | File format and external stage created without embedded credentials |
| [ ] | `INFER_SCHEMA` output inspected before table creation |
| [ ] | `COPY INTO` result and two validation checks recorded |
| [ ] | Team design defense presented |
| [ ] | Four core SQL transfer drills completed, with extension drills attempted if time allowed |
| [ ] | SQL and CTE mastery core completed with a grain comment for every multi-step query |
| [ ] | pandas mirror completed and SQL-to-pandas parity assertion passed |
| [ ] | `snow.cfg` completed locally with `[DEV]`, your login, `role = DE`, `warehouse = COMPUTE_WH`, and your schema |
| [ ] | Pandas rename mapping, guided cleaning steps, and IQR interpretation completed |
| [ ] | Four pandas analysis outputs loaded and reconciled with their Snowflake targets |
| [ ] | Knowledge check completed |
