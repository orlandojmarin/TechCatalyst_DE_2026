# Databricks notebook source
# MAGIC %md
# MAGIC # Week 5 Shared Setup
# MAGIC
# MAGIC This small helper prepares a private place for tables and files that **you create** during Week 5.
# MAGIC
# MAGIC You do not need it for read-only work with `samples.nyctaxi` or `samples.wanderbricks`. The learning notebooks call it only when a lesson begins writing Delta tables or governed files.
# MAGIC
# MAGIC ## Why keep setup in one notebook?
# MAGIC
# MAGIC - You choose your schema name once.
# MAGIC - Later notebooks reuse the same catalog, schema, and volume variables with `%run`.
# MAGIC - The teaching notebooks stay focused on SQL, PySpark, Delta Lake, and pipelines.
# MAGIC
# MAGIC When another notebook runs `%run ./00_Shared_Setup`, Databricks executes this notebook in the same Python session. The variables defined here become available to the calling notebook.

# COMMAND ----------

import re

dbutils.widgets.text("user_schema", "w5_yourname", "Your Week 5 schema")
USER_SCHEMA = dbutils.widgets.get("user_schema").strip().lower()

if not re.fullmatch(r"[a-z][a-z0-9_]{2,40}", USER_SCHEMA):
    raise ValueError(
        "Use 3 to 41 lowercase letters, numbers, or underscores. "
        "The name must start with a letter, for example w5_maria."
    )

CATALOG = "workspace"
VOLUME_NAME = "landing"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{USER_SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {USER_SCHEMA}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{USER_SCHEMA}.{VOLUME_NAME}")

VOLUME_PATH = f"/Volumes/{CATALOG}/{USER_SCHEMA}/{VOLUME_NAME}"

print(f"Ready: {CATALOG}.{USER_SCHEMA}")
print(f"Governed file area: {VOLUME_PATH}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## What this helper created
# MAGIC
# MAGIC | Object | Purpose |
# MAGIC |---|---|
# MAGIC | `workspace.<your_schema>` | Your private namespace for Week 5 tables |
# MAGIC | `workspace.<your_schema>.landing` | A governed volume for files and checkpoints |
# MAGIC | `CATALOG`, `USER_SCHEMA`, `VOLUME_PATH` | Python variables reused by later cells |
# MAGIC
# MAGIC If you ran this notebook directly, you are finished. Return to the numbered learning notebook.
