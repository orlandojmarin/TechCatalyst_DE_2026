# Activity 6: Retail SQL and pandas Parallel Circuit

**Module:** Week 4 Day 4  
**Estimated Time:** 70 to 100 minutes for the core, plus optional stretch  
**Difficulty:** Beginner to intermediate  
**Format:** Instructor launch, individual work, then partner explanation  
**Prerequisites:** Activity 5 core complete or in progress, Activity 0 complete, and access to your assigned Snowflake schema

## Objective

Practice the same business logic twice on one small retail dataset: once in Snowflake SQL and once in pandas. This is a second pass at CTEs on a fresh domain (stores and regions instead of customers and segments), followed by a side-by-side window circuit that shows how SQL clauses and pandas methods map to each other.

This is an AI-Free Zone activity. Write and explain your own SQL and pandas code. Use the checkpoints, hints, official documentation, and partner discussion.

## The central idea

You saw the "named intermediate result" method in Activity 5. Today you prove it was not about customers. It was about a way of thinking:

> Build the table you wish already existed, inspect it, then build the next one on top of it.

Then in Part B you see the punchline of the whole week:

> pandas and SQL are the same thinking. `GROUP BY` is `groupby`. A window frame is `.rolling`. `LAG` is `.shift`. `CASE` is a Python function.

## Why this dataset lives in your Snowflake schema

The setup creates two small transient tables in your assigned schema:

| Table | One row represents |
|---|---|
| `W4D4_STORES` | One store and its region |
| `W4D4_SALES` | One sale of one product on one day |

Transient tables persist across Snowflake sessions until dropped, so Snowsight and the Python connector read the exact same 20 rows. That is what lets the pandas parity check line up with your SQL.

## Setup

1. Open a Snowsight worksheet. Run the dataset setup below **once** in your own schema. Confirm 5 stores and 20 sales rows. Stop if `CURRENT_SCHEMA()` is not your personal schema.
2. Work Part A, then the SQL half of Part B, in a Snowsight worksheet.
3. For the pandas half of Part B, open `Activity_6_Pandas_Parallel.ipynb` with the repository-root interpreter. It reads the same tables through the `snow.cfg` connection you completed in Activity 0.

Everywhere below, replace `<YOUR_NAME>` with your assigned schema.

### Dataset setup (copy into Snowsight, run once)

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;

SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
-- Stop if the schema is not your own.

CREATE OR REPLACE TRANSIENT TABLE W4D4_STORES (
  store_id INTEGER,
  store_name VARCHAR,
  region VARCHAR
);

INSERT INTO W4D4_STORES (store_id, store_name, region) VALUES
  (1, 'A', 'East'),
  (2, 'B', 'East'),
  (3, 'C', 'West'),
  (4, 'D', 'West'),
  (5, 'E', 'West');

CREATE OR REPLACE TRANSIENT TABLE W4D4_SALES (
  sale_id INTEGER,
  store_name VARCHAR,
  product VARCHAR,
  sale_date DATE,
  sales NUMBER(10, 2)
);

INSERT INTO W4D4_SALES (sale_id, store_name, product, sale_date, sales) VALUES
  (1,  'A', 'APPLES',  '2024-07-01', 100),
  (2,  'A', 'APPLES',  '2024-07-03', 130),
  (3,  'A', 'APPLES',  '2024-07-05', 120),
  (4,  'A', 'ORANGES', '2024-07-02', 150),
  (5,  'A', 'ORANGES', '2024-07-04', 105),
  (6,  'B', 'APPLES',  '2024-07-01', 200),
  (7,  'B', 'APPLES',  '2024-07-04', 210),
  (8,  'B', 'ORANGES', '2024-07-02', 110),
  (9,  'B', 'ORANGES', '2024-07-03', 110),
  (10, 'B', 'ORANGES', '2024-07-05',  90),
  (11, 'C', 'APPLES',  '2024-07-01',  90),
  (12, 'C', 'APPLES',  '2024-07-03',  95),
  (13, 'C', 'ORANGES', '2024-07-02',  80),
  (14, 'C', 'ORANGES', '2024-07-04',  70),
  (15, 'D', 'APPLES',  '2024-07-02', 160),
  (16, 'D', 'APPLES',  '2024-07-05', 200),
  (17, 'D', 'ORANGES', '2024-07-01',  60),
  (18, 'D', 'ORANGES', '2024-07-03', 140),
  (19, 'E', 'APPLES',  '2024-07-05',  40),
  (20, 'E', 'ORANGES', '2024-07-05',  30);

SELECT
  (SELECT COUNT(*) FROM W4D4_STORES) AS store_count,
  (SELECT COUNT(*) FROM W4D4_SALES) AS sales_count;
