# Databricks notebook source
# MAGIC %md
# MAGIC # Task 2: Build Wanderbricks Silver
# MAGIC
# MAGIC Aggregate completed payments to booking grain, then create one trusted row per booking.

# COMMAND ----------

# MAGIC %run ./_shared_config

# COMMAND ----------

from pyspark.sql import functions as F

booking_rows = dbutils.jobs.taskValues.get(
    taskKey="build_bronze", key="booking_rows", debugValue=0
)

completed_payments = (
    spark.table(BRONZE_PAYMENTS_TABLE)
    .filter(F.col("status") == "completed")
    .groupBy("booking_id")
    .agg(F.round(F.sum("amount"), 2).alias("paid_amount"))
    .alias("pay")
)

bookings = spark.table(BRONZE_BOOKINGS_TABLE).alias("b")
properties = spark.table("samples.wanderbricks.properties").alias("p")
users = spark.table("samples.wanderbricks.users").alias("u")

silver = (
    bookings
    .join(completed_payments, F.col("b.booking_id") == F.col("pay.booking_id"), "left")
    .join(properties, F.col("b.property_id") == F.col("p.property_id"), "inner")
    .join(users, F.col("b.user_id") == F.col("u.user_id"), "inner")
    .select(
        F.col("b.booking_id"),
        F.col("b.user_id"),
        F.col("b.property_id"),
        F.col("b.check_in"),
        F.col("b.check_out"),
        F.col("b.status").alias("booking_status"),
        F.col("p.title").alias("property_title"),
        F.col("p.property_type"),
        F.col("u.country").alias("guest_country"),
        F.coalesce(F.col("pay.paid_amount"), F.lit(0)).alias("paid_amount"),
        F.col("b._ingested_at"),
        F.col("b._batch_id"),
    )
)

silver.write.mode("overwrite").saveAsTable(SILVER_TABLE)
silver_rows = spark.table(SILVER_TABLE).count()
distinct_bookings = spark.table(SILVER_TABLE).select("booking_id").distinct().count()
silver_revenue = spark.table(SILVER_TABLE).agg(F.round(F.sum("paid_amount"), 2)).first()[0]

assert 0 < silver_rows <= booking_rows, "Silver row count did not reconcile to bronze."
assert silver_rows == distinct_bookings, "Silver is not at one row per booking."

dbutils.jobs.taskValues.set(key="silver_rows", value=silver_rows)
dbutils.jobs.taskValues.set(key="silver_revenue", value=float(silver_revenue or 0))
print(f"Silver complete: {silver_rows:,} trusted bookings, revenue={silver_revenue}")
