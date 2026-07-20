# Lesson 1: Stages and Loading, a Guided Journey

**Module:** Week 5 Day 1
**Format:** In-class walkthrough. Your instructor drives; run every statement yourself in Snowsight as you go.
**Dataset:** A small, deliberately messy weather dataset in three formats, all in the course bucket under `raw/weather/`: `weather_raw.csv`, `weather_raw.parquet`, and `weather_raw.json`. Twenty rows per file, the same twenty observations three ways.

After this lesson you practice everything on the taxi data (Activities 2, 3, and 4). The weather data is small so every result fits on one screen; the taxi data is 3.7 million rows so the same commands feel real.

## The question this lesson answers

Your data lives in S3. Your tables live in Snowflake. Today you learn every part of the bridge between them: how Snowflake sees files (stages), how it parses them (file formats), how you peek at files without loading anything (`SELECT` straight from a stage), and the three ways to get a real table out of a file (DDL then `COPY INTO`; `CREATE TABLE AS SELECT`; and schema inference). Plus one production-grade behavior that will surprise you: what happens when you load the same file twice.

## 1. The cast of characters

Three Snowflake objects, three jobs. Run these and read the output:

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;

DESCRIBE STORAGE INTEGRATION s3_int;
SHOW STAGES IN SCHEMA TECHCATALYST.EXTERNAL_STAGE;
DESCRIBE STAGE TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE;
```

- The **storage integration** (`s3_int`) holds the trust relationship with AWS. It is why nobody in this room ever pastes an AWS key into SQL.
- The **stage** (`AWS_STAGE`) is a named pointer at the bucket, through that trust. A stage holds no rows; it points at files.
- A **file format** (coming in section 3) is a parsing contract: how to read the bytes.

## 2. Look before you load

Never assume what is in a folder. `LIST` it:

```sql
LIST @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/;
```

Three files, one dataset. Note the sizes: same twenty rows, and the Parquet is already the smallest. On the taxi data later, that gap becomes 380 MB versus 77 MB for one month; ask yourself now why (Parquet is columnar, compressed, and carries its own schema).

## 3. File formats: the parsing contracts

```sql
USE SCHEMA TECHCATALYST.<YOUR_NAME>;

CREATE OR REPLACE FILE FORMAT weather_csv_ff
  TYPE = 'CSV'
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  SKIP_HEADER = 1;

CREATE OR REPLACE FILE FORMAT weather_json_ff
  TYPE = 'JSON';

CREATE OR REPLACE FILE FORMAT weather_parquet_ff
  TYPE = 'PARQUET';
```

Read the asymmetry: the CSV format needed instructions (skip the header, respect quotes) because CSV files carry no self-description. The Parquet format needed nothing, because Parquet files describe themselves. JSON sits in between: it carries field names, but no types.

## 4. SELECT straight from the stage: peek without loading

This is the move most people do not know exists: you can query a staged file directly, no table anywhere. It is the "inspect" step, and it is how you catch problems **before** they become bad loads.

### CSV: columns by position

```sql
SELECT $1, $2, $3, $4, $5
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.csv
     (FILE_FORMAT => 'weather_csv_ff')
LIMIT 10;
```

CSV gives you **numbered columns**: `$1` is the first column, `$5` the fifth, and nothing tells you which is which except the header you skipped. Position is the only language CSV speaks.

Now actually read the rows on your screen. This file is dirty on purpose: a station typed as `us1ny` in lowercase, a date with a leading space, a temperature that says `N/A`, another that says `bad`, and some blanks. Staged-file peeking just did its job: you know all of this **before** designing a single table.

### Parquet: columns by name

```sql
SELECT t.$1:STATION::STRING AS station,
       t.$1:DATE::STRING    AS obs_date,
       t.$1:TMAX::STRING    AS tmax
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.parquet
     (FILE_FORMAT => 'weather_parquet_ff') t
LIMIT 10;
```

Parquet arrives as one structured value per row, and you reach into it **by field name**: `$1:STATION`. Names, not positions. Rename a column upstream and this query tells you loudly; the CSV version would silently give you the wrong `$3`.

### JSON: documents, by path

```sql
SELECT $1                          AS whole_document,
       $1:STATION::STRING          AS station,
       $1:TMAX::STRING             AS tmax
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.json
     (FILE_FORMAT => 'weather_json_ff')
