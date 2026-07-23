# Databricks notebook source
# MAGIC %md
# MAGIC # Shared Wanderbricks job configuration
# MAGIC
# MAGIC Every Lakeflow Job task runs in its own notebook session. Each task uses `%run` to load the same validated parameters and table names.

# COMMAND ----------

import re

dbutils.widgets.text("target_catalog", "workspace")
dbutils.widgets.text("target_schema", "w5_yourname")
dbutils.widgets.text("batch_id", "manual")

TARGET_CATALOG = dbutils.widgets.get("target_catalog").strip().lower()
TARGET_SCHEMA = dbutils.widgets.get("target_schema").strip().lower()
BATCH_ID = dbutils.widgets.get("batch_id").strip()

for value, label in [(TARGET_CATALOG, "target_catalog"), (TARGET_SCHEMA, "target_schema")]:
    if not re.fullmatch(r"[a-z][a-z0-9_]{2,40}", value):
        raise ValueError(f"Invalid {label}: {value!r}")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {TARGET_CATALOG}.{TARGET_SCHEMA}")

BRONZE_BOOKINGS_TABLE = f"{TARGET_CATALOG}.{TARGET_SCHEMA}.job_bronze_wander_bookings"
BRONZE_PAYMENTS_TABLE = f"{TARGET_CATALOG}.{TARGET_SCHEMA}.job_bronze_wander_payments"
SILVER_TABLE = f"{TARGET_CATALOG}.{TARGET_SCHEMA}.job_silver_wander_booking_facts"
GOLD_TABLE = f"{TARGET_CATALOG}.{TARGET_SCHEMA}.job_gold_wander_daily_revenue"

print(f"Target schema: {TARGET_CATALOG}.{TARGET_SCHEMA}")
print(f"Batch ID: {BATCH_ID}")
