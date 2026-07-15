---
title: "CTEs, Subqueries, Temporary Tables, Views, and CTAS"
module: "Week 4 Day 3"
type: explainer
audience: "TechCatalyst Data Engineering learners"
---

# CTEs, Subqueries, Temporary Tables, Views, and CTAS

## Begin with the result

Before choosing a SQL feature, write this sentence:

> One row in my result represents __________.

The answer is the result grain. A readable query makes the source, filters, named steps, and final grain visible.

## Choose the smallest useful tool

| Tool | Scope | Stores rows? | Good choice when |
|---|---|---:|---|
| Subquery | One statement | No | A small, one-time calculation is easiest to read next to where it is used. |
| CTE | One statement | No | You want to name, test, or reuse a logical step inside one statement. |
| Temporary table | One session | Yes | Several statements need the same intermediate rows or you want to inspect a pipeline step. |
| View | Until dropped | No | People need a reusable, current query result across sessions. |
| CTAS table | Until dropped | Yes | You need stored rows as a snapshot or downstream target. |

A CTE is not automatically faster than a subquery. Its first purpose is clarity. A temporary table can improve repeated work because later statements read stored intermediate rows, but writing and storing those rows also has a cost.

## CTE and subquery comparison

This scalar subquery calculates one benchmark:

```sql
SELECT company, avg_trip_total
FROM company_metrics
WHERE avg_trip_total > (
  SELECT AVG(trip_total)
  FROM base_trips
);
```

The same idea can use a named one-row CTE:

```sql
WITH weekly_average AS (
  SELECT AVG(trip_total) AS benchmark
  FROM base_trips
)
SELECT company, avg_trip_total
FROM company_metrics
CROSS JOIN weekly_average
WHERE avg_trip_total > benchmark;
```

Use the first when the calculation is short and obvious. Use the second when the benchmark deserves a name, must be tested, or will be referenced more than once.

## BigQuery temporary tables and sessions

BigQuery session mode groups multiple query entries into one session. Temporary tables, temporary functions, and session variables can remain available to later queries in the same editor tab.

```sql
SELECT @@session_id AS session_id;

CREATE TEMP TABLE selected_routes AS
SELECT 'R10' AS route_id, 'Downtown Loop' AS route_name;

SELECT * FROM _SESSION.selected_routes;
```

Turn on **Use session mode** in Query settings before running the first statement. Keep the query tab open. Closing the tab ends the session, and temporary objects are removed when the session ends. If you run a multi-statement script without session mode, its temporary tables are reliable inside that script, but a separate query job should not be expected to retain them.

## BigQuery STRUCT and UNNEST

BigQuery can place named records in an array, then turn them into rows:

```sql
SELECT route_id, route_name
FROM UNNEST([
  STRUCT('R10' AS route_id, 'Downtown Loop' AS route_name),
  STRUCT('R20' AS route_id, 'Airport Express' AS route_name)
]);
```

`STRUCT` creates a record with fields. `UNNEST` expands the array to rows. This is GoogleSQL syntax, not portable standard SQL. Snowflake usually expresses the same tiny inline setup with `VALUES`.

## Views and table types across platforms

### BigQuery

- A logical view stores a query definition and is read-only.
- A materialized view stores precomputed results and refreshes them under platform rules and SQL restrictions.
- An authorized view is an access pattern that shares selected results without granting direct access to the source tables.
- Common table choices include managed tables, temporary tables, external or BigLake tables, snapshots, and clones.

BigQuery Sandbox supports the query work in this lesson, including CTEs and temporary setup. Sandbox limitations include no DML, no streaming, and automatic expiration rules for persistent sandbox objects. Use Snowflake or SQLite for today’s `INSERT INTO` practice.

### Snowflake

- A standard view stores a query definition.
- A secure view limits some optimizer details and is used when data exposure is a concern.
- A materialized view stores maintained results and requires an eligible Snowflake edition.
- Permanent tables are the default and include Fail-safe protection.
- Transient tables persist until dropped but omit Fail-safe.
- Temporary tables are visible only in their creating session and are purged when that session ends.

Day 3 uses permanent CTAS tables, standard views, and temporary tables inside your assigned schema. Day 4 goes deeper into Snowflake-specific objects and loading.

## Freshness test

Suppose a source table has five open claims. You run CTAS and create a view, then insert a sixth open claim.

- The CTAS table still has the five rows captured when it was created.
- The view returns six because it reruns its saved query against the current source.
- A temporary table behaves like stored rows too, but it lasts only for the session.

## Review checklist

1. What does one final row represent?
2. Does the question need one table or a join?
3. Would a short subquery be clear enough?
4. Does a logical step deserve a CTE name?
5. Will several later statements reuse the rows?
6. Must the result survive the session?
7. Must the result stay current or preserve a snapshot?
8. Who should be allowed to query it?

## Official references

- [BigQuery sessions](https://cloud.google.com/bigquery/docs/sessions)
- [BigQuery multi-statement queries](https://cloud.google.com/bigquery/docs/multi-statement-queries)
- [BigQuery views](https://cloud.google.com/bigquery/docs/views-intro)
- [BigQuery tables](https://cloud.google.com/bigquery/docs/tables-intro)
- [Snowflake temporary and transient tables](https://docs.snowflake.com/en/user-guide/tables-temp-transient)
- [Snowflake views](https://docs.snowflake.com/en/user-guide/views-introduction)

Currentness checked: July 15, 2026.
