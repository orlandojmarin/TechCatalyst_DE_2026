# Week 4 Day 3 Resources

This is an AI-Free Zone. Use documentation, notes, and partner discussion. Do not use an AI assistant to write the SQL.

## Core Documentation

| Resource | Why it helps |
|---|---|
| [BigQuery sessions](https://cloud.google.com/bigquery/docs/sessions) | Enable one query tab to retain temporary objects across query entries. |
| [BigQuery arrays and structs](https://cloud.google.com/bigquery/docs/arrays) | Understand the provided `STRUCT` and `UNNEST` GTFS setup. |
| [GoogleSQL query syntax](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax) | Review CTEs, joins, grouping, and query order. |
| [BigQuery Sandbox](https://cloud.google.com/bigquery/docs/sandbox) | Check quotas and features that are unavailable without billing. |
| [BigQuery views](https://cloud.google.com/bigquery/docs/views-intro) | Compare logical, materialized, and authorized view patterns. |
| [Snowflake temporary and transient tables](https://docs.snowflake.com/en/user-guide/tables-temp-transient) | Compare temporary, transient, and permanent table behavior. |
| [Snowflake views](https://docs.snowflake.com/en/user-guide/views-introduction) | Review standard, secure, and materialized views. |
| [Snowflake TPC-H sample data](https://docs.snowflake.com/en/user-guide/sample-data-tpch) | Understand the read-only source used in the transfer lab. |

## Decision guide

| Need | First choice |
|---|---|
| Name a step inside one statement | CTE |
| Embed one small one-time calculation | Subquery |
| Reuse stored intermediate rows during one session | Temporary table |
| Reuse a current query across sessions | View |
| Preserve stored rows or create a target table | CTAS |

## Platform boundaries

| Platform | Today’s safe work |
|---|---|
| BigQuery Sandbox | Public-data `SELECT`, CTEs, joins, aggregates, sessions, and temporary tables. Do not use DML. |
| SQLite | `CREATE TABLE`, `INSERT INTO`, CTAS, and views in your local database. |
| Snowflake | Read fully qualified sample tables and create tables, temporary tables, CTAS tables, and views only in your assigned `TECHCATALYST` schema. |

## Manual visualization boundary

Activity 3 adds a chart only after your SQL is complete and validated. You may manually choose the chart type, category, metric, sorting, labels, and title. Do not use a natural-language prompt, generated SQL, Auto-Chart, or generated Insights during Week 4. Your team must write its own interpretation.

If the classroom BigQuery interface opens [data canvas](https://docs.cloud.google.com/bigquery/docs/data-canvas), paste your completed SQL into a SQL node, run it, and configure the visualization manually. The visualization node supports bar charts and PNG export. If the feature is unavailable, follow the chart-sketch fallback in Activity 3.

## Lab Deliverable Checklist

| Complete | Item |
|---|---|
| [ ] | I enabled BigQuery session mode and confirmed `@@session_id`. |
| [ ] | My six GTFS outputs match the posted results. |
| [ ] | My five taxi CTE outputs use the verified 2023 week. |
| [ ] | My team completed one equally scoped two-CTE business query and five-row validation. |
| [ ] | My team created a manual chart and separated evidence, interpretation, recommendation, and limitation. |
| [ ] | I can choose among a subquery, CTE, temporary table, view, and CTAS table. |
| [ ] | I completed the SQLite-to-Snowflake DDL comparison if my schema was available. |
| [ ] | Every Snowflake object I created is in my assigned schema. |
| [ ] | I kept all authored work under `student-work/week4/day3/`. |

Currentness checked: July 15, 2026.
