# Databricks notebook source
# MAGIC %md
# MAGIC # 04: Explore Wanderbricks with SQL and PySpark
# MAGIC
# MAGIC Day 2 used NYC Taxi to build your Spark foundation. Day 3 changes the business context.
# MAGIC
# MAGIC **Wanderbricks** is a simulated vacation rental platform. Its tables model users, hosts, properties, destinations, bookings, payments, reviews, support interactions, and clickstream events.
# MAGIC
# MAGIC In this notebook, you will:
# MAGIC
# MAGIC - discover an unfamiliar catalog dataset instead of assuming its shape;
# MAGIC - reason about table grain and keys;
# MAGIC - join related tables with SQL first;
# MAGIC - translate the join into PySpark;
# MAGIC - query nested clickstream data;
# MAGIC - complete an independent business analysis at the end.
# MAGIC
# MAGIC **Dataset:** `samples.wanderbricks`  
# MAGIC **Writes:** none  
# MAGIC **Setup helper needed:** no
# MAGIC
# MAGIC Source documentation: [Wanderbricks dataset](https://docs.databricks.com/aws/en/discover/wanderbricks-dataset)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: Understand the business model
# MAGIC
# MAGIC A booking platform is relational. One business event often requires several tables.
# MAGIC
# MAGIC ![Wanderbricks primary table relationships](https://docs.databricks.com/aws/en/assets/images/wanderbricks-relationships-f119f9c2b01cf599aacaaefa0da3fcb2.png)
# MAGIC
# MAGIC **Read the arrows as questions:**
# MAGIC
# MAGIC - Which user made a booking?
# MAGIC - Which property was booked?
# MAGIC - Was the booking paid?
# MAGIC - Which destination contains the property?
# MAGIC - What did the guest review after the stay?
# MAGIC
# MAGIC Before joining tables, identify the grain and key of each source.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: Discover before you query
# MAGIC
# MAGIC Sample datasets can evolve. A data engineer verifies the catalog rather than trusting memory.
# MAGIC
# MAGIC **Goal:** List the currently available Wanderbricks tables.
# MAGIC
# MAGIC **Predict:** Which command lists objects without scanning their rows?

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN samples.wanderbricks;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** `users`, `properties`, `bookings`, `payments`, `reviews`, `clickstream`, and other related tables.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.1 Inspect the two central tables
# MAGIC
# MAGIC `DESCRIBE TABLE` reveals column names and types. It is the schema equivalent of reading a table contract.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE samples.wanderbricks.bookings;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE samples.wanderbricks.payments;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Record the grains
# MAGIC
# MAGIC Based on the schemas and the relationship diagram:
# MAGIC
# MAGIC | Table | Likely grain | Key used today |
# MAGIC |---|---|---|
# MAGIC | `bookings` | one booking | `booking_id` |
# MAGIC | `payments` | one payment transaction | payment key, with `booking_id` as a foreign key |
# MAGIC | `properties` | one property listing | `property_id` |
# MAGIC | `users` | one platform user | `user_id` |
# MAGIC
# MAGIC **Important:** A booking can have more than one payment row. Joining raw bookings directly to raw payments can multiply booking rows. We will aggregate payments to booking grain before joining.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3: Build a booking-level result in SQL
# MAGIC
# MAGIC ### 3.1 Aggregate payments before the join
# MAGIC
# MAGIC **Goal:** Produce one payment summary row per booking.
# MAGIC
# MAGIC **Predict:** Why is `booking_id` the only `GROUP BY` column?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   booking_id,
# MAGIC   COUNT(*) AS payment_attempts,
# MAGIC   ROUND(SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END), 2) AS paid_amount
# MAGIC FROM samples.wanderbricks.payments
# MAGIC GROUP BY booking_id
# MAGIC ORDER BY paid_amount DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** one row per booking ID, even if the source contains multiple payment attempts.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3.2 Join at a controlled grain
# MAGIC
# MAGIC **Question:** Which bookings produced completed payment revenue, and which guest and property were involved?
# MAGIC
# MAGIC The payment subquery first creates booking grain. The outer query then joins one booking to one payment summary, one user, and one property.
# MAGIC
# MAGIC **Predict:** Why is the payment join a `LEFT JOIN` instead of an inner join?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   b.booking_id,
# MAGIC   b.check_in,
# MAGIC   b.check_out,
# MAGIC   b.status AS booking_status,
# MAGIC   u.name AS guest_name,
# MAGIC   u.country AS guest_country,
# MAGIC   p.title AS property_title,
# MAGIC   p.property_type,
# MAGIC   pay.payment_attempts,
# MAGIC   pay.paid_amount
# MAGIC FROM samples.wanderbricks.bookings AS b
# MAGIC JOIN samples.wanderbricks.users AS u
# MAGIC   ON b.user_id = u.user_id
# MAGIC JOIN samples.wanderbricks.properties AS p
# MAGIC   ON b.property_id = p.property_id
# MAGIC LEFT JOIN (
# MAGIC   SELECT
# MAGIC     booking_id,
# MAGIC     COUNT(*) AS payment_attempts,
# MAGIC     SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS paid_amount
# MAGIC   FROM samples.wanderbricks.payments
# MAGIC   GROUP BY booking_id
# MAGIC ) AS pay
# MAGIC   ON b.booking_id = pay.booking_id
# MAGIC ORDER BY b.check_in DESC
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** Booking rows remain visible even when no completed payment exists. That is useful when investigating unpaid or failed bookings.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 4: Translate the controlled join to PySpark
# MAGIC
# MAGIC Build the same grains before joining.
# MAGIC
# MAGIC | SQL | PySpark |
# MAGIC |---|---|
# MAGIC | table alias | `.alias("b")` |
# MAGIC | grouped payment subquery | `groupBy(...).agg(...)` |
# MAGIC | `JOIN ... ON` | `.join(other, condition, join_type)` |
# MAGIC | qualified column | `F.col("b.booking_id")` |
# MAGIC
# MAGIC **Before you run:** Find the point where payments change from transaction grain to booking grain.

