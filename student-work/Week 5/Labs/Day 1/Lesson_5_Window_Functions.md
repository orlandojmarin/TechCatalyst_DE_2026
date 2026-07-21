# Lesson 5: Window Functions and Why `GROUP BY` Is Not Enough

**Module:** Week 5, Day 5  
**Format:** Self-study lesson  
**Platform:** Snowflake  
**Dataset:** A small temporary table named `sales_demo`

---

## What you will learn

SQL already has `GROUP BY`, so why do we need window functions?

The short answer is that `GROUP BY` summarizes rows by collapsing them, while a window function can calculate totals, rankings, and comparisons **without removing the original rows**.

By the end of this lesson, you will be able to:

- Explain the difference between `GROUP BY` and a window function.
- Use `OVER()` to calculate a value across all rows.
- Use `PARTITION BY` to create separate calculation groups.
- Use `ORDER BY` inside `OVER(...)` to define a sequence.
- Calculate running totals with `SUM(...) OVER(...)`.
- Rank rows with `ROW_NUMBER()`.
- Compare a row with the previous row using `LAG()`.
- Combine grouped aggregates and window functions in the same query.

## How to use this lesson

Work through the sections in order. Run every query in Snowflake and inspect the result before continuing.

Whenever you see **Pause and predict**, stop before running the query. Try to predict:

1. How many rows the query will return.
2. Which columns will appear.
3. Whether any values will repeat.

Making a prediction first will help you understand the result instead of simply observing it.

---

## 0. Set up the practice data

You will use a small dataset so that you can reason about every row without being distracted by data volume.

Run the following SQL:

```sql
CREATE OR REPLACE TEMPORARY TABLE sales_demo (
  region         VARCHAR,
  salesperson    VARCHAR,
  order_date     DATE,
  order_id       INTEGER,
  order_amount   NUMBER
);

INSERT INTO sales_demo (region, salesperson, order_date, order_id, order_amount)
VALUES
  ('EAST',  'Alice', '2024-01-01', 101, 100),
  ('EAST',  'Alice', '2024-01-03', 102, 250),
  ('EAST',  'Bob',   '2024-01-02', 103, 300),
  ('WEST',  'Cara',  '2024-01-01', 201, 200),
  ('WEST',  'Cara',  '2024-01-05', 202, 150),
  ('WEST',  'Dave',  '2024-01-03', 203, 400);
```

Because this is a temporary table, it is available only during your current Snowflake session.

Check the data:

```sql
SELECT *
FROM sales_demo
ORDER BY region, salesperson, order_date;
```

You should see six orders:

- Three orders in the `EAST` region.
- Three orders in the `WEST` region.
- Two orders for Alice.
- One order for Bob.
- Two orders for Cara.
- One order for Dave.

If you do not see six rows, rerun the setup code before continuing.

---

## 1. What `GROUP BY` does well

Suppose you need to answer this question:

> What is the total order amount for each region?

This is a classic `GROUP BY` problem:

```sql
SELECT
  region,
  SUM(order_amount) AS region_total
FROM sales_demo
GROUP BY region
ORDER BY region;
```

The result contains two rows:

| region | region_total |
| --- | ---: |
| EAST | 650 |
| WEST | 750 |

SQL grouped the six original rows by `region`, then reduced each group to one total.

This is the defining behavior of `GROUP BY`:

> `GROUP BY` changes the level of detail in the result.

The source table contains one row per order. The result contains one row per region. The individual order IDs, dates, and amounts are no longer visible.

### Adding another grouping column

Run this query:

```sql
SELECT
  region,
  salesperson,
  SUM(order_amount) AS total_amount
FROM sales_demo
GROUP BY region, salesperson
ORDER BY region, salesperson;
```

The result now contains one row per `(region, salesperson)` combination. It still does not contain one row per order.

You could add `order_id` and `order_date` to the `GROUP BY`, but doing that would change the grouping level again. It would not solve the real problem if your goal is to preserve each order and attach a regional total to it.

### Check your understanding

Why can you not add `order_id` directly to the first query's `SELECT` list?

<details>
<summary>Check your answer</summary>

