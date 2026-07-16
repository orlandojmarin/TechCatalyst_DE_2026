# Activity 2: BigQuery Public Taxi CTE Drills

**Module:** Week 4 Day 3  
**Estimated Time:** 60 minutes for core drills, plus extensions  
**Difficulty:** Intermediate  
**Format:** Pairs  
**Prerequisites:** Activity 1 and BigQuery Sandbox access

## Objective

Turn multi-step business questions into readable GoogleSQL by naming each step with a CTE. Every drill uses one source table, so no join to another source table is needed.

## Source and filter contract

Use only this table:

`bigquery-public-data.chicago_taxi_trips.taxi_trips`

Use this seven-day window in every drill:

`DATE(trip_start_timestamp) BETWEEN DATE '2023-12-25' AND DATE '2023-12-31'`

Use `fare > 0` in Drills 1 through 7 and 9 through 12. Drill 8 is the one exception because it measures missing company and payment values across all rows in the selected week.

When a drill reports company results, exclude missing or blank company names in the company-level CTE:

`company IS NOT NULL AND TRIM(company) <> ''`

These rules are part of the activity contract. Do not change the source, dates, or filters when comparing your output with the checkpoints.

## How to complete each drill

1. Copy `starter/day3_public_taxi_cte_drills.sql` to `student-work/week4/day3/`.
2. Write the required CTEs in the stated order.
3. Keep each CTE at the grain stated in the starter comments.
4. While debugging, temporarily replace the final query with `SELECT * FROM cte_name LIMIT 10`.
5. Restore the required final query, ordering, and limit.
6. Write the final grain in the provided SQL comment.
7. Compare your output with the checkpoint.
8. Record BigQuery's byte estimate for at least one query.

## Core drill contract

| Drill | Business question | Required CTEs | Required final output |
|---|---|---|---|
| 1 | How many positive-fare trips occurred, and what was their average trip total? | `base_trips` | One row: `trip_count`, `avg_trip_total`. |
| 2 | Which five named companies completed the most positive-fare trips? | `base_trips`, `company_metrics` | `company`, `trip_count`, `avg_trip_total`. Order by trip count descending, then company ascending. Return 5 rows. |
| 3 | Which named companies had an average trip total above the positive-fare weekly average? | `base_trips`, `company_metrics`, `weekly_average` | `company`, `trip_count`, `avg_trip_total`, `selected_week_avg_total`. Use a `CROSS JOIN` to the one-row benchmark. Order by company average descending, then company ascending. |
| 4 | Which five named companies completed the most trips after removing distance outliers? | `base_trips`, `outlier_free_trips`, `company_metrics` | Keep `trip_miles BETWEEN 0 AND 50`. Return `company`, `trip_count`, `avg_trip_total`. Order by trip count descending, then company ascending. Return 5 rows. |
| 5 | How did trip volume, revenue, and tip rate differ by payment type? | `base_trips`, `payment_metrics` | `payment_type`, `trip_count`, `total_revenue`, `safe_tip_rate_percent`. Order by trip count descending, then payment type ascending. |

## CTE grain hints

| Drill | CTE | One row represents |
|---|---|---|
| 1 to 5 | `base_trips` | One positive-fare taxi trip in the selected week. |
| 2 and 3 | `company_metrics` | One named company. |
| 3 | `weekly_average` | The positive-fare weekly benchmark, exactly one row. |
| 4 | `outlier_free_trips` | One positive-fare trip from 0 through 50 miles. |
| 4 | `company_metrics` | One named company after the distance filter. |
| 5 | `payment_metrics` | One payment type. |

## Expected core results

Small displayed-decimal differences are acceptable if you round at a different stage. Row counts and ordering must match.

### Drill 1

| trip_count | avg_trip_total |
|---:|---:|
| 78715 | 26.77 |

### Drill 2

| company | trip_count | avg_trip_total |
|---|---:|---:|
| Flash Cab | 18116 | 25.04 |
| Taxi Affiliation Services | 15630 | 26.69 |
| Sun Taxi | 8350 | 26.95 |
| Taxicab Insurance Agency Llc | 7235 | 28.73 |
| City Service | 6672 | 26.09 |

