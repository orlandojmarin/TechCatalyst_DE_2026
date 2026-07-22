# Activity 4 Solution: Window Functions

Instructor reference. Replace `<YOUR_NAME>` with the student's schema.

Where a question has more than one clean way to solve it, this key shows **Option A** (the most direct approach) and additional options (**Option B**, **Option C**) so students can see the trade-offs. All options are functionally equivalent unless a note says otherwise.

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;
```

---

## W1: Rank trading days by close price, highest = 1

### Option A — DENSE_RANK (no gaps on ties)

```sql
SELECT
  trade_date,
  close_price,
  DENSE_RANK() OVER (ORDER BY close_price DESC) AS price_rank
FROM W5D1_STOCK
ORDER BY price_rank;
```

### Option B — RANK (leaves gaps on ties)

```sql
SELECT
  trade_date,
  close_price,
  RANK() OVER (ORDER BY close_price DESC) AS price_rank
FROM W5D1_STOCK
ORDER BY price_rank;
```

**Why two options?** With this dataset there are no tied close prices, so `DENSE_RANK`, `RANK`, and even `ROW_NUMBER` all return the same result. Ask students: *if two days tied for 2nd place, would the next rank be 3 or 4?* `RANK` skips to 4 (leaves a gap), `DENSE_RANK` continues at 3 (no gap). Pick `DENSE_RANK` when you want ranks to reflect "how many distinct price levels," and `RANK` when the gap itself is meaningful (e.g., matching a leaderboard where ties should visibly cost you position).

---

## W2: Previous close and daily change

### Option A — LAG

```sql
SELECT
  trade_date,
  close_price,
  LAG(close_price) OVER (ORDER BY trade_date) AS prev_close,
  close_price - LAG(close_price) OVER (ORDER BY trade_date) AS daily_change
FROM W5D1_STOCK
ORDER BY trade_date;
```

### Option B — LAG computed once in a CTE, reused by alias

```sql
WITH base AS (
  SELECT
    trade_date,
    close_price,
    LAG(close_price) OVER (ORDER BY trade_date) AS prev_close
  FROM W5D1_STOCK
)
SELECT
  trade_date,
  close_price,
  prev_close,
  close_price - prev_close AS daily_change
FROM base
ORDER BY trade_date;
```

**Why two options?** Option A repeats the same `LAG(...) OVER (...)` twice. Snowflake does not let you reference a `SELECT`-list alias in the same `SELECT`, so Option B moves the window function into a CTE first, then does plain arithmetic on the alias afterward. Same result, but every window expression is written exactly once — this pattern becomes important once queries have five or six window columns (see W6).

---

## W3: Running maximum and running average close

```sql
SELECT
  trade_date,
  close_price,
  MAX(close_price) OVER (ORDER BY trade_date) AS running_max_close,
  ROUND(AVG(close_price) OVER (ORDER BY trade_date), 2) AS running_avg_close
FROM W5D1_STOCK
ORDER BY trade_date;
```

No alternate option needed — the default frame for `ORDER BY` without an explicit `ROWS`/`RANGE` clause is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which is exactly "running from the start through today." Writing the frame out explicitly (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`) is equivalent here and can be shown as an optional, more explicit variant for students who want to see the frame spelled out.

---

## W4: 3-day moving average

```sql
SELECT
  trade_date,
  close_price,
  ROUND(
    AVG(close_price) OVER (
      ORDER BY trade_date
      ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ),
    2
  ) AS moving_avg_3d
FROM W5D1_STOCK
ORDER BY trade_date;
```

Only one clean option — the frame clause `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` is the standard way to express "this row plus the two before it." Note for students: the first two rows will average over fewer than 3 days because there aren't 2 prior rows yet — that's expected, not a bug.

---

## W5: Biggest single-day gain

### Option A — CTE + correlated scalar subquery

```sql
WITH changes AS (
  SELECT
    trade_date,
    close_price - LAG(close_price) OVER (ORDER BY trade_date) AS daily_change
  FROM W5D1_STOCK
)
SELECT trade_date, daily_change
FROM changes
WHERE daily_change = (SELECT MAX(daily_change) FROM changes)
ORDER BY trade_date;
```

### Option B — QUALIFY (Snowflake-specific, no subquery needed)

```sql
WITH changes AS (
  SELECT
    trade_date,
    close_price - LAG(close_price) OVER (ORDER BY trade_date) AS daily_change
  FROM W5D1_STOCK
)
SELECT trade_date, daily_change
FROM changes
QUALIFY daily_change = MAX(daily_change) OVER ()
ORDER BY trade_date;
```

**Why two options?** Option A mixes a window function with a classic subquery in `WHERE` — valid SQL, and portable to any database (Postgres, MySQL, SQL Server included). Option B uses Snowflake's `QUALIFY` clause, which filters directly on a window function result the same way `WHERE` filters on regular columns, and `HAVING` filters on aggregates. `QUALIFY` isn't ANSI standard SQL, but it also works on Databricks, BigQuery, Teradata, and Oracle — so it's safe to teach as the idiomatic choice on any of those platforms, just flag that it won't run on Postgres/MySQL/SQL Server. Both options correctly return two rows: 2024-07-08 and 2024-07-11, each with a +5 gain.

---

## W6: Combine all window functions into a single query