After grouping by `region`, each result row represents many orders. SQL cannot choose one `order_id` to display for the entire region. A selected column must normally be part of the grouping key or be passed to an aggregate function.

</details>

---

## 2. Window functions preserve row-level detail

Now suppose the requirement changes:

> Show every order and display the grand total beside each order.

This requires two levels of information in the same result:

- Row-level information, such as `order_id` and `order_amount`.
- Summary information, such as the total of all orders.

A window function can provide both:

```sql
SELECT
  region,
  salesperson,
  order_id,
  order_amount,
  SUM(order_amount) OVER () AS grand_total
FROM sales_demo
ORDER BY order_id;
```

### How to read the expression

Break this expression into two parts:

```sql
SUM(order_amount) OVER ()
```

- `SUM(order_amount)` tells SQL which calculation to perform.
- `OVER()` tells SQL to perform it as a window function.
- The empty parentheses mean that all rows belong to one window.

The query returns all six orders. Each row receives the same `grand_total` value: `1400`.

Compare it with a normal aggregate:

```sql
SELECT
  SUM(order_amount) AS grand_total
FROM sales_demo;
```

This query returns only one row because it summarizes the table.

The difference is the presence of `OVER()`:

| Expression | Result shape |
| --- | --- |
| `SUM(order_amount)` | One summarized row |
| `SUM(order_amount) OVER()` | Every original row, with the total attached |

### The central idea

> `GROUP BY` collapses rows. A window function adds context to rows.

### Pause and predict

Before running the next query, predict its row count and the values in `avg_order_amount`:

```sql
SELECT
  order_id,
  order_amount,
  AVG(order_amount) OVER () AS avg_order_amount
FROM sales_demo
ORDER BY order_id;
```

<details>
<summary>Check your prediction</summary>

The query returns six rows. The average is approximately `233.33`, and it is repeated on every row.

</details>

---

## 3. Use `PARTITION BY` to create separate windows

An empty `OVER()` uses all rows as one window. You can divide the rows into smaller windows with `PARTITION BY`.

Consider this requirement:

> Show every order and display the total for that order's region.

Run the query:

```sql
SELECT
  region,
  salesperson,
  order_id,
  order_amount,
  SUM(order_amount) OVER (
    PARTITION BY region
  ) AS region_total
FROM sales_demo
ORDER BY region, order_id;
```

`PARTITION BY region` divides the rows into two independent windows:

- An `EAST` window containing three orders.
- A `WEST` window containing three orders.

The sum is calculated separately inside each window. Every `EAST` row receives `650`, while every `WEST` row receives `750`.

The query still returns six rows because a window function does not collapse them.

### `GROUP BY` compared with `PARTITION BY`

| Query pattern | Row count | Level of detail |
| --- | ---: | --- |
| `GROUP BY region` | 2 | One row per region |
| `OVER(PARTITION BY region)` | 6 | One row per order |

`GROUP BY` and `PARTITION BY` may describe similar groups, but they do not produce the same result shape.

### Your turn

Write a query that keeps every order and attaches the salesperson's total sales to it.

<details>
<summary>View one solution</summary>

```sql
SELECT
  salesperson,
  order_id,
  order_amount,
  SUM(order_amount) OVER (
    PARTITION BY salesperson
  ) AS salesperson_total
FROM sales_demo
ORDER BY salesperson, order_id;
```

Alice's rows should show `350`, Cara's rows should show `350`, Bob's row should show `300`, and Dave's row should show `400`.

</details>

---

## 4. Use `ORDER BY` inside `OVER(...)` to define sequence

So far, the order of rows has not affected the calculation. That changes when you need a result such as a running total.

Consider this requirement:

> For each salesperson, show how their sales accumulate over time.

Run this query:

```sql
SELECT
  region,
  salesperson,
  order_date,
  order_id,
  order_amount,
  SUM(order_amount) OVER (
    PARTITION BY salesperson
    ORDER BY order_date, order_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM sales_demo
ORDER BY salesperson, order_date, order_id;
```

### Read the window from top to bottom

```sql
PARTITION BY salesperson
```

Create a separate calculation window for each salesperson.

