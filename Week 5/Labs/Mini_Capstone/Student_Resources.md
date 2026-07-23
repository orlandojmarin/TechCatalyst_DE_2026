# Student Resources: Million Song Lakehouse

AI assistance is allowed with review required. Use an assistant to explain or critique, but run every result and make sure your team can defend it.

The project notebook contains the required path. Use this page when you need a short reminder or the official documentation.

## Core Documentation

| Resource | Why it helps |
|---|---|
| [Databricks Free Edition limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations) | Confirms the serverless-only environment and Free Edition limits |
| [Work with files in Unity Catalog volumes](https://docs.databricks.com/aws/en/volumes/volume-files) | Shows how to upload, list, and read the provided data files |
| [`COPY INTO` with Unity Catalog volumes](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into/unity-catalog) | Shows how to load files from a volume into a Delta table |
| [Delta Lake tables](https://docs.databricks.com/aws/en/delta/) and [Unity Catalog views](https://docs.databricks.com/aws/en/views/create-views) | References for managed tables and the persistent analyst-facing view |
| [PySpark DataFrame functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html) | Reference for columns, dates, strings, hashes, and aggregations |
| [PySpark window functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/window.html) | Reference for selecting the latest user record |
| [Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/) | Shows how to create tasks, dependencies, and job runs |
| [Databricks SQL dashboards](https://docs.databricks.com/aws/en/dashboards/) | Helps turn a Gold query into a clear visualization |

## A Simple Mental Model

```text
JSONL files downloaded through Chrome
    -> upload to the team Unity Catalog volume
    -> translate the data dictionary into SQL DDL
    -> COPY INTO source-shaped Bronze tables
    -> Silver cleans
    -> Gold organizes for analysts
    -> analyst view joins the star without copying the data
    -> Validation checks the contracts
```

Complete the project in Databricks. You do not need the virtual machine or a local Python environment. Databricks reads the uploaded JSONL files from `/Volumes/workspace/<team_schema>/landing/`.

Bronze should not quietly change business meaning. Silver should make the records easier and safer to use. Gold should have clear consumers and clear grains.

## Choosing SQL or PySpark

Use SQL for familiar questions:

```sql
SELECT page, COUNT(*) AS events
FROM bronze_logs
GROUP BY page
ORDER BY events DESC;
```

Use PySpark when programmatic transformation is clearer:

```python
from pyspark.sql import functions as F

listens = (
    logs
    .filter((F.col("page") == "NextSong") & (F.col("userId") != ""))
    .withColumn("event_time", F.timestamp_millis("ts"))
)
```

Neither language is automatically better. Choose the clearest tool for the task.

For this project:

- use SQL DDL and `COPY INTO` for Bronze
- use SQL for profiling
- use the provided PySpark scaffold for Silver
- use the provided SQL time-dimension example
- choose SQL or PySpark for each remaining Gold table
- use SQL for the analyst-facing view and business questions

Keep one implementation of each table. Your choice does not change the required table name, columns, grain, row count, or validation checks.

In the presentation, explain one Gold choice using evidence from the transformation. Good reasons include readability, the kind of transformation, maintainability, and ease of validation. Do not claim that one interface is always faster.

## Analyst-Facing View

`gold_songplay_analysis_vw` is a virtual table over the Gold star schema. It should make common analysis easier without storing another copy of the data.

Protect its grain:

1. Begin with the fact table.
2. Use inner joins for required user and time dimensions.
3. Use left joins for optional song and artist dimensions.
4. Select columns explicitly and give ambiguous fields clear names.
5. Confirm that total rows and distinct `songplay_id` values both equal 6,820.

The fact's subscription level describes the event. The user dimension's level is the latest known user value. Keep both only when their aliases make that difference clear.

## Grain Before Join

Write the grain in plain language before every important join.

Example:

```text
silver_listen_events: one row per eligible NextSong log event
gold_fact_songplay: one row per eligible NextSong log event
```

If the row count grows after adding song metadata, investigate duplicate matches before continuing.

## Stable Fact Keys

Distributed row numbers are not repeatable business keys. Spark documents `monotonically_increasing_id()` as non-deterministic because its values depend on partition IDs. A rerun can repartition the data and assign a different number to the same event.

Build a deterministic fingerprint from fields that identify the event:

```python
event_key = F.sha2(
    F.concat_ws(
        "||",
        F.coalesce(F.col("event_timestamp").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("customer_id").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("session_id").cast("string"), F.lit("<null>")),
    ),
    256,
)
```

This pattern works because it:

1. uses fields that should remain stable
2. casts each value to a string
3. represents nulls explicitly
4. combines values in a fixed order
5. hashes the combined value with SHA-256

The same selected inputs produce the same 64-character hexadecimal result. The hash does not make duplicate events unique. If two rows have the same selected fields, they receive the same hash, so you must still validate key uniqueness.

References: [Spark `monotonically_increasing_id()`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.monotonically_increasing_id.html), [Spark `sha2()`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.sha2.html)

## Small Files Are Not Big Data

The original song source has 14,896 files but only about 3.7 MB of content. Opening thousands of remote files can cost more than processing their contents.

The compact course file preserves the rows and original filenames. It removes repeated file-open overhead so the project can focus on Spark transformations, Delta tables, dimensional modeling, SQL, and validation.

Do not manually partition these project tables. Current Databricks guidance recommends avoiding partitioning for tables under 1 TB.

## Lab Deliverable Checklist

| Done | Deliverable |
|---|---|
| [ ] | The work was completed in the team's Databricks Workspace folder |
| [ ] | Architecture diagram has the source, volume, layers, job, and analyst surface |
| [ ] | ERD shows grains, primary keys, foreign keys, and optional relationships |
| [ ] | Implementation choice record explains at least one Gold SQL or PySpark decision |
| [ ] | Bronze tables use explicit SQL DDL translated from the data dictionary |
| [ ] | Both JSONL files were loaded from the team volume with `COPY INTO` |
| [ ] | Bronze row counts are 14,896 songs and 8,056 logs |
| [ ] | Silver listening-event count is 6,820 |
| [ ] | Gold contains four dimensions and one fact table |
| [ ] | `gold_songplay_analysis_vw` joins all four dimensions without changing the 6,820-row fact grain |
| [ ] | Fact row count reconciles to Silver |
| [ ] | Match percentage is calculated and explained |
| [ ] | Two-task Lakeflow Job has a green run |
| [ ] | One failed validation and repaired run are shown in the presentation |
| [ ] | At least two business-question SQL queries are saved |
| [ ] | Both answers are stated as findings in the final presentation |
| [ ] | At least one visualization supports one of the findings |
| [ ] | Every team member has a speaking role |
| [ ] | Build and validation notebooks are exported as source `.py` files |
| [ ] | Presentation, architecture diagram, and Gold ERD are ready to submit |