# COMMAND ----------

from pyspark.sql import functions as F

bookings_df = spark.table("samples.wanderbricks.bookings").alias("b")
payments_df = spark.table("samples.wanderbricks.payments")
properties_df = spark.table("samples.wanderbricks.properties").alias("p")
users_df = spark.table("samples.wanderbricks.users").alias("u")

payment_summary_df = (
    payments_df
    .groupBy("booking_id")
    .agg(
        F.count("*").alias("payment_attempts"),
        F.round(
            F.sum(F.when(F.col("status") == "completed", F.col("amount")).otherwise(F.lit(0))),
            2,
        ).alias("paid_amount"),
    )
    .alias("pay")
)

booking_detail_df = (
    bookings_df
    .join(users_df, F.col("b.user_id") == F.col("u.user_id"), "inner")
    .join(properties_df, F.col("b.property_id") == F.col("p.property_id"), "inner")
    .join(payment_summary_df, F.col("b.booking_id") == F.col("pay.booking_id"), "left")
    .select(
        F.col("b.booking_id"),
        F.col("b.check_in"),
        F.col("b.check_out"),
        F.col("b.status").alias("booking_status"),
        F.col("u.name").alias("guest_name"),
        F.col("u.country").alias("guest_country"),
        F.col("p.title").alias("property_title"),
        F.col("p.property_type"),
        F.col("pay.payment_attempts"),
        F.col("pay.paid_amount"),
    )
)

