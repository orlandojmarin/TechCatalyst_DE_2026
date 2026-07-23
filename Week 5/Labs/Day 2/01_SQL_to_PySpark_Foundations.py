# Databricks notebook source
# MAGIC %md
# MAGIC # 01: From SQL to PySpark
# MAGIC
# MAGIC You already know how to ask useful questions with SQL. That is our starting point.
# MAGIC
# MAGIC In this notebook, you will:
# MAGIC
# MAGIC 1. query NYC Taxi data with familiar SQL;
# MAGIC 2. learn what Spark and a Spark DataFrame are;
# MAGIC 3. translate a SQL query into PySpark one step at a time;
# MAGIC 4. pass data and parameters between SQL and Python in both directions;
# MAGIC 5. complete an independent activity at the end.
# MAGIC
# MAGIC **Dataset:** `samples.nyctaxi.trips`  
# MAGIC **Writes:** none  
# MAGIC **Setup helper needed:** no
# MAGIC
# MAGIC This is a self-study notebook. For each worked example, read the explanation, make the prediction, run the cell, and compare the result with the "Look for" note.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: Begin with the SQL you know
# MAGIC
# MAGIC A Spark table still feels like a table. Start by inspecting its columns and types.
# MAGIC
# MAGIC **Goal:** Find the columns that could help us measure trip volume, distance, duration, and fares.
# MAGIC
# MAGIC **Before you run:** Predict whether this command reads every taxi row or only table metadata.
# MAGIC
# MAGIC **Look for:** timestamp columns, numeric fare and distance columns, and ZIP code columns. `DESCRIBE TABLE` reads metadata, not the entire dataset.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE samples.nyctaxi.trips;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.1 Ask a business question in SQL
# MAGIC
# MAGIC **Question:** Which pickup ZIP codes produced the most valid trips?
# MAGIC
# MAGIC The query below uses skills you recently practiced: `WHERE`, `GROUP BY`, an aggregate, an alias, and `ORDER BY`.
# MAGIC
# MAGIC **Predict:** Does `WHERE` remove rows before or after the groups are formed?
# MAGIC
# MAGIC **Look for:** one row per pickup ZIP code, with the busiest ZIP code first.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   pickup_zip,
# MAGIC   COUNT(*) AS trip_count,
# MAGIC   ROUND(AVG(trip_distance), 2) AS avg_miles
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 0
# MAGIC   AND fare_amount > 0
# MAGIC GROUP BY pickup_zip
# MAGIC ORDER BY trip_count DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Why Databricks SQL works on this data
# MAGIC
# MAGIC Databricks SQL is not a separate copy of the data. SQL statements are translated into a Spark query plan and run by Databricks compute.
# MAGIC
# MAGIC That gives us a useful mental model:
# MAGIC
# MAGIC | What you write | What Databricks builds | When rows are produced |
# MAGIC |---|---|---|
# MAGIC | SQL query | A Spark logical and physical plan | When the result is requested |
# MAGIC | PySpark DataFrame transformations | A Spark logical and physical plan | When an action requests rows |
# MAGIC
# MAGIC SQL and PySpark are two ways to describe work to the same engine. You do not abandon SQL when you learn PySpark.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: Meet `spark` and the DataFrame
# MAGIC
# MAGIC In a Databricks Python notebook, `spark` is the ready-to-use `SparkSession`. It is the entry point for reading tables, running SQL, and creating DataFrames.
# MAGIC
# MAGIC A Spark DataFrame is a distributed table with named columns and a schema. It resembles a pandas DataFrame, but its data can be spread across many workers and its transformations are usually lazy.
# MAGIC
# MAGIC **Goal:** Create a DataFrame that refers to the NYC Taxi table.
# MAGIC
# MAGIC **Predict:** Does the assignment below copy all rows into the notebook process?
# MAGIC
# MAGIC **Look for:** the variable is created quickly. The assignment describes the source; it does not collect every row to the driver.

# COMMAND ----------

trips_df = spark.table("samples.nyctaxi.trips")

