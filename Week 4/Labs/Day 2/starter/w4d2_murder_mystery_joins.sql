-- Week 4 Day 2: Murder Mystery Join Starter
-- Copy this file into student-work/week4/day2/ before adding your work.
-- Run in DBeaver against your copied crime_database.db.
-- AI-Free Zone: write every query yourself.
-- Scope: SELECT, WHERE, INNER JOIN, counts, and simple filters.
-- Not today: CTEs, subqueries, window functions, or DML.

-- Q1: Attach driver details to people.
SELECT
  i.id,
  i.name,
  d.gender,
  d.hair_color,
  d.eye_color,
  d.car_make,
  d.car_model,
  d.plate
FROM individual AS i
INNER JOIN drivers AS d
  ON i.driver_id = d.id
LIMIT 20;

-- Validation: How many person-to-driver rows should this return?


-- Q2: Rebuild the four-person Day 1 suspect board.


-- Q3: Read Tris MacVagh's statement.


-- Q4: Translate the statement into driver-profile filters.


-- Q5: Add the 2016 rock-event evidence.


-- Q6: Case close.


-- Final finding:
-- Evidence:

-- Stretch: Return the culprit's driver and event details in one evidence table.
