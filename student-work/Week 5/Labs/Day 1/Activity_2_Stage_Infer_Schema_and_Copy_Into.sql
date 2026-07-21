-- ============================================================
-- Activity 2: Stage, Infer Schema, and Load at Scale
-- Week 5, Day 1
-- Schema: TECHCATALYST.ORLANDO
-- ============================================================

-- Context block (run first)
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.ORLANDO;

-- ============================================================
-- PART A: One Parquet file (the careful start)
-- ============================================================

-- Step 1: Create Parquet file format
CREATE OR REPLACE FILE FORMAT yellow_tripdata_parquet_orlando
  TYPE = 'PARQUET'
  USE_LOGICAL_TYPE = TRUE;

-- Step 2: Create named external stage pointing at s3://techcatalyst-de-2026/stages/
CREATE OR REPLACE STAGE yellow_tripdata_s3_stage_orlando
  STORAGE_INTEGRATION = s3_int
  URL = 's3://techcatalyst-de-2026/stages/';

-- Step 3: LIST the stage - confirm all 4 taxi files are visible
LIST @yellow_tripdata_s3_stage_orlando;

-- Step 4: Peek at the Parquet file (direct SELECT from stage)
SELECT $1:VendorID::NUMBER          AS vendorid,
       $1:tpep_pickup_datetime      AS pickup_datetime,
       $1:trip_distance::FLOAT      AS trip_distance,
       $1:total_amount::FLOAT       AS total_amount
FROM @yellow_tripdata_s3_stage_orlando/yellow_tripdata_2026-01.parquet
     (FILE_FORMAT => 'yellow_tripdata_parquet_orlando')
LIMIT 10;

-- Step 5: Create the Parquet target table (using provided DDL - schema is known and stable)
CREATE OR REPLACE TRANSIENT TABLE raw_yellow_tripdata_parquet (
  vendorid              NUMBER,
  tpep_pickup_datetime  TIMESTAMP_NTZ,
  tpep_dropoff_datetime TIMESTAMP_NTZ,
  passenger_count       NUMBER,
  trip_distance         FLOAT,
  ratecodeid            NUMBER,
  store_and_fwd_flag    STRING,
  pulocationid          NUMBER,
  dolocationid          NUMBER,
  payment_type          NUMBER,
  fare_amount           FLOAT,
  extra                 FLOAT,
  mta_tax               FLOAT,
  tip_amount            FLOAT,
  tolls_amount          FLOAT,
  improvement_surcharge FLOAT,
  total_amount          FLOAT,
  congestion_surcharge  FLOAT,
  airport_fee           FLOAT,
  cbd_congestion_fee    FLOAT
);

DESCRIBE TABLE raw_yellow_tripdata_parquet;

-- Step 6: COPY INTO from only the January Parquet file
COPY INTO raw_yellow_tripdata_parquet
FROM @yellow_tripdata_s3_stage_orlando
FILES = ('yellow_tripdata_2026-01.parquet')
FILE_FORMAT = 'yellow_tripdata_parquet_orlando'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

-- Step 7: Validate - expect 3,724,889 rows
SELECT COUNT(*) FROM raw_yellow_tripdata_parquet;

-- ============================================================
-- PART B: All Parquet files (scale up, check for duplicates)
-- ============================================================

-- Step 8: "before" count (3,724,889 from Part A)
SELECT COUNT(*) AS before_count FROM raw_yellow_tripdata_parquet;

-- Step 9: COPY INTO using PATTERN (loads all matching Parquet files)
COPY INTO raw_yellow_tripdata_parquet
FROM @yellow_tripdata_s3_stage_orlando
PATTERN = '.*yellow_tripdata_2026-.*\.parquet'
FILE_FORMAT = 'yellow_tripdata_parquet_orlando'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
-- Only 2026-02 loads here. Snowflake's load metadata skips 2026-01
-- because it was already loaded in Step 6 (idempotency).

-- Step 10: "after" count - expect 7,232,642 rows
SELECT COUNT(*) AS after_count FROM raw_yellow_tripdata_parquet;

-- ============================================================
-- PART C: Both CSV files
-- ============================================================

-- Step 12: Create CSV file format
CREATE OR REPLACE FILE FORMAT yellow_tripdata_csv_orlando
  TYPE = 'CSV'
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE;

-- Step 13: Create the CSV target table (same columns as Parquet table)
CREATE OR REPLACE TRANSIENT TABLE raw_yellow_tripdata_csv (
  vendorid              NUMBER,
  tpep_pickup_datetime  TIMESTAMP_NTZ,
  tpep_dropoff_datetime TIMESTAMP_NTZ,
  passenger_count       NUMBER,
  trip_distance         FLOAT,
  ratecodeid            NUMBER,
  store_and_fwd_flag    STRING,
  pulocationid          NUMBER,
  dolocationid          NUMBER,
  payment_type          NUMBER,
  fare_amount           FLOAT,
  extra                 FLOAT,
  mta_tax               FLOAT,
  tip_amount            FLOAT,
  tolls_amount          FLOAT,
  improvement_surcharge FLOAT,
  total_amount          FLOAT,
  congestion_surcharge  FLOAT,
  airport_fee           FLOAT,
  cbd_congestion_fee    FLOAT
);

-- Step 14: COPY INTO using PATTERN (loads both CSV files at once)
COPY INTO raw_yellow_tripdata_csv
FROM @yellow_tripdata_s3_stage_orlando
PATTERN = '.*yellow_tripdata_2026-.*\.csv'
FILE_FORMAT = 'yellow_tripdata_csv_orlando'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

-- Step 15: Validate - expect 7,232,642 rows
-- Answer: 7,124,755
SELECT COUNT(*) FROM raw_yellow_tripdata_csv;

-- ============================================================
-- PART D: Cross-format validation
-- ============================================================

-- Step 16: Compare totals (should match exactly)
-- Answer: both have 7,124,755 rows
SELECT 'parquet' AS source, COUNT(*) AS row_count FROM raw_yellow_tripdata_parquet
UNION ALL
SELECT 'csv'     AS source, COUNT(*) AS row_count FROM raw_yellow_tripdata_csv;

-- Step 17a: Date range for Parquet table
-- Earliest pickup: 2025-12-31
-- Latest pickup: 2026-03-01
SELECT MIN(tpep_pickup_datetime) AS earliest_pickup,
       MAX(tpep_pickup_datetime) AS latest_pickup
FROM raw_yellow_tripdata_parquet;

-- Step 17a: Date range for CSV table
-- Earliest pickup: 2025-12-31
-- Latest pickup: 2026-03-01
SELECT MIN(tpep_pickup_datetime) AS earliest_pickup,
       MAX(tpep_pickup_datetime) AS latest_pickup
FROM raw_yellow_tripdata_csv;

-- Step 17b: Negative trip distances - Parquet
-- Answer: 0
SELECT COUNT(*) AS negative_distance_count
FROM raw_yellow_tripdata_parquet
WHERE trip_distance < 0;

-- Step 17b: Negative trip distances - CSV
-- Answer: 0
SELECT COUNT(*) AS negative_distance_count
FROM raw_yellow_tripdata_csv
WHERE trip_distance < 0;

-- Step 18: Parquet vs CSV for production
-- 1. Parquet is columnar and compressed (smaller files, faster loads).
-- 2. Parquet is self-describing (embeds column names and types),
--    so a column reorder upstream won't silently scramble data.
