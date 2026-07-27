# Databricks notebook source
# MAGIC %md
# MAGIC # Solution: 02 PySpark DataFrames and Lazy Evaluation

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

trips_df = spark.table("samples.nyctaxi.trips")

activity_clean_df = (
    trips_df
    .withColumn("pickup_date", F.to_date("tpep_pickup_datetime"))
    .withColumn(
        "trip_minutes",
        (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 60.0,
    )
    .withColumn("fare_per_mile", F.col("fare_amount") / F.col("trip_distance"))
    .filter(
        (F.col("trip_distance") > 0)
        & (F.col("fare_amount") > 0)
        & (F.col("trip_minutes") > 0)
    )
    .select("pickup_date", "trip_distance", "fare_amount", "trip_minutes", "fare_per_mile")
)

activity_daily_df = (
    activity_clean_df
    .groupBy("pickup_date")
    .agg(
        F.count("*").alias("trip_count"),
        F.round(F.avg("trip_minutes"), 2).alias("avg_trip_minutes"),
        F.round(F.avg("fare_per_mile"), 2).alias("avg_fare_per_mile"),
    )
    .orderBy("pickup_date")
)

activity_window = Window.orderBy("pickup_date")
activity_change_df = (
    activity_daily_df
    .withColumn("previous_day_trips", F.lag("trip_count").over(activity_window))
    .withColumn("trip_count_change", F.col("trip_count") - F.col("previous_day_trips"))
)

activity_change_df.explain(mode="formatted")
display(activity_change_df)

# COMMAND ----------

assert activity_clean_df.filter(
    (F.col("trip_distance") <= 0) | (F.col("fare_amount") <= 0) | (F.col("trip_minutes") <= 0)
).limit(1).count() == 0
assert {"previous_day_trips", "trip_count_change"}.issubset(activity_change_df.columns)
assert len(activity_change_df.limit(31).toPandas()) <= 31
print("Solution checks passed.")
