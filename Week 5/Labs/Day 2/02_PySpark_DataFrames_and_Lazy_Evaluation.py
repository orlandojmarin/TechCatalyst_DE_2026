# Databricks notebook source
# MAGIC %md
# MAGIC # 02: PySpark DataFrames and Lazy Evaluation
# MAGIC
# MAGIC Notebook 01 showed that SQL and PySpark describe work to the same Spark engine. This notebook develops the PySpark side more carefully.
# MAGIC
# MAGIC You will learn to:
# MAGIC
# MAGIC - read a DataFrame pipeline as a translation of SQL;
# MAGIC - create and replace columns with expressions;
# MAGIC - aggregate and use window functions;
# MAGIC - distinguish transformations from actions;
# MAGIC - inspect a query plan;
# MAGIC - move only a safe, bounded result to pandas;
# MAGIC - complete a PySpark activity at the end.
# MAGIC
# MAGIC **Dataset:** `samples.nyctaxi.trips`  
# MAGIC **Writes:** none  
# MAGIC **Setup helper needed:** no

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: The same transformation in SQL and PySpark
# MAGIC
# MAGIC Start with a familiar SQL transformation. It creates useful columns but does not persist them.
# MAGIC
# MAGIC **Goal:** Keep valid trips and derive trip minutes, pickup date, and fare per mile.
# MAGIC
# MAGIC **Predict:** What should happen when `trip_distance` is zero? The `WHERE` clause prevents division by zero before `fare_per_mile` is calculated.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   to_date(tpep_pickup_datetime) AS pickup_date,
# MAGIC   pickup_zip,
# MAGIC   dropoff_zip,
# MAGIC   trip_distance,
# MAGIC   fare_amount,
# MAGIC   ROUND(
# MAGIC     (unix_timestamp(tpep_dropoff_datetime) - unix_timestamp(tpep_pickup_datetime)) / 60.0,
# MAGIC     1
# MAGIC   ) AS trip_minutes,
# MAGIC   ROUND(fare_amount / trip_distance, 2) AS fare_per_mile
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 0
# MAGIC   AND fare_amount > 0
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.1 Translate it into PySpark
# MAGIC
# MAGIC Read each method as a SQL clause or expression:
# MAGIC
# MAGIC | PySpark | SQL idea |
# MAGIC |---|---|
# MAGIC | `.filter(...)` | `WHERE` |
# MAGIC | `.withColumn(name, expression)` | add or replace a `SELECT` expression |
# MAGIC | `.select(...)` | choose output columns |
# MAGIC | `F.to_date(...)` | `to_date(...)` |
# MAGIC | `F.unix_timestamp(...)` | `unix_timestamp(...)` |
# MAGIC
# MAGIC **Before you run:** Count the transformations in the chain. Is `display` part of the DataFrame plan or the action that requests the result?

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

trips_df = spark.table("samples.nyctaxi.trips")