print(type(trips_df))
print(f"Columns: {len(trips_df.columns)}")
trips_df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Spark DataFrame compared with pandas
# MAGIC
# MAGIC | Question | pandas DataFrame | Spark DataFrame |
# MAGIC |---|---|---|
# MAGIC | Where are the rows? | Usually in one Python process | Distributed across Spark partitions |
# MAGIC | When does a filter run? | Usually immediately | Usually after an action is requested |
# MAGIC | Typical strength | Fast local analysis on data that fits memory | Large data, parallel ETL, governed tables |
# MAGIC | Common display | `df.head()` | `display(df.limit(10))` |
# MAGIC | Move all rows to Python? | Rows are already local | `collect()` or `toPandas()`, which can overload the driver |
# MAGIC
# MAGIC Spark is valuable when the data is too large for one machine, when a team needs a repeatable data pipeline, or when the result must become a governed table. pandas remains excellent for smaller local analysis.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3: Translate SQL into PySpark
# MAGIC
# MAGIC Read the two versions side by side.
# MAGIC
# MAGIC | SQL idea | PySpark DataFrame method |
# MAGIC |---|---|
# MAGIC | `FROM table` | `spark.table(...)` |
# MAGIC | `WHERE condition` | `.filter(...)` or `.where(...)` |
# MAGIC | `SELECT columns` | `.select(...)` |
# MAGIC | `GROUP BY columns` | `.groupBy(...)` |
# MAGIC | aggregate functions | `.agg(...)` |
# MAGIC | `ORDER BY` | `.orderBy(...)` |
# MAGIC | `LIMIT` | `.limit(...)` |
# MAGIC
# MAGIC **Goal:** Rebuild the earlier SQL result with PySpark.
# MAGIC
# MAGIC **Before you run:** Trace the chain from top to bottom. Which line filters rows? Which line changes the grain to one row per ZIP code?

# COMMAND ----------

from pyspark.sql import functions as F

top_pickups_df = (
    trips_df
    .filter((F.col("trip_distance") > 0) & (F.col("fare_amount") > 0))
    .groupBy("pickup_zip")
    .agg(
        F.count("*").alias("trip_count"),
        F.round(F.avg("trip_distance"), 2).alias("avg_miles"),
    )
    .orderBy(F.col("trip_count").desc())
    .limit(10)
)

display(top_pickups_df)

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** The result has the same shape as the SQL result: pickup ZIP, trip count, and average miles.
# MAGIC
# MAGIC **Why the parentheses matter:** Each DataFrame method returns another DataFrame. Parentheses let us format the transformation as a readable pipeline.
# MAGIC
# MAGIC **Why `F.col(...)` matters:** Spark builds a column expression. Python is not looping through taxi rows one at a time.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 4: Cross the SQL and Python bridge
# MAGIC
# MAGIC Real Databricks notebooks often mix SQL and Python. Choose the language that makes each step clearest.
# MAGIC
# MAGIC We will practice four different crossings:
# MAGIC
# MAGIC 1. SQL query to a Python DataFrame;
# MAGIC 2. SQL scalar value to a Python variable;
# MAGIC 3. Python value into a parameterized SQL query;
# MAGIC 4. Python DataFrame to a SQL temporary view.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.1 SQL query to a Python DataFrame
# MAGIC
# MAGIC `spark.sql(...)` accepts SQL text and returns a Spark DataFrame. The result stays distributed.
# MAGIC
# MAGIC **Predict:** What is the Python type of `daily_sql_df`?

# COMMAND ----------

daily_sql_df = spark.sql("""
    SELECT
      to_date(tpep_pickup_datetime) AS pickup_date,
      COUNT(*) AS trip_count,
      ROUND(AVG(fare_amount), 2) AS avg_fare
    FROM samples.nyctaxi.trips
    WHERE fare_amount > 0
    GROUP BY to_date(tpep_pickup_datetime)
    ORDER BY pickup_date
""")

