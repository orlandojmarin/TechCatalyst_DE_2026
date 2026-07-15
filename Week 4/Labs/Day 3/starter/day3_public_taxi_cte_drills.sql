-- Week 4 Day 3 public taxi CTE drills. GoogleSQL.
-- Copy this file to student-work/week4/day3 before editing it.
--
-- Only source:
-- bigquery-public-data.chicago_taxi_trips.taxi_trips
--
-- Fixed date filter for every drill:
-- DATE(trip_start_timestamp) BETWEEN DATE '2023-12-25' AND DATE '2023-12-31'
--
-- Fare filter:
-- Use fare > 0 in Drills 1 through 7 and 9 through 12.
-- Drill 8 intentionally uses all rows in the selected week.
--
-- Company filter:
-- In company-level CTEs, exclude NULL and blank company names with:
-- company IS NOT NULL AND TRIM(company) <> ''


-- =============================================================================
-- CORE DRILLS
-- =============================================================================

-- Drill 1: Weekly positive-fare benchmark
-- Create ONE CTE: base_trips.
-- base_trips grain: one positive-fare trip in the selected week.
-- Final grain: exactly one row for the selected week.
-- Final columns: trip_count, avg_trip_total.
-- Round avg_trip_total to 2 decimals.
-- Expected: 78,715 trips and 26.77 average trip total.

-- Write Drill 1 below:



-- Drill 2: Five companies with the most trips
-- Create TWO CTEs in this order: base_trips, company_metrics.
-- base_trips grain: one positive-fare trip with company and trip_total.
-- company_metrics grain: one named company.
-- Exclude NULL and blank company names in company_metrics.
-- Final columns: company, trip_count, avg_trip_total.
-- Round avg_trip_total to 2 decimals.
-- Order by trip_count DESC, company ASC. Return 5 rows.
-- Final grain:

-- Write Drill 2 below:



-- Drill 3: Companies above the weekly benchmark
-- Create THREE CTEs in this order:
-- base_trips, company_metrics, weekly_average.
-- base_trips grain: one positive-fare trip with company and trip_total.
-- company_metrics grain: one named company.
-- weekly_average grain: exactly one row for the selected week.
-- CROSS JOIN company_metrics to weekly_average in the final query.
-- Keep avg_trip_total > selected_week_avg_total before rounding.
-- Final columns: company, trip_count, avg_trip_total,
-- selected_week_avg_total.
-- Round both averages to 2 decimals.
-- Order by avg_trip_total DESC, company ASC.
-- Expected: 15 rows. The rounded benchmark is 26.77.
-- Final grain:

-- Write Drill 3 below:



-- Drill 4: Company ranking after distance cleanup
-- Create THREE CTEs in this order:
-- base_trips, outlier_free_trips, company_metrics.
-- base_trips grain: one positive-fare trip with company, trip_total,
-- and trip_miles.
-- outlier_free_trips grain: one trip with trip_miles from 0 through 50.
-- company_metrics grain: one named company after distance cleanup.
-- Exclude NULL and blank company names in company_metrics.
-- Final columns: company, trip_count, avg_trip_total.
-- Round avg_trip_total to 2 decimals.
-- Order by trip_count DESC, company ASC. Return 5 rows.
-- Final grain:

-- Write Drill 4 below:



-- Drill 5: Payment-type metrics
-- Create TWO CTEs in this order: base_trips, payment_metrics.
-- base_trips grain: one positive-fare trip with payment and charge fields.
-- payment_metrics grain: one payment_type.
-- Tip-rate formula:
-- SAFE_DIVIDE(SUM(tips), SUM(fare)) * 100
-- Final columns: payment_type, trip_count, total_revenue,
-- safe_tip_rate_percent.
-- Round revenue and tip rate to 2 decimals.
-- Order by trip_count DESC, payment_type ASC.
-- Final grain:

-- Write Drill 5 below:



-- =============================================================================
-- EXTENSION DRILLS
-- =============================================================================

-- Drill 6: Daily metrics
-- CTEs: base_trips, daily_metrics.
-- Use fare > 0.
-- Final columns: trip_date, trip_count, total_revenue, avg_trip_total.
-- Order by trip_date. Expect 7 rows.

-- Write Drill 6 below:



-- Drill 7: Five busiest hours
-- CTEs: base_trips, hourly_demand.
-- Use fare > 0.
-- Extract HOUR from trip_start_timestamp as trip_hour.
-- Final columns: trip_hour, trip_count.
-- Order by trip_count DESC, trip_hour ASC. Return 5 rows.

-- Write Drill 7 below:



-- Drill 8: Completeness check
-- CTEs: base_trips, completeness_check.
-- Do NOT apply fare > 0. Measure all rows in the selected week.
-- Treat NULL or TRIM(value) = '' as missing.
-- Final columns: trip_count, missing_company_count,
-- missing_company_percent, missing_payment_type_count,
-- missing_payment_type_percent.
-- Expect exactly 1 row.

-- Write Drill 8 below:



-- Drill 9: Highest average fares among established companies
-- CTEs: base_trips, company_metrics.
-- Use fare > 0 and exclude NULL or blank company names.
-- company_metrics must keep companies with COUNT(*) >= 100.
-- Final columns: company, trip_count, avg_fare.
-- Order by avg_fare DESC, company ASC. Return 5 rows.

-- Write Drill 9 below:



-- Drill 10: Distance buckets
-- CTEs: base_trips, distance_buckets.
-- Use fare > 0 and trip_miles BETWEEN 0 AND 50.
-- Bucket rules:
-- short: trip_miles < 2
-- medium: trip_miles BETWEEN 2 AND 10
-- long: trip_miles > 10 through 50
-- Final columns: distance_bucket, trip_count, avg_trip_total.
-- Return short, medium, long in that order. Expect 3 rows.

-- Write Drill 10 below:



-- Drill 11: Payment groups
-- CTEs: base_trips, payment_groups.
-- Use fare > 0.
-- Mapping:
-- payment_type containing cash -> Cash
-- payment_type containing credit -> Credit
-- everything else, including NULL -> Other
-- Final columns: payment_group, trip_count, safe_tip_rate_percent.
-- Order by trip_count DESC, payment_group ASC. Expect 3 rows.

-- Write Drill 11 below:



-- Drill 12: First three days versus last four days
-- CTEs: base_trips, period_labeled.
-- Use fare > 0.
-- first_three_days: 2023-12-25 through 2023-12-27
-- last_four_days: 2023-12-28 through 2023-12-31
-- Final columns: period_name, trip_count, total_revenue, avg_trip_total.
-- Return first_three_days, then last_four_days. Expect 2 rows.

-- Write Drill 12 below:

