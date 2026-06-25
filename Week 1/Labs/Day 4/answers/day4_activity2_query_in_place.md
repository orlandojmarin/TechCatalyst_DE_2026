# Day 4 Lab Worksheet: Query Files in Place with BigQuery

## Concept Checkpoint

1. Where is the data? The Cloud Storage URI pointing to the object
2. What file format is it? The file format (CSV, JSON, Parquet, etc.)
3. How are columns identified and typed? A schema (column names and data types), either declared or auto-detected
4. Is there a header row to skip? Whether the first row is column names (not data) so the engine skips it

---

## Part 1: Inspect the Stored CSV

1. Delimiter: `,` (comma)
2. Header present? Yes (`PULocationID,fare_amount,trip_date`)
3. Predicted types for the three columns: `PULocationID` = INT64, `fare_amount` = FLOAT64, `trip_date` = DATE
4. What could go wrong if a later file contains `unknown` in `fare_amount`? The value `unknown` is a string and cannot be parsed as FLOAT64, so BigQuery would return an error or null when reading that row, potentially breaking the query.

---

## Part 2: Review or Create the External Table

**Before running:** What do the three options control, and what omitted DDL element causes schema autodetection?

> Answer: `format` tells BigQuery the file is a CSV, `uris` points to where the file lives in Cloud Storage, and `skip_leading_rows` tells it to skip the first row since it contains column names, not data. The omitted element is the column list (no columns are declared between the table name and `OPTIONS`), which causes BigQuery to auto-detect the schema from the file itself.

**After running:** Record the schema shown by BigQuery.

| Column | BigQuery type | Does it match your prediction? |
| :--- | :--- | :--- |
| `PULocationID` | INTEGER (NULLABLE) | Yes |
| `fare_amount` | FLOAT (NULLABLE) | Yes |
| `trip_date` | DATE (NULLABLE) | Yes |

---

## Part 3: Run the Supplied Queries

### Query A: Preview Rows

**Predict:** Does `LIMIT 10` mean BigQuery can stop scanning a row-oriented CSV after exactly ten rows? Why or why not?

> Prediction: No, because CSV is row-oriented and has no index, so BigQuery has to read the entire file even if it only needs 10 rows.

**Results:**

- Result schema observation (column names and types): PULocationID (INTEGER), fare_amount (FLOAT), trip_date (DATE)
- Estimated bytes before Run: 409 B
- Bytes processed after Run: 409 B
- One external-CSV limitation revealed or relevant to this query: LIMIT doesn't reduce the amount of data scanned because CSV is row-oriented, so BigQuery must read the entire file regardless of how few rows are returned.

### Query B: Aggregate by Date

**Predict:** What data must BigQuery read to calculate the count and total for every date?

> Prediction: BigQuery needs to read every row to count how many trips fall on each date and to sum the fare amounts per date. It needs the trip_date column to group by and fare_amount to sum.

**Results:**

- Date with the greatest `total_fare`: 2025-01-23
- Result schema observation (column names and types): trip_date (DATE), trip_count (INTEGER), total_fare (FLOAT)
- Estimated bytes before Run: 0 B
- Bytes processed after Run: 409 B
- One external-CSV limitation revealed or relevant to this query: CSV is row-oriented, so BigQuery can't read only the columns it needs (trip_date and fare_amount). It has to scan the entire file, including PULocationID, even though that column isn't used in this query.

---

## Part 4: Compare the Scan Signal and Limitations

| Observation | Query A | Query B |
| :--- | :--- | :--- |
| Rows returned | 10 | 7 |
| Bytes processed | 409 B | 409 B |
| Did fewer output rows guarantee fewer input bytes? | No | No |

Which limitation would matter most for a repeated production workload, and why?

> Answer: The inability to read only the columns you need (because CSV is row-oriented) matters most for repeated workloads. If your file had many columns but your query only used a few, you'd still scan the entire file every time the query runs, wasting bytes and increasing cost with each execution. A columnar format would let you skip unused columns and reduce the scan.

---

## Part 5: External or Loaded Curated Table?

1. A new partner CSV needs a one-time quality check: **external**, because the data is exploratory and only queried once, so there's no reason to spend time loading it into a managed table.
2. A daily executive dashboard needs predictable performance and stable fields: **loaded**, because repeated queries need consistent performance and a stable schema, which a managed warehouse table provides over an external file that could change or break.
