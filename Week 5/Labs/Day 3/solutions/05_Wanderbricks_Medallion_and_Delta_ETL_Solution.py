# Databricks notebook source
# MAGIC %md
# MAGIC # Solution: 05 Wanderbricks Medallion and Delta ETL

# COMMAND ----------

# MAGIC %run ./00_Shared_Setup

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bronze_wander_reviews
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT *, current_timestamp() AS _ingested_at
# MAGIC FROM samples.wanderbricks.reviews;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_wander_reviews
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   review_id,
# MAGIC   user_id,
# MAGIC   property_id,
# MAGIC   rating,
# MAGIC   comment,
# MAGIC   is_deleted,
# MAGIC   _ingested_at
# MAGIC FROM bronze_wander_reviews
# MAGIC WHERE is_deleted = false
# MAGIC   AND user_id IS NOT NULL
# MAGIC   AND property_id IS NOT NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_wander_property_ratings
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC   p.property_id,
# MAGIC   p.title AS property_title,
# MAGIC   p.property_type,
# MAGIC   COUNT(r.review_id) AS review_count,
# MAGIC   ROUND(AVG(r.rating), 2) AS avg_rating
# MAGIC FROM silver_wander_reviews AS r
# MAGIC JOIN samples.wanderbricks.properties AS p
# MAGIC   ON r.property_id = p.property_id
# MAGIC GROUP BY p.property_id, p.title, p.property_type
# MAGIC HAVING COUNT(r.review_id) >= 5;

# COMMAND ----------

from pyspark.sql import functions as F

REVIEW_KEY = "review_id"
silver_reviews_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.silver_wander_reviews")
gold_ratings_df = spark.table(f"{CATALOG}.{USER_SCHEMA}.gold_wander_property_ratings")

assert silver_reviews_df.count() == silver_reviews_df.select(REVIEW_KEY).distinct().count()
assert silver_reviews_df.filter(F.col("is_deleted") != F.lit(False)).limit(1).count() == 0
assert gold_ratings_df.count() == gold_ratings_df.select("property_id").distinct().count()
assert gold_ratings_df.filter(F.col("review_count") < 5).limit(1).count() == 0
display(gold_ratings_df.orderBy(F.col("avg_rating").desc()))
print("Solution checks passed.")
