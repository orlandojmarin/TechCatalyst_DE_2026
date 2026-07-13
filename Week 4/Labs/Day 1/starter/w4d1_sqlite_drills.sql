-- Week 4 Day 1 Local SQLite Drills
-- Copy this file into student-work/week4/day1/w4d1_sqlite_drills.sql.
-- Complete the queries in your own student-work folder.
-- AI-Free Zone: do not use AI assistants to write these queries.
-- Scope: SELECT, WHERE, LIMIT, ORDER BY, aggregates, GROUP BY, HAVING, simple CASE.
-- Not today: joins, CTEs, subqueries, window functions, DML.

-- Activity 1, Q1: First Look
SELECT
  G,
  Date,
  Opp,
  HomeAway,
  PTS
FROM king_james
LIMIT 15;

-- Activity 1, Q2: Away Games
-- Write your query below.


-- Activity 1, Q3: High Scoring Games
-- Write your query below.


-- Activity 1, Q4: Opponent Filter
-- Write your query below.


-- Activity 1, Q5: Missing Stat Lines
-- Write your query below.


-- Activity 1, Q6: Combined Conditions
-- Write your query below.


-- Activity 1, Q7: Three Stat Columns
-- Write your query below.


-- Activity 2, Q1: Count Agents
-- Switch DBeaver connection to call_center_database2.db before running this section.
SELECT
  COUNT(*) AS agent_count
FROM agent;

-- Activity 2, Q2: Count Calls
-- Write your query below.


-- Activity 2, Q3: Answered Calls
-- Write your query below.


-- Activity 2, Q4: Total Sales
-- Write your query below.


-- Activity 2, Q5: Average Call Duration
-- Write your query below.


-- Activity 2, Q6: Calls By AgentID
-- Write your query below.


-- Activity 2, Q7: Agents With Enough Calls
-- Write your query below.


-- Activity 2, Q8: Picked Up Calls By AgentID
-- Write your query below.


-- Activity 2, Q9: Customer Age Groups
-- Write your query below.


-- Activity 3, Q1: Inspect Crime Scenes
-- Switch DBeaver connection to crime_database.db before running this section.
SELECT
  date,
  type,
  city,
  country,
  description
FROM crime_scene
LIMIT 10;

-- Activity 3, Q2: Murder Reports
-- Write your query below.


-- Activity 3, Q3: Incident Counts
-- Write your query below.


-- Activity 3, Q4: City Counts
-- Write your query below.


-- Activity 3, Q5: Driver Profile Filter
-- Write your query below.


-- Activity 3, Q6: Vehicle Filter
-- Write your query below.


-- Activity 3, Q7: Income Categories
-- Write your query below.


-- Activity 3, Q8: Existing Suspect View
-- Write your query below.


-- Reflection
-- 1. Local SQLite query I understood best:
-- 2. Local SQLite query that made me think hardest:
-- 3. One question I want SQL to answer next:
