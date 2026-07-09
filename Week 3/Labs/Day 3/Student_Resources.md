# Week 3 Day 3 Student Resources: SQL on BigQuery

AI-Free Zone reminder: Weeks 1 to 4 are for building your own coding and debugging muscles. Do not use AI assistants to write or complete your SQL. Read BigQuery errors carefully, ask your partner, ask the instructor, and use the documentation below.

## Core Documentation

| Resource | Date checked | Why it helps |
|---|---|---|
| [BigQuery GoogleSQL query syntax](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax) | 2026-07-05 | Reference for `SELECT`, `FROM`, joins, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, and `WITH`. |
| [BigQuery aggregate functions](https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions) | 2026-07-05 | Reference for `COUNT`, `COUNTIF`, `SUM`, `AVG`, `MIN`, and `MAX`. |
| [BigQuery conditional expressions](https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions) | 2026-07-05 | Reference for `CASE`, `COALESCE`, `IF`, and related conditional logic. |
| [BigQuery conversion functions](https://cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions) | 2026-07-05 | Reference for `CAST` and `SAFE_CAST`. |
| [BigQuery date functions](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions) | 2026-07-05 | Reference for `DATE`, `DATE_SUB`, `DATE_TRUNC`, `FORMAT_DATE`, and `EXTRACT`. |
| [BigQuery timestamp functions](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions) | 2026-07-05 | Reference for `TIMESTAMP_DIFF`, `TIMESTAMP_TRUNC`, and timestamp arithmetic. |
| [NYC TLC Yellow Taxi data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) | 2026-07-05 | Defines taxi columns such as pickup time, location IDs, payment type, fare, tip, and total amount. |
| [GTFS Schedule Reference](https://gtfs.org/documentation/schedule/reference/) | 2026-07-05 | Defines transit tables such as `routes`, `trips`, and `stop_times`, which inspire the warm-up. |

## SQL Execution Order

The engine does not process clauses in the same order you write them.

| Step | Clause | What happens |
|---|---|---|
| 1 | `FROM` and `JOIN` | Assemble source rows. |
| 2 | `WHERE` | Filter individual rows. |
| 3 | `GROUP BY` | Collapse rows into groups. |
| 4 | `HAVING` | Filter groups after aggregation. |
| 5 | `SELECT` | Compute output columns. |
| 6 | `ORDER BY` | Sort result rows. |
| 7 | `LIMIT` | Trim output rows. |

Use this table when an error feels confusing. Most beginner SQL issues come from using a value before the engine has created it.

## Filtering Rows

```sql
SELECT
  VendorID,
  tpep_pickup_datetime,
  fare_amount
FROM `PROJECT_ID.taxi_yourteam.trips_part_clust`
WHERE DATE(tpep_pickup_datetime) = DATE '2024-01-15'
  AND fare_amount > 25
ORDER BY fare_amount DESC
LIMIT 10;
```

Important habits:

- Filter on the date expression used for partitioning when possible.
- Select only the columns needed for the question.
- Treat `LIMIT` as output control, not scan-cost control.

## Grouping and `HAVING`

Rule: every selected column is either aggregated or included in `GROUP BY`.

```sql
SELECT
  PULocationID,
  COUNT(*) AS trip_count,
  ROUND(AVG(fare_amount), 2) AS avg_fare
FROM `PROJECT_ID.taxi_yourteam.trips_part_clust`
WHERE DATE(tpep_pickup_datetime) BETWEEN DATE '2024-01-15' AND DATE '2024-01-21'
GROUP BY PULocationID
HAVING COUNT(*) >= 100
ORDER BY trip_count DESC;
```

Use `WHERE` for row filters. Use `HAVING` for filters that depend on group results.

## Counting Carefully

```sql
SELECT
  COUNT(*) AS row_count,
  COUNT(fare_amount) AS non_null_fare_count,
  COUNTIF(fare_amount > 100) AS high_fare_count
FROM `PROJECT_ID.taxi_yourteam.trips_part_clust`
WHERE DATE(tpep_pickup_datetime) = DATE '2024-01-15';
```

`COUNT(*)` counts rows. `COUNT(column)` counts non-null values in that column. `COUNTIF(condition)` counts rows where the condition is true.

## Join Discipline

```sql
SELECT
  z.Zone AS pickup_zone,
  z.Borough AS pickup_borough,
  COUNT(*) AS trip_count
FROM `PROJECT_ID.taxi_yourteam.trips_part_clust` AS t
LEFT JOIN `PROJECT_ID.taxi_yourteam.dim_zone` AS z
  ON t.PULocationID = z.LocationID
WHERE DATE(t.tpep_pickup_datetime) BETWEEN DATE '2024-01-15' AND DATE '2024-01-21'
GROUP BY pickup_zone, pickup_borough
ORDER BY trip_count DESC;
```

Two traps:

| Trap | Symptom | Defense |
|---|---|---|
| Fan-out | Counts or sums grow after the join. | Check row counts before and after the join. Check duplicate keys in the dimension. |
| Right-side filter after `LEFT JOIN` | Missing unmatched rows. | Put the right-side filter in `ON`, or explicitly test for nulls. |

Row-count check:

```sql
SELECT COUNT(*) AS before_join
FROM `PROJECT_ID.taxi_yourteam.trips_part_clust`;

SELECT COUNT(*) AS after_join
FROM `PROJECT_ID.taxi_yourteam.trips_part_clust` AS t
LEFT JOIN `PROJECT_ID.taxi_yourteam.dim_zone` AS z
  ON t.PULocationID = z.LocationID;
```

Duplicate dimension check:

```sql
SELECT
  LocationID,
  COUNT(*) AS records
FROM `PROJECT_ID.taxi_yourteam.dim_zone`
GROUP BY LocationID
HAVING COUNT(*) > 1;
```

## `CASE`, `COALESCE`, and `SAFE_CAST`

```sql
SELECT
  CASE
    WHEN trip_distance < 1 THEN 'short'
    WHEN trip_distance <= 5 THEN 'medium'
    ELSE 'long'
  END AS distance_bucket,
  COALESCE(tip_amount, 0) AS tip_amount_clean,
  SAFE_CAST(passenger_count AS INT64) AS passenger_count_int
FROM `PROJECT_ID.taxi_yourteam.trips_part_clust`
WHERE DATE(tpep_pickup_datetime) = DATE '2024-01-15';
```

Use `CASE` to create labels. Use `COALESCE` to replace nulls with a fallback. Use `SAFE_CAST` when bad values should become null instead of crashing the query.

## Date and Timestamp Patterns

```sql
SELECT
  DATE(tpep_pickup_datetime) AS pickup_date,
  EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
  EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS pickup_dayofweek,
  TIMESTAMP_DIFF(tpep_dropoff_datetime, tpep_pickup_datetime, MINUTE) AS duration_minutes
FROM `PROJECT_ID.taxi_yourteam.trips_part_clust`
WHERE DATE(tpep_pickup_datetime) BETWEEN DATE '2024-01-15' AND DATE '2024-01-21';
```

BigQuery `DAYOFWEEK` returns 1 for Sunday and 7 for Saturday.

## CTEs

Common table expressions help you name steps.

```sql
WITH valid_trips AS (
  SELECT
    PULocationID,
    fare_amount,
    trip_distance
  FROM `PROJECT_ID.taxi_yourteam.trips_part_clust`
  WHERE DATE(tpep_pickup_datetime) BETWEEN DATE '2024-01-15' AND DATE '2024-01-21'
    AND fare_amount BETWEEN 0 AND 300
    AND trip_distance BETWEEN 0 AND 100
),
zone_stats AS (
  SELECT
    PULocationID,
    COUNT(*) AS trip_count,
    ROUND(AVG(fare_amount), 2) AS avg_fare
  FROM valid_trips
  GROUP BY PULocationID
)
SELECT
  z.Zone AS pickup_zone,
  z.Borough AS pickup_borough,
  s.trip_count,
  s.avg_fare
FROM zone_stats AS s
LEFT JOIN `PROJECT_ID.taxi_yourteam.dim_zone` AS z
  ON s.PULocationID = z.LocationID
WHERE s.trip_count >= 100
ORDER BY s.avg_fare DESC;
```

Debug a CTE chain by temporarily selecting from one CTE:

```sql
SELECT * FROM zone_stats LIMIT 10;
```

## Lab Deliverable Checklist

| Done | Deliverable | Evidence |
|---|---|---|
| [ ] | Setup complete | `student-work/week3/day3/` exists with copied starter files. |
| [ ] | GTFS warm-up complete | `gtfs_warmup.sql` has answers and at least one result pasted into notes. |
| [ ] | Taxi drills complete | `taxi_sql_drills.sql` has at least 10 completed drills. |
| [ ] | Business challenge complete | `business_challenge.sql` has at least 3 completed challenges and bytes comments. |
| [ ] | Join check complete | `day3_query_review.md` includes before and after row counts. |
| [ ] | CTE used | At least one completed query uses `WITH`. |
| [ ] | Group presentation ready | One query, one result, one risk, and one recommendation are ready to present. |
| [ ] | AI-Free Zone honored | SQL was written by hand. |

## Common Errors

| Error or symptom | Likely cause | Fix |
|---|---|---|
| Column is neither grouped nor aggregated | A selected column is missing from `GROUP BY`. | Add it to `GROUP BY` or aggregate it. |
| Aggregate functions are not allowed in `WHERE` | You filtered a group result too early. | Move the condition to `HAVING`. |
| Unexpected row-count increase after join | Dimension key is duplicated or join key is wrong. | Check duplicates in the dimension and inspect the `ON` condition. |
| Query scans more data than expected | No date filter, too many selected columns, or wrong table variant. | Add a partition-friendly date filter and select only needed columns. |
| Results show only numeric location IDs | The dimension join is missing. | Join to `dim_zone` and return zone names and boroughs. |