-- Expected: 5 stores and 20 sales rows.
```

### SQL drill scaffold (copy into a Snowsight worksheet)

Part A is the CTE ladder. Part B is the SQL half of the parallel circuit; each drill has a twin cell in `Activity_6_Pandas_Parallel.ipynb`.

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;

-- ===== PART A: CTE ladder (store to region) =====

-- A1: One query is enough. store_name, region, transaction_count, total_sales per store.
-- Join W4D4_STORES to W4D4_SALES. No CTE. Order by store_name.

-- A2: Create store_totals (one row per store). Inspect it.

-- A3: eligible_stores = store_totals with at least four transactions.

-- A4: region_benchmarks = average store total per region, eligible stores only.

-- A5: Eligible stores above their eligible region average.
--     Return store_name, region, total_sales, region_avg_sales, amount_above_average.

-- A6: Regions whose average store total beats the overall average store total (all stores with a sale).

-- A7: Repair a query that averages raw sale rows per region instead of store totals per region.
WITH region_sale_rows AS (
  SELECT st.region, s.sales
  FROM W4D4_STORES AS st
  JOIN W4D4_SALES AS s ON st.store_name = s.store_name
),
wrong_region_benchmarks AS (
  SELECT region, AVG(sales) AS wrong_average
  FROM region_sale_rows
  GROUP BY region
)
SELECT * FROM wrong_region_benchmarks ORDER BY region;
-- Name the grain, then rebuild correctly using store_totals (East should be the only region above).

-- ===== PART B: window parallel circuit =====

-- B1: product_daily_sales = one row per product per day, daily_sales = SUM(sales).

-- B2: Add a 3-day moving average per product:
--     AVG(daily_sales) OVER (PARTITION BY product ORDER BY sale_date
--                            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW). Round to 2.

-- B3: Add prev_day_sales per product with LAG over the same partition and order.

-- B4: Rank sales within each store, highest first, using DENSE_RANK.

-- B5: For each sale: product_avg_sales = AVG(sales) OVER (PARTITION BY product),
--     sales_diff_from_avg = sales - that average (round 2), high_sales = sales > 100.

-- B6: sales_bin via CASE (< 100 Low, <= 200 Medium, else High), then one row per bin with a count.

-- B7: Store summary: total_sales, average_sale (round 2), highest_sale, lowest_sale per store.
```

## Part A: Second CTE ladder (store to region)

Same method as Activity 5. Complete the planning frame in a SQL comment before each multi-step query.

| Drill | Business question | Required reasoning |
|---|---|---|
| A1 | Show transaction count and total sales for every store. | One join and one aggregation. No CTE needed. |
| A2 | Create `store_totals`, one row per store. | Name the store-level dataset and inspect it. |
| A3 | Keep stores with at least four transactions. | Add `eligible_stores`. A 2-sale store should not set a benchmark. |
| A4 | Average store total per region, eligible stores only. | Add `region_benchmarks` after eligibility is known. |
| A5 | Find eligible stores above their eligible region average. | Join two prepared datasets at different grains. |
| A6 | Find regions whose average store total beats the overall average store total. | Aggregate of an aggregate. Use all stores with a sale. |
| A7 | Repair a query that averages sale rows when the question asks for average store total. | Diagnose the wrong grain before changing syntax. |

### Part A checkpoints

`store_totals`:

| store | region | transactions | total sales |
|---|---|---:|---:|
| A | East | 5 | 605.00 |
| B | East | 5 | 720.00 |
| C | West | 4 | 335.00 |
| D | West | 4 | 560.00 |
| E | West | 2 | 70.00 |

- Eligible stores (at least four transactions): A, B, C, D. Store E drops out.
- Eligible region benchmarks: East 662.50, West 447.50.
- Drill A5 above-benchmark answer, in order:

| store | region | total sales | region average | amount above |
|---|---|---:|---:|---:|
| D | West | 560.00 | 447.50 | 112.50 |
| B | East | 720.00 | 662.50 | 57.50 |

- Drill A6: the overall average store total is 458.00. East (662.50) is above it. West (321.67) is not. The answer is East only.
- Drill A7: the wrong benchmark has one row per region but averages raw sale rows. The corrected query reuses `store_totals` and returns East only, matching A6.

## Part B: SQL window circuit and its pandas twin

Write each Part B drill in SQL first, then complete the matching cell in `Activity_6_Pandas_Parallel.ipynb`. The table below is the Rosetta Stone for the week.

