-- ============================================================
-- Lesson 1: Stages and Loading
-- Week 5, Day 1
-- Schema: TECHCATALYST.ORLANDO
-- ============================================================

-- Section 1: The cast of characters
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.ORLANDO;

DESCRIBE STORAGE INTEGRATION s3_int;
SHOW STAGES IN SCHEMA TECHCATALYST.EXTERNAL_STAGE;
DESCRIBE STAGE TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE;

-- Section 2: Look before you load
LIST @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/;

-- Section 3: File formats (parsing contracts)
USE SCHEMA TECHCATALYST.ORLANDO;

CREATE OR REPLACE FILE FORMAT weather_csv_orlando
  TYPE = 'CSV'
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  SKIP_HEADER = 1;

CREATE OR REPLACE FILE FORMAT weather_json_orlando
  TYPE = 'JSON';

CREATE OR REPLACE FILE FORMAT weather_parquet_orlando
  TYPE = 'PARQUET';

-- Section 4: SELECT straight from the stage (peek without loading)

-- CSV (columns by position)
SELECT $1, $2, $3, $4, $5
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.csv
     (FILE_FORMAT => 'weather_csv_orlando')
LIMIT 10;

-- Parquet (columns by name)
SELECT t.$1:STATION::STRING AS station,
       t.$1:DATE::STRING    AS obs_date,
       t.$1:TMAX::STRING    AS tmax
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.parquet
     (FILE_FORMAT => 'weather_parquet_orlando') t
LIMIT 10;

-- JSON (columns by path)
SELECT $1                          AS whole_document,
       $1:STATION::STRING          AS station,
       $1:TMAX::STRING             AS tmax
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.json
     (FILE_FORMAT => 'weather_json_orlando')
LIMIT 10;

-- Section 5: Loading path A - DDL then COPY INTO (the standard)

CREATE OR REPLACE TABLE weather_raw_csv (
  station STRING,
  obs_date STRING,
  tmax STRING,
  tmin STRING,
  prcp STRING
);

COPY INTO weather_raw_csv
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.csv')
FILE_FORMAT = 'weather_csv_orlando';

SELECT COUNT(*) FROM weather_raw_csv;
SELECT * FROM weather_raw_csv LIMIT 10;

-- Section 6: The surprise - run the COPY again (idempotency)

COPY INTO weather_raw_csv
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.csv')
FILE_FORMAT = 'weather_csv_orlando';
-- Result: 0 files processed

SELECT COUNT(*) FROM weather_raw_csv;
-- Still 20 rows. Snowflake remembers what it already loaded.

-- Now with FORCE = TRUE (demonstrates the danger of overriding)
COPY INTO weather_raw_csv
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.csv')
FILE_FORMAT = 'weather_csv_orlando'
FORCE = TRUE;

SELECT COUNT(*) FROM weather_raw_csv;
-- 40 rows now. Every row is duplicated.

-- Reset: recreate the table and reload cleanly
CREATE OR REPLACE TABLE weather_raw_csv (
  station STRING,
  obs_date STRING,
  tmax STRING,
  tmin STRING,
  prcp STRING
);

COPY INTO weather_raw_csv
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.csv')
FILE_FORMAT = 'weather_csv_orlando';

SELECT COUNT(*) FROM weather_raw_csv;
-- Back to 20

-- Section 7: Loading path B - CTAS (query becomes a table)

CREATE OR REPLACE TABLE weather_raw_parquet AS
SELECT t.$1:STATION::STRING AS station,
       t.$1:DATE::STRING    AS obs_date,
       t.$1:TMAX::STRING    AS tmax,
       t.$1:TMIN::STRING    AS tmin,
       t.$1:PRCP::STRING    AS prcp
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.parquet
     (FILE_FORMAT => 'weather_parquet_orlando') t;

SELECT COUNT(*) FROM weather_raw_parquet;
-- 20

-- Section 8: Loading path C - INFER_SCHEMA (when you don't know the columns)

-- Step 1: See what Snowflake detects
SELECT *
FROM TABLE(INFER_SCHEMA(
  LOCATION => '@TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.parquet',
  FILE_FORMAT => 'weather_parquet_orlando'
));

-- Step 2: Create a table from the inferred schema
CREATE OR REPLACE TABLE weather_inferred
USING TEMPLATE (
  SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
  FROM TABLE(INFER_SCHEMA(
    LOCATION => '@TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.parquet',
    FILE_FORMAT => 'weather_parquet_orlando'
  ))
);

DESCRIBE TABLE weather_inferred;

-- Step 3: Load by column name (not position)
COPY INTO weather_inferred
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.parquet')
FILE_FORMAT = 'weather_parquet_orlando'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT COUNT(*) FROM weather_inferred;
-- 20

-- ============================================================
-- Cleanup (drop tables, keep file formats for later activities)
-- ============================================================
DROP TABLE IF EXISTS weather_raw_csv;
DROP TABLE IF EXISTS weather_raw_parquet;
DROP TABLE IF EXISTS weather_inferred;
