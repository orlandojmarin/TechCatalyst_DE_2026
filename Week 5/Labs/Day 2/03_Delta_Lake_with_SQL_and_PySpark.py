# Databricks notebook source
# MAGIC %md
# MAGIC # 03: Delta Lake with SQL and PySpark
# MAGIC
# MAGIC The first two notebooks were read-only. This notebook creates tables, so it needs a private schema.
# MAGIC
# MAGIC You will learn to:
# MAGIC
# MAGIC - understand the difference between a data file and a table format;
# MAGIC - create a managed Delta table with SQL;
# MAGIC - inspect Delta metadata and transaction history;
# MAGIC - create a new table version and query an earlier version;
# MAGIC - read a SQL-created table with PySpark;
# MAGIC - complete an independent Delta activity.
# MAGIC
# MAGIC **Dataset:** `samples.nyctaxi.trips`  
# MAGIC **Writes:** managed Delta tables in your schema  
# MAGIC **Setup helper needed:** yes, once at the start

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: Connect to your Week 5 workspace
# MAGIC
# MAGIC The next cell runs the shared helper notebook. `%run` executes the helper in this same session, so its `CATALOG`, `USER_SCHEMA`, and `VOLUME_PATH` variables become available here.
# MAGIC
# MAGIC **Before you run:** Make sure `00_Shared_Setup` is in the same Databricks Workspace folder as this notebook. Set the `user_schema` widget to a unique name such as `w5_maria`.
# MAGIC
# MAGIC **Look for:** two short confirmation lines showing your schema and governed file path.

# COMMAND ----------

# MAGIC %run ./00_Shared_Setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: What Delta Lake adds
# MAGIC
# MAGIC Parquet and Delta solve different layers of the storage problem.
# MAGIC
# MAGIC | Layer | What it provides |
# MAGIC |---|---|
# MAGIC | Parquet file format | Columnar storage, compression, and typed values inside individual files |
# MAGIC | Delta table format | A transaction log that coordinates a set of data files as one reliable table |
# MAGIC | Unity Catalog | Names, permissions, discovery, lineage, and governance around tables and files |
# MAGIC
# MAGIC A Delta table normally stores data in Parquet files and records table changes in a transaction log. That log enables ACID transactions, schema enforcement, history, and time travel.
# MAGIC
# MAGIC **Why we care:** A folder of unrelated files cannot by itself tell readers which files form the current table after concurrent updates. The Delta log records the valid table state.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3: Create a managed Delta table with SQL
# MAGIC
# MAGIC We start in SQL because table creation is concise and familiar.
# MAGIC
# MAGIC `CREATE OR REPLACE TABLE ... AS SELECT` is often called CTAS. Databricks creates the table and fills it with the query result.
# MAGIC
# MAGIC **Goal:** Create one row per pickup date.
# MAGIC
# MAGIC **Predict:** Is the result a temporary notebook object or a persistent catalog table?

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE taxi_daily_demo
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   to_date(tpep_pickup_datetime) AS pickup_date,
# MAGIC   COUNT(*) AS trip_count,
# MAGIC   ROUND(AVG(fare_amount), 2) AS avg_fare,
# MAGIC   ROUND(SUM(fare_amount), 2) AS total_fare
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 0
# MAGIC   AND fare_amount > 0
# MAGIC GROUP BY to_date(tpep_pickup_datetime);

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** The command succeeds even though no storage path was supplied. This is a managed table. Unity Catalog manages its storage location and lifecycle.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM taxi_daily_demo
# MAGIC ORDER BY pickup_date;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 4: Inspect the table, do not guess
# MAGIC
# MAGIC `DESCRIBE DETAIL` answers questions about the current table. `DESCRIBE HISTORY` answers questions about changes over time.
# MAGIC
# MAGIC **Predict:** Which command should show `delta` as the table format? Which command should show operations such as `CREATE OR REPLACE TABLE`?

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL taxi_daily_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY taxi_daily_demo;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for in detail:** format, number of files, size, and table properties.
# MAGIC
# MAGIC **Look for in history:** ordered versions, timestamps, operations, and operation metrics. Each successful table-changing transaction adds a version.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.1 The same history through the Python Delta API
# MAGIC
# MAGIC SQL is the shortest way to inspect history interactively. PySpark also exposes the history as a DataFrame through `DeltaTable`, which is useful when Python must filter, validate, or reuse the history programmatically.
# MAGIC
# MAGIC **Predict:** Will the Python result contain the same version and operation columns as `DESCRIBE HISTORY`?

