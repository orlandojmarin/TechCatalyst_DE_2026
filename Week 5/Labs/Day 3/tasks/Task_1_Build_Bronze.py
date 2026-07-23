# Databricks notebook source
# MAGIC %md
# MAGIC # Task 1: Build Wanderbricks Bronze
# MAGIC
# MAGIC Copy booking and payment source tables into the target schema. Bronze preserves source columns and adds ingestion metadata.

# COMMAND ----------

# MAGIC %run ./_shared_config

# COMMAND ----------

from pyspark.sql import functions as F

for source_table, target_table in [
    ("samples.wanderbricks.bookings", BRONZE_BOOKINGS_TABLE),
    ("samples.wanderbricks.payments", BRONZE_PAYMENTS_TABLE),
]:
    bronze_df = (
        spark.table(source_table)
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_batch_id", F.lit(BATCH_ID))
    )
    bronze_df.write.mode("overwrite").saveAsTable(target_table)

booking_rows = spark.table(BRONZE_BOOKINGS_TABLE).count()
payment_rows = spark.table(BRONZE_PAYMENTS_TABLE).count()

assert booking_rows > 0, "Bronze bookings source was empty."
assert payment_rows > 0, "Bronze payments source was empty."

dbutils.jobs.taskValues.set(key="booking_rows", value=booking_rows)
dbutils.jobs.taskValues.set(key="payment_rows", value=payment_rows)
print(f"Bronze complete: {booking_rows:,} bookings and {payment_rows:,} payments")
