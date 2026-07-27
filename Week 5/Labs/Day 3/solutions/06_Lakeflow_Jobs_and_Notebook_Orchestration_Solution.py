# Databricks notebook source
# MAGIC %md
# MAGIC # Reference: 06 Lakeflow Jobs and Notebook Orchestration
# MAGIC
# MAGIC The primary solution is the configured job in the Jobs & Pipelines UI.
# MAGIC
# MAGIC Expected task chain:
# MAGIC
# MAGIC ```text
# MAGIC build_bronze -> build_silver -> build_gold -> validate_gold
# MAGIC ```
# MAGIC
# MAGIC Expected job parameters:
# MAGIC
# MAGIC | Key | Value |
# MAGIC |---|---|
# MAGIC | `target_catalog` | `workspace` |
# MAGIC | `target_schema` | your Week 5 schema |
# MAGIC | `batch_id` | `manual_01` |
# MAGIC
# MAGIC Every task receives the three job parameters through dynamic references. `validate_gold` also receives `minimum_dates=1`.

# COMMAND ----------

dbutils.widgets.text("validation_schema", "w5_yourname", "Schema used by the job")
VALIDATION_SCHEMA = dbutils.widgets.get("validation_schema").strip().lower()

bronze_bookings = f"workspace.{VALIDATION_SCHEMA}.job_bronze_wander_bookings"
bronze_payments = f"workspace.{VALIDATION_SCHEMA}.job_bronze_wander_payments"
silver_table = f"workspace.{VALIDATION_SCHEMA}.job_silver_wander_booking_facts"
gold_table = f"workspace.{VALIDATION_SCHEMA}.job_gold_wander_daily_revenue"

for table_name in [bronze_bookings, bronze_payments, silver_table, gold_table]:
    assert spark.catalog.tableExists(table_name), f"Missing {table_name}"

silver_rows = spark.table(silver_table).count()
gold_rows = spark.table(gold_table).agg({"booking_count": "sum"}).first()[0]
silver_revenue = spark.table(silver_table).agg({"paid_amount": "sum"}).first()[0]
gold_revenue = spark.table(gold_table).agg({"completed_revenue": "sum"}).first()[0]

assert silver_rows == gold_rows
assert round(float(silver_revenue or 0), 2) == round(float(gold_revenue or 0), 2)
display(spark.table(gold_table).orderBy("check_in_date"))
print("Job output checks passed.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Expected failure and repair
# MAGIC
# MAGIC Setting `minimum_dates=9999` should fail only `validate_gold` after the three build tasks succeed. Reset the value to `1` and use **Repair run**. The repaired run should reuse successful upstream work.
