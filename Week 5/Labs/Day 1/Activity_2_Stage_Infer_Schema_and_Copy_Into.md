# Activity 2: Stage, Infer Schema, and Load at Scale

**Module:** Week 5 Day 1  
**Estimated Time:** 50 to 60 minutes  
**Difficulty:** Intermediate  
**Format:** Pairs  
**Prerequisites:** Lesson 1 (the weather walkthrough, including the Pipe vs. COPY INTO comparison), your Week 4 Snowflake access, instructor storage-integration preflight passed

## Objective

Everything Lesson 1 showed you on twenty weather rows, now on millions of taxi rows. You will load Parquet and CSV files through one stage, learn the difference between loading a single named file and loading by pattern, check for duplicates, and validate row counts across formats.

## Source contract

The S3 bucket contains four taxi trip files under `stages/`:

| File | Format | Rows (expected) |
|---|---|---|
| `yellow_tripdata_2026-01.parquet` | Parquet | 3,724,889 |
| `yellow_tripdata_2026-02.parquet` | Parquet | 3,507,753 |
| `yellow_tripdata_2026-01.csv` | CSV | 3,724,889 |
| `yellow_tripdata_2026-02.csv` | CSV | 3,507,753 |

Use the instructor-provided storage integration. Do not add AWS keys, passwords, or access tokens to SQL, a notebook, or a configuration file.

## Instructions

### Part A: One Parquet file (the careful start)

1. Copy the SQL scaffold at the bottom of this activity into a Snowsight worksheet. Run the context block first.
2. Create the Parquet file format and a named external stage pointed at `s3://techcatalyst-de-2026/stages/`. The supplied integration name is an instructor value.
3. Run `LIST` and confirm all four taxi files are visible (two `.parquet`, two `.csv`). If any file is missing, stop and ask the instructor.
4. Peek at `yellow_tripdata_2026-01.parquet` with a direct `SELECT` (Lesson 1, section 4). Confirm the columns you expect are there.
5. Create `raw_yellow_tripdata_parquet` as a TRANSIENT table, **your choice of technique**: run the DDL provided below (the schema is known and stable, so this is the standard path), or practice the Lesson 1 inference path (`INFER_SCHEMA` alone first, then `USING TEMPLATE`). Either way, run `DESCRIBE TABLE` before loading.
6. Run `COPY INTO` naming **only** `yellow_tripdata_2026-01.parquet`, with `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE`.
7. Record the `COPY INTO` result. Run `SELECT COUNT(*)` and confirm the count matches the expected value for that one file.

### Part B: All Parquet files (scale up and check for duplicates)

8. Record the current row count (from step 7) as your "before" count.
9. Run a second `COPY INTO` against the same `raw_yellow_tripdata_parquet` table, but this time use `PATTERN = '.*yellow_tripdata_2026-.*\\.parquet'` instead of `FILES`. This tells Snowflake to load every matching file in the stage.
10. Record the new row count as your "after" count.
11. Answer these questions in your Day 1 notes:
    - How many new rows were added? Does the "after" count equal the sum of both Parquet files, or did the 2026-01 file get loaded again?
    - Explain *why* (Lesson 1, section 6). What Snowflake behavior protects you from duplicates here?
    - When would `FORCE = TRUE` override that protection, and why should you avoid it in a pipeline?

### Part C: Both CSV files

12. Create a CSV file format with `PARSE_HEADER = TRUE` (do not use `SKIP_HEADER = 1`) and `FIELD_OPTIONALLY_ENCLOSED_BY = '"'`.
13. Create `raw_yellow_tripdata_csv` as a TRANSIENT table using the same DDL (or inference) you used for the Parquet table. The columns are identical across formats.
14. Run `COPY INTO` using `PATTERN = '.*yellow_tripdata_2026-.*\\.csv'` to load both CSV files in one statement. Use `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE`.
15. Record the `COPY INTO` result and run `SELECT COUNT(*)`.

### Part D: Cross-format validation

