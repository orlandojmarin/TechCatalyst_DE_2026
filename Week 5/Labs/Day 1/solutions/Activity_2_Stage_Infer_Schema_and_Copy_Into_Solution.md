# Activity 2 Solution: Stage and COPY INTO at Scale

Instructor reference. Replace `<YOUR_NAME>` with the student's schema. Copy blocks into Snowsight to verify.

```sql
-- Supply the current classroom context and integration name before running.

USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;

-- ============================================================
-- PART A: One Parquet file
-- ============================================================

CREATE OR REPLACE FILE FORMAT yellow_tripdata_parquet_ff
  TYPE = PARQUET
  USE_LOGICAL_TYPE = TRUE;

CREATE OR REPLACE STAGE yellow_tripdata_s3_stage
  URL = 's3://techcatalyst-de-2026/stages/'
  STORAGE_INTEGRATION = <INSTRUCTOR_STORAGE_INTEGRATION>
  FILE_FORMAT = (FORMAT_NAME = 'yellow_tripdata_parquet_ff');

LIST @yellow_tripdata_s3_stage;

-- Peek before designing anything (Lesson 1, section 4)
SELECT t.$1:VendorID::NUMBER      AS vendorid,
       t.$1:tpep_pickup_datetime  AS pickup_at,
       t.$1:trip_distance::FLOAT  AS trip_distance,
       t.$1:fare_amount::FLOAT    AS fare_amount
FROM @yellow_tripdata_s3_stage/yellow_tripdata_2026-01.parquet t
LIMIT 10;

-- Target table, PATH A (standard: the schema is known and stable, so explicit
-- DDL is the simplest correct form; it is the contract, in our types)
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
  airport_fee           FLOAT
);

DESCRIBE TABLE raw_yellow_tripdata_parquet;

-- Target table, PATH B (equivalent result via inference; the Lesson 1
-- convenience tool for wide, unknown, or changing schemas)
-- SELECT * FROM TABLE(INFER_SCHEMA(
--   LOCATION => '@yellow_tripdata_s3_stage/yellow_tripdata_2026-01.parquet',
--   FILE_FORMAT => 'yellow_tripdata_parquet_ff'));
--
-- CREATE OR REPLACE TRANSIENT TABLE raw_yellow_tripdata_parquet
--   USING TEMPLATE (
--     SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*)) WITHIN GROUP (ORDER BY order_id)
--     FROM TABLE(INFER_SCHEMA(
--       LOCATION => '@yellow_tripdata_s3_stage/yellow_tripdata_2026-01.parquet',
--       FILE_FORMAT => 'yellow_tripdata_parquet_ff')));

COPY INTO raw_yellow_tripdata_parquet
  FROM @yellow_tripdata_s3_stage/yellow_tripdata_2026-01.parquet
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT COUNT(*) AS trip_count
FROM raw_yellow_tripdata_parquet;

-- ============================================================
-- PART B: All Parquet files (scale up, check for duplicates)
-- ============================================================

COPY INTO raw_yellow_tripdata_parquet
  FROM @yellow_tripdata_s3_stage
  PATTERN = '.*yellow_tripdata_2026-.*\\.parquet'
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

-- The 2026-01 file is NOT reloaded because Snowflake tracks files that have already been 
-- successfully loaded into the target table.

SELECT COUNT(*) AS total_parquet_trips
FROM raw_yellow_tripdata_parquet;

-- ============================================================
-- PART C: Both CSV files
-- ============================================================

CREATE OR REPLACE FILE FORMAT yellow_tripdata_csv_ff
  TYPE = CSV
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-- Reusing the DDL to create the CSV table
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
  fare_amount            FLOAT,
  extra                  FLOAT,
  mta_tax                FLOAT,
  tip_amount             FLOAT,
  tolls_amount           FLOAT,
  improvement_surcharge  FLOAT,
  total_amount           FLOAT,
  congestion_surcharge   FLOAT,
  airport_fee            FLOAT,
  cbd_congestion_fee     FLOAT
);

COPY INTO raw_yellow_tripdata_csv
  FROM @yellow_tripdata_s3_stage
  PATTERN = '.*yellow_tripdata_2026-.*\\.csv'
  FILE_FORMAT = (FORMAT_NAME = 'yellow_tripdata_csv_ff')
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT COUNT(*) AS total_csv_trips
FROM raw_yellow_tripdata_csv;

-- ============================================================
-- PART D: Cross-format validation
-- ============================================================

-- Compare row counts (they should match exactly)
SELECT 'parquet' AS source, COUNT(*) AS row_count FROM raw_yellow_tripdata_parquet
UNION ALL
SELECT 'csv'     AS source, COUNT(*) AS row_count FROM raw_yellow_tripdata_csv;

-- Validation queries for Parquet
SELECT
  MIN(DATE(tpep_pickup_datetime)) AS first_pickup_date,
  MAX(DATE(tpep_pickup_datetime)) AS last_pickup_date
FROM raw_yellow_tripdata_parquet;

SELECT COUNT(*) AS negative_trip_distance_count
FROM raw_yellow_tripdata_parquet
WHERE trip_distance < 0;

-- Validation queries for CSV
SELECT
  MIN(DATE(tpep_pickup_datetime)) AS first_pickup_date,
  MAX(DATE(tpep_pickup_datetime)) AS last_pickup_date
FROM raw_yellow_tripdata_csv;

SELECT COUNT(*) AS negative_trip_distance_count
FROM raw_yellow_tripdata_csv
WHERE trip_distance < 0;

-- Notes on Parquet vs CSV:
-- 1. Parquet is columnar, making analytical queries that only select a few columns much faster and cheaper.
-- 2. Parquet is strongly typed and self-describing, removing the need to parse strings into timestamps or numbers, and naturally supports MATCH_BY_COLUMN_NAME without needing PARSE_HEADER workarounds.
-- 3. Parquet is highly compressed, saving storage and network transfer costs.
```