### Option A — Repeat each window expression inline

```sql
SELECT
  trade_date,
  close_price,
  LAG(close_price) OVER (ORDER BY trade_date) AS prev_close,
  close_price - LAG(close_price) OVER (ORDER BY trade_date) AS daily_change,
  ROUND(
    AVG(close_price) OVER (
      ORDER BY trade_date
      ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ),
    2
  ) AS moving_avg_3d,
  MAX(close_price) OVER (ORDER BY trade_date) AS running_max_close,
  ROUND(AVG(close_price) OVER (ORDER BY trade_date), 2) AS running_avg_close,
  DENSE_RANK() OVER (ORDER BY close_price DESC) AS price_rank
FROM W5D1_STOCK
ORDER BY trade_date;
```

### Option B — Compute each window function once in a CTE, then reference aliases

```sql
WITH base AS (
  SELECT
    trade_date,
    close_price,
    LAG(close_price) OVER (ORDER BY trade_date) AS prev_close,
    ROUND(
      AVG(close_price) OVER (
        ORDER BY trade_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
      ), 2
    ) AS moving_avg_3d,
    MAX(close_price) OVER (ORDER BY trade_date) AS running_max_close,
    ROUND(AVG(close_price) OVER (ORDER BY trade_date), 2) AS running_avg_close,
    DENSE_RANK() OVER (ORDER BY close_price DESC) AS price_rank
  FROM W5D1_STOCK
)
SELECT
  trade_date,
  close_price,
  prev_close,
  close_price - prev_close AS daily_change,
  moving_avg_3d,
  running_max_close,
  running_avg_close,
  price_rank
FROM base
ORDER BY trade_date;
```

**Why two options?** Option A is the most literal answer — every drill's window expression pasted into one `SELECT`. It works, but `LAG(close_price) OVER (ORDER BY trade_date)` is computed twice (once as its own column, once to derive `daily_change`), which is easy to typo and wasteful to read. Option B computes every window function exactly once inside a CTE, then does the plain-arithmetic `daily_change` calculation on the alias afterward. Same output, fewer places for a copy-paste mistake, and it reinforces the two-step "window first, then arithmetic" habit from W2 Option B.

---

## Part B: TPC-H stretch (window over an aggregate)

```sql
USE SCHEMA SNOWFLAKE_SAMPLE_DATA.TPCH_SF1;
```

### S1: Grand total of sales on every yearly row

```sql
SELECT
  YEAR(o_orderdate) AS order_year,
  COUNT(*) AS num_orders,
  SUM(o_totalprice) AS tot_sales,
  SUM(SUM(o_totalprice)) OVER () AS grand_total
FROM orders
GROUP BY order_year
ORDER BY order_year;
```

Only one option shown here — this is the cleanest way to express "an aggregate, plus a total-of-totals repeated on every row." The key idea for students: `GROUP BY` runs first and collapses rows to one per year, then the outer `OVER ()` window (with no `PARTITION BY`) treats the entire already-grouped result as a single window and sums across it.

### S2: Top 3 months by total sales within each year

### Option A — RANK with QUALIFY (Snowflake-specific)

```sql
WITH monthly AS (
  SELECT
    YEAR(o_orderdate) AS order_year,
    MONTH(o_orderdate) AS order_month,
    COUNT(*) AS num_orders,
    SUM(o_totalprice) AS tot_sales
  FROM orders
  GROUP BY order_year, order_month
)
SELECT
  order_year,
  order_month,
  num_orders,
  tot_sales,
  RANK() OVER (PARTITION BY order_year ORDER BY tot_sales DESC) AS month_rank
FROM monthly
QUALIFY month_rank <= 3
ORDER BY order_year, month_rank;
```

### Option B — RANK with a filtering CTE (portable to any database)

```sql
WITH monthly AS (
  SELECT
    YEAR(o_orderdate) AS order_year,
    MONTH(o_orderdate) AS order_month,
    COUNT(*) AS num_orders,
    SUM(o_totalprice) AS tot_sales
  FROM orders
  GROUP BY order_year, order_month
),
ranked AS (
  SELECT
    order_year,
    order_month,
    num_orders,
    tot_sales,
    RANK() OVER (PARTITION BY order_year ORDER BY tot_sales DESC) AS month_rank
  FROM monthly
)
SELECT *
FROM ranked
WHERE month_rank <= 3
ORDER BY order_year, month_rank;
```

**Why two options?** Option B is the "textbook" pattern: rank in one CTE, filter with a plain `WHERE` in the next step — this is the safest pattern to teach first because it works identically on Postgres, MySQL, SQL Server, BigQuery, Databricks, etc. Option A collapses the final filter step using Snowflake's `QUALIFY`, avoiding the extra CTE layer. Once students are comfortable with Option B, introduce Option A as "the Snowflake shortcut."

> **Note on S2:** the 2025 reference solution ranked `ORDER BY tot_sales` (ascending), which returned the *bottom* three months instead of the top three. Both options above use `ORDER BY tot_sales DESC` — always sanity-check rank direction against the question wording ("top" vs. "bottom").
> **Tie caveat:** `RANK()` can return more than 3 rows per year if there's a 4-way (or more) tie for 3rd place, since ties share the same rank. That's expected, textbook-correct behavior — flag it for students so a surprising row count doesn't look like a bug.
