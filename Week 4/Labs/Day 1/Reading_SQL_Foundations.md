---
title: "SQL Foundations for DataFrame Thinkers"
module: "Week 4 Day 1"
type: explainer
audience: "TechCatalyst Data Engineering learners"
---

# SQL Foundations for DataFrame Thinkers

## Why This Matters

Every warehouse, lakehouse, and analytics platform you will touch for the rest of this course speaks SQL: SQLite today, BigQuery and DuckDB midweek, Snowflake from Thursday on, and Spark SQL in Week 5. Pandas is your tool when data lives in files and memory. SQL is your tool when data lives in tables and the engine does the heavy lifting. A data engineer needs both, and needs to know when each one is the right reach.

## Tables Are Strict DataFrames

A relational table looks like a DataFrame, with three habits that make it stricter:

- Every column has a declared type, and the database enforces it (SQLite is famously relaxed here; the warehouses later this week are not).
- Rows have no meaningful order until you ask for one with `ORDER BY`. There is no index like pandas.
- Tables live inside schemas, and schemas live inside databases. Think folders for tables.

A primary key is a column (or combination) that uniquely identifies each row, like `claim_id`. Tomorrow we use keys to connect tables to each other. Today, one table at a time.

## Anatomy of a Query

```sql
SELECT state, COUNT(*) AS claim_count   -- which columns, and any calculations
FROM claims                             -- which table
WHERE claim_type = 'auto'               -- which rows to keep, before grouping
GROUP BY state                          -- how to group the kept rows
HAVING COUNT(*) >= 2                    -- which groups to keep
ORDER BY claim_count DESC               -- how to sort the result
LIMIT 10;                               -- how many rows to show
```

You write it top to bottom, but the engine thinks about it in a different order: `FROM`, then `WHERE`, then `GROUP BY`, then `HAVING`, then `SELECT`, then `ORDER BY`, then `LIMIT`. Two practical consequences:

1. `WHERE` cannot see aggregate results, because filtering happens before grouping. Filtering groups is `HAVING`'s job.
2. Column aliases from `SELECT` are not reliably available in `WHERE` (they are made late in the process).

## The Pandas Dictionary

| pandas | SQL | Notes |
|---|---|---|
| `df[["a", "b"]]` | `SELECT a, b` | Ask for exactly the columns you need |
| `df["a"].unique()` | `SELECT DISTINCT a` | Deduplicated values |
| `df.rename(columns={"a": "x"})` on output | `SELECT a AS x` | Aliases are display names |
| `df[df["a"] > 5]` | `WHERE a > 5` | Comparison operators are the same idea |
| `df[df["a"].isin([1, 2])]` | `WHERE a IN (1, 2)` | Membership |
| `df[df["a"].between(1, 9)]` | `WHERE a BETWEEN 1 AND 9` | Inclusive on both ends |
| `df[df["s"].str.contains("ob")]` | `WHERE s LIKE '%ob%'` | `%` is any run of characters, `_` is one |
| `df[df["a"].isna()]` | `WHERE a IS NULL` | Never `= NULL`; see below |
| `df.sort_values("a", ascending=False)` | `ORDER BY a DESC` | Default is ascending |
| `df.head(10)` | `LIMIT 10` | Only trims the display of the result |
| `df["a"] * 2` as a new column | `SELECT a * 2 AS doubled` | Calculated columns |
| `df.groupby("g")["a"].mean()` | `SELECT g, AVG(a) ... GROUP BY g` | One output row per group |
| `len(df)` | `SELECT COUNT(*)` | Rows, including nulls |
| filter after groupby (`.loc` on the result) | `HAVING` | Filter on the grouped result |
| `np.where(cond, x, y)` | `CASE WHEN cond THEN x ELSE y END` | Conditional column |

## NULL: The One Real Newcomer

`NULL` means "no value recorded". It is not zero, not an empty string, and not equal to anything, including another `NULL`. That is why `WHERE amount = NULL` matches nothing and the correct spelling is `WHERE amount IS NULL` (or `IS NOT NULL`). Aggregates like `AVG` and `SUM` skip nulls; `COUNT(*)` counts rows, while `COUNT(amount)` counts only non-null values. When those two counts differ, you just learned something about your data.

## WHERE vs HAVING, One More Time

`WHERE` filters rows before they are grouped. `HAVING` filters groups after aggregation. If the condition mentions an aggregate (`COUNT(*) > 900`, `AVG(x) < 3`), it belongs in `HAVING`. If it mentions plain column values (`state = 'CT'`), it belongs in `WHERE`, and putting it there is also cheaper: fewer rows reach the grouping step.

## CASE Makes Categories

```sql
SELECT
  CASE
    WHEN income < 35000 THEN 'Low'
    WHEN income <= 50000 THEN 'Medium'
    ELSE 'High'
  END AS income_group,
  COUNT(*) AS people
FROM individual
GROUP BY income_group;
```

Conditions are checked top to bottom and the first match wins, exactly like an `if/elif/else` chain.

## Habits Worth Starting Today

- Name the question in a comment above every query. Queries are evidence; label the evidence.
- Select only needed columns. On SQLite it is politeness; on BigQuery and Snowflake it is money.
- Read the result and ask "what does one row represent?" before trusting it.
- When a count surprises you, check your `WHERE` clause before blaming the data.

## Key Takeaways

SQL describes the result you want and the engine figures out how. You already know the concepts from pandas; today is new notation, not new thinking. The clauses have a fixed logical order, `NULL` needs `IS NULL`, row filters go in `WHERE`, group filters go in `HAVING`, and `CASE` builds categories. Tomorrow: connecting tables with keys and joins.
