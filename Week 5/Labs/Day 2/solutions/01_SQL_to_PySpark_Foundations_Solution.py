# Databricks notebook source
# MAGIC %md
# MAGIC # Solution: 01 SQL to PySpark Foundations
# MAGIC
# MAGIC Compare this solution with your own only after your validation attempt. More than one clear solution can be correct.

# COMMAND ----------

from pyspark.sql import functions as F

minimum_fare = 25.0

candidate_trips_df = spark.sql(
    """
    SELECT dropoff_zip, trip_distance, fare_amount
    FROM samples.nyctaxi.trips
    WHERE trip_distance > 0
      AND fare_amount >= :minimum_fare
    """,
    args={"minimum_fare": minimum_fare},
)

banded_trips_df = candidate_trips_df.withColumn(
    "fare_band",
    F.when(F.col("fare_amount") < 40, "standard")
    .when(F.col("fare_amount") < 80, "high")
    .otherwise("premium"),
)

banded_trips_df.createOrReplaceTempView("banded_trips_python")

activity_result_df = spark.sql("""
    SELECT
      dropoff_zip,
      fare_band,
      COUNT(*) AS trip_count,
      ROUND(AVG(trip_distance), 2) AS avg_trip_distance
    FROM banded_trips_python
    GROUP BY dropoff_zip, fare_band
    HAVING COUNT(*) >= 5
    ORDER BY trip_count DESC
""")

display(activity_result_df)

# COMMAND ----------

assert set(candidate_trips_df.columns) == {"dropoff_zip", "trip_distance", "fare_amount"}
assert candidate_trips_df.filter(F.col("fare_amount") < minimum_fare).limit(1).count() == 0
assert "fare_band" in banded_trips_df.columns
assert activity_result_df.filter(F.col("trip_count") < 5).limit(1).count() == 0
print("Solution checks passed.")
