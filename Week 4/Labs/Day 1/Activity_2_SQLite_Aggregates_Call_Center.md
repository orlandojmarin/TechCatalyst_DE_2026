# Activity 2: Call Center Aggregates

**Module:** Week 4 Day 1
**Estimated Time:** 60 to 75 minutes
**Difficulty:** Beginner
**Format:** Guided examples, then student practice
**Prerequisites:** Activity 1 or equivalent `SELECT` and `WHERE` practice

## Objective

In this activity, you will use `COUNT`, `SUM`, `AVG`, `GROUP BY`, and `HAVING` to summarize call center performance.

## Story

You are an operations analyst for a financial services call center. Leadership wants a fair first pass at performance: total calls, answered calls, product sales, and conversion rates. Your job is to summarize the data without changing it.

## Database

Open this SQLite database in DBeaver:

```text
Week 4/Labs/Day 1/data/call_center_database2.db
```

Use these tables:

| Table | Grain |
|---|---|
| `agent` | One row per agent |
| `call` | One row per call |
| `customer` | One row per customer |

Important columns:

| Table | Columns |
|---|---|
| `agent` | `AgentID`, `Name` |
| `call` | `CallID`, `AgentID`, `CustomerID`, `PickedUp`, `Duration`, `ProductSold` |
| `customer` | `CustomerID`, `Name`, `Occupation`, `Age` |

## Guided Demo: Whole Table Summary

Run this together:

```sql
SELECT
  COUNT(*) AS total_calls,
  SUM(ProductSold) AS total_sales,
  AVG(ProductSold) AS sales_rate
FROM call;
```

Discuss:

- Why does `COUNT(*)` count calls?
- Why does `SUM(ProductSold)` count sales?
- Why does `AVG(ProductSold)` behave like a sales rate when values are 0 and 1?

## Guided Demo: Grouped Summary

Run this together:

```sql
SELECT
  AgentID,
  COUNT(*) AS total_calls,
  SUM(ProductSold) AS total_sales,
  AVG(ProductSold) AS sales_rate
FROM call
GROUP BY AgentID
ORDER BY sales_rate DESC;
```

Discuss:

- What is one row in the result?
- Why does every selected non-aggregate column need to be in `GROUP BY`?
- What does it mean if an `AgentID` appears in calls but not in the agent table?

## Your Turn

Write each answer in `student-work/week4/day1/w4d1_sqlite_drills.sql`.

### Q1: Count Agents

How many agents are in the `agent` table?

### Q2: Count Calls

How many calls are in the `call` table?

### Q3: Answered Calls

How many calls were picked up? Use `PickedUp = 1`.

### Q4: Total Sales

How many products were sold across all calls?

### Q5: Average Call Duration

What is the average duration for calls where `Duration` is greater than `0`?

### Q6: Calls By AgentID

For each `AgentID`, calculate total calls, total sales, and average product sold rate. Sort by average product sold rate from highest to lowest.

### Q7: Agents With Enough Calls

Modify Q6 to show only agent groups with more than `900` calls. Use `HAVING`.

### Q8: Picked Up Calls By AgentID

For each `AgentID`, count picked up calls only. Sort from most picked up calls to fewest.

### Q9: Customer Age Groups

Use the `customer` table to count customers by age group:

| Group | Rule |
|---|---|
| `Under 18` | age less than 18 |
| `18 to 34` | age from 18 through 34 |
| `35 and older` | age 35 or more |

Use `CASE`, `COUNT`, and `GROUP BY`.

## Check Yourself

| Check | Expected |
|---|---|
| Agents in `agent` (Q1) | 11 |
| Calls in `call` (Q2) | 9,940 |
| Picked up calls (Q3) | 6,920 |
| Total products sold (Q4) | 2,089 |
| Groups remaining after `HAVING COUNT(*) > 900` (Q7) | 7 |

One more thing to notice in Q6: there are 12 `AgentID` groups in `call` but only 11 agents in `agent`. One call has `AgentID = -1`. Hold that thought; tomorrow joins explain what to do with it.

## Stretch

Find occupations with more than `20` customers. Return occupation and customer count, sorted from largest to smallest.

## Reflection

At the bottom of your SQL file, add comments answering:

```sql
-- What is the grain of the call table?
-- What does GROUP BY change about the result?
-- When should you use HAVING instead of WHERE?
```

## Success Criteria

- You can explain what each aggregate function returns.
- You group by the same non-aggregate columns you select.
- You use `WHERE` before grouping to filter rows.
- You use `HAVING` after grouping to filter groups.
- You do not use joins, CTEs, subqueries, or window functions in this activity.

