# Databricks notebook source
# MAGIC %md
# MAGIC # Mini-Capstone: The Million Song Lakehouse
# MAGIC
# MAGIC **Team build notebook**
# MAGIC
# MAGIC Sparkify has song metadata and application logs. Your team will turn those records into a small lakehouse that analysts can trust.
# MAGIC
# MAGIC This notebook has two parts:
# MAGIC
# MAGIC 1. **Learn together:** set up the project, inspect the data with SQL, and understand the small-file problem.
# MAGIC 2. **Build together:** design and create Bronze, Silver, and Gold Delta tables.
# MAGIC
# MAGIC Keep the solution simple. Use a direct transformation when it answers the question clearly.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0. Reuse the Week 5 setup
# MAGIC
# MAGIC `00_Shared_Setup` creates your team schema and landing volume. It also gives this notebook three useful variables:
# MAGIC
# MAGIC - `CATALOG`
# MAGIC - `USER_SCHEMA`
# MAGIC - `VOLUME_PATH`
# MAGIC
# MAGIC When the widget appears, use the same team schema every member agreed on, such as `w5_team_orange`.

# COMMAND ----------

# MAGIC %run ./00_Shared_Setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Find the two source files
# MAGIC
# MAGIC You downloaded the compact course files through Chrome and uploaded them to the team `landing` volume. Databricks reads them from `/Volumes/workspace/<team_schema>/landing/`.
# MAGIC
# MAGIC Let us confirm that Databricks can see them before doing any transformation work.

# COMMAND ----------

SONGS_PATH = f"{VOLUME_PATH}/songs_compact.jsonl"
LOGS_PATH = f"{VOLUME_PATH}/logs_compact.jsonl"

available_files = {item.name for item in dbutils.fs.ls(VOLUME_PATH)}
required_files = {"songs_compact.jsonl", "logs_compact.jsonl"}
missing_files = required_files - available_files

if missing_files:
    raise FileNotFoundError(
        f"Upload these files to {VOLUME_PATH}: {sorted(missing_files)}"
    )

