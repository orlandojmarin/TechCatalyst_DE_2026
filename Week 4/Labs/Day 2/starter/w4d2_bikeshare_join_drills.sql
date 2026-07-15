-- Week 4 Day 2: Austin Bikeshare Join Drills
-- Copy this file into student-work/week4/day2/ before adding your work.
-- Run in BigQuery Sandbox with GoogleSQL selected.
-- AI-Free Zone: write every query yourself.
-- Public dataset totals can change. Record your validation results in comments.
-- Not today: CTEs, subqueries, window functions, or DML.

-- Activity 1, Q1: Inspect trip events.
SELECT
  trip_id,
  start_station_id,
  start_station_name,
  end_station_id,
  end_station_name,
  duration_minutes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
LIMIT 20;

-- Activity 1, Q2: Inspect station lookup rows.
SELECT
  station_id,
  name,
  status,
  number_of_docks
FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations`
LIMIT 20;

-- Activity 1, Q3: Validate whether station_id is unique.


-- Activity 1, Q4: First inner join from trips to stations.


-- Activity 1, Q5: Count trips with no start-station lookup match.


-- Activity 1, Q6: Preserve every station and count trip starts.


-- Activity 1, Stretch: Repeat Q4 and Q5 using end_station_id.


-- Activity 2 core, Q1: Busiest start stations.


-- Activity 2 core, Q2: Busiest end stations.


-- Activity 2 core, Q3: Average duration by start station.


-- Activity 2 core, Q4: Station status and trip volume.


-- Activity 2 core, Q5: Dock count and usage.


-- Activity 2 core, Q6: Subscriber type by start station.


-- Activity 2 stretch, Q7: Missing lookup details.


-- Activity 2 stretch, Q8: Active stations with few starts.


-- Activity 2 stretch, Q9: Same start and end station.


-- Activity 2 stretch, Q10: Two station lookups.


-- Stretch plus: Most common station pairs.


-- Reflection
-- 1. An inner join keeps:
-- 2. A left join keeps:
-- 3. Before I trust a join, I will:
