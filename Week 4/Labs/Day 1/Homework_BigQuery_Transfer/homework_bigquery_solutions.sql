-- Week 4 Day 1 BigQuery Solutions
-- Instructor-only solution file.
-- Run in BigQuery with GoogleSQL.

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
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE year = 2020
LIMIT 25;

-- Activity 1, Q4: One Name
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE name = 'Jordan'
ORDER BY year
LIMIT 25;

-- Activity 1, Q5: Larger Counts
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE number > 500
ORDER BY number DESC
LIMIT 25;

-- Activity 1, Q6: Multiple Conditions
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE state = 'CT'
  AND gender = 'F'
  AND year = 2020
ORDER BY name;

-- Activity 1, Q7: Range Filter
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE state = 'CT'
  AND year BETWEEN 2010 AND 2020
ORDER BY year, number DESC;

-- Activity 1, Stretch
SELECT
  year,
  state,
  gender,
  name,
  number
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE name LIKE 'Mar%'
ORDER BY name, year;

-- Activity 2, Q1: Count Rows
SELECT
  COUNT(*) AS row_count
FROM `bigquery-public-data.usa_names.usa_1910_current`;

-- Activity 2, Q2: Total Babies Represented
SELECT
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`;

-- Activity 2, Q3: Average Row Count
SELECT
  AVG(number) AS average_number
FROM `bigquery-public-data.usa_names.usa_1910_current`;

-- Activity 2, Q4: Rows By State
SELECT
  state,
  COUNT(*) AS row_count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY state
ORDER BY row_count DESC;

-- Activity 2, Q5: Babies By Gender
SELECT
  gender,
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY gender
ORDER BY total_babies DESC;

-- Activity 2, Q6: Babies By Year
SELECT
  year,
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY year
ORDER BY year DESC;

-- Activity 2, Q7: Top Names Overall
SELECT
  name,
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
ORDER BY total_babies DESC
LIMIT 20;

-- Activity 2, Q8: Names Over A Threshold
SELECT
  name,
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
HAVING SUM(number) > 1000000
ORDER BY total_babies DESC;

-- Activity 2, Q9: Connecticut Names Over A Threshold
SELECT
  name,
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE state = 'CT'
GROUP BY name
HAVING SUM(number) > 5000
ORDER BY total_babies DESC;

-- Activity 2, Q10: State And Gender Groups
SELECT
  state,
  gender,
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY state, gender
HAVING SUM(number) > 1000000
ORDER BY total_babies DESC;

-- Activity 2, Stretch
SELECT
  year,
  SUM(number) AS total_babies
FROM `bigquery-public-data.usa_names.usa_1910_current`
WHERE state = 'CT'
  AND year BETWEEN 2010 AND 2020
GROUP BY year
ORDER BY year;
