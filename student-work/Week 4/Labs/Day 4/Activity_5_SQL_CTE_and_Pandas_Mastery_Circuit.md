# Activity 5: SQL, CTE, and pandas Mastery Circuit

**Module:** Week 4 Day 4  
**Estimated Time:** 75 to 110 minutes for the core, plus 30 minutes for transfer practice  
**Difficulty:** Beginner to intermediate  
**Format:** Instructor launch, individual work, then partner explanation  
**Prerequisites:** Day 3 Activities 1 through 3 in progress or complete, Activity 0 complete, and access to your assigned Snowflake schema

## Objective

Use one small, predictable dataset to practice the same business transformations in Snowflake SQL and pandas. You will build CTEs as named intermediate results, inspect each step, and explain what one row represents before moving to the next step.

This is an AI-Free Zone activity. Write and explain your own SQL and pandas code. Use the checkpoints, hints, official documentation, and partner discussion.

## The central idea

Do not begin with, "How do I write a CTE?"

Begin with:

> What intermediate result must exist before the final answer becomes easy?

Use one CTE per meaningful business transformation. Do not create one CTE per SQL keyword.

## Why this dataset lives in your Snowflake schema

The setup creates two small transient tables in your assigned schema:

| Table | One row represents |
|---|---|
| `W4D4_DEMO_CUSTOMERS` | One customer |
| `W4D4_DEMO_ORDERS` | One order placed by a customer |

Transient tables remain available to later Snowflake sessions until they are dropped. That lets Snowsight and the Python connector use the same tables. A temporary table would be visible only in the session that created it.

## Setup

1. Open a Snowsight worksheet. Run the dataset setup below **once** in your own schema. Confirm 8 customers and 21 orders. Stop if `CURRENT_SCHEMA()` is not your personal schema.
2. Keep these tables for the whole activity. The pandas half reads them through a separate Snowflake connection.
3. For Part B, open `Activity_5_Pandas_Mirror.ipynb` and select the repository-root interpreter. If the connector is not installed yet, run this from the repository root: `uv add "snowflake-connector-python[pandas]"`.

Everywhere below, replace `<YOUR_NAME>` with your assigned schema.

### Dataset setup (copy into Snowsight, run once)

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;

SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
-- Stop if the schema is not your own.

CREATE OR REPLACE TRANSIENT TABLE W4D4_DEMO_CUSTOMERS (
  customer_id INTEGER,
  customer_name VARCHAR,
  segment VARCHAR,
  region VARCHAR
);

INSERT INTO W4D4_DEMO_CUSTOMERS (customer_id, customer_name, segment, region) VALUES
  (1, 'Amina', 'Retail', 'North'),
  (2, 'Omar', 'Retail', 'North'),
  (3, 'Lina', 'Retail', 'South'),
  (4, 'Sami', 'Corporate', 'North'),
  (5, 'Noor', 'Corporate', 'South'),
  (6, 'Yara', 'Corporate', 'South'),
  (7, 'Zaid', 'Small Business', 'North'),
  (8, 'Maya', 'Small Business', 'South');

CREATE OR REPLACE TRANSIENT TABLE W4D4_DEMO_ORDERS (
  order_id INTEGER,
  customer_id INTEGER,
  order_date DATE,
  amount NUMBER(10, 2),
  status VARCHAR
);

INSERT INTO W4D4_DEMO_ORDERS (order_id, customer_id, order_date, amount, status) VALUES
  (101, 1, '2026-01-05', 120, 'COMPLETED'),
  (102, 1, '2026-01-12', 180, 'COMPLETED'),
  (103, 1, '2026-01-20', 200, 'COMPLETED'),
  (104, 1, '2026-01-25', 900, 'CANCELLED'),
  (105, 2, '2026-01-06',  90, 'COMPLETED'),
  (106, 2, '2026-01-18', 110, 'COMPLETED'),
  (107, 3, '2026-01-03', 300, 'COMPLETED'),
  (108, 3, '2026-01-10', 250, 'COMPLETED'),
  (109, 3, '2026-01-17', 150, 'COMPLETED'),
  (110, 3, '2026-01-24', 100, 'COMPLETED'),
  (111, 4, '2026-01-08', 400, 'COMPLETED'),
  (112, 4, '2026-01-22', 300, 'COMPLETED'),
  (113, 5, '2026-01-04', 100, 'COMPLETED'),
  (114, 5, '2026-01-14', 150, 'COMPLETED'),
  (115, 5, '2026-01-27', 200, 'COMPLETED'),
  (116, 6, '2026-01-02', 500, 'COMPLETED'),
  (117, 6, '2026-01-15', 600, 'COMPLETED'),
  (118, 6, '2026-01-29', 400, 'COMPLETED'),
  (119, 7, '2026-01-07', 250, 'COMPLETED'),
  (120, 7, '2026-01-16', 250, 'COMPLETED'),
  (121, 7, '2026-01-28', 250, 'COMPLETED');

