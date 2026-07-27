# Databricks notebook source
# MAGIC %md
# MAGIC # Solution: 03 Delta Lake with SQL and PySpark
# MAGIC
# MAGIC Keep this solution in the same Workspace folder as `00_Shared_Setup`.

# COMMAND ----------

# MAGIC %run ./00_Shared_Setup

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE taxi_dropoff_activity
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   dropoff_zip,
# MAGIC   COUNT(*) AS trip_count,
# MAGIC   ROUND(AVG(trip_distance), 2) AS avg_trip_distance,
# MAGIC   ROUND(SUM(fare_amount), 2) AS total_fare
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 0 AND fare_amount > 0
# MAGIC GROUP BY dropoff_zip;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL taxi_dropoff_activity;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY taxi_dropoff_activity;

# COMMAND ----------

from delta.tables import DeltaTable

activity_table_name = f"{CATALOG}.{USER_SCHEMA}.taxi_dropoff_activity"
activity_delta_table = DeltaTable.forName(spark, activity_table_name)
activity_history_python_df = activity_delta_table.history()
activity_baseline_version = activity_history_python_df.agg({"version": "max"}).first()[0]
activity_baseline_total = spark.table(activity_table_name).agg({"trip_count": "sum"}).first()[0]

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE taxi_dropoff_activity
# MAGIC SET trip_count = trip_count + 50
# MAGIC WHERE dropoff_zip = (
# MAGIC   SELECT dropoff_zip
# MAGIC   FROM taxi_dropoff_activity
# MAGIC   ORDER BY trip_count DESC
# MAGIC   LIMIT 1
# MAGIC );

# COMMAND ----------

activity_historical_sql_df = spark.sql(f"""
    SELECT *
    FROM {activity_table_name} VERSION AS OF {int(activity_baseline_version)}
""")

activity_historical_pyspark_df = (
    spark.read
    .option("versionAsOf", activity_baseline_version)
    .table(activity_table_name)
)
activity_current_total = spark.table(activity_table_name).agg({"trip_count": "sum"}).first()[0]
activity_sql_historical_total = activity_historical_sql_df.agg({"trip_count": "sum"}).first()[0]
activity_pyspark_historical_total = (
    activity_historical_pyspark_df.agg({"trip_count": "sum"}).first()[0]
)

assert activity_sql_historical_total == activity_pyspark_historical_total
assert activity_current_total - activity_sql_historical_total == 50
assert activity_sql_historical_total == activity_baseline_total
print("Solution checks passed.")