```sql
ORDER BY order_date, order_id
```

Arrange each salesperson's rows chronologically. `order_id` acts as a tie-breaker if two orders have the same date.

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

For each row, include every row from the beginning of the salesperson's partition through the current row.

This is called the **window frame**. It is what makes the sum cumulative.

For Alice, the calculation progresses like this:

| order_date | order_amount | running_total |
| --- | ---: | ---: |
| 2024-01-01 | 100 | 100 |
| 2024-01-03 | 250 | 350 |

For Cara, the running total starts again because she belongs to a different partition:

| order_date | order_amount | running_total |
| --- | ---: | ---: |
| 2024-01-01 | 200 | 200 |
| 2024-01-05 | 150 | 350 |

### Two different `ORDER BY` clauses

Notice that the query contains two `ORDER BY` clauses:

1. `ORDER BY` inside `OVER(...)` controls the sequence used by the window calculation.
2. `ORDER BY` at the end controls how the final rows are displayed.

They serve different purposes. The final `ORDER BY` does not define the running total.

### Pause and predict

What would this query calculate if you removed the `ORDER BY` and window frame from `OVER(...)`?

```sql
SUM(order_amount) OVER (
  PARTITION BY salesperson
)
```

<details>
<summary>Check your answer</summary>

It would calculate each salesperson's complete total and repeat it on all of that salesperson's rows. It would no longer be a running total because there would be no sequence or frame ending at the current row.

</details>

### Memory aid

> `PARTITION BY` answers Which rows belong together?
> `ORDER BY` answers In what sequence should SQL process them?
> The frame answers Which rows in that sequence should affect this row?

---

## 5. Rank rows with `ROW_NUMBER()`

Not all window functions are aggregates. Some assign a position to each row.

Consider this requirement:

> Rank orders from highest to lowest amount within each region.

```sql
SELECT
  region,
  salesperson,
  order_date,
  order_id,
  order_amount,
  ROW_NUMBER() OVER (
    PARTITION BY region
    ORDER BY order_amount DESC, order_id
  ) AS row_num_in_region
FROM sales_demo
ORDER BY region, row_num_in_region;
```

### How it works

- `PARTITION BY region` restarts the numbering in each region.
- `ORDER BY order_amount DESC` places the highest amount first.
- `order_id` provides a consistent tie-breaker.
- `ROW_NUMBER()` assigns a unique sequence: `1`, `2`, `3`, and so on.

The highest order in `EAST` receives `1`. The highest order in `WEST` also receives `1` because the numbering restarts for each partition.

### `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`

These functions behave differently when values are tied:

| Function | Example for values `400, 300, 300, 200` |
| --- | --- |
| `ROW_NUMBER()` | `1, 2, 3, 4` |
| `RANK()` | `1, 2, 2, 4` |
| `DENSE_RANK()` | `1, 2, 2, 3` |

Use:

- `ROW_NUMBER()` when every row must receive a unique position.
- `RANK()` when tied rows should share a rank and gaps are acceptable.
- `DENSE_RANK()` when tied rows should share a rank without creating gaps.

Our current data does not contain tied order amounts within a region, so all three functions would currently produce the same numbers.

---

## 6. Compare rows with `LAG()` and `LEAD()`

Window functions can also retrieve values from nearby rows.

- `LAG()` looks backward.
- `LEAD()` looks forward.

These functions are especially useful when working with time-based data.

### Compare each order with the previous order

Run this query:

```sql
SELECT
  region,
  salesperson,
  order_date,
  order_id,
  order_amount,
  LAG(order_amount) OVER (
    PARTITION BY salesperson
    ORDER BY order_date, order_id
  ) AS previous_order_amount
FROM sales_demo
ORDER BY salesperson, order_date, order_id;
```

For each salesperson, `LAG(order_amount)` retrieves the amount from the preceding row in chronological order.

The first order in every salesperson's partition has no previous order, so its `previous_order_amount` is `NULL`.

### Calculate the change from the previous order

You can use the previous value in a calculation:

```sql
SELECT
  region,
  salesperson,
  order_date,
  order_id,
  order_amount,
  LAG(order_amount) OVER (
    PARTITION BY salesperson
    ORDER BY order_date, order_id
  ) AS previous_order_amount,
  order_amount
    - LAG(order_amount) OVER (
        PARTITION BY salesperson
        ORDER BY order_date, order_id
      ) AS change_from_previous
FROM sales_demo
ORDER BY salesperson, order_date, order_id;
```

Alice's second order is `150` higher than her first. Cara's second order is `50` lower than her first.

### Why the partition matters

If you remove `PARTITION BY salesperson`, SQL treats all orders as one sequence. A salesperson's first order could then be compared with an order belonging to someone else.

The query might still run, but the result would answer a differentâ€”and probably incorrectâ€”business question.

### Your turn

Modify the previous query to display the **next** order amount for each salesperson.

<details>
<summary>View one solution</summary>

```sql
SELECT
  salesperson,
  order_date,
  order_id,
  order_amount,
  LEAD(order_amount) OVER (
    PARTITION BY salesperson
    ORDER BY order_date, order_id
  ) AS next_order_amount
FROM sales_demo
ORDER BY salesperson, order_date, order_id;
```

The last order for each salesperson will have `NULL` in `next_order_amount` because there is no later row in that partition.

</details>

---

## 7. Apply a window function after `GROUP BY`

`GROUP BY` and window functions are not competitors. A query can use both when you need information at more than one level.

Consider this reporting requirement:

> Show one row per region, its subtotal, the grand total, and its percentage of all sales.

Start with one row per region:

```sql
SELECT
  region,
  SUM(order_amount) AS region_sales_subtotal
FROM sales_demo
GROUP BY region
ORDER BY region;
```

Now add a window calculation over those grouped rows:

```sql
SELECT
  region,
  SUM(order_amount) AS region_sales_subtotal,
  SUM(SUM(order_amount)) OVER () AS grand_total_sales,
  ROUND(
    100.0 * SUM(order_amount)
    / SUM(SUM(order_amount)) OVER (),
    2
  ) AS pct_of_total_sales
FROM sales_demo
GROUP BY region
ORDER BY region;
```

The result should be:

| region | region_sales_subtotal | grand_total_sales | pct_of_total_sales |
| --- | ---: | ---: | ---: |
| EAST | 650 | 1400 | 46.43 |
| WEST | 750 | 1400 | 53.57 |

### Understand `SUM(SUM(...)) OVER()`

The nested expression can look confusing at first:

```sql
SUM(SUM(order_amount)) OVER ()
```

Read it from the inside out:

1. `SUM(order_amount)` works with `GROUP BY region` and produces each region's subtotal.
2. The outer `SUM(...) OVER()` operates on those subtotal rows.
3. `OVER()` uses all grouped rows as one window and repeats the grand total on each region row.

This does not double-count the original orders. Each order contributes once to a regional subtotal, and each regional subtotal contributes once to the grand total.

### A CTE version

If the nested expression feels difficult to read, split the work into two logical steps:

```sql
WITH region_summary AS (
  SELECT
    region,
    SUM(order_amount) AS region_sales_subtotal
  FROM sales_demo
  GROUP BY region
)
SELECT
  region,
  region_sales_subtotal,
  SUM(region_sales_subtotal) OVER () AS grand_total_sales,
  ROUND(
    100.0 * region_sales_subtotal
    / SUM(region_sales_subtotal) OVER (),
    2
  ) AS pct_of_total_sales
FROM region_summary
ORDER BY region;
```

Both versions produce the same result.

- The single-query version is compact.
- The CTE version separates the grouped calculation from the window calculation and may be easier to test or extend.

Neither version is automatically better. Choose the structure that makes the logic easiest to understand and maintain.

---

## 8. Decide which tool to use

Use `GROUP BY` when you want to reduce many rows into fewer summary rows.

Examples:

- One row per region.
- One row per customer.
- One row per month.
- One row per product category.

Use a window function when you want to keep the current rows and add information about their context.

Examples:

- A total attached to every row.
- A running total.
- A ranking within a group.
- A previous or next value.
- A percentage of a grand total.

