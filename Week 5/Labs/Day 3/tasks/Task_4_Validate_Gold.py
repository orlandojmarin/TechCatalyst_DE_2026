# Databricks notebook source
# MAGIC %md
# MAGIC # Task 4: Validate Wanderbricks Gold
# MAGIC
# MAGIC Fail clearly when the published daily revenue product violates its contract.

# COMMAND ----------

# MAGIC %run ./_shared_config

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("minimum_dates", "1")
minimum_dates = int(dbutils.widgets.get("minimum_dates"))

expected_bookings = dbutils.jobs.taskValues.get(
    taskKey="build_gold", key="reconciled_bookings", debugValue=0
)
expected_revenue = dbutils.jobs.taskValues.get(
    taskKey="build_gold", key="reconciled_revenue", debugValue=0
)
gold = spark.table(GOLD_TABLE)

date_count = gold.count()
actual_bookings = gold.agg(F.sum("booking_count")).first()[0]
actual_revenue = gold.agg(F.round(F.sum("completed_revenue"), 2)).first()[0]
bad_rows = gold.filter(
    (F.col("booking_count") <= 0)
    | (F.col("paid_booking_count") < 0)
    | (F.col("paid_booking_count") > F.col("booking_count"))
    | (F.col("completed_revenue") < 0)
).count()

assert date_count >= minimum_dates, f"Expected at least {minimum_dates} dates, found {date_count}."
assert actual_bookings == expected_bookings, "Gold bookings do not match the build task value."
assert float(actual_revenue or 0) == float(expected_revenue or 0), (
    "Gold revenue does not match the build task value."
)
assert bad_rows == 0, f"Found {bad_rows} invalid gold rows."

message = (
    f"[{BATCH_ID}] gold validated: {date_count} dates, "
    f"{actual_bookings:,} bookings, revenue={actual_revenue}"
)
print(message)
dbutils.notebook.exit(message)