# COMMAND ----------

from delta.tables import DeltaTable

table_name = f"{CATALOG}.{USER_SCHEMA}.taxi_daily_demo"
delta_table = DeltaTable.forName(spark, table_name)
history_python_df = delta_table.history()

display(
    history_python_df.select("version", "timestamp", "operation", "operationMetrics")
)

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** the same Delta commits shown by SQL, now represented as a Spark DataFrame that Python can filter or validate.
# MAGIC
# MAGIC **Choice:** Prefer `DESCRIBE HISTORY` when you are inspecting a table. Prefer `DeltaTable.history()` when later Python logic needs the result.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 5: Capture a version before changing the table
# MAGIC
# MAGIC A fixed version number is brittle because you may rerun this notebook. Instead, ask the table history for the current version and save it in Python.
# MAGIC
# MAGIC This is another SQL-to-Python handoff: SQL returns one scalar, and Python stores it.

# COMMAND ----------

baseline_version = (
    spark.sql(f"DESCRIBE HISTORY {table_name}")
    .agg({"version": "max"})
    .first()[0]
)

baseline_total = (
    spark.table(table_name)
    .agg({"trip_count": "sum"})
    .first()[0]
)

print(f"Baseline version: {baseline_version}")
print(f"Baseline total trips: {baseline_total:,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 6: Create a new Delta version
# MAGIC
# MAGIC The next statement changes one row. Delta commits the change atomically: readers see the state before the commit or the state after it, not a half-finished table.
# MAGIC
# MAGIC **Predict:** How should the version number change?

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE taxi_daily_demo
# MAGIC SET trip_count = trip_count + 100
# MAGIC WHERE pickup_date = (SELECT MIN(pickup_date) FROM taxi_daily_demo);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY taxi_daily_demo;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** a newer `UPDATE` version. The earlier version remains available while it is retained.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 7: Time travel with SQL and PySpark
# MAGIC
# MAGIC You are already comfortable with SQL, so begin there. SQL time travel places `VERSION AS OF` directly after the table name:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT *
# MAGIC FROM workspace.your_schema.taxi_daily_demo VERSION AS OF 3;
# MAGIC ```
# MAGIC
# MAGIC The version must be a literal, not a subquery. Because notebook reruns change version numbers, Python inserts the dynamically discovered and validated integer into the SQL text. The transformation itself is still SQL.
# MAGIC
# MAGIC **Goal:** Read the same historical snapshot with SQL and PySpark, then prove both approaches agree.

# COMMAND ----------

assert isinstance(baseline_version, int), "Expected a version number from Delta history."

sql_time_travel_query = f"""
    SELECT *
    FROM {table_name} VERSION AS OF {int(baseline_version)}
"""

print("SQL sent to Spark:")
print(sql_time_travel_query)

historical_sql_df = spark.sql(sql_time_travel_query)
display(historical_sql_df.orderBy("pickup_date"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** SQL returns the table as it existed at `baseline_version`, before the update.
# MAGIC
# MAGIC In SQL Editor, you would copy the version from `DESCRIBE HISTORY` and write the literal directly. In a rerunnable notebook, generating the SQL from a validated history value avoids a hardcoded version.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7.1 The PySpark equivalent
# MAGIC
# MAGIC PySpark expresses the same read through the DataFrame reader option `versionAsOf`. This is useful when the next transformations are already being built with DataFrame methods.

# COMMAND ----------

current_total = spark.table(table_name).agg({"trip_count": "sum"}).first()[0]

historical_pyspark_df = (
    spark.read
    .option("versionAsOf", baseline_version)
    .table(table_name)
)
sql_historical_total = historical_sql_df.agg({"trip_count": "sum"}).first()[0]
pyspark_historical_total = historical_pyspark_df.agg({"trip_count": "sum"}).first()[0]

print(f"SQL historical total at version {baseline_version}:     {sql_historical_total:,}")
print(f"PySpark historical total at version {baseline_version}: {pyspark_historical_total:,}")
print(f"Current total: {current_total:,}")
print(f"Difference from baseline: {current_total - sql_historical_total:,}")

assert sql_historical_total == pyspark_historical_total
assert sql_historical_total == baseline_total
assert current_total - sql_historical_total == 100

# COMMAND ----------

# MAGIC %md
# MAGIC ### What time travel is for
# MAGIC
# MAGIC - audit what a table contained at a previous version;
# MAGIC - reproduce an earlier analysis;
# MAGIC - investigate when bad data appeared;
# MAGIC - recover from an accidental change when the historical files are still retained.
# MAGIC
# MAGIC Time travel is not a permanent backup. Retention and cleanup policies determine how long older data files remain available.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 8: SQL created it, PySpark can use it
# MAGIC
# MAGIC A catalog table is not owned by the language that created it.
# MAGIC
# MAGIC **Goal:** Read the SQL-created table with PySpark and add a quality label.

# COMMAND ----------

from pyspark.sql import functions as F

taxi_daily_df = spark.table(table_name)

labeled_daily_df = taxi_daily_df.withColumn(
    "volume_band",
    F.when(F.col("trip_count") >= 1000, "high").otherwise("normal"),
)

display(labeled_daily_df.orderBy("pickup_date"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** PySpark reads the same current Delta version that SQL sees.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 8.1 Choose the clearest interface
# MAGIC
# MAGIC You do not need to abandon SQL to work with Delta Lake. Many Delta operations have both interfaces.
# MAGIC
# MAGIC | Intent | SQL | Python or PySpark |
# MAGIC |---|---|---|
# MAGIC | Inspect history | `DESCRIBE HISTORY taxi_daily_demo` | `DeltaTable.forName(spark, table_name).history()` |
# MAGIC | Read an old version | `SELECT * FROM taxi_daily_demo VERSION AS OF 3` | `spark.read.option("versionAsOf", 3).table(table_name)` |
# MAGIC | Update rows | `UPDATE taxi_daily_demo SET ... WHERE ...` | `DeltaTable.forName(...).update(condition=..., set={...})` |
# MAGIC | Restore a version | `RESTORE TABLE taxi_daily_demo TO VERSION AS OF 3` | `DeltaTable.forName(...).restoreToVersion(3)` |
# MAGIC | Write a transformed DataFrame | SQL CTAS when the transformation is SQL | `df.write.format("delta").mode("overwrite").saveAsTable(...)` |
# MAGIC
# MAGIC In this notebook, SQL is clearest for CTAS and the one-row update. PySpark is clearest when a historical DataFrame continues into Python calculations. We do not run two equivalent state-changing updates or restores merely to demonstrate syntax because the second command would create another transaction.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 9: Your activity
# MAGIC
# MAGIC ### Scenario
# MAGIC
# MAGIC Build a reliable drop-off summary for the taxi operations team. You will create the table with SQL, inspect it in both APIs, change it, and prove the previous state with both SQL and PySpark.
# MAGIC
# MAGIC ### Success criteria
# MAGIC
# MAGIC Your work must:
# MAGIC
# MAGIC - create a managed Delta table named `taxi_dropoff_activity`;
# MAGIC - use one row per `dropoff_zip`;
# MAGIC - include trip count, average distance, and total fare;
# MAGIC - capture the current version dynamically;
# MAGIC - update exactly one row;
# MAGIC - inspect Delta history with SQL and the Python Delta API;
# MAGIC - read the captured version with both SQL and PySpark;
# MAGIC - prove the two historical results agree;
# MAGIC - pass all validation checks.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Create the Delta table in SQL
# MAGIC
# MAGIC Create or replace `taxi_dropoff_activity` from valid taxi trips.
# MAGIC
# MAGIC Required columns:
# MAGIC
# MAGIC - `dropoff_zip`
# MAGIC - `trip_count`
# MAGIC - `avg_trip_distance`, rounded to two decimals
# MAGIC - `total_fare`, rounded to two decimals
# MAGIC
# MAGIC <details><summary>Hint</summary>Use `CREATE OR REPLACE TABLE ... USING DELTA AS SELECT`, then group by `dropoff_zip`.</details>

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Create taxi_dropoff_activity.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Inspect and capture the baseline
# MAGIC
# MAGIC Run `DESCRIBE DETAIL` and `DESCRIBE HISTORY` in SQL cells. Then use `DeltaTable.forName(...).history()` to create `activity_history_python_df`.
# MAGIC
# MAGIC Finally, use Python to save:
# MAGIC
# MAGIC - `activity_table_name`, the fully qualified table name;
# MAGIC - `activity_baseline_version`, the current maximum version;
# MAGIC - `activity_baseline_total`, the sum of `trip_count`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Inspect table detail.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Inspect table history.

# COMMAND ----------

# TODO: Create activity_history_python_df, then capture the fully qualified name,
# baseline version, and baseline trip total.
activity_table_name = None
activity_history_python_df = None
activity_baseline_version = None
activity_baseline_total = None

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Change one row
# MAGIC
# MAGIC Update the row with the largest `trip_count`. Add `50` to that row's count.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Update exactly one row by choosing the dropoff ZIP with the largest trip_count.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Prove the past with SQL and PySpark
# MAGIC
# MAGIC First create `activity_historical_sql_df` with a SQL query containing:
# MAGIC
# MAGIC ```sql
# MAGIC FROM <table> VERSION AS OF <captured version>
# MAGIC ```
# MAGIC
# MAGIC Execute that SQL with `spark.sql(...)` so the dynamically captured integer can become the required version literal.
# MAGIC
# MAGIC Then use `spark.read.option("versionAsOf", activity_baseline_version).table(...)` to create `activity_historical_pyspark_df`.
# MAGIC
# MAGIC Calculate the current total and one historical total from each approach.
# MAGIC
# MAGIC <details><summary>Hint</summary>Cast the captured version with `int(activity_baseline_version)` before placing it in the SQL text. The value came from trusted table history, not from user input.</details>

# COMMAND ----------

# TODO: Read the historical version through SQL and PySpark, then calculate totals.
activity_historical_sql_df = None
activity_historical_pyspark_df = None
activity_current_total = None
activity_sql_historical_total = None
activity_pyspark_historical_total = None

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validation

# COMMAND ----------

assert spark.catalog.tableExists(f"{CATALOG}.{USER_SCHEMA}.taxi_dropoff_activity"), (
    "Task 1: taxi_dropoff_activity does not exist."
)

activity_columns = set(spark.table(f"{CATALOG}.{USER_SCHEMA}.taxi_dropoff_activity").columns)
expected_columns = {"dropoff_zip", "trip_count", "avg_trip_distance", "total_fare"}
assert activity_columns == expected_columns, "Task 1: check the requested table columns."

assert activity_table_name == f"{CATALOG}.{USER_SCHEMA}.taxi_dropoff_activity", (
    "Task 2: activity_table_name must be fully qualified."
)
assert activity_history_python_df is not None, "Task 2: create history with the Python Delta API."
assert isinstance(activity_baseline_version, int), "Task 2: capture the baseline version as an integer."
assert activity_historical_sql_df is not None, "Task 4: SQL historical DataFrame is still None."
assert activity_historical_pyspark_df is not None, "Task 4: PySpark historical DataFrame is still None."
assert activity_sql_historical_total == activity_pyspark_historical_total, (
    "Task 4: SQL and PySpark should read the same historical total."
)
assert activity_current_total - activity_sql_historical_total == 50, (
    "Tasks 3 and 4: current total should be exactly 50 above the SQL historical total."
)
assert activity_sql_historical_total == activity_baseline_total, (
    "Task 4: the SQL historical total should match the captured baseline."
)

print("All checks passed. SQL and PySpark agree on the historical Delta snapshot.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stretch
# MAGIC
# MAGIC Restore `taxi_dropoff_activity` to `activity_baseline_version`, then verify that the current total once again equals `activity_baseline_total`.
# MAGIC
# MAGIC Choose one approach:
# MAGIC
# MAGIC - SQL: `RESTORE TABLE ... TO VERSION AS OF ...`
# MAGIC - Python: `DeltaTable.forName(spark, activity_table_name).restoreToVersion(...)`
# MAGIC
# MAGIC Explain why you should not run both restore approaches merely to prove you can. One correct state-changing operation is enough.
# MAGIC
# MAGIC ### Reflection
# MAGIC
# MAGIC Explain why a Delta table is more than a folder of Parquet files.