display(booking_detail_df.orderBy(F.col("check_in").desc()).limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.1 Validate the grain
# MAGIC
# MAGIC Never assume a join preserved the intended grain. Test it.

# COMMAND ----------

detail_rows = booking_detail_df.count()
distinct_bookings = booking_detail_df.select("booking_id").distinct().count()

print(f"Rows: {detail_rows:,}")
print(f"Distinct bookings: {distinct_bookings:,}")
assert detail_rows == distinct_bookings, "The join multiplied booking rows."
print("Grain check passed: one row per booking.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 5: Query nested clickstream data
# MAGIC
# MAGIC Wanderbricks also contains semi-structured behavior data. The `metadata` column is nested.
# MAGIC
# MAGIC SQL uses dot notation to reach a field inside a struct.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   metadata.device AS device_type,
# MAGIC   event,
# MAGIC   COUNT(*) AS event_count
# MAGIC FROM samples.wanderbricks.clickstream
# MAGIC GROUP BY metadata.device, event
# MAGIC ORDER BY event_count DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.1 The PySpark equivalent
# MAGIC
# MAGIC `F.col("metadata.device")` follows the same nested path.

# COMMAND ----------

clickstream_df = spark.table("samples.wanderbricks.clickstream")

device_events_df = (
    clickstream_df
    .groupBy(
        F.col("metadata.device").alias("device_type"),
        F.col("event"),
    )
    .agg(F.count("*").alias("event_count"))
    .orderBy(F.col("event_count").desc())
)

display(device_events_df)

# COMMAND ----------

# MAGIC %md
# MAGIC **Why this matters:** Spark can preserve and query nested structures. You do not have to flatten every JSON-like field before asking a useful question.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 6: Your activity
# MAGIC
# MAGIC ### Scenario
# MAGIC
# MAGIC The marketplace team wants a property performance view that combines bookings, completed payments, and guest reviews. The result will help identify high-value properties with enough review evidence.
# MAGIC
# MAGIC ### Success criteria
# MAGIC
# MAGIC Your work must:
# MAGIC
# MAGIC - begin with SQL discovery;
# MAGIC - keep payment aggregation at booking grain;
# MAGIC - exclude soft-deleted reviews;
# MAGIC - build a PySpark result at property grain;
# MAGIC - validate that each property appears once;
# MAGIC - register a temporary view and finish the analysis in SQL.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Inspect reviews
# MAGIC
# MAGIC Use SQL to inspect the `reviews` schema and preview ten active reviews.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: DESCRIBE TABLE samples.wanderbricks.reviews;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: Preview 10 rows where is_deleted = false.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Build property-level measures in PySpark
# MAGIC
# MAGIC Create `property_performance_df` with one row per property and these columns:
# MAGIC
# MAGIC - `property_id`
# MAGIC - `property_title`
# MAGIC - `property_type`
# MAGIC - `booking_count`
# MAGIC - `completed_revenue`
# MAGIC - `review_count`
# MAGIC - `avg_rating`, rounded to two decimals
# MAGIC
# MAGIC Design the intermediate grains carefully:
# MAGIC
# MAGIC 1. Aggregate completed payments to one row per `booking_id`.
# MAGIC 2. Join that result to bookings, then aggregate booking measures to property grain.
# MAGIC 3. Filter active reviews, then aggregate review measures to property grain.
# MAGIC 4. Join both property-level results to properties.
# MAGIC
# MAGIC <details><summary>Hint</summary>Do not join raw payments and raw reviews in one large detail table. That can multiply rows. Aggregate each many-side table before the final property join.</details>

# COMMAND ----------

# TODO: Build property_performance_df.
property_performance_df = None

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Pass the result to SQL
# MAGIC
# MAGIC Register the DataFrame as `property_performance_python`.
# MAGIC
# MAGIC Use SQL to return the ten properties with:
# MAGIC
# MAGIC - at least 5 active reviews;
# MAGIC - positive completed revenue;
# MAGIC - highest completed revenue first.

# COMMAND ----------

# TODO: Register property_performance_python.

# COMMAND ----------

# TODO: Save the final SQL result in top_properties_df with spark.sql(...).
top_properties_df = None

# display(top_properties_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validation

# COMMAND ----------

assert property_performance_df is not None, "Task 2: property_performance_df is still None."
required_columns = {
    "property_id",
    "property_title",
    "property_type",
    "booking_count",
    "completed_revenue",
    "review_count",
    "avg_rating",
}
assert set(property_performance_df.columns) == required_columns, "Task 2: check the required columns."
assert property_performance_df.count() == property_performance_df.select("property_id").distinct().count(), (
    "Task 2: each property must appear once."
)
assert spark.catalog.tableExists("property_performance_python"), (
    "Task 3: register property_performance_python."
)
assert top_properties_df is not None, "Task 3: top_properties_df is still None."
assert top_properties_df.count() <= 10, "Task 3: return at most ten properties."
assert top_properties_df.filter(
    (F.col("review_count") < 5) | (F.col("completed_revenue") <= 0)
).limit(1).count() == 0, "Task 3: apply both business filters."

print("All checks passed. Your multi-table result preserved the intended grain.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stretch
# MAGIC
# MAGIC Join `destinations` so the final result includes a destination name. Recheck the grain after adding the join.
# MAGIC
# MAGIC ### Reflection
# MAGIC
# MAGIC Why did you aggregate payments and reviews separately before joining them to properties?
