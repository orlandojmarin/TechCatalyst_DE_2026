-- ============================================================
-- Activity 3: From RAW to CLEAN to FINAL
-- Week 5, Day 1
-- Schema: TECHCATALYST.ORLANDO
-- ============================================================

-- Context block (run first)
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.ORLANDO;

-- Setup: Confirm RAW table from Activity 2 is intact
DESCRIBE TABLE raw_yellow_tripdata_parquet;
SELECT COUNT(*) FROM raw_yellow_tripdata_parquet;

-- ============================================================
-- TASK 1: Build CLEAN
-- ============================================================

-- One CTAS that selects, types, derives, consolidates, and filters
CREATE OR REPLACE TRANSIENT TABLE clean_yellow_taxi AS
SELECT
    -- 1. VendorID cast to INT
    vendorid::INT                                           AS vendorid,

    -- 2. Timestamps renamed
    tpep_pickup_datetime                                    AS pickup_at,
    tpep_dropoff_datetime                                   AS dropoff_at,

    -- 3. Passenger count: cast to INT, NULL becomes 1
    COALESCE(passenger_count, 1)::INT                       AS passenger_count,

    -- 4. Distance and location IDs
    trip_distance,
    pulocationid::INT                                       AS pulocationid,
    dolocationid::INT                                       AS dolocationid,
    payment_type::INT                                       AS payment_type,

    -- 5. Date features derived from pickup
    tpep_pickup_datetime::DATE                              AS pickup_date,
    HOUR(tpep_pickup_datetime)                              AS pickup_hour,
    DAYNAME(tpep_pickup_datetime)                           AS pickup_dow,
    DAYNAME(tpep_pickup_datetime) IN ('Sat', 'Sun')         AS is_weekend,

    -- 6. Trip duration in minutes
    TIMESTAMPDIFF(MINUTE, tpep_pickup_datetime, tpep_dropoff_datetime) AS trip_minutes,

    -- 7. Fare and tip as-is
    fare_amount,
    tip_amount,

    -- 8. Consolidated surcharges (COALESCE each to 0 to avoid NULL poisoning)
    COALESCE(extra, 0)
      + COALESCE(mta_tax, 0)
      + COALESCE(improvement_surcharge, 0)
      + COALESCE(congestion_surcharge, 0)
      + COALESCE(airport_fee, 0)
      + COALESCE(cbd_congestion_fee, 0)                     AS total_surcharges,

    -- 9. Total amount kept for reconciliation
    total_amount

FROM raw_yellow_tripdata_parquet

-- 10. Physics filters: only keep valid trips
WHERE trip_distance > 0
  AND TIMESTAMPDIFF(MINUTE, tpep_pickup_datetime, tpep_dropoff_datetime) > 0;

-- ============================================================
-- TASK 1 CHECKPOINTS
-- ============================================================

-- Checkpoint 1: CLEAN should be smaller than RAW
-- Raw rows: 7,124,755
-- Clean rows: 6,777,859
SELECT
  (SELECT COUNT(*) FROM raw_yellow_tripdata_parquet) AS raw_rows,
  (SELECT COUNT(*) FROM clean_yellow_taxi)           AS clean_rows;

-- Checkpoint 2: Zero violations (must return 0)
-- Violations: 0
SELECT COUNT(*) AS violations
FROM clean_yellow_taxi
WHERE trip_distance <= 0 OR trip_minutes <= 0 OR passenger_count IS NULL;

-- ============================================================
-- TASK 2: Build FINAL
-- ============================================================

-- One CTAS: daily summary, one row per pickup_date
CREATE OR REPLACE TRANSIENT TABLE daily_taxi_summary AS
SELECT
    pickup_date,
    COUNT(*)                                                AS total_trips,
    ROUND(SUM(total_amount), 2)                             AS total_revenue,
    ROUND(AVG(fare_amount), 2)                              AS avg_fare,
    ROUND(AVG(CASE WHEN fare_amount > 0
              THEN tip_amount / fare_amount END) * 100, 1)  AS avg_tip_pct,
    COUNT_IF(is_weekend)                                    AS weekend_trips
FROM clean_yellow_taxi
GROUP BY pickup_date
ORDER BY pickup_date;

-- ============================================================
-- TASK 2 CHECKPOINTS
-- ============================================================

-- Checkpoint 1: Roughly one row per day
-- Days: 61
SELECT COUNT(*) AS days FROM daily_taxi_summary;

-- Checkpoint 2: FINAL reconciles with CLEAN exactly
-- From final: 6,777,859
-- From clean: 6,777,859
SELECT
  (SELECT SUM(total_trips) FROM daily_taxi_summary) AS from_final,
  (SELECT COUNT(*)         FROM clean_yellow_taxi)  AS from_clean;

-- Checkpoint 3: The dashboard question - top 3 revenue days
-- January 30, 2026
-- January 29, 2026
-- February 7, 2026
SELECT * FROM daily_taxi_summary ORDER BY total_revenue DESC LIMIT 3;

-- ============================================================
-- TASK 3: Close the loop
-- ============================================================

-- Q1: A teammate finds a bug in total_surcharges logic next week.
--     What do you rebuild, and what do you not re-download?
-- Answer: Rebuild CLEAN and FINAL. No need to re-download or touch RAW.

-- Q2: Why is dropping columns in CLEAN safe, and what would make it unsafe?
-- Answer: Safe because RAW still has everything. Unsafe if someone deleted RAW.

-- Q3: daily_taxi_summary disagrees with CLEAN's count someday. Which is wrong?
-- Answer: FINAL is wrong. CLEAN is its source, so the aggregation has a bug.

-- Q4: You built RAW to CLEAN to FINAL with three CTAS statements.
--     What breaks when the pipeline needs to run every morning without you?
-- Answer: Nothing runs automatically. You need a scheduler (tasks, dbt, Airflow)
--     to handle timing, dependencies, and failures.