16. Compare the total row count in `raw_yellow_tripdata_parquet` with `raw_yellow_tripdata_csv`. They should match exactly. If they do not, investigate and record why.
17. For each table, run the date-range and data-quality queries from the scaffold. Record: pickup-date range, count of negative trip distances.
18. Answer in your notes: the Parquet and CSV files hold the same data. Given what you learned in Lesson 1 about file sizes and self-describing schemas, name two reasons you would prefer Parquet for a production pipeline.

## Expected Output

| Check | Expected |
|---|---|
| `LIST` shows | 4 taxi files (2 `.parquet`, 2 `.csv`) |
| `DESCRIBE TABLE` | 19 columns with sensible types before any load |
| Parquet table after step 7 (one file) | 3,724,889 rows |
| Parquet table after step 10 (both files) | 7,232,642 rows |
| CSV table after step 15 (both files) | 7,232,642 rows |
| Parquet total equals CSV total | Yes |
| Negative trip distances | A non-zero count; record the number as a finding |

## Success Criteria

- Your stage uses a storage integration and no embedded credentials.
- You inspect the staged file before creating the target table, and you can say why you chose DDL or inference.
- Both target tables are transient and named with a `_parquet` or `_csv` suffix.
- You loaded one Parquet file first, then used PATTERN for the rest, and your before/after counts prove no duplicates were introduced.
- Your CSV and Parquet row totals match.
- You can explain why `MATCH_BY_COLUMN_NAME` is used for both Parquet and CSV loads.
- Your notes include the COPY result, row reconciliation, date-range evidence, one data-quality finding, and a reasoned Parquet vs. CSV comparison.

## Hints

<details>
<summary>I received an insufficient-privileges error on the stage.</summary>

The class role needs both `CREATE STAGE` on the schema and `USAGE` on the storage integration. Record the exact error and ask the instructor to repair the grant. Do not use a personal key or an administrator role.

</details>

<details>
<summary>Why does the second COPY INTO (with PATTERN) not reload the 2026-01 file?</summary>

Snowflake tracks successfully loaded files for a target table and avoids loading the same file again by default. The PATTERN matches both files, but only the one not yet loaded (2026-02) is ingested. That behavior protects a pipeline from accidental duplicates. Do not use `FORCE = TRUE` in this lab.

</details>

<details>
<summary>My CSV load returned errors or fewer rows than expected.</summary>

