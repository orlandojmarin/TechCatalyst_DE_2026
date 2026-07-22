# Activity 3 Solution: From RAW to CLEAN to FINAL

Run the setup block from the activity. Column names assume the Activity 2 raw table; if the two datetime columns landed as NUMBER (raw parquet microseconds), swap in the `TO_TIMESTAMP(col::NUMBER, 6)` variants shown in the comments.

## Task 1: Build CLEAN

```sql
CREATE OR REPLACE TRANSIENT TABLE clean_yellow_taxi AS
SELECT
    vendorid::INT                                   AS vendorid,
    tpep_pickup_datetime                            AS pickup_at,
    tpep_dropoff_datetime                           AS dropoff_at,
    -- If the raw columns are NUMBER microseconds, use these instead:
    -- TO_TIMESTAMP(tpep_pickup_datetime::NUMBER, 6)  AS pickup_at,
    -- TO_TIMESTAMP(tpep_dropoff_datetime::NUMBER, 6) AS dropoff_at,
    COALESCE(passenger_count::INT, 1)               AS passenger_count,
    trip_distance,
    pulocationid::INT                               AS pulocationid,
    dolocationid::INT                               AS dolocationid,
    payment_type::INT                               AS payment_type,

    -- Date features
    DATE(tpep_pickup_datetime)                      AS pickup_date,
    HOUR(tpep_pickup_datetime)                      AS pickup_hour,
    DAYNAME(tpep_pickup_datetime)                   AS pickup_dow,
    DAYNAME(tpep_pickup_datetime) IN ('Sat', 'Sun') AS is_weekend,
    TIMESTAMPDIFF('minute', tpep_pickup_datetime, tpep_dropoff_datetime) AS trip_minutes,

    -- Money, consolidated
    fare_amount,
    tip_amount,
    COALESCE(extra, 0)
      + COALESCE(mta_tax, 0)
      + COALESCE(improvement_surcharge, 0)
      + COALESCE(congestion_surcharge, 0)
      + COALESCE(airport_fee, 0)                    AS total_surcharges,
    total_amount
FROM raw_yellow_tripdata_parquet
WHERE trip_distance > 0
  AND TIMESTAMPDIFF('minute', tpep_pickup_datetime, tpep_dropoff_datetime) > 0;
```

Notes worth saying out loud when reviewing:

- `COALESCE` before summing the surcharges: one NULL surcharge would otherwise null the whole consolidation. This is the same fill-what-a-rule-authorizes idea as everywhere else this week; each COALESCE encodes "absent means zero", which is a business claim, not a syntax choice.
- The physics filters repeat the `TIMESTAMPDIFF` expression rather than referencing `trip_minutes`, because a column alias is not visible in its own `WHERE` clause. If that repetition offends, this is a legitimate two-step build (CTE for the derivation, then filter); with exactly one reused expression, inline is still the simpler correct form.
- The `airport_fee` column is `Airport_fee` in some source files; Snowflake's case-insensitive resolution handles it unless the raw table was created with quoted identifiers.

Checkpoint 2 returns 0 by construction. Checkpoint 1's difference is the count of zero-distance and nonpositive-duration rows the filters rejected.

## Task 2: Build FINAL

```sql
CREATE OR REPLACE TRANSIENT TABLE daily_taxi_summary AS
SELECT
    pickup_date,
    COUNT(*)                                        AS total_trips,
    ROUND(SUM(total_amount), 2)                     AS total_revenue,
    ROUND(AVG(fare_amount), 2)                      AS avg_fare,
    ROUND(AVG(IFF(fare_amount > 0, tip_amount / fare_amount, NULL)) * 100, 1) AS avg_tip_pct,
    COUNT_IF(is_weekend)                            AS weekend_trips
FROM clean_yellow_taxi
GROUP BY pickup_date
ORDER BY pickup_date;
```

Notes:

- The tip percentage guards the division (`fare_amount > 0`) and passes NULL, not 0, for unguardable rows: a zero would drag the average down with fake data, a NULL simply sits out of the AVG. Same guard-then-derive habit as the fare-per-mile drill.
- `COUNT_IF(is_weekend)` works because `is_weekend` is a real BOOLEAN; `SUM(IFF(is_weekend, 1, 0))` is the equivalent spelling.

Checkpoint 2 must be an exact match: every CLEAN row belongs to exactly one date, so the sum of daily trips is the row count. If it ever disagreed, the summary (the most recently derived layer) is the suspect, per the debug-backward rule.

## Task 3: sample answers

1. Rebuild CLEAN and FINAL from RAW with the fixed logic. RAW is never re-downloaded; being able to say that is the entire argument for keeping it.
2. Safe because RAW retains every column, so nothing is lost, only omitted from the working copy. It becomes unsafe the day someone treats CLEAN as the archive and deletes RAW.
3. CLEAN is presumed right: FINAL is derived from it, so a mismatch means the derivation (or a stale rebuild order) broke. Verify by rebuilding FINAL from the current CLEAN and re-checking.
4. Nothing reruns itself, nothing validates itself, and nothing stops a half-updated state from being read: no scheduling, no dependency order, no gates. Lakeflow Jobs (Wednesday) and dbt's `build` (Thursday) exist precisely to close those gaps.

## Stretch notes

1. `trip_distance / (trip_minutes / 60) AS avg_mph`, and yes, a cap belongs in the filters; 100 mph is the defensible classroom threshold (it returns Wednesday in the Spark ETL with the same justification).
2. The FINAL-to-CLEAN reconciliation survives unchanged at the hourly grain: summing trips over a finer grain still counts every CLEAN row exactly once. The days-in-month check does not survive; the grain changed.
3. Typical distribution: the zero-distance rule does most of the work, nonpositive duration a distant second; exact counts vary with the month's file.
