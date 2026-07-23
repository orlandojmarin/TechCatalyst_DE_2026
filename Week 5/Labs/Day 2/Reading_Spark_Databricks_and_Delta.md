---
title: "Spark, Databricks, and Delta Lake"
module: "Week 5 Day 2"
type: explainer
audience: "Junior data engineers"
---

# Spark, Databricks, and Delta Lake

## Why Spark After pandas and SQL?

pandas is excellent when data fits comfortably in one machine's memory and an analyst wants rapid, local exploration. SQL is excellent when the data already lives in a database or lakehouse and the transformation is naturally declarative. Spark becomes valuable when the engine must coordinate work across partitions, optimize a larger plan, recover work, and process data that should not be collected into one Python process.

Spark does not make every workload faster. Starting distributed work has overhead. A 5,000-row CSV is usually easier in pandas. A large, recurring pipeline with joins, aggregations, and many files is a better Spark candidate.

| Question | pandas | Spark |
|---|---|---|
| Where does work run? | Local Python process | Distributed engine managed by Databricks |
| Typical evaluation | Mostly eager | Lazy transformations, actions trigger work |
| Memory boundary | One machine | Distributed partitions, plus a limited driver |
| Best fit | Exploration and small extracts | Scalable ETL and governed lakehouse tables |
| Common risk | Running out of local memory | Expensive shuffles or collecting too much to the driver |

## A DataFrame Is a Plan

When you write this code, Spark records a logical plan:

```python
result = trips.filter("trip_distance > 0").groupBy("pickup_zip").count()
```

The variable `result` does not hold all result rows. It points to a plan. An action such as `display`, `show`, `count`, `write`, `first`, or `collect` asks Spark to execute work.

Lazy evaluation lets Spark examine the complete plan before execution. It can push filters earlier, skip unused columns, and choose join or aggregation strategies. Use `explain("formatted")` to inspect the plan. In Free Edition serverless notebooks, use query profiles to inspect executed work.

## Two Different Kinds of Partition

The word partition appears in several places:

1. Execution partitions divide distributed work.
2. A window `partitionBy` separates analytical groups, such as one ranking per ZIP code.
3. Static table partitioning creates physical directory groups.

These are not interchangeable. Databricks currently recommends avoiding manual table partitioning for most tables below 1 TB and recommends liquid clustering when data layout optimization is genuinely needed. A small classroom table should normally remain unpartitioned.

## SQL and PySpark Share an Engine

Use the clearest notation for the task. A SQL query in `%sql` and a PySpark DataFrame plan both run through the Databricks engine.

```sql
SELECT pickup_zip, COUNT(*) AS trips
FROM samples.nyctaxi.trips
GROUP BY pickup_zip;
```

```python
trips.groupBy("pickup_zip").count()
```

Create a temp view when a DataFrame should be queried from SQL. Use `spark.sql()` when Python should receive a SQL result as a DataFrame. Temp views are session-scoped, while managed tables are durable and governed.

## Crossing Between SQL and Python

Databricks supports several different handoffs. Choose the one that matches the size and lifetime of the value.

| Need | Pattern |
|---|---|
| SQL result remains distributed in Python | `df = spark.sql("SELECT ...")` |
| Python needs one SQL value | `value = spark.sql("SELECT ... AS x").first()["x"]` |
| SQL needs a Python value | `spark.sql("... WHERE x >= :limit", args={"limit": value})` |
| A separate `%sql` cell and Python share one input | widget plus a named parameter marker |
| SQL needs to query a Python DataFrame | `df.createOrReplaceTempView("name")` |

A local Python variable is not automatically visible in a separate `%sql` cell. Widgets or parameter markers provide an explicit contract. Avoid inserting filter values into SQL with f-strings when a named parameter marker can represent the value safely.

## Delta Lake Adds Reliability

Parquet files store typed columnar data efficiently. Delta Lake adds a transaction log around data files. The log records committed table versions and enables:

- Atomic changes, so readers see a complete committed state.
- Schema enforcement and controlled schema evolution.
- Table history and time-travel reads.
- Updates, deletes, and `MERGE` operations.
- Recovery through `RESTORE` while retained historical files remain available.

Time travel reads an old version without changing the current table. `RESTORE` creates a new current version that references an earlier valid state.

### Delta operations in SQL and Python

The table behavior is the same. Choose the interface that keeps the surrounding work clearest.

| Need | SQL | Python or PySpark |
|---|---|---|
| Inspect history | `DESCRIBE HISTORY table_name` | `DeltaTable.forName(spark, table_name).history()` |
| Read version 3 | `SELECT * FROM table_name VERSION AS OF 3` | `spark.read.option("versionAsOf", 3).table(table_name)` |
| Read an earlier timestamp | `SELECT * FROM table_name TIMESTAMP AS OF '2026-07-22 09:00:00'` | `spark.read.option("timestampAsOf", timestamp).table(table_name)` |
| Restore a version | `RESTORE TABLE table_name TO VERSION AS OF 3` | `DeltaTable.forName(spark, table_name).restoreToVersion(3)` |

SQL is usually clearer for direct inspection and table administration. PySpark is useful when the historical DataFrame continues through Python transformations, validations, functions, or pipeline logic. Do not perform the same state-changing restore twice merely to demonstrate both syntaxes.

## Databricks Notebook Tools

- `%sql` runs SQL.
- `%fs` is shorthand for file-system utility operations.
- `%run` executes another notebook inline in the same session.
- `dbutils.widgets` provides notebook and job parameters.
- `dbutils.fs` works with governed volume paths and other permitted storage.
- `dbutils.jobs.taskValues` passes small run metadata between job tasks.

Job tasks do not share notebook variables. Durable tables, parameters, and task values are the contracts between isolated tasks.

## Common Mistakes

- Calling `collect()` or `toPandas()` before reducing the data.
- Assuming a transformation has executed because a cell finished.
- Comparing date strings instead of typed dates or timestamps.
- Hardcoding a Delta version before inspecting history.
- Teaching static table partitioning on tiny data.
- Relying on a previous interactive notebook's catalog or schema inside a job task.

## Key Takeaways

1. Use Spark when distributed, governed, repeatable processing earns its overhead.
2. Treat a Spark DataFrame as a logical plan, not a local container of rows.
3. Keep large data in Spark and collect only bounded results.
4. Use SQL and PySpark as complementary interfaces.
5. Delta Lake provides transactional table reliability on object storage.
