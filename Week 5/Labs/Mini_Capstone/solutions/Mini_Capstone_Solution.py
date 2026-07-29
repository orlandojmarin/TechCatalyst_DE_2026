# Databricks notebook source
# MAGIC %md
# MAGIC # Solution Guide: The Million Song Lakehouse
# MAGIC
# MAGIC **Instructor reference**
# MAGIC
# MAGIC This solution uses direct SQL and PySpark. It intentionally avoids helper classes, manual partitioning, and duplicate Silver-to-Gold copies.

# COMMAND ----------

# MAGIC %run ./00_Shared_Setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Bronze DDL and `COPY INTO`
# MAGIC
# MAGIC Bronze preserves the source shape. The explicit SQL DDL translates the project data dictionary into an enforceable table contract.

# COMMAND ----------

SONGS_PATH = f"{VOLUME_PATH}/songs_compact.jsonl"
LOGS_PATH = f"{VOLUME_PATH}/logs_compact.jsonl"

from pyspark.sql import functions as F

spark.sql("DROP TABLE IF EXISTS bronze_songs")
spark.sql("""
CREATE TABLE bronze_songs (
  _source_file STRING,
  artist_id STRING,
  artist_latitude DOUBLE,
  artist_location STRING,
  artist_longitude DOUBLE,
  artist_name STRING,
  duration DOUBLE,
  num_songs BIGINT,
  song_id STRING,
  title STRING,
  year BIGINT
)
USING DELTA
""")

spark.sql(f"""
COPY INTO bronze_songs
FROM '{SONGS_PATH}'
FILEFORMAT = JSON
""")

spark.sql("DROP TABLE IF EXISTS bronze_logs")
spark.sql("""
CREATE TABLE bronze_logs (
  _source_file STRING,
  artist STRING,
  auth STRING,
  firstName STRING,
  gender STRING,
  itemInSession BIGINT,
  lastName STRING,
  length DOUBLE,
  level STRING,
  location STRING,
  method STRING,
  page STRING,
  registration DOUBLE,
  sessionId BIGINT,
  song STRING,
  status BIGINT,
  ts BIGINT,
  userAgent STRING,
  userId STRING
)
USING DELTA
""")

spark.sql(f"""
COPY INTO bronze_logs
FROM '{LOGS_PATH}'
FILEFORMAT = JSON
""")

bronze_songs_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_songs")
bronze_logs_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_logs")

assert bronze_songs_df.count() == 14_896
assert bronze_logs_df.count() == 8_056

print("Bronze complete: 14,896 songs and 8,056 logs")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Silver
# MAGIC
# MAGIC Silver creates consistent matching keys and a typed listening timestamp. It does not change the declared grains.

# COMMAND ----------

bronze_songs_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_songs")
bronze_logs_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_logs")

silver_song_catalog = (
    bronze_songs_df
    .select(
        "song_id",
        F.trim("title").alias("title"),
        F.lower(F.trim("title")).alias("title_key"),
        "artist_id",
        F.trim("artist_name").alias("artist_name"),
        F.lower(F.trim("artist_name")).alias("artist_key"),
        "artist_location",
        "artist_latitude",
        "artist_longitude",
        "year",
        "duration",
        F.round("duration", 3).alias("duration_key"),
        "_source_file",
    )
    .dropDuplicates(["song_id"])
)

silver_listen_events = (
    bronze_logs_df
    .filter((F.col("page") == "NextSong") & (F.trim("userId") != ""))
    .withColumn("event_time", F.timestamp_millis("ts"))
    .withColumn("song_key", F.lower(F.trim("song")))
    .withColumn("artist_key", F.lower(F.trim("artist")))
    .withColumn("duration_key", F.round("length", 3))
    .select(
        "ts",
        "event_time",
        "userId",
        "firstName",
        "lastName",
        "gender",
        "level",
        "sessionId",
        "location",
        "userAgent",
        "song",
        "song_key",
        "artist",
        "artist_key",
        "length",
        "duration_key",
        "_source_file",
    )
)

silver_song_catalog.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.{USER_SCHEMA}.silver_song_catalog"
)
silver_listen_events.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.{USER_SCHEMA}.silver_listen_events"
)

assert silver_song_catalog.count() == 14_896
assert silver_listen_events.count() == 6_820
print("Silver complete: 14,896 songs and 6,820 listening events")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Gold dimensions

# COMMAND ----------

silver_songs_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.silver_song_catalog")

gold_dim_song = silver_songs_df.select(
    "song_id",
    "title",
    "artist_id",
    "year",
    "duration",
)

gold_dim_artist = (
    silver_songs_df
    .groupBy("artist_id")
    .agg(
        F.max("artist_name").alias("artist_name"),
        F.max("artist_location").alias("artist_location"),
        F.max("artist_latitude").alias("artist_latitude"),
        F.max("artist_longitude").alias("artist_longitude"),
    )
)

gold_dim_song.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.{USER_SCHEMA}.gold_dim_song"
)
gold_dim_artist.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.{USER_SCHEMA}.gold_dim_artist"
)

# COMMAND ----------

from pyspark.sql.window import Window

user_window = Window.partitionBy("userId").orderBy(F.col("ts").desc())

gold_dim_user = (
    bronze_logs_df
    .filter(F.trim("userId") != "")
    .withColumn("row_number", F.row_number().over(user_window))
    .filter(F.col("row_number") == 1)
    .select(
        F.col("userId").cast("int").alias("user_id"),
        F.col("firstName").alias("first_name"),
        F.col("lastName").alias("last_name"),
        "gender",
        "level",
    )
)

gold_dim_user.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.{USER_SCHEMA}.gold_dim_user"
)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_dim_time AS
# MAGIC SELECT DISTINCT
# MAGIC   ts AS time_id,
# MAGIC   event_time,
# MAGIC   HOUR(event_time) AS hour,
# MAGIC   DAY(event_time) AS day,
# MAGIC   WEEKOFYEAR(event_time) AS week,
# MAGIC   MONTH(event_time) AS month,
# MAGIC   YEAR(event_time) AS year,
# MAGIC   DAYOFWEEK(event_time) AS weekday
# MAGIC FROM silver_listen_events

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Gold fact
# MAGIC
# MAGIC The left join preserves all 6,820 listening events. Song and artist keys are nullable because the metadata is a subset.

# COMMAND ----------

events = spark.table(f"{CATALOG}.{USER_SCHEMA}.silver_listen_events").alias("e")
song_lookup = spark.table(f"{CATALOG}.{USER_SCHEMA}.silver_song_catalog").alias("s")

join_condition = (
    (F.col("e.song_key") == F.col("s.title_key"))
    & (F.col("e.artist_key") == F.col("s.artist_key"))
    & (F.col("e.duration_key") == F.col("s.duration_key"))
)

songplay_id = F.sha2(
    F.concat_ws(
        "||",
        F.coalesce(F.col("e.ts").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("e.userId").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("e.sessionId").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("e.song").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("e.artist").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("e.length").cast("string"), F.lit("<null>")),
    ),
    256,
)

gold_fact_songplay = (
    events
    .join(song_lookup, join_condition, "left")
    .select(
        songplay_id.alias("songplay_id"),
        F.col("e.ts").alias("time_id"),
        F.col("e.userId").cast("int").alias("user_id"),
        F.col("s.song_id"),
        F.col("s.artist_id"),
        F.col("e.level"),
        F.col("e.sessionId").alias("session_id"),
        F.col("e.location"),
        F.col("e.userAgent").alias("user_agent"),
    )
)

gold_fact_songplay.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.{USER_SCHEMA}.gold_fact_songplay"
)

assert gold_fact_songplay.count() == 6_820
print("Gold complete: four dimensions and one 6,820-row fact table")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: Analyst-facing view
# MAGIC
# MAGIC The view exposes descriptive dimension fields without copying the Gold data. Required user and time relationships use inner joins. Optional song and artist relationships use left joins.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW gold_songplay_analysis_vw AS
# MAGIC SELECT
# MAGIC   f.songplay_id,
# MAGIC   f.time_id,
# MAGIC   f.user_id,
# MAGIC   f.song_id,
# MAGIC   f.artist_id,
# MAGIC   f.level AS event_level,
# MAGIC   f.session_id,
# MAGIC   f.location AS event_location,
# MAGIC   f.user_agent,
# MAGIC   t.event_time,
# MAGIC   t.hour AS listening_hour,
# MAGIC   t.day AS day_of_month,
# MAGIC   t.week AS week_of_year,
# MAGIC   t.month AS month_number,
# MAGIC   t.year AS calendar_year,
# MAGIC   t.weekday AS day_of_week,
# MAGIC   u.first_name,
# MAGIC   u.last_name,
# MAGIC   u.gender,
# MAGIC   u.level AS current_user_level,
# MAGIC   s.title AS song_title,
# MAGIC   s.year AS song_year,
# MAGIC   s.duration AS song_duration_seconds,
# MAGIC   a.artist_name,
# MAGIC   a.artist_location,
# MAGIC   a.artist_latitude,
# MAGIC   a.artist_longitude
# MAGIC FROM gold_fact_songplay AS f
# MAGIC JOIN gold_dim_user AS u
# MAGIC   ON f.user_id = u.user_id
# MAGIC JOIN gold_dim_time AS t
# MAGIC   ON f.time_id = t.time_id
# MAGIC LEFT JOIN gold_dim_song AS s
# MAGIC   ON f.song_id = s.song_id
# MAGIC LEFT JOIN gold_dim_artist AS a
# MAGIC   ON f.artist_id = a.artist_id

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS view_rows,
# MAGIC   COUNT(DISTINCT songplay_id) AS distinct_songplays
# MAGIC FROM gold_songplay_analysis_vw

# COMMAND ----------

# MAGIC %md
# MAGIC ## Completed Code: SQL analysis

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   event_level,
# MAGIC   COUNT(*) AS listening_events,
# MAGIC   COUNT(DISTINCT user_id) AS listeners
# MAGIC FROM gold_songplay_analysis_vw
# MAGIC GROUP BY event_level
# MAGIC ORDER BY listening_events DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS total_listening_events,
# MAGIC   COUNT(song_id) AS catalog_matched_events,
# MAGIC   ROUND(100.0 * COUNT(song_id) / COUNT(*), 2) AS match_percentage
# MAGIC FROM gold_songplay_analysis_vw

# COMMAND ----------

# MAGIC %md
# MAGIC ## Example findings
# MAGIC
# MAGIC 1. Paid accounts generated 5,591 of 6,820 listening events, while free accounts generated 1,229. Paid listening represented about 82 percent of observed activity.
# MAGIC 2. Only 319 listening events, about 4.68 percent, matched the provided song catalog. This reflects the catalog's limited coverage, not failed event ingestion.
# MAGIC
# MAGIC A bar chart comparing paid and free listening events would support the first finding.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Explanation
# MAGIC
# MAGIC - The compact files remove tiny-file overhead while preserving every source record and filename.
# MAGIC - Bronze keeps the source shape and enforces its schema with SQL DDL and `COPY INTO`.
# MAGIC - Silver creates typed, normalized records and matching keys.
# MAGIC - Gold has clear dimension and fact grains.
# MAGIC - The analyst view joins all four dimensions without storing another copy of the data.
# MAGIC - The fact uses a stable hash key, so reruns produce the same identifiers.
# MAGIC - The left join keeps unmatched listening events. This is why song and artist keys may be null.
# MAGIC - No table is manually partitioned because the complete project is small.
# MAGIC
# MAGIC ## Common Mistakes
# MAGIC
# MAGIC - Running the original 14,896-file S3 read during every build
# MAGIC - Using `monotonically_increasing_id()` for a repeatable fact key
# MAGIC - Building the user dimension from only `NextSong` events
# MAGIC - Using an inner join and silently losing unmatched listening events
# MAGIC - Joining on title alone and multiplying facts
# MAGIC - Using inner joins for optional song and artist metadata in the analyst view
# MAGIC - Using `SELECT *` in the view and creating ambiguous duplicate columns
# MAGIC - Copying identical Silver tables into Gold without changing the contract
# MAGIC - Partitioning tiny tables by year, month, or artist
# MAGIC
# MAGIC ## Discussion Questions
# MAGIC
# MAGIC 1. When is pandas a reasonable ingestion helper, and when is it unsafe?
# MAGIC 2. Why are unmatched song IDs allowed but unmatched user IDs are not?
# MAGIC 3. Which table would grow fastest in a real streaming product?
# MAGIC 4. What would change if daily log files arrived after this batch?