SELECT
  (SELECT COUNT(*) FROM W4D4_DEMO_CUSTOMERS) AS customer_count,
  (SELECT COUNT(*) FROM W4D4_DEMO_ORDERS) AS order_count;
-- Expected: 8 customers and 21 orders.
```

## Before every multi-step query

Complete this planning frame in a SQL comment:

```text
Final result grain:
Missing metric or concept:
Step 1 CTE name and grain:
Step 2 CTE name and grain:
Step 3 CTE name and grain:
Final combination:
```

During development, use the final `SELECT` as an inspection window:

```sql
WITH customer_totals AS (
  ...
)
SELECT *
FROM customer_totals
ORDER BY customer_id;
```

Point the final `SELECT` at the CTE you are currently testing. Add the next CTE only after the current result has the right columns, row count, and grain.

## Part A: Snowflake SQL drills

| Drill | Business question | Required reasoning |
|---|---|---|
| 1 | Show total completed spending and completed order count for every customer who has a completed order. | One join and one aggregation. Do not use a CTE because one query is already clear. |
| 2 | Create `customer_totals` with one row per customer who has a completed order. | Name the missing customer-level dataset and inspect it. |
| 3 | Keep customers with at least three completed orders. | Add `eligible_customers` after `customer_totals`. |
| 4 | Calculate average customer spending by segment, using only eligible customers. | Add `segment_benchmarks` after eligibility is known. |
| 5 | Find eligible customers whose spending is above their eligible segment average. | Join two prepared datasets at different grains. |
| 6 | Find completed orders whose amount is above that customer's completed-order average. | Calculate one benchmark per customer, then compare order rows with it. |
| 7 | Find segments whose average customer spending is above the overall average customer spending. | Calculate an aggregate of an aggregate. Use customers with at least one completed order. |
| 8 | Find customers who have no completed orders. | Preserve customer rows with a `LEFT JOIN`, then test for a null joined key. |
| 9 | Repair a query that averages orders when the question asks for average customer spending. | Diagnose the wrong grain before changing syntax. |

### SQL drill scaffold (copy into a Snowsight worksheet)

Work top to bottom. Fill in the planning-frame comment before each multi-step query, then write the query beneath its prompt.

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;

-- DRILL 1: One query is enough.
-- Show customer_id, customer_name, segment, completed_order_count, and total_spend
-- for every customer with at least one completed order. Do not use a CTE. Order by customer_id.
-- Final result grain:


-- DRILL 2: Create the customer-level result you wish already existed.
-- Required CTE: customer_totals. Inspect it before moving on.
-- Final result grain / Missing metric / Step 1 CTE name and grain:


-- DRILL 3: Apply the eligibility rule.
-- Required CTEs: customer_totals, eligible_customers (at least three completed orders).


-- DRILL 4: Create the segment benchmark.
-- Required CTEs: customer_totals, eligible_customers, segment_benchmarks
-- Average customer spending per segment, eligible customers only.


-- DRILL 5: Complete the comparison.
-- Find eligible customers whose total spend is above their eligible segment average.
-- Return customer_name, segment, completed_order_count, total_spend,
-- average_segment_spend, amount_above_average. Order by amount_above_average DESC.


-- DRILL 6: Orders above the customer's average completed-order amount.
-- Required CTEs: completed_orders, customer_order_averages.
-- Return order_id, customer_name, amount, average_order_amount.


-- DRILL 7: Segments above the overall customer average.
-- Use customers with at least one completed order.
-- Required CTEs: customer_totals, segment_averages, global_average.


-- DRILL 8: Customers with no completed orders.
-- Use a LEFT JOIN and preserve all customer rows. Return customer_id, customer_name.


-- DRILL 9: Diagnose and repair the wrong grain.
-- The query below averages orders when the question asks for average customer spending.
-- Name the grain of wrong_segment_benchmarks, then rebuild it correctly so it produces
-- the same two above-benchmark customers as Drill 5.
WITH completed_orders AS (
  SELECT c.customer_name, c.segment, o.amount
  FROM W4D4_DEMO_CUSTOMERS AS c
  JOIN W4D4_DEMO_ORDERS AS o ON c.customer_id = o.customer_id
  WHERE o.status = 'COMPLETED'
),
wrong_segment_benchmarks AS (
  SELECT segment, AVG(amount) AS wrong_average
  FROM completed_orders
  GROUP BY segment
)
SELECT * FROM wrong_segment_benchmarks ORDER BY segment;
-- Wrong benchmark grain / Why it is wrong / Corrected query:
```

## SQL checkpoints

### Customer totals for Drills 1 and 2

| customer | segment | completed orders | total spend |
|---|---|---:|---:|
| Amina | Retail | 3 | 500.00 |
| Omar | Retail | 2 | 200.00 |
| Lina | Retail | 4 | 800.00 |
| Sami | Corporate | 2 | 700.00 |
| Noor | Corporate | 3 | 450.00 |
| Yara | Corporate | 3 | 1500.00 |
| Zaid | Small Business | 3 | 750.00 |

