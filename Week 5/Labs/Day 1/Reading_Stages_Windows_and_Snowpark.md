# Reading: Stages, Window Functions, and Snowpark

This explainer supports Week 5 Day 1. Read it before or alongside the activities.

## 1. Stages and file formats

Loading data into Snowflake has three separate pieces, and keeping them separate is the whole point.

- A **stage** is a named pointer to files in storage (here, an approved S3 location through a storage integration). The stage does not hold rows; it points at files.
- A **file format** is a parsing contract: how to read a file. CSV needs a delimiter and a header rule; JSON needs to know it is JSON; Parquet already carries a typed schema. You name the format once and reuse it.
- `COPY INTO` is the command that reads staged files through a file format and loads rows into a table.

Two habits that keep loads trustworthy:

- **Name the exact file** you are loading (`FILES = ('taxi_zone_lookup.csv')`), never a whole bucket prefix. That prevents loading the wrong month or an unexpected file.
- **Keep raw JSON in a `VARIANT` column** first, then flatten the fields you need with path syntax (`payload:batch_id::VARCHAR`). You keep the original shape and can adapt when a new key appears.

Why three formats behave differently:

| Format | Strength | Risk |
|---|---|---|
| CSV | Simple, universal, easy to exchange | No embedded schema; parsing depends on conventions |
| JSON | Preserves named and changing fields | Consumers must handle paths and types |
| Parquet | Typed, columnar, compact | Period and quality still need validation after load |

## 2. Window functions

`GROUP BY` collapses many rows into one summary row. A **window function** keeps every row and adds a value computed over a related set of rows. You describe that set with `OVER (PARTITION BY ... ORDER BY ... frame)`.

- `PARTITION BY` splits rows into groups, but the rows stay.
- `ORDER BY` inside `OVER` orders rows within each partition. Ranking, `LAG`/`LEAD`, and running totals all need it.
- A **frame** such as `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` limits the window to nearby rows, which is how moving averages work.

The three families you will use most:

1. **Ranking**: `ROW_NUMBER` (unique 1, 2, 3), `RANK` (ties share a rank, then a gap), `DENSE_RANK` (ties share a rank, no gap).
2. **Neighbor comparison**: `LAG` (previous row) and `LEAD` (next row), for daily change, previous value, or next value.
3. **Accumulation**: an aggregate with an `ORDER BY` window, for a running total, running maximum, or moving average.

A window function can also wrap an aggregate. `SUM(SUM(sales)) OVER ()` gives a grand total on every grouped row. That is how you show a total next to each group without a second query.

Rule of thumb: if the question keeps every row but adds context from other rows (rank, previous value, running total), reach for a window function. If it truly collapses rows into one summary, `GROUP BY` is enough.

## 3. Snowpark

In Week 4 you connected to Snowflake with the Python connector and used `write_pandas` to push a DataFrame up through a stage and `COPY INTO`. That pattern pulls data to your machine, works on it in pandas, then pushes results back.

**Snowpark** is a different approach. It is a DataFrame API (Python, Java, or Scala) where the DataFrame operations run **inside Snowflake's compute**, not on your laptop. You write DataFrame-style code, and Snowpark translates it to SQL that Snowflake executes. The data does not leave Snowflake until you ask for it.

A small Python example (conceptual):

```python
from snowflake.snowpark import Session

session = Session.builder.configs(params).create()

orders = session.table("ORDERS")
result = (
    orders
    .group_by("O_ORDERSTATUS")
    .agg({"O_TOTALPRICE": "sum"})
)
result.show()          # runs in Snowflake
pdf = result.to_pandas()  # pull the small result to the client only when you need it
```

When to reach for each:

| You want to | Use |
|---|---|
| Move a local DataFrame into a Snowflake table | Python connector plus `write_pandas` |
| Transform large data that already lives in Snowflake, without moving it | Snowpark |
| Do rich, local, single-machine Python or ML on modest data | pandas or Polars |
| Process data too big for one machine, in a cluster | Spark (Databricks), later this week |

The through-line for the week: SQL, Snowpark, and Spark are all ways to express the same transformations. Pick the one that fits where the data lives and how big it is. Snowpark keeps the work in Snowflake; Spark (next) distributes it across a cluster.

## References

- [Snowflake stages](https://docs.snowflake.com/en/user-guide/data-load-overview)
- [COPY INTO table](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table)
- [Window functions](https://docs.snowflake.com/en/sql-reference/functions-analytic)
- [Snowpark Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
