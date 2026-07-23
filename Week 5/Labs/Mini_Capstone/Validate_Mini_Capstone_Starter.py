# Databricks notebook source
# MAGIC %md
# MAGIC # Validate the Million Song Lakehouse
# MAGIC
# MAGIC **Team validation notebook**
# MAGIC
# MAGIC A pipeline is not complete because tables exist. It is complete when its important contracts are checked.
# MAGIC
# MAGIC This notebook does not load the JSONL source files or rebuild the lakehouse. It reads the tables created by `Mini_Capstone_Starter.py`.
# MAGIC
# MAGIC Run the build notebook first. Then replace every `TODO`, implement each assertion, and remove each `NotImplementedError` below. Use the completed validation notebook as the second task in your Lakeflow Job.

# COMMAND ----------

# MAGIC %run ./00_Shared_Setup

# COMMAND ----------

from pyspark.sql import functions as F

bronze_songs = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_songs")
bronze_logs = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_logs")
silver_songs = spark.table(f"{CATALOG}.{USER_SCHEMA}.silver_song_catalog")
silver_events = spark.table(f"{CATALOG}.{USER_SCHEMA}.silver_listen_events")
dim_song = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_dim_song")
dim_artist = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_dim_artist")
dim_user = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_dim_user")
dim_time = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_dim_time")
fact = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_fact_songplay")
analysis_view = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_songplay_analysis_vw")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Layer counts
# MAGIC
# MAGIC Add assertions for:
# MAGIC
# MAGIC - 14,896 Bronze song rows
# MAGIC - 8,056 Bronze log rows
# MAGIC - 14,896 Silver song rows
# MAGIC - 6,820 Silver listening events
# MAGIC - Gold fact rows equal Silver listening-event rows

# COMMAND ----------

assert bronze_songs.count() == 14_896, "Bronze song count changed"

# TODO: add the other four count assertions by following the pattern above
raise NotImplementedError("Add the remaining four layer-count assertions, then remove this line.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Dimension keys
# MAGIC
# MAGIC For each Gold dimension, prove that its primary key is not null and not duplicated.

# COMMAND ----------

dimension_keys = [
    ("gold_dim_song", dim_song, "song_id"),
    ("gold_dim_artist", dim_artist, "artist_id"),
    ("gold_dim_user", dim_user, "user_id"),
    ("gold_dim_time", dim_time, "time_id"),
]

for table_name, dataframe, key_column in dimension_keys:
    # TODO: count null keys
    # TODO: count duplicated keys
    # TODO: assert that both counts are zero
    pass

raise NotImplementedError("Complete the dimension-key loop, then remove this line.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Fact contract
# MAGIC
# MAGIC Check that:
# MAGIC
# MAGIC - `songplay_id` is not null and is unique
# MAGIC - `user_id` is not null
# MAGIC - `time_id` is not null
# MAGIC - every fact user exists in `gold_dim_user`
# MAGIC - every fact timestamp exists in `gold_dim_time`
# MAGIC - the join did not multiply listening events

# COMMAND ----------

assert fact.filter(F.col("songplay_id").isNull()).count() == 0

# TODO: add the remaining fact assertions by following the pattern above
raise NotImplementedError("Add the fact-contract assertions, then remove this line.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Analyst-view grain
# MAGIC
# MAGIC Prove that joining all four dimensions did not remove or multiply fact rows:
# MAGIC
# MAGIC - view rows equal fact rows
# MAGIC - distinct `songplay_id` values in the view equal fact rows

# COMMAND ----------

# TODO: add the two analyst-view grain assertions
raise NotImplementedError("Add the analyst-view grain assertions, then remove this line.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Match coverage
# MAGIC
# MAGIC The song catalog is a subset, so unmatched fact rows are allowed. Calculate and print the matched row count and percentage. Do not assert that every event matches.

# COMMAND ----------

# TODO: calculate matched_rows, fact_rows, and match_percentage
# print(...)
raise NotImplementedError("Calculate and print match coverage, then remove this line.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Team quality rule
# MAGIC
# MAGIC Add one additional check that would prevent a meaningful business or analytical error. Explain the rule in a markdown cell before the code.

# COMMAND ----------

# TODO: add the team's quality rule
raise NotImplementedError("Add the team quality rule, then remove this line.")

# COMMAND ----------

print("Million Song lakehouse validation passed.")
