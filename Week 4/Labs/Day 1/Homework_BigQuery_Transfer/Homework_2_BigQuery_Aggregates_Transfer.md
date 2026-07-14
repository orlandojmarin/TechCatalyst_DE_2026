# Homework 2: BigQuery Transfer Drills, Aggregates, GROUP BY, HAVING

**Module:** Week 4 Day 1 Homework (optional, after class)
**Estimated Time:** 60 to 75 minutes
**Difficulty:** Beginner
**Format:** Individual first, then partner check
**Prerequisites:** Homework 1 or the Day 1 SQLite drills

## Objective

In this homework, you will use aggregate functions to summarize rows, then use `GROUP BY` and `HAVING` to answer grouped questions.

## Dataset

Use this table:

```text
bigquery-public-data.usa_names.usa_1910_current
```

This table contains U.S. baby name records by state, gender, year, name, and number of babies with that name. Nothing to load: see the Getting To The Data section in Homework 1 if you have not opened BigQuery yet.

## Instructions

1. Continue working in `student-work/week4/day1/homework_bigquery_drills.sql`.
2. Add each answer below your Homework 1 answers.
3. Add a SQL comment before each query with the question number.
4. Check the validator before running each query.
5. Read the result and write one short SQL comment that explains what the result means.

## Starter Patterns

```sql
-- Aggregate over the whole table.
SELECT
  COUNT(*) AS row_count
FROM `bigquery-public-data.usa_names.usa_1910_current`;
```

```sql
-- Aggregate by group.
SELECT
  state,
  COUNT(*) AS row_count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY state
ORDER BY row_count DESC;
```

## Questions

### Q1: Count Rows

How many rows are in the table?

### Q2: Total Babies Represented

What is the total number of babies represented in the table? Use the `number` column.

### Q3: Average Row Count

What is the average value of the `number` column across all rows?

### Q4: Rows By State

How many rows are there for each state? Return `state` and `row_count`, sorted by `row_count` from largest to smallest.

### Q5: Babies By Gender

How many babies are represented for each `gender` across the whole table? Return `gender` and `total_babies`.

### Q6: Babies By Year

How many babies are represented for each `year`? Return `year` and `total_babies`, sorted from newest year to oldest year.

### Q7: Top Names Overall

What are the 20 names with the highest total count across all years, states, and genders? Return `name` and `total_babies`.

### Q8: Names Over A Threshold

Which names have more than `1,000,000` total babies represented? Return `name` and `total_babies`, sorted from largest to smallest.

### Q9: Connecticut Names Over A Threshold

For Connecticut only, which names have more than `5,000` total babies represented? Return `name` and `total_babies`.

### Q10: State And Gender Groups

For each combination of `state` and `gender`, calculate total babies represented. Only show groups where the total is greater than `1,000,000`.

## Stretch

For each year from `2010` through `2020`, calculate the total babies represented in Connecticut. Return `year` and `total_babies`, sorted by year.

## Success Criteria

- You use aggregate functions only when the question asks for summary information.
- Every non-aggregated selected column appears in `GROUP BY`.
- You use `WHERE` to filter rows before grouping.
- You use `HAVING` to filter grouped results after grouping.
- No query uses CTEs, subqueries, joins, or window functions.

## Hints

<details>
<summary>When do I use WHERE?</summary>

Use `WHERE` to filter rows before aggregation, such as `WHERE state = 'CT'`.

</details>

<details>
<summary>When do I use HAVING?</summary>

Use `HAVING` to filter grouped results, such as `HAVING SUM(number) > 5000`.

</details>

<details>
<summary>Why does BigQuery ask me to GROUP BY a column?</summary>

If a selected column is not inside an aggregate function, BigQuery needs to know how to group by it.

</details>
