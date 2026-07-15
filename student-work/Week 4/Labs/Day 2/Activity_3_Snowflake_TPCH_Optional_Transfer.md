# Activity 3: Snowflake SQL Transfer Drills

**Module:** Week 4 Day 2  
**Estimated Time:** 75 to 105 minutes  
**Difficulty:** Beginner to Intermediate  
**Format:** Individual work with partner validation  
**Prerequisites:** Day 2 core join work complete and instructor-provided Snowflake access

**For ERD Diagram** you can reference this page https://docs.snowflake.com/en/user-guide/sample-data-tpch 

## Objective

Apply the SQL habits you developed in SQLite and BigQuery to Snowflake. You will progress from one-table retrieval to multi-table analysis using joins, grouping, and `HAVING`. The SQL reasoning transfers. The session setup commands are specific to Snowflake.

This is a read-only lab. Query `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1`. Do not create tables, stages, views, or other objects.

## What You Will Write

The starter contains Snowflake session setup and 15 empty drill sections. You write every `SELECT` statement.

| Tier | Drills | Focus | Target |
|---|---:|---|---|
| A: Foundation | 1 to 5 | Filter, sort, calculate, group, and summarize | Complete first |
| B: Relationships | 6 to 10 | Join tables and answer business questions | Core target |
| C: Challenge | 11 to 13 | Follow longer relationship paths and validate grain | Continue if ready |
| D: Intermediate Extension | 14 to 15 | Grouped join analysis without nested queries | Fast-finisher lane |

## Setup

1. Copy `starter/w4d2_snowflake_tpch_transfer.sql` to `student-work/week4/day2/`.
2. Open the copied file in Snowsight Workspaces.
3. Replace `<INSTRUCTOR_WAREHOUSE>` with the warehouse name your instructor provides.
4. Run only the setup section first. Confirm that the current schema is `TPCH_SF1`.
5. Complete the drills in order. Run and check each query before moving on.

## Relationship Map

Use the question and required columns to decide which tables are necessary. Do not add a table unless it contributes a required column or relationship.

```text
REGION   1 ---- many NATION   1 ---- many CUSTOMER 1 ---- many ORDERS
                          \
                           +---- many SUPPLIER

ORDERS   1 ---- many LINEITEM many ---- 1 PART
                              many ---- 1 SUPPLIER

PART     1 ---- many PARTSUPP many ---- 1 SUPPLIER
```

Key pairs:

- `REGION.R_REGIONKEY = NATION.N_REGIONKEY`
- `NATION.N_NATIONKEY = CUSTOMER.C_NATIONKEY`
- `NATION.N_NATIONKEY = SUPPLIER.S_NATIONKEY`
- `CUSTOMER.C_CUSTKEY = ORDERS.O_CUSTKEY`
- `ORDERS.O_ORDERKEY = LINEITEM.L_ORDERKEY`
- `PART.P_PARTKEY = LINEITEM.L_PARTKEY`
- `SUPPLIER.S_SUPPKEY = LINEITEM.L_SUPPKEY`
- `PART.P_PARTKEY = PARTSUPP.PS_PARTKEY`
- `SUPPLIER.S_SUPPKEY = PARTSUPP.PS_SUPPKEY`

## Tier A: Foundation

### Drill 1: Customers from One Nation

**Use:** `CUSTOMER`  
**One output row means:** one customer

Return `C_CUSTKEY`, `C_NAME`, `C_ADDRESS`, and `C_NATIONKEY` for customers whose `C_NATIONKEY` is 3. Sort by customer name and show the first 20 rows.

**Check:** Every displayed `C_NATIONKEY` should be 3.

### Drill 2: Suppliers with Strong Account Balances

**Use:** `SUPPLIER`  
**One output row means:** one supplier

Return supplier key, name, and account balance for suppliers with an account balance greater than 5,000. Sort from the highest account balance to the lowest and show the first 20 rows.

**Check:** The first balance should be greater than or equal to the second balance.

### Drill 3: Categorize Part Sizes

**Use:** `PART`  
**One output row means:** one part

Return part key, part name, part size, and a calculated column named `SIZE_BAND`. Label a part `SMALL` when its size is 20 or less. Label it `LARGE` otherwise. Sort by part key and show the first 50 rows.

**Check:** Test at least one row from each size band against the rule.

### Drill 4: Order Count by Year

**Use:** `ORDERS`  
**One output row means:** one calendar year

Return the order year and number of orders in that year. Use `DATE_TRUNC` so the year is represented as a date. Sort chronologically.

**Check:** The yearly counts should add up to the total number of rows in `ORDERS`.

### Drill 5: Order Status Summary

**Use:** `ORDERS`  
**One output row means:** one order status

For each `O_ORDERSTATUS`, return the order count, average order total, and total order value. Round the monetary results to two decimal places. Sort by order count from largest to smallest.

**Check:** The status counts should add up to the total number of orders.

## Tier B: Relationships

### Drill 6: High-Volume Order Clerks