LIMIT 10;
```

Each line of the file is one JSON document, and `$1` is the whole document; you navigate it with paths, like Parquet. One caution from real life: JSON **shape** matters. This file is one object per line (the shape loaders want). Export the same data column-oriented, as some tools do by default, and the entire dataset becomes a single giant document that loads as **one row**. Peek first; shape surprises are exactly what this step catches.

### The three styles, side by side

| Format | How you reference a column | Why |
|---|---|---|
| CSV | `$1`, `$2`, `$3` by position | The file carries no names or types |
| Parquet | `$1:STATION` by name | The file embeds names and types |
| JSON | `$1:STATION` by path | The file embeds names, but not types |

## 5. Loading, path A: DDL then COPY INTO (the standard)

The bread-and-butter pattern you will use for the rest of your career: **create the table you want, then copy files into it.**

Step one, the DDL. You know the five columns from peeking, so write them down. Every column is a string on purpose: this is a RAW landing table, and you already saw `N/A` and `bad` hiding in the numerics; a typed column would reject those rows at the door, and RAW's job is to receive what arrived:

```sql
CREATE OR REPLACE TABLE weather_raw_csv (
  station STRING,
  obs_date STRING,
  tmax STRING,
  tmin STRING,
  prcp STRING
);
```

Step two, the load:

```sql
COPY INTO weather_raw_csv
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.csv')
FILE_FORMAT = 'weather_csv_ff';
```

Read the result grid out loud, every column of it: the file name, `status`, `rows_parsed`, `rows_loaded`, errors seen. That grid is `COPY INTO`'s meaning in one row: **read the named staged files through the format contract, insert their rows into the table, and report exactly what happened.** Then verify like an engineer:

```sql
SELECT COUNT(*) FROM weather_raw_csv;   -- 20
SELECT * FROM weather_raw_csv LIMIT 10;
```

Two habits inside that COPY worth naming: `FILES = (...)` loads the exact file you intend, never a whole folder by accident. And CSV loads map by **position** ($1 into the first column), which is why the DDL's column order mirrors the file.

## 6. The surprise: run the COPY again

Same statement, second time:

```sql
COPY INTO weather_raw_csv
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.csv')
FILE_FORMAT = 'weather_csv_ff';

SELECT COUNT(*) FROM weather_raw_csv;   -- still 20
```

The result says **zero files processed**, and the count did not move. Snowflake keeps **load metadata** per table: a memory of which files it already loaded successfully, and it refuses to load them again by default. The property this gives you has a name, **idempotency**: running the load twice causes no damage. If this morning's group activity asked you how a rerun avoids double-loading, you are looking at Snowflake's built-in answer.

And if you truly want a reload (you fixed the file in place, say), you say so explicitly:

```sql
-- Demonstration only. Watch what it does, then we undo it.
COPY INTO weather_raw_csv
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.csv')
FILE_FORMAT = 'weather_csv_ff'
FORCE = TRUE;

SELECT COUNT(*) FROM weather_raw_csv;   -- 40. Every row is now duplicated.
```

`FORCE = TRUE` overrides the memory, and the count proves the danger: 40 rows, all duplicates. Reset cleanly (rerun the `CREATE OR REPLACE` and the first COPY) and remember the shape of this mistake; you will meet it again in production stories.

## 7. Loading, path B: CTAS, the query that becomes a table

You already wrote a working `SELECT` against the staged Parquet in section 4. `CREATE TABLE AS SELECT` turns any query into a table, including that one:

```sql
CREATE OR REPLACE TABLE weather_raw_parquet AS
SELECT t.$1:STATION::STRING AS station,
       t.$1:DATE::STRING    AS obs_date,
       t.$1:TMAX::STRING    AS tmax,
       t.$1:TMIN::STRING    AS tmin,
       t.$1:PRCP::STRING    AS prcp
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.parquet
     (FILE_FORMAT => 'weather_parquet_ff') t;

SELECT COUNT(*) FROM weather_raw_parquet;   -- 20
```

One statement: table created, data loaded, columns named and cast by your `SELECT`. So when is this the right tool, and when is COPY?

| | DDL + COPY INTO | CTAS from a stage query |
|---|---|---|
| Statements | Two (create, load) | One |
| Column control | The DDL is the contract | The SELECT is the contract |
| Rerun behavior | Load metadata: reruns are safe, incremental loads accumulate | Replaces the whole table every run; no memory of files |
| Best for | Recurring loads, pipelines, anything that grows | One-shot materialization of an inspection query |

The rerun row is the important one: CTAS has no load memory, so it cannot do "load only the new files" and it silently rebuilds from scratch each time. Fine for a one-off; wrong for a daily feed.

## 8. Loading, path C: INFER_SCHEMA, when you do not know the columns

Weather has five columns; you wrote the DDL in ten seconds. Now imagine the file has 190 columns, or a vendor changes it monthly. Snowflake can read a Parquet file's embedded schema **for** you. Watch it work in two steps, because the two steps are clearer than the one-liner you will meet online.

Step one: `INFER_SCHEMA` is just a function that returns rows describing the file's columns. Run it alone and read the output:

```sql
SELECT *
FROM TABLE(INFER_SCHEMA(
  LOCATION => '@TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.parquet',
  FILE_FORMAT => 'weather_parquet_ff'
));
```

One row per detected column: name, inferred type, nullability. Nothing was created; this is metadata you could read and hand-type into a DDL yourself.

Step two: or you let Snowflake type it for you. `CREATE TABLE ... USING TEMPLATE` consumes that metadata and generates the DDL, and the `ARRAY_AGG(OBJECT_CONSTRUCT(*))` wrapper is nothing more than "bundle those metadata rows into the shape TEMPLATE expects":

```sql
CREATE OR REPLACE TABLE weather_inferred
USING TEMPLATE (
  SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
  FROM TABLE(INFER_SCHEMA(
    LOCATION => '@TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/weather_raw.parquet',
    FILE_FORMAT => 'weather_parquet_ff'
  ))
);