The cancelled 900.00 order must not appear in the count or spend.

### Eligibility and benchmarks for Drills 3 through 5

Eligible customers are Amina, Lina, Noor, Yara, and Zaid.

| segment | eligible segment average |
|---|---:|
| Corporate | 975.00 |
| Retail | 650.00 |
| Small Business | 750.00 |

The final above-benchmark answer contains exactly two customers:

| customer | segment | total spend | benchmark | amount above |
|---|---|---:|---:|---:|
| Yara | Corporate | 1500.00 | 975.00 | 525.00 |
| Lina | Retail | 800.00 | 650.00 | 150.00 |

### Independent checkpoints for Drills 6 through 9

- Drill 6 returns 8 completed orders. No order equal to its customer average qualifies.
- Drill 7 uses seven customers with completed orders. The overall average customer spend is 700.00. Corporate and Small Business are above it.
- Drill 8 returns Maya only.
- Drill 9 must produce the same two final customers as Drill 5. If it does not, inspect the row grain used to calculate the segment average.

## Part B: pandas mirror drills

Open `Activity_5_Pandas_Mirror.ipynb` and run the cells top to bottom with the repository-root interpreter. The Snowflake connector loads the two small tables into DataFrames. You write only the transformations in the `# %%`-style cells.

If the connector dependency is not already in the repository-root project, run this from the repository root:

```bash
uv add "snowflake-connector-python[pandas]"
```

Do not run `uv init`. Keep using `<repo-root>/.venv` and the existing root project.

| pandas drill | SQL idea being mirrored | Required DataFrame |
|---|---|---|
| P1 | `WHERE status = 'COMPLETED'` | `completed_orders` |
| P2 | Join, group, and aggregate to customer grain | `customer_totals` |
| P3 | Apply the eligibility business rule | `eligible_customers` |
| P4 | Aggregate eligible customers to segment grain | `segment_benchmarks` |
| P5 | Join prepared datasets and compare | `above_benchmark` |
| P6 | Calculate and join a per-customer order benchmark | `orders_above_customer_average` |
| P7 | Preserve customers and find those without a completed order | `customers_without_completed_orders` |
| P8 | Paste your completed Drill 5 query, fetch its answer, and prove SQL and pandas agree | `sql_answer` plus a parity assertion |

## Expected pandas evidence

- `completed_orders` has 20 rows.
- `customer_totals` has 7 rows.
- `eligible_customers` has 5 rows.
- `segment_benchmarks` has 3 rows.
- `above_benchmark` contains Yara and Lina in that order.
- `orders_above_customer_average` has 8 rows.
- `customers_without_completed_orders` contains Maya only.
- The final parity assertion passes.

## Success Criteria

- You ran the setup only in your assigned schema.
- Every multi-step SQL answer includes the requested planning comment.
- You inspected each CTE before building on it.
- You can say what one row represents in every CTE and DataFrame.
- You distinguish average order amount from average customer spending.
- SQL and pandas return the same two above-benchmark customers.
- You can explain why the Snowflake tables are transient rather than temporary.
- Your editable files remain under `student-work/week4/day4/`.

## Hints

<details>
<summary>Drill 3 filters the wrong rows</summary>

Eligibility is a customer-level rule. Filter `completed_order_count` after `customer_totals` exists, not individual rows in `W4D4_DEMO_ORDERS`.

</details>

<details>
<summary>Drill 5 gives too many or too few customers</summary>

Calculate `segment_benchmarks` from `eligible_customers`, not from raw orders or all customers. Join on `segment`, then compare `total_spend` with `average_segment_spend`.

</details>

<details>
<summary>Drill 7 produces the average order amount</summary>

Your first CTE must create one row per customer. Only then can the next CTE calculate one average customer total per segment.

</details>

<details>
<summary>The pandas merge creates duplicate or confusing column names</summary>

Select only the columns needed from the right-hand DataFrame before merging. Check the join key and print `.columns.tolist()` after the merge.

</details>

<details>
<summary>The connector opens in the wrong schema</summary>

Check the `[DEV]` values in `snow.cfg`, then query `CURRENT_DATABASE()` and `CURRENT_SCHEMA()` through the connection. Do not hardcode a password into the script.

</details>

## Stretch Goals

1. Complete one question from `Activity_3_Snowflake_SQL_Transfer_Drills.md` against TPC-H. Draw its intermediate datasets before writing SQL.
2. Rewrite Drill 5 with nested subqueries only after the CTE version works. Compare which version is easier to inspect.
3. Add a new region benchmark, then find customers above both their segment and region averages.

## Official References

- [Snowflake CTEs](https://docs.snowflake.com/en/user-guide/queries-cte)
- [Snowflake `WITH` clause](https://docs.snowflake.com/en/sql-reference/constructs/with)
- [Snowflake temporary and transient tables](https://docs.snowflake.com/en/user-guide/tables-temp-transient)
- [Snowflake Python connector pandas methods](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-pandas)