| Drill | Business question | SQL tool | pandas twin |
|---|---|---|---|
| B1 | One row per product per day. | `GROUP BY product, sale_date` | `groupby(["product","sale_date"]).agg(...)` |
| B2 | Three-day moving average per product. | `AVG(...) OVER (... ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` | `.rolling(3, min_periods=1).mean()` |
| B3 | Previous-day sales per product. | `LAG(daily_sales) OVER (...)` | `.shift(1)` |
| B4 | Rank sales within each store. | `DENSE_RANK() OVER (PARTITION BY store ...)` | `.rank(method="dense", ascending=False)` |
| B5 | Each sale versus its product average. | `AVG(sales) OVER (PARTITION BY product)` | `groupby("product")["sales"].transform("mean")` |
| B6 | Bin each sale Low, Medium, High. | `CASE WHEN ...` | a Python function with `.apply` |
| B7 | Store summary of total, average, max, min. | `GROUP BY store` | `groupby("store_name").agg(...)` |

### Part B checkpoints

`product_daily_sales` (Drill B1):

| product | 07-01 | 07-02 | 07-03 | 07-04 | 07-05 |
|---|---:|---:|---:|---:|---:|
| APPLES | 390 | 160 | 225 | 210 | 360 |
| ORANGES | 60 | 340 | 250 | 175 | 120 |

- Drill B2 moving average, APPLES: 390.00, 275.00, 258.33, 198.33, 265.00. ORANGES: 60.00, 200.00, 216.67, 255.00, 181.67.
- Drill B3 previous day, APPLES: null, 390, 160, 225, 210. ORANGES: null, 60, 340, 250, 175.
- Drill B4: in store B the two 110 sales share rank 3, and the 90 sale is rank 4 (dense rank leaves no gap).
- Drill B5 product averages: APPLES 134.50, ORANGES 94.50. Example: the APPLES sale of 100 has `sales_diff_from_avg` of -34.50.
- Drill B6 bins: Low 8, Medium 11, High 1. The only High row is the 210 sale.
- Drill B7 store summary:

| store | total | average | highest | lowest |
|---|---:|---:|---:|---:|
| A | 605 | 121.00 | 150 | 100 |
| B | 720 | 144.00 | 210 | 90 |
| C | 335 | 83.75 | 95 | 70 |
| D | 560 | 140.00 | 200 | 60 |
| E | 70 | 35.00 | 40 | 30 |

## Expected pandas evidence

- `store_totals` has 5 rows, `eligible_stores` has 4, `region_benchmarks` has 2.
- `above_benchmark` is `["D", "B"]` in that order.
- `product_daily_sales` has 10 rows.
- The bin counts are Low 8, Medium 11, High 1.
- The final parity assertion passes: pandas and SQL both return `["D", "B"]`.

## Success Criteria

- You ran the setup only in your assigned schema.
- Every Part A multi-step answer includes the planning comment.
- You can state what one row represents in each CTE and each DataFrame.
- You changed the level to product-day before applying the window functions.
- For each Part B drill, you can point to the SQL tool and its pandas twin.
- SQL and pandas return the same two above-benchmark stores.
- Your editable files remain under `student-work/week4/day4/`.

## Hints

<details>
<summary>Drill A3 filters the wrong rows</summary>

Eligibility is a store-level rule. Filter `transaction_count` after `store_totals` exists, not individual rows in `W4D4_SALES`.

</details>

<details>
<summary>My moving average does not match the checkpoint</summary>

The window must be partitioned by product and ordered by `sale_date`. In pandas, sort `product_daily_sales` by product and date before the grouped `.rolling(3, min_periods=1)`. Without `min_periods=1` the first two rows become null instead of a partial average.

</details>

<details>
<summary>My ranks skip numbers on ties</summary>

Use `DENSE_RANK` in SQL and `method="dense"` in pandas. Plain `RANK` and the default pandas method leave a gap after a tie.

</details>

<details>
<summary>The bin counts are off by one</summary>

Check the boundaries. A sale of exactly 100 is Medium, and exactly 200 is Medium. Only sales strictly above 200 are High.

</details>

## Stretch Goals

1. Add a product dimension question: which product has the highest total sales in each region? Draw the intermediate tables first.
2. Rewrite Drill A5 with nested subqueries only after the CTE version works, then compare which one you would rather debug at 2 a.m.
3. In pandas, reproduce Drill B4 with `.groupby(...).rank()` and also with `.sort_values(...)` plus `cumcount()`. Explain which is closer to `DENSE_RANK`.

## Official References

- [Snowflake CTEs](https://docs.snowflake.com/en/user-guide/queries-cte)
- [Snowflake window functions](https://docs.snowflake.com/en/sql-reference/functions-analytic)
- [Snowflake LAG](https://docs.snowflake.com/en/sql-reference/functions/lag)
- [pandas window operations](https://pandas.pydata.org/docs/user_guide/window.html)
- [pandas groupby](https://pandas.pydata.org/docs/user_guide/groupby.html)