DESCRIBE TABLE weather_inferred;
```

Compare the DESCRIBE with the INFER_SCHEMA output: same columns, and you typed none of them. Load it with the by-name option, since the table's columns came from the file's names:

```sql
COPY INTO weather_inferred
FROM @TECHCATALYST.EXTERNAL_STAGE.AWS_STAGE/raw/weather/
FILES = ('weather_raw.parquet')
FILE_FORMAT = 'weather_parquet_ff'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT COUNT(*) FROM weather_inferred;   -- 20
```

`MATCH_BY_COLUMN_NAME` is the partner habit: load columns by name rather than position, so a reordered source cannot scramble your table. It is standard for Parquet loads whether the DDL was written or inferred.

**Honest positioning, because you will see all three in the wild:** for a known, stable schema like weather or taxi, explicit DDL is the simplest correct form and the one to reach for first; it is your contract, in your types, in plain sight. `INFER_SCHEMA` earns its keep when the schema is unknown, very wide, or changes under you, and as a bootstrap when you need a lost table back without retyping 19 columns. It is a convenience tool, not an upgrade.

## 9. The decision card

| You want to | Reach for |
|---|---|
| See what is in a staged file before doing anything | `SELECT` from the stage with a format |
| Load a known schema, especially repeatedly | Write the DDL, then `COPY INTO` with `FILES = (...)` |
| Materialize an inspection query once | CTAS |
| Create a table for a wide or unknown Parquet schema | `INFER_SCHEMA`, alone first, then `USING TEMPLATE` |
| Reload a file Snowflake already loaded | Understand why first; then `FORCE = TRUE`, sparingly |
| Never | Paste credentials anywhere; the integration owns trust |

## 10. Pipe versus COPY INTO: the loading spectrum

You have seen `COPY INTO` run on demand: you write the statement, you run it, it loads the named files, and it reports what happened. That is **batch loading**, and it is the pattern for most of this week.

Snowflake also offers **Snowpipe**, a continuous-loading service. Instead of you running a COPY, Snowpipe listens for new files in a stage (through an S3 event notification or a REST call) and loads them automatically within minutes of arrival. No schedule to manage, no `COPY INTO` to run.

| | COPY INTO (batch) | Snowpipe (continuous) |
|---|---|---|
| Who triggers the load | You (or a scheduler, DAG, stored procedure) | An event from the cloud provider or a REST API call |
| When it runs | On demand, when you say so | Continuously, within minutes of file arrival |
| Compute | Uses your virtual warehouse | Uses Snowflake-managed compute (serverless) |
| Cost model | Warehouse credits while running | Per-file serverless credits |
| Load metadata (idempotency) | Yes, per table, tracks loaded files | Yes, per pipe, tracks loaded files |
| Best for | Scheduled batch jobs, backfills, manual loads | Near-real-time ingestion of many small files |

The practical takeaway: if you are loading files on a schedule or on demand, `COPY INTO` is the standard tool, and it is what you will use in every activity today. If your data arrives continuously and you need it queryable within minutes, Snowpipe is the answer, and you will see it again in the streaming and orchestration modules. Both share the same stage, the same file format, and the same load-metadata idempotency you saw in section 6.

You do not need to create a Pipe today. The point is to know it exists so that when Activity 2 asks "batch or continuous?", you have a frame for the question.

## Cleanup

```sql
DROP TABLE IF EXISTS weather_raw_csv;
DROP TABLE IF EXISTS weather_raw_parquet;
DROP TABLE IF EXISTS weather_inferred;
```

Keep the file formats; the activities reuse the same ideas.

## Your turn

The taxi data is waiting: Activity 2 starts with one Parquet file, scales to all Parquet and CSV files in the stage, and compares row counts across formats. Activity 3 takes the raw tables through a cleaning pipeline. Everything you just watched on twenty rows, you now do at scale.