clean_trips_df = (
    trips_df
    .filter((F.col("trip_distance") > 0) & (F.col("fare_amount") > 0))
    .withColumn("pickup_date", F.to_date("tpep_pickup_datetime"))
    .withColumn(
        "trip_minutes",
        F.round(
            (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 60.0,
            1,
        ),
    )
    .withColumn("fare_per_mile", F.round(F.col("fare_amount") / F.col("trip_distance"), 2))
    .select(
        "pickup_date",
        "pickup_zip",
        "dropoff_zip",
        "trip_distance",
        "fare_amount",
        "trip_minutes",
        "fare_per_mile",
    )
)

display(clean_trips_df.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** The output columns and values mirror the SQL query.
# MAGIC
# MAGIC **Why this matters:** PySpark becomes easier to learn when you connect every method to a SQL idea you already understand.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: Transformations are lazy
# MAGIC
# MAGIC Spark separates describing work from executing work.
# MAGIC
# MAGIC - A **transformation** returns another DataFrame and extends the plan. Examples: `select`, `filter`, `withColumn`, `groupBy`, `join`.
# MAGIC - An **action** asks Spark to produce a result. Examples: `display`, `count`, `first`, `collect`, and writing a table.
# MAGIC
# MAGIC **Goal:** Build a new plan without requesting rows.
# MAGIC
# MAGIC **Predict:** Will the next cell scan the taxi table?

# COMMAND ----------

long_trip_plan_df = (
    clean_trips_df
    .filter(F.col("trip_distance") >= 10)
    .select("pickup_date", "pickup_zip", "trip_distance", "fare_amount")
)

print("A DataFrame plan now exists. No action has been called in this cell.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.1 Inspect the plan
# MAGIC
# MAGIC `explain` shows how Spark plans to execute the transformations. Look for filters and projections pushed close to the data source.

# COMMAND ----------

long_trip_plan_df.explain(mode="formatted")

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** A physical plan that includes a filter on trip distance and a projection of only the requested columns.
# MAGIC
# MAGIC **Why laziness helps:** Spark can inspect the whole chain before it runs, combine compatible operations, avoid unused columns, and choose an execution strategy.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.2 Trigger an action
# MAGIC
# MAGIC `count()` asks Spark to scan the relevant rows and return one small number to Python.

# COMMAND ----------

long_trip_count = long_trip_plan_df.count()
print(f"Long trips: {long_trip_count:,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3: Aggregation and the grain of a DataFrame
# MAGIC
# MAGIC The **grain** describes what one row represents.
# MAGIC
# MAGIC - Before `groupBy`: one row represents one trip.
# MAGIC - After grouping by `pickup_date`: one row represents one day.
# MAGIC
# MAGIC **Goal:** Calculate daily trip volume and average fare.
# MAGIC
# MAGIC **Predict:** Which method changes the grain?

# COMMAND ----------

daily_df = (
    clean_trips_df
    .groupBy("pickup_date")
    .agg(
        F.count("*").alias("trip_count"),
        F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
        F.round(F.sum("fare_amount"), 2).alias("total_fare"),
    )
    .orderBy("pickup_date")
)

display(daily_df)

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** one row per pickup date. `groupBy` sets the new grain; `agg` defines the measures at that grain.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 4: Window functions preserve row detail
# MAGIC
# MAGIC A grouped aggregate collapses rows. A window function calculates across related rows while keeping the original row grain.
# MAGIC
# MAGIC Start with SQL because you already know its window syntax.

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH daily AS (
# MAGIC   SELECT
# MAGIC     to_date(tpep_pickup_datetime) AS pickup_date,
# MAGIC     COUNT(*) AS trip_count
# MAGIC   FROM samples.nyctaxi.trips
# MAGIC   WHERE trip_distance > 0 AND fare_amount > 0
# MAGIC   GROUP BY to_date(tpep_pickup_datetime)
# MAGIC )
# MAGIC SELECT
# MAGIC   pickup_date,
# MAGIC   trip_count,
# MAGIC   LAG(trip_count) OVER (ORDER BY pickup_date) AS previous_day_trips,
# MAGIC   trip_count - LAG(trip_count) OVER (ORDER BY pickup_date) AS change_from_previous_day
# MAGIC FROM daily
# MAGIC ORDER BY pickup_date;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.1 The PySpark window object
# MAGIC
# MAGIC PySpark separates the window definition from the function:
# MAGIC
# MAGIC 1. `Window.orderBy(...)` defines which rows are neighbors and their order.
# MAGIC 2. `F.lag(...).over(window)` applies the window function.
# MAGIC
# MAGIC **Predict:** Why is there no `groupBy` in this step? `daily_df` is already at one row per date.

# COMMAND ----------

by_date = Window.orderBy("pickup_date")

daily_change_df = (
    daily_df
    .withColumn("previous_day_trips", F.lag("trip_count").over(by_date))
    .withColumn("change_from_previous_day", F.col("trip_count") - F.col("previous_day_trips"))
)

display(daily_change_df)

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** the first row has no previous day, so its lag value is null. Later rows retain their dates and receive a comparison value.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 5: The driver boundary and pandas
# MAGIC
# MAGIC The Spark driver coordinates the work. `collect()` and `toPandas()` move result rows to the driver process.
# MAGIC
# MAGIC That is safe only when the result is deliberately small.
# MAGIC
# MAGIC **Unsafe pattern:** `spark.table("huge_table").toPandas()`
# MAGIC
# MAGIC **Safer pattern:** aggregate or limit with Spark first, then convert the small result.

# COMMAND ----------

daily_pandas = daily_df.limit(31).toPandas()

print(type(daily_pandas))
print(daily_pandas.head())

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** `daily_pandas` is now a pandas DataFrame in the Python process. The taxi trip details stayed distributed; only the bounded daily result crossed the driver boundary.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 6: Useful Databricks notebook commands
# MAGIC
# MAGIC A cell beginning with `%` changes how Databricks interprets that cell.
# MAGIC
# MAGIC | Command | Purpose | Example use |
# MAGIC |---|---|---|
# MAGIC | `%sql` | Run the cell as SQL | Explore or validate a table |
# MAGIC | `%python` | Run the cell as Python | Useful if the notebook default language differs |
# MAGIC | `%md` | Render Markdown | Explanations and activity instructions |
# MAGIC | `%run` | Execute another notebook in the same session | Load a small shared setup or helper |
# MAGIC | `%fs` | Run a DBFS-style filesystem command | Quick file listing, though `dbutils.fs` is easier to reuse in Python |
# MAGIC
# MAGIC `dbutils` is a Python utility object. Common Week 5 uses are:
# MAGIC
# MAGIC - `dbutils.widgets`: notebook and job parameters;
# MAGIC - `dbutils.fs`: list, inspect, and manage governed file paths;
# MAGIC - `dbutils.jobs.taskValues`: pass small values between Lakeflow Job tasks;
# MAGIC - `dbutils.notebook.run`: call another notebook directly when that pattern is appropriate.
# MAGIC
# MAGIC We use `%run` only when shared code genuinely reduces repetition. That is why the read-only notebooks did not begin with the Week 5 setup helper.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 7: Your activity
# MAGIC
# MAGIC ### Scenario
# MAGIC
# MAGIC The operations team wants a daily reliability view of taxi trips. You will build it entirely with PySpark, inspect its plan, and return a bounded result to pandas.
# MAGIC
# MAGIC ### Success criteria
# MAGIC
# MAGIC Your pipeline must:
# MAGIC
# MAGIC - keep only trips with positive distance, fare, and duration;
# MAGIC - derive `pickup_date`, `trip_minutes`, and `fare_per_mile`;
# MAGIC - aggregate to one row per pickup date;
# MAGIC - add a previous-day trip count with a window;
# MAGIC - pass the validation cell;
# MAGIC - convert no more than 31 result rows to pandas.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Build the valid trip plan
# MAGIC
# MAGIC Create `activity_clean_df` from `trips_df`.
# MAGIC
# MAGIC Required columns:
# MAGIC
# MAGIC - `pickup_date`
# MAGIC - `trip_distance`
# MAGIC - `fare_amount`
# MAGIC - `trip_minutes`
# MAGIC - `fare_per_mile`
# MAGIC
# MAGIC Keep only rows where distance, fare, and calculated duration are greater than zero.
# MAGIC
# MAGIC <details><summary>Hint</summary>Create the derived columns first, then filter all three validity conditions and select the required columns.</details>

# COMMAND ----------

# TODO: Build the lazy transformation plan.
activity_clean_df = None

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Aggregate to the daily grain
# MAGIC
# MAGIC Create `activity_daily_df` with one row per `pickup_date` and these measures:
# MAGIC
# MAGIC - `trip_count`
# MAGIC - `avg_trip_minutes`, rounded to two decimals
# MAGIC - `avg_fare_per_mile`, rounded to two decimals
# MAGIC
# MAGIC Order the result by date.

# COMMAND ----------

# TODO: Aggregate activity_clean_df.
activity_daily_df = None

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Add day-over-day context
# MAGIC
# MAGIC Create `activity_change_df` with:
# MAGIC
# MAGIC - all columns from `activity_daily_df`;
# MAGIC - `previous_day_trips` using `lag`;
# MAGIC - `trip_count_change` as current minus previous.

# COMMAND ----------

# TODO: Define a window and add the two columns.
activity_change_df = None

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Inspect before acting
# MAGIC
# MAGIC Call `explain(mode="formatted")` on `activity_change_df`. Read the plan before you display the result.

# COMMAND ----------

# TODO: Explain the plan.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validation

# COMMAND ----------

assert activity_clean_df is not None, "Task 1: activity_clean_df is still None."
required_clean = {"pickup_date", "trip_distance", "fare_amount", "trip_minutes", "fare_per_mile"}
assert set(activity_clean_df.columns) == required_clean, "Task 1: check the required columns."
assert activity_clean_df.filter(
    (F.col("trip_distance") <= 0) | (F.col("fare_amount") <= 0) | (F.col("trip_minutes") <= 0)
).limit(1).count() == 0, "Task 1: invalid rows remain."

assert activity_daily_df is not None, "Task 2: activity_daily_df is still None."
required_daily = {"pickup_date", "trip_count", "avg_trip_minutes", "avg_fare_per_mile"}
assert set(activity_daily_df.columns) == required_daily, "Task 2: check the daily columns."

assert activity_change_df is not None, "Task 3: activity_change_df is still None."
assert {"previous_day_trips", "trip_count_change"}.issubset(activity_change_df.columns), (
    "Task 3: add both window columns."
)

bounded_pandas = activity_change_df.limit(31).toPandas()
assert len(bounded_pandas) <= 31, "Keep the pandas result bounded to 31 rows."

display(activity_change_df)
print("All checks passed. Your PySpark pipeline is valid and the pandas handoff is bounded.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stretch
# MAGIC
# MAGIC Add a seven-day moving average of `trip_count`. Think carefully about the window frame. Should the current date be included?
# MAGIC
# MAGIC ### Reflection
# MAGIC
# MAGIC Explain the difference between a transformation and an action using one example from your activity.
