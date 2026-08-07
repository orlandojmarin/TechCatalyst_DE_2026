-- Loading the raw taxi files from S3 into Snowflake.
--
-- This is the Pattern A ingestion path and the fastest way to get 30 million
-- rows into Snowflake. Adapt the names and paths to your team's setup.
--
-- Run this in a Snowflake worksheet or through the Python connector.

-- ---------------------------------------------------------------------------
-- 1. Set up your context
-- ---------------------------------------------------------------------------

CREATE DATABASE IF NOT EXISTS TECHCATALYST;
CREATE SCHEMA IF NOT EXISTS TECHCATALYST.BRONZE;

USE DATABASE TECHCATALYST;
USE SCHEMA BRONZE;

-- ---------------------------------------------------------------------------
-- 2. File format and stage
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FILE FORMAT parquet_ff
  TYPE = PARQUET;

-- Your instructor will provide the credentials for the capstone bucket.
CREATE OR REPLACE STAGE capstone_raw_stage
  URL = 's3://techcatalyst-de-2026/raw/'
  CREDENTIALS = (AWS_KEY_ID = '<provided>' AWS_SECRET_KEY = '<provided>')
  FILE_FORMAT = parquet_ff;

-- Always look before you load.
LIST @capstone_raw_stage/yellow_taxi/;

-- ---------------------------------------------------------------------------
-- 3. Inspect the schema before you trust it
-- ---------------------------------------------------------------------------

-- Do this for a 2025 file AND a 2026 file. Compare the results.
-- Do not assume ten files per fleet share a schema because they share a naming pattern.

SELECT *
FROM TABLE(
  INFER_SCHEMA(
    LOCATION => '@capstone_raw_stage/yellow_taxi/',
    FILE_FORMAT => 'parquet_ff'
  )
);

-- ---------------------------------------------------------------------------
-- 4. Create the bronze table from the inferred schema
-- ---------------------------------------------------------------------------

CREATE OR REPLACE TABLE yellow_raw
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
      INFER_SCHEMA(
        LOCATION => '@capstone_raw_stage/yellow_taxi/',
        FILE_FORMAT => 'parquet_ff'
      )
    )
  );

-- ---------------------------------------------------------------------------
-- 5. Load
-- ---------------------------------------------------------------------------

-- MATCH_BY_COLUMN_NAME handles Parquet column mapping for you.
-- Loading the whole prefix at once lets Snowflake parallelize across files.

COPY INTO yellow_raw
FROM @capstone_raw_stage/yellow_taxi/
FILE_FORMAT = (FORMAT_NAME = parquet_ff)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

-- Repeat for green_taxi into its own bronze table.
-- Green has different timestamp column names, so it needs its own table here.
-- You reconcile the two in your silver layer, not at load time.

-- ---------------------------------------------------------------------------
-- 6. Verify. Do not skip this.
-- ---------------------------------------------------------------------------

-- What did COPY INTO actually do, file by file?
SELECT
    file_name,
    status,
    row_count,
    row_parsed,
    first_error_message
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'YELLOW_RAW',
    START_TIME => DATEADD(hours, -1, CURRENT_TIMESTAMP())
))
ORDER BY file_name;

-- ON_ERROR = 'CONTINUE' skips bad rows silently. If you used it, you MUST
-- check how many rows were skipped and account for them in your data quality
-- report. A load that "worked" while dropping 2 percent of your data is a
-- load that lied to you.

SELECT COUNT(*) AS loaded_rows FROM yellow_raw;

-- Reconcile this against the row counts in the source files.
-- If they do not match, find out why before you build anything on top.