print(type(daily_sql_df))
display(daily_sql_df.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** `daily_sql_df` is a Spark DataFrame, not a pandas DataFrame. SQL created its plan; Python now holds the DataFrame reference.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.2 SQL scalar to a Python variable
# MAGIC
# MAGIC Sometimes Python needs one small result, such as a threshold, maximum date, or row count.
# MAGIC
# MAGIC `.first()` is an action. It asks Spark to produce one row. Access the named field so the code explains what it is extracting.

# COMMAND ----------

summary_row = spark.sql("""
    SELECT ROUND(AVG(fare_amount), 2) AS network_avg_fare
    FROM samples.nyctaxi.trips
    WHERE fare_amount > 0
""").first()

network_avg_fare = summary_row["network_avg_fare"]
print(f"SQL returned a Python value: {network_avg_fare}")
print(type(network_avg_fare))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.3 Python variable into SQL
# MAGIC
# MAGIC Use named parameter markers instead of inserting a value into SQL with an f-string. Parameter markers keep values separate from SQL syntax and avoid quoting mistakes.
# MAGIC
# MAGIC **Goal:** Let Python choose the minimum distance, then let SQL calculate the result.

# COMMAND ----------

minimum_miles = 10.0

long_trip_summary_df = spark.sql(
    """
    SELECT
      COUNT(*) AS long_trip_count,
      ROUND(AVG(fare_amount), 2) AS avg_long_trip_fare
    FROM samples.nyctaxi.trips
    WHERE trip_distance >= :minimum_miles
      AND fare_amount > 0
    """,
    args={"minimum_miles": minimum_miles},
)

display(long_trip_summary_df)

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** The SQL contains `:minimum_miles`; the Python dictionary supplies its value.
# MAGIC
# MAGIC A Python variable is **not automatically visible** inside a separate `%sql` cell. For `%sql`, use a notebook widget as the shared parameter contract.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.4 One widget, visible to Python and `%sql`
# MAGIC
# MAGIC Widgets always return text. Python reads the widget with `dbutils.widgets.get(...)`. SQL reads the same widget with a named marker such as `:minimum_distance`.

# COMMAND ----------

dbutils.widgets.text("minimum_distance", "5", "Minimum trip distance")
minimum_distance_python = float(dbutils.widgets.get("minimum_distance"))
print(f"Python sees minimum_distance={minimum_distance_python}")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS qualifying_trips,
# MAGIC   ROUND(AVG(fare_amount), 2) AS avg_fare
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance >= :minimum_distance
# MAGIC   AND fare_amount > 0;

# COMMAND ----------

# MAGIC %md
# MAGIC Change the widget value at the top of the notebook and rerun the Python and SQL cells. Both languages now use the same input.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.5 Python DataFrame to SQL
# MAGIC
# MAGIC A temporary view gives a Python DataFrame a SQL name. It lasts for the current Spark session and does not create a permanent table.
# MAGIC
# MAGIC **Goal:** Build a cleaned DataFrame in PySpark, then analyze it in SQL.

# COMMAND ----------

valid_trips_df = (
    trips_df
    .filter((F.col("trip_distance") > 0) & (F.col("fare_amount") > 0))
    .withColumn(
        "fare_per_mile",
        F.round(F.col("fare_amount") / F.col("trip_distance"), 2),
    )
    .select("pickup_zip", "dropoff_zip", "trip_distance", "fare_amount", "fare_per_mile")
)

valid_trips_df.createOrReplaceTempView("valid_trips_python")
print("Python registered the temporary view: valid_trips_python")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   pickup_zip,
# MAGIC   COUNT(*) AS trip_count,
# MAGIC   ROUND(AVG(fare_per_mile), 2) AS avg_fare_per_mile
# MAGIC FROM valid_trips_python
# MAGIC GROUP BY pickup_zip
# MAGIC HAVING COUNT(*) >= 20
# MAGIC ORDER BY trip_count DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** SQL can query the temporary view created by Python.
# MAGIC
# MAGIC **Important boundary:** A temporary view is session-scoped. A managed Delta table is persistent and can be reused by other notebooks, SQL queries, dashboards, and jobs. Notebook 03 will create persistent Delta tables.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 5: Your activity
# MAGIC
# MAGIC Now complete the bridge without copying the worked example.
# MAGIC
# MAGIC ### Scenario
# MAGIC
# MAGIC A taxi operations analyst wants to compare drop-off ZIP codes for trips above a configurable fare threshold. You will start in SQL, pass the result to Python, enrich it with PySpark, and pass it back to SQL.
# MAGIC
# MAGIC ### Success criteria
# MAGIC
# MAGIC Your completed work must:
# MAGIC
# MAGIC - use a Python variable as a safe SQL parameter;
# MAGIC - return a Spark DataFrame from `spark.sql`;
# MAGIC - add a `fare_band` column with PySpark;
# MAGIC - register a temporary view;
# MAGIC - use SQL to return one row per drop-off ZIP code;
# MAGIC - pass every validation at the end.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Python parameter to SQL DataFrame
# MAGIC
# MAGIC Set `minimum_fare` to `25.0`. Complete the SQL so `candidate_trips_df` contains:
# MAGIC
# MAGIC - `dropoff_zip`
# MAGIC - `trip_distance`
# MAGIC - `fare_amount`
# MAGIC
# MAGIC Keep only rows with a positive distance and a fare at or above the Python threshold.
# MAGIC
# MAGIC <details><summary>Hint</summary>Use `:minimum_fare` in the SQL text and `args={"minimum_fare": minimum_fare}` in `spark.sql`.</details>

# COMMAND ----------

minimum_fare = 25.0

# TODO: Replace None with a parameterized spark.sql(...) call.
candidate_trips_df = None

# display(candidate_trips_df.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Enrich the SQL result with PySpark
# MAGIC
# MAGIC Create `banded_trips_df` from `candidate_trips_df`.
# MAGIC
# MAGIC Add `fare_band` with these rules:
# MAGIC
# MAGIC - fare below 40: `standard`
# MAGIC - fare from 40 through 79.99: `high`
# MAGIC - fare 80 or more: `premium`
# MAGIC
# MAGIC <details><summary>Hint</summary>Use `F.when(condition, value).when(...).otherwise(...)` inside `withColumn`.</details>

# COMMAND ----------

# TODO: Build banded_trips_df.
banded_trips_df = None

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Pass the DataFrame back to SQL
# MAGIC
# MAGIC Register `banded_trips_df` as the temporary view `banded_trips_python`.
# MAGIC
# MAGIC Then complete the SQL query so it returns:
# MAGIC
# MAGIC - one row per `dropoff_zip` and `fare_band`;
# MAGIC - `trip_count`;
# MAGIC - average `trip_distance`, rounded to two decimals;
# MAGIC - only groups with at least 5 trips;
# MAGIC - largest trip count first.

# COMMAND ----------

# TODO: Register the temporary view.

# COMMAND ----------

# TODO: Replace None with spark.sql("""...""") and save the result.
activity_result_df = None

# display(activity_result_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validation
# MAGIC
# MAGIC Run this cell after completing all three tasks. A validation failure tells you which contract is missing.

# COMMAND ----------

assert candidate_trips_df is not None, "Task 1: candidate_trips_df is still None."
assert set(candidate_trips_df.columns) == {"dropoff_zip", "trip_distance", "fare_amount"}, (
    "Task 1: candidate_trips_df needs exactly the requested columns."
)
assert candidate_trips_df.filter(F.col("fare_amount") < minimum_fare).limit(1).count() == 0, (
    "Task 1: a row is below minimum_fare."
)

assert banded_trips_df is not None, "Task 2: banded_trips_df is still None."
assert "fare_band" in banded_trips_df.columns, "Task 2: add fare_band."
assert banded_trips_df.filter(~F.col("fare_band").isin("standard", "high", "premium")).limit(1).count() == 0, (
    "Task 2: fare_band contains an unexpected value."
)

assert spark.catalog.tableExists("banded_trips_python"), (
    "Task 3: register the banded_trips_python temporary view."
)
assert activity_result_df is not None, "Task 3: activity_result_df is still None."
assert {"dropoff_zip", "fare_band", "trip_count", "avg_trip_distance"}.issubset(activity_result_df.columns), (
    "Task 3: activity_result_df is missing a required column."
)
assert activity_result_df.filter(F.col("trip_count") < 5).limit(1).count() == 0, (
    "Task 3: keep only groups with at least 5 trips."
)

print("All checks passed. You crossed the SQL and Python bridge in both directions.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stretch
# MAGIC
# MAGIC Add a widget named `minimum_group_size`. Use it in the final SQL query so the analyst can change the `HAVING` threshold without editing the query.
# MAGIC
# MAGIC ### Reflection
# MAGIC
# MAGIC In one or two sentences, answer: Why might an engineer choose SQL for the aggregation but PySpark for the column enrichment?
