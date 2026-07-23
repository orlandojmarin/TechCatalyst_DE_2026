# Databricks notebook source
# MAGIC %md
# MAGIC # 05: Build a Wanderbricks Medallion ETL Pipeline
# MAGIC
# MAGIC Notebook 04 explored Wanderbricks without changing it. This notebook turns sample source data into your own governed data product.
# MAGIC
# MAGIC You will learn to:
# MAGIC
# MAGIC - write and inspect files in a Unity Catalog volume;
# MAGIC - use `dbutils.fs` and SQL `read_files`;
# MAGIC - build bronze, silver, and gold Delta tables;
# MAGIC - reason about the purpose and grain of each layer;
# MAGIC - use `MERGE` for a safe, repeatable correction;
# MAGIC - validate a pipeline before calling it complete;
# MAGIC - build a second medallion path independently at the end.
# MAGIC
# MAGIC **Dataset:** `samples.wanderbricks`  
# MAGIC **Writes:** governed files and managed Delta tables in your schema  
# MAGIC **Setup helper needed:** yes

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: Reuse the shared workspace setup
# MAGIC
# MAGIC This is the same helper used in Notebook 03. It creates nothing new if your schema and volume already exist.
# MAGIC
# MAGIC `%run` is appropriate here because all write-oriented Week 5 notebooks need the same three variables. The read-only notebooks did not call it.

# COMMAND ----------

# MAGIC %run ./00_Shared_Setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: Medallion architecture is a set of data contracts
# MAGIC
# MAGIC Bronze, silver, and gold are not merely folder names.
# MAGIC
# MAGIC | Layer | Primary question | Typical grain today |
# MAGIC |---|---|---|
# MAGIC | Bronze | What arrived from the source? | one source booking row |
# MAGIC | Silver | What clean, joined business facts can teams trust? | one booking |
# MAGIC | Gold | What stable measure does a consumer need? | one check-in date |
# MAGIC
# MAGIC A strong pipeline can state the grain, keys, quality rules, and intended consumer for every output.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3: Create a file landing area
# MAGIC
# MAGIC The built-in sample is already a table. To practice file-oriented ingestion without relying on missing S3 data, we will export a bounded snapshot to your governed volume.
# MAGIC
# MAGIC SQL is excellent for querying files once they exist. PySpark is the clearer choice for this setup step because the dynamic volume path is already a Python variable and the DataFrame writer can produce JSON files directly.
# MAGIC
# MAGIC **Goal:** Create JSON source files that behave like an incoming booking batch.
# MAGIC
# MAGIC **Predict:** Is `.write` a lazy transformation or an action?

# COMMAND ----------

from pyspark.sql import functions as F

booking_batch_path = f"{VOLUME_PATH}/wanderbricks/bookings_batch"

(
    spark.table("samples.wanderbricks.bookings")
    .limit(1000)
    .write
    .mode("overwrite")
    .json(booking_batch_path)
)

