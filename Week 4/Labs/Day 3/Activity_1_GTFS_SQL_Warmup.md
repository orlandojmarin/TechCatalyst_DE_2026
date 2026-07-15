# Activity 1: GTFS SQL Warm-up

**Module:** Week 4 Day 3  
**Estimated Time:** 55 to 70 minutes  
**Difficulty:** Beginner to intermediate  
**Format:** Instructor launch, then pairs  
**Prerequisites:** Activity 0 and access to BigQuery

## Objective

Create three tiny temporary transit tables in a BigQuery session, then practice joins, grouping, `HAVING`, `CASE`, and a CTE. You will also explain how a temporary table differs from a CTE, view, and permanent table.

## What GTFS represents

GTFS, the General Transit Feed Specification, is a common format for public transportation schedules. A real feed contains related text files. This activity uses three of the most important ideas:

| GTFS-style table | One row represents | Connection |
|---|---|---|
| `routes` | One transit route | `route_id` |
| `trips` | One scheduled trip on a route | `route_id`, then `trip_id` |
| `stop_times` | One scheduled stop record within a trip | `trip_id` |

The relationship is `routes` one-to-many `trips`, then `trips` one-to-many `stop_times`. The data is intentionally small, but the relationships match the shape of a real transit schedule.

## BigQuery session setup

A temporary table normally belongs to the query job that creates it. BigQuery session mode allows later query entries in the same editor tab to reuse temporary tables.

1. Open a new BigQuery query tab.
2. Select **More**, then **Query settings**. In some console layouts, select **Edit**, then **Query settings**.
3. Under **Session management**, turn on **Use session mode**.
4. Set the processing location to **US**, then save the settings.
5. Keep this query tab open for the entire activity. A different tab is a different session.
6. Run this check:

   ```sql
   SELECT @@session_id AS session_id;
   ```

   A non-null value confirms that the query is running in a session.

7. Run your copied `gtfs_setup.sql` in this same tab. It creates `routes`, `trips`, and `stop_times` as temporary tables.
8. Confirm one temporary table with:

   ```sql
   SELECT * FROM _SESSION.routes ORDER BY route_short_name;
   ```

9. Open your copied `gtfs_warmup.sql`, paste each answer into the same session tab, and run one statement at a time.

If session mode is unavailable, paste the provided setup above one warm-up query and run the combined text as one multi-statement script. Tell the instructor, because the preferred class workflow is session mode.

## Read the provided setup

The setup contains code such as:

```sql
FROM UNNEST([
  STRUCT('R10' AS route_id, '10' AS route_short_name)
])
```

`STRUCT` is a BigQuery record with named fields. The square brackets create an array of records. `UNNEST` turns the array elements into table rows, with each struct field becoming a column. This is a convenient BigQuery method for creating a tiny inline dataset. It is provided setup code, not a pattern you must memorize today.

In Snowflake, the same tiny-table setup is commonly written with `VALUES`:

```sql
CREATE OR REPLACE TEMP TABLE routes AS
SELECT
  column1::VARCHAR AS route_id,
  column2::VARCHAR AS route_short_name
FROM VALUES
  ('R10', '10'),
  ('R20', '20');
```

The two platforms express the inline rows differently, but both temporary tables last only for the active session.

## Required warm-ups

| Warm-up | Requirement |
|---|---|
| 1 | Return `route_short_name` and `route_long_name`, ordered by the short name. |
| 2 | Join `trips` to `routes`; return the short name, trip ID, and headsign. |
| 3 | Return the number of trips per route. |
| 4 | Return only routes with at least two trips. |
| 5 | Label arrivals before `09:00:00` as `morning_peak` and all others as `later_service`; count records in each bucket. |
| 6 | Create a CTE named `trip_stop_counts`, then return total stop records per route. |

After Warm-up 3, tell your partner what one row in the result represents.

## Expected results

### Warm-up 1

| route_short_name | route_long_name |
|---|---|
| 10 | Downtown Loop |
| 20 | Airport Express |
| 30 | University Connector |

### Warm-up 2

| route_short_name | trip_id | trip_headsign |
|---|---|---|
| 10 | T100 | Downtown clockwise |
| 10 | T101 | Downtown counterclockwise |
| 20 | T200 | Airport terminal |
| 20 | T201 | Airport terminal |
| 30 | T300 | University campus |

### Warm-up 3

| route_short_name | trip_count |
|---|---:|
| 10 | 2 |
| 20 | 2 |
| 30 | 1 |

### Warm-up 4

| route_short_name | trip_count |
|---|---:|
| 10 | 2 |
| 20 | 2 |

### Warm-up 5

| service_bucket | stop_record_count |
|---|---:|
| later_service | 5 |
| morning_peak | 9 |

### Warm-up 6

| route_short_name | route_long_name | total_stop_records |
|---|---|---:|
| 10 | Downtown Loop | 6 |
| 20 | Airport Express | 4 |
| 30 | University Connector | 4 |

Row order can differ unless your query includes the required `ORDER BY`.

## Success criteria

- `@@session_id` returns a value and the three temporary tables remain available in the same query tab.
- You complete all six warm-ups in your own starter file.
- Your outputs match the expected results.
- You can explain both join keys.
- You can explain why `HAVING` filters groups after aggregation.
- You can distinguish the statement scope of a CTE from the session scope of a temporary table.

## Hints

<details>
<summary>Warm-up 2</summary>

Join `trips.route_id` to `routes.route_id`.

</details>

<details>
<summary>Warm-ups 3 and 4</summary>

Join the same two tables, group by `route_short_name`, and count trip rows. Warm-up 4 adds `HAVING COUNT(*) >= 2`.

</details>

<details>
<summary>Warm-up 6</summary>

The CTE should be named `trip_stop_counts` and should contain one row per `trip_id`. Join that result to `trips`, then to `routes`.

</details>

## Stretch goals

- Rewrite Warm-up 6 as a subquery and compare readability.
- Save the Warm-up 6 result in a temporary table, query it in a later statement, then drop it.

## Official references

- [BigQuery sessions](https://cloud.google.com/bigquery/docs/sessions)
- [BigQuery arrays and structs](https://cloud.google.com/bigquery/docs/arrays)
- [Snowflake temporary tables](https://docs.snowflake.com/en/user-guide/tables-temp-transient)
- [Snowflake VALUES](https://docs.snowflake.com/en/sql-reference/constructs/values)