print("Both source files are ready.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Translate the source contract into Bronze tables
# MAGIC
# MAGIC The project README contains the data dictionary for both JSONL files. Your team must translate those column names and SQL types into explicit Delta table DDL.
# MAGIC
# MAGIC Do not use schema inference. A production-shaped pipeline should state the contract it expects.
# MAGIC
# MAGIC A few names and titles contain only digits and appear as JSON numbers. The data dictionary correctly treats them as strings because their business meaning is text.
# MAGIC
# MAGIC Use the SQL pattern you already know:
# MAGIC
# MAGIC 1. `DROP TABLE IF EXISTS` so a clean build can start again.
# MAGIC 2. `CREATE TABLE ... USING DELTA` with the source columns and types.
# MAGIC 3. `COPY INTO` the table from the matching Volume path with `FILEFORMAT = JSON`.
# MAGIC
# MAGIC The first `COPY INTO` pattern is provided. Complete the `bronze_songs` DDL, then create and load `bronze_logs` by following the same pattern. We use `spark.sql()` here so the SQL can reuse the `SONGS_PATH` and `LOGS_PATH` variables from the shared setup.

# COMMAND ----------

from pyspark.sql import functions as F

spark.sql("DROP TABLE IF EXISTS bronze_songs")
spark.sql("""
CREATE TABLE bronze_songs (
  -- TODO: translate every songs data-dictionary row into column_name SQL_TYPE
)
USING DELTA
""")

spark.sql(f"""
COPY INTO bronze_songs
FROM '{SONGS_PATH}'
FILEFORMAT = JSON
""")

# TODO: drop and create bronze_logs with its explicit SQL DDL.
# TODO: use COPY INTO to load LOGS_PATH into bronze_logs.

# COMMAND ----------

songs_source = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_songs")
logs_source = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_logs")

song_count = songs_source.count()
log_count = logs_source.count()

print(f"Songs: {song_count:,}")
print(f"Log events: {log_count:,}")

assert song_count == 14_896, f"Expected 14,896 songs, found {song_count:,}"
assert log_count == 8_056, f"Expected 8,056 log events, found {log_count:,}"

# COMMAND ----------

display(songs_source.limit(5))
display(logs_source.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Checkpoint
# MAGIC
# MAGIC You should have:
# MAGIC
# MAGIC - 14,896 song records
# MAGIC - 8,056 log records
# MAGIC - an explicit SQL DDL schema for each Bronze table
# MAGIC - the original relative filename in `_source_file`
# MAGIC - two managed Delta tables visible in Catalog Explorer
# MAGIC
# MAGIC If those checks pass, move to SQL profiling.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Start with SQL
# MAGIC
# MAGIC You already know how to ask useful data questions in SQL. Profile the Bronze tables before deciding how Silver and Gold should transform them.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   page,
# MAGIC   COUNT(*) AS event_count
# MAGIC FROM bronze_logs
# MAGIC GROUP BY page
# MAGIC ORDER BY event_count DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS eligible_listening_events,
# MAGIC   COUNT(DISTINCT userId) AS known_listeners
# MAGIC FROM bronze_logs
# MAGIC WHERE page = 'NextSong'
# MAGIC   AND userId <> ''

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   MIN(CASE WHEN year > 0 THEN year END) AS earliest_nonzero_year,
# MAGIC   MAX(year) AS latest_year,
# MAGIC   SUM(CASE WHEN year = 0 THEN 1 ELSE 0 END) AS unknown_years,
# MAGIC   COUNT(DISTINCT song_id) AS distinct_song_ids,
# MAGIC   COUNT(*) AS song_rows
# MAGIC FROM bronze_songs

# COMMAND ----------

# MAGIC %md
# MAGIC ### Your turn: add two profiling queries
# MAGIC
# MAGIC Add two SQL cells below this one:
# MAGIC
# MAGIC 1. Find the five locations with the most eligible listening events.
# MAGIC 2. Check whether any `song_id` appears more than once.
# MAGIC
# MAGIC **Expected results:** the eligible listening-event count is 6,820, and every song ID is unique.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Why the course provides compact files
# MAGIC
# MAGIC The original song source has 14,896 JSON files but only about 3.7 MB of content. A remote read must list and open every object before Spark can process its few hundred bytes.
# MAGIC
# MAGIC The compact file contains the same 14,896 rows. It removes repeated file-open overhead, not data. This lets the capstone spend time on Spark transformations, Delta Lake, SQL, dimensional modeling, validation, and teamwork.
# MAGIC
# MAGIC **Tool choice lesson:** pandas was a reasonable one-time way to collect this bounded source and create the compact course asset. It would not be the default for a dataset that cannot fit safely in one Python process.
# MAGIC
# MAGIC Do not run the original recursive S3 read as part of the graded build. Your instructor may demonstrate it separately.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Design gate
# MAGIC
# MAGIC Pause before building Silver and Gold. Complete these four items with your team:
# MAGIC
# MAGIC 1. Draw the architecture diagram required in the project README.
# MAGIC 2. Draw the Gold ERD with grains, primary keys, foreign keys, and optional relationships.
# MAGIC 3. Write the short compact-file decision record.
# MAGIC 4. Start the Gold implementation choice record.
# MAGIC
# MAGIC Add your diagram links and decision record in markdown cells below. Ask another team to review the diagrams before you continue.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Team design goes here
# MAGIC
# MAGIC **Architecture diagram:** TODO
# MAGIC
# MAGIC **Gold ERD:** TODO
# MAGIC
# MAGIC **Compact-file decision:** TODO
# MAGIC
# MAGIC **Gold implementation choice:** TODO

# COMMAND ----------

# MAGIC %md
# MAGIC # Team Build
# MAGIC
# MAGIC The guided orientation is complete. The rest of the notebook gives your team contracts, starter code, checkpoints, and hints. Your team supplies the transformation logic.
# MAGIC
# MAGIC Bronze used SQL DDL and `COPY INTO`. Silver provides a partial PySpark scaffold. The worked time dimension uses SQL. For every other Gold table, your team chooses SQL or PySpark and supplies the transformation.
# MAGIC
# MAGIC Keep one final implementation per table. The table name, columns, grain, row counts, and validation rules do not change with the language. Record at least one Gold choice and be ready to explain why it was clearer for that transformation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Silver: clean without changing the grain
# MAGIC
# MAGIC Build:
# MAGIC
# MAGIC - `silver_song_catalog`: one row per `song_id`
# MAGIC - `silver_listen_events`: one row per eligible `NextSong` event
# MAGIC
# MAGIC For the song catalog:
# MAGIC
# MAGIC - trim titles and artist names
# MAGIC - create lowercase `title_key` and `artist_key` columns for matching
# MAGIC - create `duration_key` by rounding duration to three decimal places
# MAGIC - keep the source IDs and descriptive columns
# MAGIC
# MAGIC For listening events:
# MAGIC
# MAGIC - keep only `page = 'NextSong'` and a nonempty `userId`
# MAGIC - convert `ts` from milliseconds to a timestamp named `event_time`
# MAGIC - create the same three matching keys
# MAGIC - keep user, session, level, location, and user-agent fields

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
        # TODO: add clean artist fields and artist_key
        # TODO: add year, duration, duration_key, and _source_file
    )
    .dropDuplicates(["song_id"])
)

silver_listen_events = (
    bronze_logs_df
    .filter((F.col("page") == "NextSong") & (F.trim("userId") != ""))
    .withColumn("event_time", F.timestamp_millis("ts"))
    .withColumn("song_key", F.lower(F.trim("song")))
    # TODO: add artist_key and duration_key
    # TODO: select the event columns needed by Gold
)

required_song_columns = {
    "song_id", "title", "title_key", "artist_id", "artist_name",
    "artist_key", "artist_location", "artist_latitude", "artist_longitude",
    "year", "duration", "duration_key", "_source_file",
}
required_event_columns = {
    "ts", "event_time", "userId", "level", "sessionId", "location",
    "userAgent", "song", "song_key", "artist", "artist_key", "length",
    "duration_key", "_source_file",
}

missing_song_columns = required_song_columns - set(silver_song_catalog.columns)
missing_event_columns = required_event_columns - set(silver_listen_events.columns)

assert not missing_song_columns, f"Complete the song catalog columns: {sorted(missing_song_columns)}"
assert not missing_event_columns, f"Complete the event columns: {sorted(missing_event_columns)}"

silver_song_catalog.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.{USER_SCHEMA}.silver_song_catalog"
)

# TODO: write silver_listen_events by following the silver_song_catalog pattern.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Run after your Silver write succeeds.
# MAGIC SELECT
# MAGIC   (SELECT COUNT(*) FROM silver_song_catalog) AS song_rows,
# MAGIC   (SELECT COUNT(DISTINCT song_id) FROM silver_song_catalog) AS distinct_song_ids,
# MAGIC   (SELECT COUNT(*) FROM silver_listen_events) AS listening_events

# COMMAND ----------

# MAGIC %md
# MAGIC ### Silver success criteria
# MAGIC
# MAGIC - Song rows equal distinct song IDs.
# MAGIC - `silver_listen_events` has 6,820 rows.
# MAGIC - `event_time` is a timestamp, not a string.
# MAGIC - Matching keys contain trimmed lowercase text and rounded duration.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Gold: build a small star schema
# MAGIC
# MAGIC | Table | Grain | Key |
# MAGIC |---|---|---|
# MAGIC | `gold_dim_song` | one row per song | `song_id` |
# MAGIC | `gold_dim_artist` | one row per artist | `artist_id` |
# MAGIC | `gold_dim_user` | one latest known record per user | `user_id` |
# MAGIC | `gold_dim_time` | one row per listening timestamp | `time_id` |
# MAGIC | `gold_fact_songplay` | one row per eligible listening event | `songplay_id` |
# MAGIC
# MAGIC We will build the time dimension in SQL as a worked example. For each remaining table, choose SQL or PySpark and build the required contract.
# MAGIC
# MAGIC Create one final implementation of each table. The language choice does not change the required columns, grain, keys, or validation.

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
# MAGIC ### 7A. Song and artist dimensions
# MAGIC
# MAGIC `gold_dim_song` can select directly from the clean catalog.
# MAGIC
# MAGIC An artist can appear on several songs. Group by `artist_id` and choose one deterministic value for each descriptive attribute. For this bounded dataset, `max()` is a simple reproducible rule.
# MAGIC
# MAGIC Required contracts:
# MAGIC
# MAGIC - `gold_dim_song`: `song_id`, `title`, `artist_id`, `year`, `duration`
# MAGIC - `gold_dim_artist`: `artist_id`, `artist_name`, `artist_location`, `artist_latitude`, `artist_longitude`
# MAGIC
# MAGIC Choose SQL or PySpark. Add the cells that create both managed tables below.