**Use:** `ORDERS`  
**One output row means:** one clerk

For each `O_CLERK`, calculate the number of orders processed and total order value. Keep only clerks who processed at least 1,500 orders. Sort by total order value from highest to lowest.

**Check:** No result should have fewer than 1,500 orders.

### Drill 7: German Customer Directory

**Use:** `CUSTOMER`, `NATION`  
**One output row means:** one customer

Return customer key, customer name, and nation name for customers in `GERMANY`. Sort by customer name and show the first 25 rows.

**Check:** Every result should show `GERMANY`. Explain why `ORDERS` is not needed.

### Drill 8: Market Segment Order Performance

**Use:** `CUSTOMER`, `ORDERS`  
**One output row means:** one customer market segment

For each customer market segment, return:

- the number of distinct customers who placed an order
- the number of orders
- the average order total, rounded to two decimal places
- the total order value, rounded to two decimal places

Sort by total order value from highest to lowest.

**Check:** The sum of the segment order counts should equal the total number of orders.

### Drill 9: Supplier Count by Region

**Use:** `REGION`, `NATION`, `SUPPLIER`  
**One output row means:** one region

Return each region name and its number of distinct suppliers. Sort from the largest supplier count to the smallest.

**Check:** You should get one row per region, not one row per nation.

### Drill 10: Top German Customers

**Use:** `CUSTOMER`, `ORDERS`, `NATION`  
**One output row means:** one customer

Return the five German customers with the highest total order value. Include customer key, customer name, order count, and total order value rounded to two decimal places.

**Check:** The result should contain no more than five rows, and every customer must be German.

## Tier C: Challenge

### Drill 11: Parts Supplied from Europe

**Use:** `PART`, `PARTSUPP`, `SUPPLIER`, `NATION`, `REGION`  
**One output row means:** one part and supplier relationship

Return part key, part name, supplier key, supplier name, and nation name for parts supplied by suppliers in the `EUROPE` region. Remove duplicate relationships, sort by part key and supplier key, and show the first 50 rows.

**Check:** Trace one result row through the join keys. Explain why `ORDERS` and `LINEITEM` are not needed.

### Drill 12: Orders Containing Part 5

**Use:** `CUSTOMER`, `ORDERS`, `LINEITEM`  
**One output row means:** one qualifying order

Return customer key, customer name, order key, order date, and order total for orders containing `L_PARTKEY = 5`. Prevent the same order from appearing more than once. Sort by order date, then order key.

**Check:** Compare `COUNT(*)` with `COUNT(DISTINCT O_ORDERKEY)` before deciding whether deduplication is necessary.

### Drill 13: Delayed Shipment Lines

**Use:** `ORDERS`, `LINEITEM`  
**One output row means:** one order line

Use `DATEDIFF` to calculate the days between the order date and ship date. Return order key, line number, order date, ship date, and `DAYS_TO_SHIP` for line items shipped more than 30 days after the order date. Sort by the longest delay first, then order key, and show the first 50 rows.

**Check:** Every displayed `DAYS_TO_SHIP` value must be greater than 30.

## Tier D: Intermediate Extension

These final drills combine joins, calculations, grouping, and `HAVING`. They do not require CTEs or subqueries.

### Drill 14: Orders with Many Line Items

**Use:** `LINEITEM`  
**One output row means:** one order

Return order key, line-item count, and discounted revenue for orders containing at least five line items. Calculate discounted revenue as `L_EXTENDEDPRICE * (1 - L_DISCOUNT)`. Sort by line-item count from largest to smallest, then discounted revenue from highest to lowest, and show the first 50 rows.

**Check:** Every result must contain at least five line items, and each output row must represent one order.

### Drill 15: Top Suppliers by Discounted Revenue

**Use:** `SUPPLIER`, `LINEITEM`  
**One output row means:** one supplier

Calculate each supplier's discounted revenue directly in one grouped join:

```text
discounted revenue = L_EXTENDEDPRICE * (1 - L_DISCOUNT)
```

Return the five suppliers with the highest discounted revenue. Include supplier key, supplier name, line-item count, and discounted revenue rounded to two decimal places.

**Check:** Confirm that the result has five suppliers and is sorted from highest to lowest revenue.

## Submission

Save your completed file as:

```text
student-work/week4/day2/w4d2_snowflake_tpch_transfer.sql
```

At the bottom of the file, add three SQL comments:

1. Name one SQL pattern that worked the same way in SQLite, BigQuery, and Snowflake.
2. Name one Snowflake session command that was platform-specific.
3. Describe one validation check that changed or confirmed your interpretation of a result.

## Success Criteria

- You wrote the queries yourself in the copied starter file.
- Every join uses an explicit key and readable table aliases.
- Each query matches the stated output grain.
- You used only the tables needed to answer each question.
- You checked counts, filters, or ordering before interpreting results.
- You queried the shared sample database without creating or changing objects.
- You can explain which SQL ideas transferred across platforms.
