# Activity 3: From RAW to CLEAN to FINAL

**Module:** Week 5 Day 1
**Estimated Time:** 35 to 45 minutes
**Difficulty:** Intermediate
**Format:** Individual, partner check at each checkpoint
**Prerequisites:** Activity 2 complete (`raw_yellow_tripdata_parquet` is loaded from the stage)

## Objective

Loading data was the easy half. Raw data is a receipt, not a product: wrong types, twenty columns where six are needed, five separate surcharge fields, and timestamps nobody has split into useful parts. In this lab you take the table you loaded from the stage and refine it in two deliberate steps: a **CLEAN** table others could trust, then a small **FINAL** summary a business user would actually query.

Three layers, three jobs:

| Layer | Table | Job |
|---|---|---|
| RAW | your loaded taxi table | Exactly what arrived. Never edited, only read. |
| CLEAN | `clean_yellow_taxi` | Typed, trimmed, derived, quality-filtered. The version you would hand a teammate. |
| FINAL | `daily_taxi_summary` | One row per day, ready for a dashboard. |

You have seen this shape before as bronze, silver, and gold. Today it is three `CREATE TABLE AS SELECT` statements in Snowflake; on Wednesday you will build the same arc in Spark. Same thinking, different engine.

## Setup

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;
```

Your RAW table is `raw_yellow_tripdata_parquet` from Activity 2. First, look at what you are standing on:

```sql
DESCRIBE TABLE raw_yellow_tripdata_parquet;

SELECT COUNT(*) FROM raw_yellow_tripdata_parquet;
```

Note the row count; the whole lab reconciles against it. And check the two datetime columns: they should be TIMESTAMP. If they landed as NUMBER instead (raw parquet microseconds), convert them in Task 1 with `TO_TIMESTAMP(col::NUMBER, 6)`; every other instruction stays the same.

## Task 1: Build CLEAN

One `CREATE OR REPLACE TRANSIENT TABLE clean_yellow_taxi AS SELECT ...` from RAW, doing all of this:

**Keep and type only what earns its place.**
1. `vendorid`, cast to INT.
2. `pickup_at` and `dropoff_at`: the two datetime columns, renamed, as TIMESTAMP.
3. `passenger_count` cast to INT, and a NULL means 1 (`COALESCE`).
4. `trip_distance`, `pulocationid`, `dolocationid`, `payment_type` (cast the IDs and payment type to INT).

**Derive the date features everyone always needs.**
5. `pickup_date` (DATE), `pickup_hour` (0 to 23), `pickup_dow` (day name), and `is_weekend` (BOOLEAN).
6. `trip_minutes`: minutes between pickup and dropoff (`TIMESTAMPDIFF`).

**Consolidate the money.**
7. `fare_amount` and `tip_amount` stay as they are.
8. `total_surcharges` = `extra + mta_tax + improvement_surcharge + congestion_surcharge + airport_fee` (COALESCE each to 0 first; any NULL would poison the sum).
9. `total_amount` stays, so the consolidation can be checked against it.

**Drop the rest.** No `store_and_fwd_flag`, no `ratecodeid`, no five separate surcharge columns. Deleting columns from CLEAN costs nothing, because RAW still has everything: that is exactly why RAW exists.

**Apply the physics filters.**
10. Keep only rows with `trip_distance > 0` and `trip_minutes > 0`.

### Checkpoints

```sql
-- 1. CLEAN is smaller than RAW, and you can say by how many rows
SELECT
  (SELECT COUNT(*) FROM raw_yellow_tripdata_parquet) AS raw_rows,
  (SELECT COUNT(*) FROM clean_yellow_taxi)           AS clean_rows;

-- 2. Zero rows violate the rules you enforced (this must return 0)
SELECT COUNT(*) AS violations
FROM clean_yellow_taxi
WHERE trip_distance <= 0 OR trip_minutes <= 0 OR passenger_count IS NULL;

-- 3. The money consolidation reconciles: fare + tip + tolls + surcharges
--    should track total_amount. Expect near-zero for almost every row
--    (pennies of rounding are fine; investigate anything larger).
SELECT COUNT(*) AS suspicious_rows
FROM clean_yellow_taxi c
JOIN raw_yellow_tripdata_parquet r
  ON  c.pickup_at = r.tpep_pickup_datetime
  AND c.dropoff_at = r.tpep_dropoff_datetime
  AND c.pulocationid = r.pulocationid
WHERE ABS((c.fare_amount + c.tip_amount + COALESCE(r.tolls_amount, 0) + c.total_surcharges)
          - c.total_amount) > 0.05;
```

That third query is optional if time is short, but it teaches the real habit: when you consolidate money columns, you prove the consolidation against a total the source already carried.

## Task 2: Build FINAL

One more CTAS: `daily_taxi_summary`, one row per `pickup_date`, with:

1. `total_trips`
2. `total_revenue` (sum of `total_amount`, rounded to 2)
3. `avg_fare` (rounded to 2)
4. `avg_tip_pct`: average of `tip_amount / fare_amount` where `fare_amount > 0`, as a percentage rounded to 1
5. `weekend_trips`: trips where `is_weekend` (a `COUNT_IF` or a `SUM(IFF(...))`)

Ordered by date.

### Checkpoints

```sql
-- 1. Roughly one row per day of the month
SELECT COUNT(*) AS days FROM daily_taxi_summary;

-- 2. FINAL reconciles with CLEAN exactly (both numbers identical)
SELECT
  (SELECT SUM(total_trips) FROM daily_taxi_summary) AS from_final,
  (SELECT COUNT(*)         FROM clean_yellow_taxi)  AS from_clean;

-- 3. The dashboard question, answered in one cheap query
SELECT * FROM daily_taxi_summary ORDER BY total_revenue DESC LIMIT 3;
```

A note on checkpoint 1: expect a few stray dates outside the month; real taxi files always carry a handful of trips whose timestamps spill past the month boundary. Seeing them, and deciding what to do about them, is data engineering. For today, keeping them is fine; say out loud what you would do in production.

## Task 3: Close the loop

Answer with your partner, one sentence each, in your day notes:

1. A teammate finds a bug in your `total_surcharges` logic next week. What do you rebuild, and what do you not re-download?
2. Why is dropping columns in CLEAN safe, and what would make it unsafe?
3. Your `daily_taxi_summary` disagrees with CLEAN's count someday. Which of the two tables is wrong, and how do you know?
4. You built RAW to CLEAN to FINAL with three CTAS statements. What breaks about this approach when the pipeline needs to run every morning without you? (You meet the answers on Wednesday and Thursday.)

## Success Criteria

- `clean_yellow_taxi` exists: typed columns, date features, consolidated surcharges, no physics violations (checkpoint 2 returns 0).
- `daily_taxi_summary` exists and reconciles with CLEAN exactly.
- RAW is untouched: you never ran an UPDATE or DELETE against it.
- You can explain the job of each layer in one sentence, and name which Wednesday concept this maps to.

## Stretch

1. Add `avg_mph` (`trip_distance / (trip_minutes / 60)`) to CLEAN, then decide: does a speed cap belong in the WHERE clause too? Justify the threshold you pick.
2. Build `hourly_taxi_summary` (grain: `pickup_date`, `pickup_hour`). Which of your reconciliation checks still works unchanged, and why?
3. Rebuild CLEAN with your filters removed and count what each rule rejects individually (three counts). Which rule does the most work?
