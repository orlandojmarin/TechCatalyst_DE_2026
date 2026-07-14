# Homework 1: BigQuery Transfer Drills, SELECT, WHERE, ORDER BY, LIMIT

**Module:** Week 4 Day 1 Homework (optional, after class)
**Estimated Time:** 45 to 60 minutes
**Difficulty:** Beginner
**Format:** Individual, then partner check
**Prerequisites:** Day 1 SQLite drills complete; BigQuery Sandbox access from Week 1 Day 2

## Objective

In this homework, you will write basic GoogleSQL queries that select columns, filter rows, sort results, and limit output.

## Dataset

Use this table:

```text
bigquery-public-data.usa_names.usa_1910_current
```

This table contains U.S. baby name records by state, gender, year, name, and number of babies with that name.

## Getting To The Data (Nothing To Load)

You do not download, upload, or load anything. Public datasets already live in BigQuery; you query them in place. The free Sandbox includes 1 TB of query processing per month, which is far more than these drills use.

1. Open https://console.cloud.google.com/bigquery in Chrome.
2. Make sure your Sandbox project from Week 1 Day 2 is selected in the project picker at the top. If you never created one (or it was deleted), click the picker, choose New Project, name it anything, and continue; the Sandbox needs no billing or credit card.
3. Click inside the query editor, paste the Q0 starter query below, and run it. The fully qualified name in the `FROM` clause (`bigquery-public-data.usa_names.usa_1910_current`) is all BigQuery needs; you do not have to find the table first.
4. Optional, to browse instead of paste: in the Explorer panel choose Add data, then Public Datasets, search for `usa_names`, and star `bigquery-public-data` so it stays pinned in your Explorer.
5. Before each run, look at the top right of the editor: the green validator shows "This query will process X MB when run." Reading that number before running is the habit that matters this week.

If the console asks you to enable the BigQuery API, click Enable and wait a few seconds; that is normal for a fresh project.

## Instructions

1. Open BigQuery as described above.
2. Create or open your file at `student-work/week4/day1/homework_bigquery_drills.sql` (write queries there first, then paste into the BigQuery editor to run).
3. For each question, write one query.
4. Add a short SQL comment before each query with the question number.
5. Before running a query, check the BigQuery validator for the estimated bytes processed.
6. Run the query and inspect whether the result answers the question.

## Starter Pattern

```sql
-- Q0 example: show a few rows from the USA Names table.
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
LIMIT 10;
```

## Questions

### Q1: First Look

Show 25 rows from the table. Include `year`, `state`, `gender`, `name`, and `number`.

### Q2: Connecticut Names

Show 25 rows where `state` is Connecticut. Connecticut uses the state abbreviation `CT`.

### Q3: One Year

Show 25 rows for names from the year `2020`. Include the same five columns from Q1.

### Q4: One Name

Show 25 rows where the name is `Jordan`. Sort the results by `year` from oldest to newest.

### Q5: Larger Counts

Show rows where `number` is greater than `500`. Include `year`, `state`, `gender`, `name`, and `number`. Sort the result by `number` from largest to smallest.

### Q6: Multiple Conditions

Show rows where `state` is `CT`, `gender` is `F`, and `year` is `2020`. Sort names alphabetically.

### Q7: Range Filter

Show rows for Connecticut from years `2010` through `2020`. Include all names and sort by `year`, then by `number` from largest to smallest.

## Stretch

Find rows where the name starts with `Mar`. Return `year`, `state`, `gender`, `name`, and `number`. Sort by `name`, then `year`.

## Success Criteria

- Each query runs in BigQuery without syntax errors.
- Each query selects only the columns needed for the question.
- Each query has a clear `WHERE` clause when the question asks for filtered rows.
- No query uses `SELECT *`.
- No query uses CTEs, subqueries, joins, or window functions.

## Hints

<details>
<summary>How do I filter for one value?</summary>

Use `WHERE column_name = 'value'`.

</details>

<details>
<summary>How do I filter for a range?</summary>

Use `WHERE year BETWEEN 2010 AND 2020`.

</details>

<details>
<summary>How do I sort from largest to smallest?</summary>

Use `ORDER BY number DESC`.

</details>
