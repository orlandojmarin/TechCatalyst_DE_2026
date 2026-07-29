# Databricks notebook source
# MAGIC %md
# MAGIC # Solution Guide: Validate the Million Song Lakehouse
# MAGIC
# MAGIC These checks form the second task in the reference Lakeflow Job.

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
# MAGIC ## Completed Code: Layer counts

# COMMAND ----------

assert bronze_songs.count() == 14_896, "Bronze song count changed"
assert bronze_logs.count() == 8_056, "Bronze log count changed"
assert silver_songs.count() == 14_896, "Silver song count changed"
assert silver_events.count() == 6_820, "Silver listening-event count changed"
assert fact.count() == silver_events.count(), "Fact does not reconcile to Silver events"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Dimension keys

# COMMAND ----------

dimension_keys = [
    ("gold_dim_song", dim_song, "song_id"),
    ("gold_dim_artist", dim_artist, "artist_id"),
    ("gold_dim_user", dim_user, "user_id"),
    ("gold_dim_time", dim_time, "time_id"),
]

for table_name, dataframe, key_column in dimension_keys:
    null_keys = dataframe.filter(F.col(key_column).isNull()).count()
    duplicate_keys = (
        dataframe
        .groupBy(key_column)
        .count()
        .filter(F.col("count") > 1)
        .count()
    )
    assert null_keys == 0, f"{table_name} has {null_keys} null keys"
    assert duplicate_keys == 0, f"{table_name} has {duplicate_keys} duplicate keys"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Fact contract

# COMMAND ----------

fact_rows = fact.count()
fact_key_rows = fact.select("songplay_id").distinct().count()

assert fact.filter(F.col("songplay_id").isNull()).count() == 0
assert fact_rows == fact_key_rows, "songplay_id is not unique"
assert fact.filter(F.col("user_id").isNull()).count() == 0
assert fact.filter(F.col("time_id").isNull()).count() == 0
assert fact_rows == 6_820, "The song join multiplied or removed listening events"

missing_users = (
    fact.select("user_id").distinct()
    .join(dim_user.select("user_id"), "user_id", "left_anti")
    .count()
)
missing_times = (
    fact.select("time_id").distinct()
    .join(dim_time.select("time_id"), "time_id", "left_anti")
    .count()
)

assert missing_users == 0, f"Fact references {missing_users} unknown users"
assert missing_times == 0, f"Fact references {missing_times} unknown timestamps"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Analyst-view grain

# COMMAND ----------

view_rows = analysis_view.count()
view_fact_keys = analysis_view.select("songplay_id").distinct().count()

assert view_rows == fact_rows, "Analyst view removed or multiplied fact rows"
assert view_fact_keys == fact_rows, "Analyst view changed the songplay grain"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Match coverage

# COMMAND ----------

matched_rows = fact.filter(F.col("song_id").isNotNull()).count()
match_percentage = round(100 * matched_rows / fact_rows, 2)

print(f"Matched song rows: {matched_rows:,} of {fact_rows:,} ({match_percentage}%)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Additional business rule
# MAGIC
# MAGIC Sparkify's known subscription levels are `free` and `paid`. Any other value would break level-based analysis.

# COMMAND ----------

invalid_levels = fact.filter(
    F.col("level").isNull() | ~F.col("level").isin("free", "paid")
).count()

assert invalid_levels == 0, f"Found {invalid_levels} invalid subscription levels"

print("Million Song lakehouse validation passed.")
