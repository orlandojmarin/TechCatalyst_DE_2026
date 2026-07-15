-- Week 4 Day 1 Local SQLite Solutions
-- Instructor-only solution file.

-- Activity 1: bron.db, table king_james

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
SELECT
  G,
  Date,
  Opp,
  HomeAway,
  PTS
FROM king_james
WHERE HomeAway = 'Away'
LIMIT 15;

-- Activity 1, Q3: High Scoring Games
SELECT
  Date,
  Opp,
  HomeAway,
  PTS
FROM king_james
WHERE PTS >= 30
ORDER BY PTS DESC;

-- Activity 1, Q4: Opponent Filter
SELECT
  Date,
  HomeAway,
  Opp,
  PTS,
  REBS,
  AST
FROM king_james
WHERE Opp = 'GSW';

-- Activity 1, Q5: Missing Stat Lines
SELECT
  G,
  Date,
  Opp,
  HomeAway,
  PTS
FROM king_james
WHERE PTS IS NULL;

-- Activity 1, Q6: Combined Conditions
SELECT
  Date,
  Opp,
  HomeAway,
  PTS
FROM king_james
WHERE HomeAway = 'Home'
  AND PTS >= 25
ORDER BY Date;

-- Activity 1, Q7: Three Stat Columns
SELECT
  Date,
  Opp,
  PTS,
  REBS,
  AST
FROM king_james
WHERE PTS IS NOT NULL
  AND REBS IS NOT NULL
  AND AST IS NOT NULL
LIMIT 20;

-- Activity 1, Stretch
SELECT
  Date,
  Opp,
  AST,
  PTS
FROM king_james
WHERE AST IS NOT NULL
ORDER BY AST DESC
LIMIT 5;

-- Activity 2: call_center_database2.db, tables agent, call, customer

-- Activity 2, Q1: Count Agents
SELECT
  COUNT(*) AS agent_count
FROM agent;

-- Activity 2, Q2: Count Calls
SELECT
  COUNT(*) AS call_count
FROM call;

-- Activity 2, Q3: Answered Calls
SELECT
  COUNT(*) AS picked_up_calls
FROM call
WHERE PickedUp = 1;

-- Activity 2, Q4: Total Sales
SELECT
  SUM(ProductSold) AS total_sales
FROM call;

-- Activity 2, Q5: Average Call Duration
SELECT
  AVG(Duration) AS average_duration
FROM call
WHERE Duration > 0;

-- Activity 2, Q6: Calls By AgentID
SELECT
  AgentID,
  COUNT(*) AS total_calls,
  SUM(ProductSold) AS total_sales,
  AVG(ProductSold) AS sales_rate
FROM call
GROUP BY AgentID
ORDER BY sales_rate DESC;

-- Activity 2, Q7: Agents With Enough Calls
SELECT
  AgentID,
  COUNT(*) AS total_calls,
  SUM(ProductSold) AS total_sales,
  AVG(ProductSold) AS sales_rate
FROM call
GROUP BY AgentID
HAVING COUNT(*) > 900
ORDER BY sales_rate DESC;

-- Activity 2, Q8: Picked Up Calls By AgentID
SELECT
  AgentID,
  COUNT(*) AS picked_up_calls
FROM call
WHERE PickedUp = 1
GROUP BY AgentID
ORDER BY picked_up_calls DESC;

-- Activity 2, Q9: Customer Age Groups
SELECT
  CASE
    WHEN Age < 18 THEN 'Under 18'
    WHEN Age BETWEEN 18 AND 34 THEN '18 to 34'
    ELSE '35 and older'
  END AS age_group,
  COUNT(*) AS customer_count
FROM customer
GROUP BY age_group
ORDER BY customer_count DESC;

-- Activity 2, Stretch
SELECT
  Occupation,
  COUNT(*) AS customer_count
FROM customer
GROUP BY Occupation
HAVING COUNT(*) > 20
ORDER BY customer_count DESC;

-- Activity 3: crime_database.db

-- Activity 3, Q1: Inspect Crime Scenes
SELECT
  date,
  type,
  city,
  country,
  description
FROM crime_scene
LIMIT 10;

-- Activity 3, Q2: Murder Reports
SELECT
  date,
  city,
  country,
  description
FROM crime_scene
WHERE type = 'murder';

-- Activity 3, Q3: Incident Counts
SELECT
  type,
  COUNT(*) AS incident_count
FROM crime_scene
GROUP BY type
ORDER BY incident_count DESC;

-- Activity 3, Q4: City Counts
SELECT
  city,
  COUNT(*) AS incident_count
FROM crime_scene
GROUP BY city
HAVING COUNT(*) > 2
ORDER BY incident_count DESC;

-- Activity 3, Q5: Driver Profile Filter
SELECT
  id,
  age,
  gender,
  height,
  hair_color,
  eye_color,
  plate
FROM drivers
WHERE hair_color = 'white';

-- Activity 3, Q6: Vehicle Filter
SELECT
  id,
  age,
  gender,
  plate,
  car_make,
  car_model,
  car_model_year
FROM drivers
WHERE car_make = 'Maserati';

-- Activity 3, Q7: Income Categories
SELECT
  CASE
    WHEN income < 35000 THEN 'Low'
    WHEN income BETWEEN 35000 AND 50000 THEN 'Medium'
    ELSE 'High'
  END AS income_group,
  COUNT(*) AS person_count
FROM individual
GROUP BY income_group
ORDER BY person_count DESC;

-- Activity 3, Q8: Existing Suspect View
SELECT
  name,
  age,
  gender,
  hair_color,
  eye_color,
  car_make,
  car_model
FROM v_suspects;

-- Activity 3, Stretch
SELECT
  individual_id,
  description
FROM interrogation
WHERE description LIKE '%Poirot%';