### Drill 3

Expect 15 named companies. The final result must include `selected_week_avg_total` so you can prove that every `avg_trip_total` is greater than the benchmark. Rounded to two decimals, the benchmark is `26.77`.

### Drill 4

| company | trip_count | avg_trip_total |
|---|---:|---:|
| Flash Cab | 18110 | 24.99 |
| Taxi Affiliation Services | 15619 | 26.56 |
| Sun Taxi | 8345 | 26.83 |
| Taxicab Insurance Agency Llc | 7232 | 28.68 |
| City Service | 6670 | 26.02 |

### Drill 5

The first five rows by trip count should be:

| payment_type | trip_count | total_revenue | safe_tip_rate_percent |
|---|---:|---:|---:|
| Cash | 27428 | 545133.75 | 0.06 |
| Credit Card | 25793 | 938553.86 | 22.27 |
| Prcard | 11411 | 295393.84 | 0.75 |
| Mobile | 9153 | 206297.93 | 21.06 |
| Unknown | 4871 | 120434.70 | 0.00 |

## Extension drill contract

| Drill | Required CTEs | Exact requirement | Expected shape |
|---|---|---|---|
| 6 | `base_trips`, `daily_metrics` | Return `trip_date`, `trip_count`, `total_revenue`, and `avg_trip_total`. Order by date. | 7 rows |
| 7 | `base_trips`, `hourly_demand` | Use positive-fare trips. Return `trip_hour` and `trip_count` for the five busiest hours. Break ties by hour ascending. | 5 rows |
| 8 | `base_trips`, `completeness_check` | Do not apply the fare filter. Return total rows plus missing company and payment counts and percentages. A blank string counts as missing. | 1 row |
| 9 | `base_trips`, `company_metrics` | Use named companies and positive fares. Keep companies with at least 100 trips. Return the five highest `avg_fare` values with `company` and `trip_count`. | 5 rows |
| 10 | `base_trips`, `distance_buckets` | Use positive fares and distances from 0 through 50. Label trips `short` when under 2 miles, `medium` from 2 through 10 miles, and `long` above 10 through 50 miles. Return bucket, trip count, and average trip total. | 3 rows |
| 11 | `base_trips`, `payment_groups` | Use positive fares. Map payment types containing `cash` to `Cash`, values containing `credit` to `Credit`, and everything else to `Other`. Return group, trip count, and safe tip rate percent. | 3 rows |
| 12 | `base_trips`, `period_labeled` | Use positive fares. Label December 25 through 27 `first_three_days` and December 28 through 31 `last_four_days`. Return period, trip count, total revenue, and average trip total. | 2 rows |

## Success criteria

- Every query uses the stated public table and fixed dates.
- The fare filter is present in every drill except Drill 8.
- Company-level results exclude missing and blank company names.
- Every core query uses the required CTE names and order.
- Final columns, ordering, limits, and row counts match the contract.
- You do not add a source-table join.
- You can state what one row represents in every CTE and final result.
- You can explain why `SAFE_DIVIDE` is safer than the `/` operator for a calculated rate.

## Hints

<details>
<summary>My query returns zero rows or a NULL average</summary>

Confirm that the date filter uses December 25 through December 31, 2023. Do not use 2024.

</details>

<details>
<summary>A later CTE fails</summary>

Temporarily replace the final query with `SELECT * FROM base_trips LIMIT 10`. Test each later CTE one at a time, in definition order.

</details>

<details>
<summary>Drill 3 cannot see the weekly benchmark</summary>

`weekly_average` is defined after `company_metrics`. In the final query, `CROSS JOIN` the one-row `weekly_average` CTE to `company_metrics`, then filter companies above the benchmark.

</details>

<details>
<summary>My tip-rate query could divide by zero</summary>

Use `SAFE_DIVIDE(SUM(tips), SUM(fare)) * 100`. Round only in the final result.

</details>

## Stretch explanation

Choose one completed drill and rewrite it with nested subqueries. Do not replace your CTE answer. Compare the two versions and explain which is easier to test one step at a time.

