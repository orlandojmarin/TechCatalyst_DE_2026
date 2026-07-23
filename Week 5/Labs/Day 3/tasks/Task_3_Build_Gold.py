# Databricks notebook source
# MAGIC %md
# MAGIC # Task 3: Build Wanderbricks Gold
# MAGIC
# MAGIC Publish one row per check-in date and reconcile it with the upstream silver task.

# COMMAND ----------

# MAGIC %run ./_shared_config

# COMMAND ----------

from pyspark.sql import functions as F

silver_rows = dbutils.jobs.taskValues.get(
    taskKey="build_silver", key="silver_rows", debugValue=0
)
silver_revenue = dbutils.jobs.taskValues.get(
    taskKey="build_silver", key="silver_revenue", debugValue=0
)

gold = (
    spark.table(SILVER_TABLE)
    .groupBy(F.to_date("check_in").alias("check_in_date"))
    .agg(
        F.count("*").alias("booking_count"),
        F.count(F.when(F.col("paid_amount") > 0, True)).alias("paid_booking_count"),
        F.round(F.sum("paid_amount"), 2).alias("completed_revenue"),
    )
)

gold.write.mode("overwrite").saveAsTable(GOLD_TABLE)
gold_df = spark.table(GOLD_TABLE)
reconciled_bookings = gold_df.agg(F.sum("booking_count")).first()[0]
reconciled_revenue = gold_df.agg(F.round(F.sum("completed_revenue"), 2)).first()[0]

assert reconciled_bookings == silver_rows, "Gold booking totals did not reconcile to silver."
assert float(reconciled_revenue or 0) == float(silver_revenue or 0), (
    "Gold revenue did not reconcile to silver."
)

dbutils.jobs.taskValues.set(key="reconciled_bookings", value=reconciled_bookings)
dbutils.jobs.taskValues.set(key="reconciled_revenue", value=float(reconciled_revenue or 0))
print(f"Gold complete: {reconciled_bookings:,} bookings, revenue={reconciled_revenue}")