Use both when you first need to change the level of detail and then compare the summarized rows.

### A useful decision question

Ask yourself:

> Should the result contain fewer rows than the input, or should it preserve the current row detail?

- If it should contain fewer summary rows, begin with `GROUP BY`.
- If it should preserve the current rows, consider a window function.

### Window function template

Most window expressions follow this pattern:

```sql
function_name(column_name) OVER (
  PARTITION BY grouping_column
  ORDER BY sequencing_column
  window_frame
)
```

Not every function needs every part:

- Use `OVER()` when all rows should belong to one window.
- Add `PARTITION BY` when the calculation should restart by group.
- Add `ORDER BY` when position or sequence matters.
- Add a frame when you need to define exactly which ordered rows participate in the calculation.

---

## 9. Independent practice

Try each task before viewing the solution.

### Practice 1: Company average on every row

Show every order and attach the average order amount across the company.

<details>
<summary>View solution</summary>

```sql
SELECT
  order_id,
  salesperson,
  order_amount,
  AVG(order_amount) OVER () AS company_avg_order_amount
FROM sales_demo
ORDER BY order_id;
```

</details>

### Practice 2: Regional average on every row

Show every order and attach the average order amount for its region.

<details>
<summary>View solution</summary>

```sql
SELECT
  region,
  order_id,
  order_amount,
  AVG(order_amount) OVER (
    PARTITION BY region
  ) AS region_avg_order_amount
FROM sales_demo
ORDER BY region, order_id;
```

</details>

### Practice 3: Order sequence by salesperson

Number each salesperson's orders from earliest to latest.

<details>
<summary>View solution</summary>

```sql
SELECT
  salesperson,
  order_date,
  order_id,
  ROW_NUMBER() OVER (
    PARTITION BY salesperson
    ORDER BY order_date, order_id
  ) AS order_sequence
FROM sales_demo
ORDER BY salesperson, order_sequence;
```

</details>

### Practice 4: Difference from the company average

Show each order and calculate how far it is above or below the company average.

<details>
<summary>View solution</summary>

```sql
SELECT
  order_id,
  order_amount,
  AVG(order_amount) OVER () AS company_avg_order_amount,
  order_amount - AVG(order_amount) OVER () AS difference_from_avg
FROM sales_demo
ORDER BY order_id;
```

A positive difference means the order is above average. A negative difference means it is below average.

</details>

---

## 10. Final knowledge check

Answer these questions without running SQL first.

1. What is the main difference between `GROUP BY region` and `OVER(PARTITION BY region)`?
2. What does an empty `OVER()` mean?
3. Why does a running total need an ordering rule?
4. Why does the first row in a partition usually return `NULL` for `LAG()`?
5. When might you use `GROUP BY` and a window function in the same query?

<details>
<summary>Review the answers</summary>

1. `GROUP BY region` returns one row per region. `OVER(PARTITION BY region)` preserves the current rows and calculates separately within each region.
2. All available rows belong to one window.
3. SQL needs a defined sequence to know which rows come before the current row.
4. There is no preceding row inside that partition.
5. Use both when you first need grouped summary rows and then need calculations across those summaries, such as a grand total or percentage of total.

</details>

---

## Lesson summary

You can now use SQL at two different levels of detail:

- `GROUP BY` summarizes and collapses rows.
- Window functions preserve rows and add context.

Remember this sentence:

> A window function answers: â€œFor this row, what is true about the other rows in its group or sequence?â€

The core patterns from this lesson are:

```sql
-- Total across all rows
SUM(value) OVER ()

-- Total within each group
SUM(value) OVER (PARTITION BY group_column)

-- Running total within each group
SUM(value) OVER (
  PARTITION BY group_column
  ORDER BY sequence_column
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

-- Position within each group
ROW_NUMBER() OVER (
  PARTITION BY group_column
  ORDER BY sort_column DESC
)

-- Previous value within each group
LAG(value) OVER (
  PARTITION BY group_column
  ORDER BY sequence_column
)
```

If these patterns make sense, you are ready to continue to more advanced window frames, ranking functions, moving averages, and filtering window results with Snowflake's `QUALIFY` clause.