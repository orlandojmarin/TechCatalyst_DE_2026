# Databricks notebook source
# MAGIC %md
# MAGIC # Solution: 04 Wanderbricks SQL and PySpark

# COMMAND ----------

from pyspark.sql import functions as F

bookings = spark.table("samples.wanderbricks.bookings").alias("b")
payments = spark.table("samples.wanderbricks.payments")
properties = spark.table("samples.wanderbricks.properties").alias("p")
reviews = spark.table("samples.wanderbricks.reviews")

paid_by_booking = (
    payments
    .filter(F.col("status") == "completed")
    .groupBy("booking_id")
    .agg(F.sum("amount").alias("paid_amount"))
)

booking_measures = (
    bookings
    .join(paid_by_booking, "booking_id", "left")
    .groupBy("property_id")
    .agg(
        F.count("*").alias("booking_count"),
        F.round(F.sum(F.coalesce(F.col("paid_amount"), F.lit(0))), 2).alias("completed_revenue"),
    )
)

review_measures = (
    reviews
    .filter(F.col("is_deleted") == F.lit(False))
    .groupBy("property_id")
    .agg(
        F.count("rating").alias("review_count"),
        F.round(F.avg("rating"), 2).alias("avg_rating"),
    )
)

property_performance_df = (
    properties
    .join(booking_measures, "property_id", "left")
    .join(review_measures, "property_id", "left")
    .select(
        "property_id",
        F.col("p.title").alias("property_title"),
        F.col("p.property_type").alias("property_type"),
        F.coalesce(F.col("booking_count"), F.lit(0)).alias("booking_count"),
        F.coalesce(F.col("completed_revenue"), F.lit(0)).alias("completed_revenue"),
        F.coalesce(F.col("review_count"), F.lit(0)).alias("review_count"),
        F.col("avg_rating"),
    )
)

property_performance_df.createOrReplaceTempView("property_performance_python")

top_properties_df = spark.sql("""
    SELECT *
    FROM property_performance_python
    WHERE review_count >= 5
      AND completed_revenue > 0
    ORDER BY completed_revenue DESC
    LIMIT 10
""")

assert property_performance_df.count() == property_performance_df.select("property_id").distinct().count()
display(top_properties_df)
print("Solution checks passed.")
