---
title: "Lesson 3: Advanced Loading, Views, and Security"
module: "Week 5 Day 1"
type: explainer
audience: "Data Engineering Students"
---

# Lesson 3: Advanced Loading, Views, and Security

## Why This Matters

You already know how to load files manually and write standard SQL views. However, in a production data platform, data rarely arrives on a predictable schedule, queries get too expensive to run on the fly, and sensitive data (like PII) must be strictly controlled.

This lesson introduces the tools Snowflake provides to solve these enterprise-scale problems: automated loading (Snowpipe), performance views (Materialized Views), and governance (Secure Views, Row-Level Security, and Dynamic Data Masking).

## 1. Batch vs. Continuous Loading: COPY INTO vs. Snowpipe

So far, you have used `COPY INTO <table> FROM @stage` to load files. This is the foundation of data ingestion, but it is fundamentally a **batch** operation. 

### When to use COPY INTO
- Your data arrives on a schedule (e.g., a nightly dump of 500 GB of CSVs).
- You want to orchestrate the load yourself (using tools like dbt, Airflow, or cron jobs).
- You are doing a one-off historical backfill.
- **Compute Model:** You pay for the active time of the virtual warehouse you use to run the command.

### When to use Snowpipe
- Your data trickles in continuously (e.g., web logs arriving every minute).
- You want the data available to analysts as soon as it lands in S3, without waiting for a nightly batch.
- **How it Works:** Snowpipe listens to a cloud event queue (like AWS SQS). As soon as a file lands in the bucket, the event triggers Snowpipe, which wakes up and ingests the file immediately.
- **Compute Model:** It is "serverless." You do not assign a warehouse to Snowpipe. Snowflake provisions the compute in the background and you are billed per second of actual compute time used.

> [!TIP]
> Think of `COPY INTO` as a cargo ship: efficient for moving massive amounts of cargo at once, but you have to schedule its departure. Think of Snowpipe as a conveyor belt: moving small items instantly as soon as they are placed on the belt.

---

## 2. The View Hierarchy

A standard View is simply a saved query. It takes up no storage space, but every time you query it, Snowflake must run the underlying SQL on the raw data. Snowflake offers two advanced view types to solve specific problems.

### Materialized Views
If your view performs a massive aggregation (like summing billions of taxi trips by month) and analysts query it 1,000 times a day, computing that sum 1,000 times is a waste of money and time. 

A **Materialized View** pre-computes the results and stores them on disk. 
- **The Trade-off:** Queries against it are blazingly fast. However, Snowflake uses background compute (which costs credits) to keep the materialized view up to date whenever the underlying table changes.
- **When to use:** Use only for heavy, frequently queried aggregations on tables that do not change constantly.

```sql
-- Creating a Materialized View
CREATE OR REPLACE MATERIALIZED VIEW taxi_monthly_summary AS
SELECT 
    DATE_TRUNC('month', tpep_pickup_datetime) AS pickup_month,
    SUM(fare_amount) AS total_revenue
FROM raw_yellow_tripdata;
```

### Secure Views
A standard view hides the *data* it filters out, but it does not hide its *definition*. Anyone who can query a standard view can run `GET_DDL()` and see the exact logic you used. Worse, a clever user can sometimes write a `WHERE` clause that tricks the Snowflake query optimizer into exposing underlying data.

A **Secure View** forces Snowflake to evaluate the authorization filters *before* any user-provided filters, and completely hides the view's DDL from unauthorized users.
- **When to use:** Whenever a view is specifically designed for data privacy (e.g., exposing only a specific tenant's data to them).

```sql
-- Creating a Secure View
CREATE OR REPLACE SECURE VIEW v_tenant_a_data AS
SELECT * FROM raw_yellow_tripdata 
WHERE tenant_id = 'A';
```

---

## 3. Row-Level Security (Row Access Policies)

Instead of building 50 different secure views for 50 different regions, Snowflake allows you to attach a **Row Access Policy** directly to a table.

A Row Access Policy acts as a bouncer for your table: before returning a row, it checks who is asking (using `CURRENT_ROLE()`) and evaluates a rule to decide if they are allowed to see it.

### Example: Regional Filtering
Imagine a single `EMPLOYEES` table. We want regional managers to only see employees in their region, while the `HR_GLOBAL` role can see everyone.

```sql
-- 1. Create the policy
CREATE OR REPLACE ROW ACCESS POLICY region_policy AS (user_region VARCHAR) RETURNS BOOLEAN ->
  CURRENT_ROLE() = 'HR_GLOBAL' 
  OR 
  user_region = (SELECT region FROM user_region_mapping WHERE role = CURRENT_ROLE());

-- 2. Attach it to the table
ALTER TABLE employees 
ADD ROW ACCESS POLICY region_policy ON (region);
```
Once attached, analysts just run `SELECT * FROM employees;`. Snowflake handles the filtering silently in the background based on their role.

---

## 4. Column-Level Security (Dynamic Data Masking)

Sometimes a user is allowed to see a row, but they should not see highly sensitive *columns* within that row, like a Social Security Number (SSN) or a personal email address.

A **Masking Policy** obfuscates the data at query time without actually altering the raw data on disk.

### Example: Masking SSNs
We want the `HR_ADMIN` role to see the full SSN, but all other roles should only see the last 4 digits (e.g., `***-**-1234`).

```sql
-- 1. Create the masking policy
CREATE OR REPLACE MASKING POLICY ssn_mask AS (val VARCHAR) RETURNS VARCHAR ->
  CASE
    WHEN CURRENT_ROLE() IN ('HR_ADMIN') THEN val
    ELSE '***-**-' || RIGHT(val, 4)
  END;

-- 2. Attach it to the column
ALTER TABLE employees 
MODIFY COLUMN ssn SET MASKING POLICY ssn_mask;
```

If an analyst (who is not an `HR_ADMIN`) runs `SELECT name, ssn FROM employees`, the table will return:
| NAME | SSN |
|---|---|
| Alice | ***-**-8492 |
| Bob | ***-**-1132 |

## Key Takeaways

1. Use **COPY INTO** for scheduled batches, and **Snowpipe** for continuous, event-driven streaming.
2. Use **Materialized Views** to trade storage/maintenance costs for blazing fast query performance on heavy aggregations.
3. Use **Secure Views** to hide logic and enforce hard security boundaries.
4. Use **Row Access Policies** and **Masking Policies** to centralize your security logic directly on the table, rather than sprawling out dozens of overlapping views.