Check your file format: `PARSE_HEADER = TRUE` must be set (otherwise CSVs don't expose headers to `MATCH_BY_COLUMN_NAME`), and `FIELD_OPTIONALLY_ENCLOSED_BY = '"'` handles quoted fields. Also confirm `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` is present so columns align by name, not position.

</details>

<details>
<summary>Batch or continuous: when would I use Snowpipe instead of COPY INTO?</summary>

`COPY INTO` is batch: you run it on demand or on a schedule. Snowpipe is continuous: it listens for new files and loads them automatically within minutes. For today's lab (loading known files on demand), `COPY INTO` is the right tool. Snowpipe would be the answer if files arrived unpredictably and you needed near-real-time availability.

</details>

## Stretch Goal

Create a `daily_trip_summary` view that unions both tables, adds a `source_format` column (`'parquet'` or `'csv'`), and aggregates one row per pickup date with `trip_count` and `total_trip_amount`. Then answer: does the summary show doubled rows (since both tables hold the same data), and how would you design this differently in a real pipeline to avoid that?

## SQL scaffold (copy into a Snowsight worksheet)

Replace `<YOUR_NAME>` with your assigned schema and `<INSTRUCTOR_STORAGE_INTEGRATION>` with the integration name your instructor provides. Complete each TODO in order.

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;

-- ============================================================
-- PART A: One Parquet file
-- ============================================================

-- 1. TODO: Create yellow_tripdata_parquet_ff with TYPE = PARQUET
--    and USE_LOGICAL_TYPE = TRUE.

-- 2. TODO: Create yellow_tripdata_s3_stage that points to:
--    s3://techcatalyst-de-2026/stages/
--    Use STORAGE_INTEGRATION = <INSTRUCTOR_STORAGE_INTEGRATION>.

-- 3. TODO: LIST the stage and confirm all four taxi files appear
--    (yellow_tripdata_2026-01.parquet, yellow_tripdata_2026-02.parquet,
--     yellow_tripdata_2026-01.csv, yellow_tripdata_2026-02.csv).

-- 4. TODO: Peek at yellow_tripdata_2026-01.parquet with a direct SELECT
--    (3 or 4 named fields, LIMIT 10).

-- 5. Create the Parquet target table. EITHER run this provided DDL as-is:
--
-- CREATE OR REPLACE TRANSIENT TABLE raw_yellow_tripdata_parquet (
--   vendorid              NUMBER,
--   tpep_pickup_datetime  TIMESTAMP_NTZ,
--   tpep_dropoff_datetime TIMESTAMP_NTZ,
--   passenger_count       NUMBER,
--   trip_distance         FLOAT,
--   ratecodeid            NUMBER,
--   store_and_fwd_flag    STRING,
--   pulocationid          NUMBER,
--   dolocationid          NUMBER,
--   payment_type          NUMBER,
--   fare_amount           FLOAT,
--   extra                 FLOAT,
--   mta_tax               FLOAT,
--   tip_amount            FLOAT,
--   tolls_amount          FLOAT,
--   improvement_surcharge FLOAT,
--   total_amount          FLOAT,
--   congestion_surcharge  FLOAT,
--   airport_fee           FLOAT
-- );
--
-- OR practice the Lesson 1 inference path: INFER_SCHEMA alone first, read its
-- output, then CREATE TRANSIENT TABLE ... USING TEMPLATE. Then DESCRIBE TABLE.

-- 6. TODO: COPY INTO raw_yellow_tripdata_parquet from only
--    yellow_tripdata_2026-01.parquet.
--    Use MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE. Do not use FORCE = TRUE.

-- 7. TODO: Record the COPY result, then validate:
--    SELECT COUNT(*) FROM raw_yellow_tripdata_parquet;
--    Expected: 3,724,889

-- ============================================================
-- PART B: All Parquet files (scale up, check for duplicates)
-- ============================================================

-- 8. TODO: Record the current count as your "before" count.

-- 9. TODO: COPY INTO raw_yellow_tripdata_parquet using:
--    PATTERN = '.*yellow_tripdata_2026-.*\.parquet'
--    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
--    Do not use FORCE = TRUE.

-- 10. TODO: Record the new count as your "after" count.
--     SELECT COUNT(*) FROM raw_yellow_tripdata_parquet;
--     Expected: 7,232,642

-- 11. TODO: Answer in your notes:
--     a. How many new rows were added?
--     b. Was yellow_tripdata_2026-01.parquet loaded again? Why or why not?
--     c. When would FORCE = TRUE override this, and why avoid it in a pipeline?

-- ============================================================
-- PART C: Both CSV files
-- ============================================================

-- 12. TODO: Create yellow_tripdata_csv_ff with TYPE = CSV,
--     PARSE_HEADER = TRUE, FIELD_OPTIONALLY_ENCLOSED_BY = '"'.

-- 13. TODO: Create raw_yellow_tripdata_csv as a TRANSIENT table.
--     Use the same column definitions as the Parquet table.

-- 14. TODO: COPY INTO raw_yellow_tripdata_csv using:
--     PATTERN = '.*yellow_tripdata_2026-.*\.csv'
--     FILE_FORMAT = yellow_tripdata_csv_ff
--     MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE

-- 15. TODO: Record the COPY result, then validate:
--     SELECT COUNT(*) FROM raw_yellow_tripdata_csv;
--     Expected: 7,124,755

-- ============================================================
-- PART D: Cross-format validation
-- ============================================================

-- 16. TODO: Compare totals. Do they match?
--     SELECT 'parquet' AS source, COUNT(*) AS row_count FROM raw_yellow_tripdata_parquet
--     UNION ALL
--     SELECT 'csv'     AS source, COUNT(*) AS row_count FROM raw_yellow_tripdata_csv;

-- 17. TODO: For EACH table, run these validation queries and record the results:
--     a. MIN and MAX of tpep_pickup_datetime
--     b. COUNT of rows where trip_distance < 0

-- 18. TODO: In your notes, name two reasons to prefer Parquet over CSV
--     for a production pipeline.
```
