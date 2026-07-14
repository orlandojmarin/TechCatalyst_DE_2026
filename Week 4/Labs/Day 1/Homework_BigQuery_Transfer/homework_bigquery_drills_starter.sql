-- Week 4 Day 1 BigQuery homework starter
-- Copy this file into student-work/week4/day1/homework_bigquery_drills.sql.
-- Complete the queries in your own student-work folder.
-- AI-Free Zone: do not use AI assistants to write these queries.
-- Scope: SELECT, WHERE, LIMIT, ORDER BY, aggregates, GROUP BY, HAVING.
-- Not today: CTEs, subqueries, window functions, joins, DML.

-- Activity 1, Q1: First Look
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
LIMIT 25;

-- Activity 1, Q2: Connecticut Names
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE state = 'CT'
LIMIT 25;

-- Activity 1, Q3: One Year
-- Write your query below.


-- Activity 1, Q4: One Name
-- Write your query below.


-- Activity 1, Q5: Larger Counts
-- Write your query below.


-- Activity 1, Q6: Multiple Conditions
-- Write your query below.


-- Activity 1, Q7: Range Filter
-- Write your query below.


-- Activity 1, Stretch
-- Write your query below.


-- Activity 2, Q1: Count Rows
SELECT
  COUNT(*) AS row_count
FROM `bigquery-public-data.usa_names.usa_1910_current`;

-- Activity 2, Q2: Total Babies Represented
SELECT
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`;

-- Activity 2, Q3: Average Row Count
-- Write your query below.


-- Activity 2, Q4: Rows By State
-- Write your query below.


-- Activity 2, Q5: Babies By Gender
-- Write your query below.


-- Activity 2, Q6: Babies By Year
-- Write your query below.


-- Activity 2, Q7: Top Names Overall
-- Write your query below.


-- Activity 2, Q8: Names Over A Threshold
-- Write your query below.


-- Activity 2, Q9: Connecticut Names Over A Threshold
-- Write your query below.


-- Activity 2, Q10: State And Gender Groups
-- Write your query below.


-- Activity 2, Stretch
-- Write your query below.


-- Reflection
-- 1. Easiest clause today:
-- 2. Hardest clause today:
-- 3. Question I still have:
