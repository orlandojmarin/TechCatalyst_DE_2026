-- Week 4 Day 3 GTFS warm-up starter
-- GoogleSQL for BigQuery.
-- Enable BigQuery session mode, run gtfs_setup.sql, then run all six answers
-- in the same BigQuery query editor tab.
-- This file intentionally contains no completed query.

-- Available tables and columns:
-- routes(route_id, route_short_name, route_long_name, route_type)
-- trips(trip_id, route_id, service_id, trip_headsign)
-- stop_times(trip_id, stop_sequence, arrival_time, stop_id)

-- ---------------------------------------------------------------------------
-- Warm-up 1: Routes ordered by route name
-- ---------------------------------------------------------------------------
-- TODO: Return route_short_name and route_long_name, ordered by route_short_name.
-- Write your complete SELECT statement below this line.


-- ---------------------------------------------------------------------------
-- Warm-up 2: Trip headsigns with route names
-- ---------------------------------------------------------------------------
-- TODO: Join trips to routes. Return route_short_name, trip_id, and trip_headsign.
-- Write your complete SELECT statement below this line.


-- ---------------------------------------------------------------------------
-- Warm-up 3: Number of trips per route
-- ---------------------------------------------------------------------------
-- TODO: Return one row per route_short_name with trip_count.
-- Write your complete SELECT statement below this line.


-- ---------------------------------------------------------------------------
-- Warm-up 4: Routes with at least 2 trips
-- ---------------------------------------------------------------------------
-- TODO: Use GROUP BY and HAVING.
-- Write your complete SELECT statement below this line.


-- ---------------------------------------------------------------------------
-- Warm-up 5: Stop-time bucket
-- ---------------------------------------------------------------------------
-- TODO: Use CASE to label rows as morning_peak when arrival_time is before 09:00:00.
-- Return service_bucket and stop_record_count.
-- Write your complete SELECT statement below this line.


-- ---------------------------------------------------------------------------
-- Warm-up 6: CTE route stop counts
-- ---------------------------------------------------------------------------
-- TODO: Create one CTE named trip_stop_counts.
-- First count stop records per trip. Then join to trips and routes.
-- Return route_short_name, route_long_name, and total_stop_records.
-- Write your complete WITH query below this line.