# COMMAND ----------

# TODO: create gold_dim_song and gold_dim_artist with SQL or PySpark.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Gold dimension checkpoint
# MAGIC
# MAGIC Run this checkpoint after both tables exist. The checkpoint verifies the interface contract without prescribing SQL or PySpark.

# COMMAND ----------

dimension_contracts = {
    "gold_dim_song": {"song_id", "title", "artist_id", "year", "duration"},
    "gold_dim_artist": {
        "artist_id", "artist_name", "artist_location",
        "artist_latitude", "artist_longitude",
    },
}

for table_name, required_columns in dimension_contracts.items():
    actual_columns = set(spark.table(f"{CATALOG}.{USER_SCHEMA}.{table_name}").columns)
    missing_columns = required_columns - actual_columns
    assert not missing_columns, f"{table_name} is missing: {sorted(missing_columns)}"

print("Song and artist dimension contracts passed.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7B. User dimension
# MAGIC
# MAGIC A user's level can change. Build the dimension from all valid Bronze log events, not only listening events.
# MAGIC
# MAGIC The required columns are:
# MAGIC
# MAGIC - `user_id` as an integer
# MAGIC - `first_name`
# MAGIC - `last_name`
# MAGIC - `gender`
# MAGIC - `level`
# MAGIC
# MAGIC The grain is one latest known record per valid user. Decide how to select that record, then create `gold_dim_user` with SQL or PySpark.
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint: selecting the latest record</summary>
# MAGIC
# MAGIC Use `row_number()` over a window partitioned by `userId` and ordered by `ts` descending. Keep row 1. Filter empty user IDs before applying the window.
# MAGIC </details>

# COMMAND ----------

# TODO: create gold_dim_user with SQL or PySpark.

# COMMAND ----------

required_user_columns = {"user_id", "first_name", "last_name", "gender", "level"}
actual_user_columns = set(
    spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_dim_user").columns
)
missing_user_columns = required_user_columns - actual_user_columns
assert not missing_user_columns, f"gold_dim_user is missing: {sorted(missing_user_columns)}"

duplicate_users = (
    spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_dim_user")
    .groupBy("user_id")
    .count()
    .filter(F.col("count") > 1)
    .count()
)
assert duplicate_users == 0, "gold_dim_user must contain one row per user"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mini lesson: build a stable fact ID
# MAGIC
# MAGIC A fact-table ID should identify the same source event after every pipeline run.
# MAGIC
# MAGIC `monotonically_increasing_id()` can create unique values during one Spark execution, but its values depend on Spark partition IDs. If Spark partitions the data differently on a later run, the same event can receive a different number.
# MAGIC
# MAGIC A deterministic hash gives the same output when its inputs are the same. This generic example creates a repeatable fingerprint from three event fields:
# MAGIC
# MAGIC ```python
# MAGIC stable_event_id = F.sha2(
# MAGIC     F.concat_ws(
# MAGIC         "||",
# MAGIC         F.coalesce(F.col("event_timestamp").cast("string"), F.lit("<null>")),
# MAGIC         F.coalesce(F.col("customer_id").cast("string"), F.lit("<null>")),
# MAGIC         F.coalesce(F.col("session_id").cast("string"), F.lit("<null>")),
# MAGIC     ),
# MAGIC     256,
# MAGIC )
# MAGIC ```
# MAGIC
# MAGIC The steps are:
# MAGIC
# MAGIC 1. Cast every input to a consistent string representation.
# MAGIC 2. Replace nulls with an explicit marker.
# MAGIC 3. Combine the fields in a fixed order with a separator.
# MAGIC 4. Apply SHA-256 to create a fixed-length hexadecimal value.
# MAGIC
# MAGIC This does not prove that the source event is unique. If two rows have the same selected fields, they receive the same hash. Your validation notebook must still check that the completed fact key is unique and not null.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7C. Songplay fact
# MAGIC
# MAGIC Build `gold_fact_songplay` from one Silver listening event. Match the optional song metadata using all three normalized keys:
# MAGIC
# MAGIC - `song_key = title_key`
# MAGIC - `artist_key = artist_key`
# MAGIC - `duration_key = duration_key`
# MAGIC
# MAGIC A left join keeps events that do not match the available song catalog.
# MAGIC
# MAGIC Create a repeatable `songplay_id` by adapting the generic SHA-256 lesson above. Use stable event fields such as timestamp, user, session, song, artist, and length. Do not use `monotonically_increasing_id()`.
# MAGIC
# MAGIC Required fact columns:
# MAGIC
# MAGIC - `songplay_id`
# MAGIC - `time_id` from `ts`
# MAGIC - `user_id`
# MAGIC - `song_id` and `artist_id`, which may be null
# MAGIC - `level`
# MAGIC - `session_id`
# MAGIC - `location`
# MAGIC - `user_agent`
# MAGIC
# MAGIC Choose SQL or PySpark and add the table-building cells below. Do not partition this small table.

# COMMAND ----------

# TODO: create gold_fact_songplay with SQL or PySpark.

# COMMAND ----------

required_fact_columns = {
    "songplay_id", "time_id", "user_id", "song_id", "artist_id",
    "level", "session_id", "location", "user_agent",
}
fact_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_fact_songplay")
missing_fact_columns = required_fact_columns - set(fact_df.columns)
assert not missing_fact_columns, f"gold_fact_songplay is missing: {sorted(missing_fact_columns)}"
assert fact_df.count() == 6_820, "Fact grain changed during the join"
assert fact_df.select("songplay_id").distinct().count() == 6_820, (
    "songplay_id must be unique"
)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Run after all Gold writes succeed.
# MAGIC SELECT
# MAGIC   COUNT(*) AS fact_rows,
# MAGIC   COUNT(song_id) AS matched_rows,
# MAGIC   ROUND(100.0 * COUNT(song_id) / COUNT(*), 2) AS match_percentage
# MAGIC FROM gold_fact_songplay

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7D. Publish the analyst-facing view
# MAGIC
# MAGIC Analysts should not have to rebuild the same star-schema joins for every question. Create a persistent SQL view named `gold_songplay_analysis_vw`.
# MAGIC
# MAGIC The view must:
# MAGIC
# MAGIC - begin with `gold_fact_songplay`
# MAGIC - join `gold_dim_user` and `gold_dim_time` with inner joins because those relationships are required
# MAGIC - join `gold_dim_song` and `gold_dim_artist` with left joins because the metadata is incomplete
# MAGIC - select and alias columns explicitly, without `SELECT *`
# MAGIC - preserve one row per eligible listening event
# MAGIC
# MAGIC Include these analyst-friendly columns:
# MAGIC
# MAGIC - fact identifiers: `songplay_id`, `time_id`, `user_id`, `song_id`, `artist_id`
# MAGIC - event context: `event_level`, `session_id`, `event_location`, `user_agent`
# MAGIC - time: `event_time`, `listening_hour`, `day_of_month`, `week_of_year`, `month_number`, `calendar_year`, `day_of_week`
# MAGIC - user: `first_name`, `last_name`, `gender`, `current_user_level`
# MAGIC - song: `song_title`, `song_year`, `song_duration_seconds`
# MAGIC - artist: `artist_name`, `artist_location`, `artist_latitude`, `artist_longitude`
# MAGIC
# MAGIC The fact's `level` describes the subscription at event time. The user dimension's `level` is the latest known value. Alias both so their meanings are clear.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: CREATE OR REPLACE VIEW gold_songplay_analysis_vw AS
# MAGIC -- Join the fact to all four dimensions using the contract above.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS view_rows,
# MAGIC   COUNT(DISTINCT songplay_id) AS distinct_songplays
# MAGIC FROM gold_songplay_analysis_vw

# COMMAND ----------

required_analysis_columns = {
    "songplay_id", "time_id", "user_id", "song_id", "artist_id",
    "event_level", "session_id", "event_location", "user_agent",
    "event_time", "listening_hour", "day_of_month", "week_of_year",
    "month_number", "calendar_year", "day_of_week", "first_name",
    "last_name", "gender", "current_user_level", "song_title",
    "song_year", "song_duration_seconds", "artist_name",
    "artist_location", "artist_latitude", "artist_longitude",
}
analysis_view_df = spark.table(
    f"{CATALOG}.{USER_SCHEMA}.gold_songplay_analysis_vw"
)
missing_analysis_columns = required_analysis_columns - set(analysis_view_df.columns)
assert not missing_analysis_columns, (
    f"gold_songplay_analysis_vw is missing: {sorted(missing_analysis_columns)}"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Analyst-view success criteria
# MAGIC
# MAGIC - `view_rows` equals 6,820.
# MAGIC - `distinct_songplays` equals 6,820.
# MAGIC - Unmatched song and artist values remain null instead of removing listening events.
# MAGIC - Every selected column has one clear business meaning.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Business questions and findings
# MAGIC
# MAGIC Answer at least two business questions with SQL. Two is the minimum, and both answers must appear as findings in the final presentation.
# MAGIC
# MAGIC Use `gold_songplay_analysis_vw` for both questions. The view already contains the required fact-to-dimension joins, so keep each analysis query direct. Save every query in this notebook.
# MAGIC
# MAGIC Keep each query direct. If one `GROUP BY` answers the question, do not add extra CTEs.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Business question 1

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Business question 2

# COMMAND ----------

# MAGIC %md
# MAGIC ### Findings for the presentation
# MAGIC
# MAGIC **Finding 1:** TODO
# MAGIC
# MAGIC **Finding 2:** TODO
# MAGIC
# MAGIC
# MAGIC Create at least one visualization that supports one of these findings.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Validate and operate
# MAGIC
# MAGIC Complete `Validate_Mini_Capstone_Starter.py`, then create a Lakeflow Job with two tasks:
# MAGIC
# MAGIC 1. this build notebook
# MAGIC 2. the validation notebook, dependent on the build
# MAGIC
# MAGIC Capture one green run. Then make one expected count wrong in the validation notebook, run the job, observe the failure, repair it, and run green again.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Final team checklist
# MAGIC
# MAGIC - [ ] Both JSONL files were uploaded to the team volume
# MAGIC - [ ] Architecture diagram and ERD reviewed by another team
# MAGIC - [ ] At least one Gold SQL or PySpark choice is recorded and ready to defend
# MAGIC - [ ] Bronze counts: 14,896 songs and 8,056 logs
# MAGIC - [ ] Silver count: 6,820 listening events
# MAGIC - [ ] Four Gold dimensions and one Gold fact table
# MAGIC - [ ] Analyst-facing view joins all four dimensions and preserves 6,820 fact rows
# MAGIC - [ ] Stable fact keys
# MAGIC - [ ] Optional song and artist relationships explained
# MAGIC - [ ] Validation notebook passes
# MAGIC - [ ] Two-task job runs green
# MAGIC - [ ] Failed validation and repaired run shown in the presentation
# MAGIC - [ ] At least two business-question SQL queries saved
# MAGIC - [ ] Both findings included in the presentation
# MAGIC - [ ] At least one visualization supports a finding
# MAGIC - [ ] Every team member can explain the complete pipeline
# MAGIC - [ ] Build and validation notebooks exported as source `.py` files
# MAGIC - [ ] Presentation, architecture diagram, and Gold ERD ready to submit