print(f"Wrote a booking snapshot to {booking_batch_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** The write triggers Spark work and creates a directory containing one or more data files plus marker files.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3.1 Inspect the files with `dbutils.fs`
# MAGIC
# MAGIC `dbutils.fs.ls(path)` returns file metadata that Python can inspect or display.

# COMMAND ----------

files = dbutils.fs.ls(booking_batch_path)
display(files)

json_files = [file for file in files if file.name.endswith(".json")]
print(f"JSON data files: {len(json_files)}")
assert json_files, "Expected at least one JSON data file."

# COMMAND ----------

# MAGIC %md
# MAGIC ### `%fs` compared with `dbutils.fs`
# MAGIC
# MAGIC Both can inspect files:
# MAGIC
# MAGIC - `%fs ls /path` is convenient for a quick interactive check.
# MAGIC - `dbutils.fs.ls(path)` returns values that Python code can reuse and validate.
# MAGIC
# MAGIC Use the programmatic form when the result affects later logic.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3.2 Share the path with SQL through a widget
# MAGIC
# MAGIC A separate `%sql` cell cannot see the Python variable `booking_batch_path` directly. We place the path in a widget, then SQL reads it as `:booking_batch_path`.

# COMMAND ----------

dbutils.widgets.text("booking_batch_path", booking_batch_path, "Booking batch path")
print(dbutils.widgets.get("booking_batch_path"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM read_files(:booking_batch_path, format => 'json')
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 4: Bronze preserves source meaning
# MAGIC
# MAGIC Bronze should make the arrival queryable and auditable with minimal business rewriting.
# MAGIC
# MAGIC **Goal:** Create a managed Delta table from the JSON batch and add source metadata.
# MAGIC
# MAGIC `_metadata.file_path` records which file supplied each row. `_ingested_at` records when this pipeline processed it.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bronze_wander_bookings
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   *,
# MAGIC   _metadata.file_path AS _source_file,
# MAGIC   current_timestamp() AS _ingested_at
# MAGIC FROM read_files(:booking_batch_path, format => 'json');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS bronze_rows,
# MAGIC   COUNT(DISTINCT booking_id) AS distinct_bookings,
# MAGIC   COUNT(DISTINCT _source_file) AS source_files
# MAGIC FROM bronze_wander_bookings;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** Bronze keeps the source booking fields and adds traceability columns. It does not yet join users, properties, or payments.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 5: Silver creates a trusted booking fact
# MAGIC
# MAGIC Silver applies business rules and aligns grains.
# MAGIC
# MAGIC We need one row per booking. Payments are more detailed, so SQL aggregates completed payments to booking grain before joining.
# MAGIC
# MAGIC **Predict:** What problem would appear if we joined raw payment attempts directly to bronze bookings?

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_wander_booking_facts
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   b.booking_id,
# MAGIC   b.user_id,
# MAGIC   b.property_id,
# MAGIC   b.check_in,
# MAGIC   b.check_out,
# MAGIC   b.status AS booking_status,
# MAGIC   u.country AS guest_country,
# MAGIC   p.title AS property_title,
# MAGIC   p.property_type,
# MAGIC   COALESCE(pay.paid_amount, 0) AS paid_amount,
# MAGIC   b._ingested_at
# MAGIC FROM bronze_wander_bookings AS b
# MAGIC JOIN samples.wanderbricks.users AS u
# MAGIC   ON b.user_id = u.user_id
# MAGIC JOIN samples.wanderbricks.properties AS p
# MAGIC   ON b.property_id = p.property_id
# MAGIC LEFT JOIN (
# MAGIC   SELECT
# MAGIC     booking_id,
# MAGIC     SUM(amount) AS paid_amount
# MAGIC   FROM samples.wanderbricks.payments
# MAGIC   WHERE status = 'completed'
# MAGIC   GROUP BY booking_id
# MAGIC ) AS pay
# MAGIC   ON b.booking_id = pay.booking_id
# MAGIC WHERE b.booking_id IS NOT NULL
# MAGIC   AND b.user_id IS NOT NULL
# MAGIC   AND b.property_id IS NOT NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.1 Validate the silver contract
# MAGIC
# MAGIC The checks below test grain, required keys, and nonnegative revenue.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS rows,
# MAGIC   COUNT(DISTINCT booking_id) AS distinct_bookings,
# MAGIC   COUNT_IF(booking_id IS NULL OR user_id IS NULL OR property_id IS NULL) AS missing_keys,
# MAGIC   COUNT_IF(paid_amount < 0) AS negative_payments
# MAGIC FROM silver_wander_booking_facts;

# COMMAND ----------

silver_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.silver_wander_booking_facts")

assert silver_df.count() == silver_df.select("booking_id").distinct().count(), (
    "Silver must contain one row per booking."
)
assert silver_df.filter(
    F.col("booking_id").isNull() | F.col("user_id").isNull() | F.col("property_id").isNull()
).limit(1).count() == 0, "Silver contains a missing required key."
assert silver_df.filter(F.col("paid_amount") < 0).limit(1).count() == 0, (
    "Silver contains negative paid_amount."
)
print("Silver contract checks passed.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 6: Gold serves a specific consumer
# MAGIC
# MAGIC The finance analyst wants daily completed revenue by check-in date. Gold changes the grain from one booking to one date.
# MAGIC
# MAGIC **Goal:** Publish a small, stable table that is easy to query from SQL Editor or a dashboard.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_wander_daily_revenue
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   to_date(check_in) AS check_in_date,
# MAGIC   COUNT(*) AS booking_count,
# MAGIC   COUNT_IF(paid_amount > 0) AS paid_booking_count,
# MAGIC   ROUND(SUM(paid_amount), 2) AS completed_revenue
# MAGIC FROM silver_wander_booking_facts
# MAGIC GROUP BY to_date(check_in);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM gold_wander_daily_revenue
# MAGIC ORDER BY check_in_date;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 6.1 Reconcile silver and gold
# MAGIC
# MAGIC A pipeline is not correct merely because every cell ran. The total completed revenue should be unchanged by the aggregation.

# COMMAND ----------

silver_revenue = silver_df.agg(F.round(F.sum("paid_amount"), 2).alias("total")).first()["total"]
gold_revenue = (
    spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_wander_daily_revenue")
    .agg(F.round(F.sum("completed_revenue"), 2).alias("total"))
    .first()["total"]
)

print(f"Silver revenue: {silver_revenue}")
print(f"Gold revenue:   {gold_revenue}")
assert silver_revenue == gold_revenue, "Silver and gold revenue do not reconcile."

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 7: Apply a correction safely with `MERGE`
# MAGIC
# MAGIC A repeatable pipeline should not apply the same logical correction again and again.
# MAGIC
# MAGIC We will create a one-row correction view, then use a conditional `MERGE`. The update occurs only when the existing status differs from the requested status.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW booking_status_correction AS
# MAGIC SELECT
# MAGIC   booking_id,
# MAGIC   'review_required' AS corrected_status
# MAGIC FROM silver_wander_booking_facts
# MAGIC ORDER BY booking_id
# MAGIC LIMIT 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO silver_wander_booking_facts AS target
# MAGIC USING booking_status_correction AS source
# MAGIC ON target.booking_id = source.booking_id
# MAGIC WHEN MATCHED AND target.booking_status <> source.corrected_status
# MAGIC   THEN UPDATE SET target.booking_status = source.corrected_status;

# COMMAND ----------

# MAGIC %md
# MAGIC Rerun the `MERGE` cell once. The second run finds the same value already present, so there is no data change to apply.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY silver_wander_booking_facts;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** `MERGE` in the history and operation metrics that describe matched and updated rows.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 8: Your activity
# MAGIC
# MAGIC ### Scenario
# MAGIC
# MAGIC The guest experience team wants a reliable property review product. Build a separate bronze, silver, and gold path from Wanderbricks reviews.
# MAGIC
# MAGIC ### Success criteria
# MAGIC
# MAGIC Your pipeline must:
# MAGIC
# MAGIC - create `bronze_wander_reviews` with source fields and `_ingested_at`;
# MAGIC - create `silver_wander_reviews` with active reviews only;
# MAGIC - preserve one row per active review;
# MAGIC - create `gold_wander_property_ratings` at property grain;
# MAGIC - include property title, review count, and average rating;
# MAGIC - include only properties with at least 5 active reviews;
# MAGIC - pass the validation cell.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Bronze reviews
# MAGIC
# MAGIC Create or replace a managed Delta table from `samples.wanderbricks.reviews`. Keep every source column and add `_ingested_at`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Create bronze_wander_reviews.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Silver active reviews
# MAGIC
# MAGIC Create `silver_wander_reviews` from bronze. Keep only `is_deleted = false`, require non-null `user_id` and `property_id`, and keep the review identifier and rating columns needed to test uniqueness.
# MAGIC
# MAGIC Before writing the `SELECT`, inspect the bronze schema and identify the review key.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Inspect bronze_wander_reviews, then create silver_wander_reviews.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Gold property ratings
# MAGIC
# MAGIC Join silver reviews to `samples.wanderbricks.properties`. Create:
# MAGIC
# MAGIC - `property_id`
# MAGIC - `property_title`
# MAGIC - `property_type`
# MAGIC - `review_count`
# MAGIC - `avg_rating`, rounded to two decimals
# MAGIC
# MAGIC Keep only properties with at least 5 active reviews.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Create gold_wander_property_ratings.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validation
# MAGIC
# MAGIC Set `REVIEW_KEY` to the review identifier you discovered in the schema. The validation intentionally asks you to use discovered metadata instead of assuming a key name.

# COMMAND ----------

REVIEW_KEY = "TODO"

for activity_table in [
    "bronze_wander_reviews",
    "silver_wander_reviews",
    "gold_wander_property_ratings",
]:
    full_name = f"{CATALOG}.{USER_SCHEMA}.{activity_table}"
    assert spark.catalog.tableExists(full_name), f"Missing activity table: {full_name}"

bronze_reviews_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.bronze_wander_reviews")
silver_reviews_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.silver_wander_reviews")
gold_ratings_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_wander_property_ratings")

assert REVIEW_KEY in bronze_reviews_df.columns, "Set REVIEW_KEY to the review identifier from the schema."
assert silver_reviews_df.filter(F.col("is_deleted") != F.lit(False)).limit(1).count() == 0, (
    "Silver must contain active reviews only."
)
assert silver_reviews_df.count() == silver_reviews_df.select(REVIEW_KEY).distinct().count(), (
    "Silver must contain one row per active review."
)
assert gold_ratings_df.count() == gold_ratings_df.select("property_id").distinct().count(), (
    "Gold must contain one row per property."
)
assert gold_ratings_df.filter(F.col("review_count") < 5).limit(1).count() == 0, (
    "Gold must keep properties with at least 5 reviews."
)
assert {"property_id", "property_title", "property_type", "review_count", "avg_rating"} == set(
    gold_ratings_df.columns
), "Gold columns do not match the contract."

print("All checks passed. Your review medallion pipeline is complete.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stretch
# MAGIC
# MAGIC Add a rating band to the gold table, then inspect its Delta history after replacing the table.
# MAGIC
# MAGIC ### Reflection
# MAGIC
# MAGIC State the grain and primary consumer of each table you created.
