-- Week 4 Day 2: Murder Mystery Join Solution
-- Instructor-only. Run in DBeaver against data/crime_database.db.

-- Checkpoint: 4
SELECT COUNT(*) AS suspect_rows
FROM v_suspects;

-- Q1 and checkpoint: 1,000
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

SELECT COUNT(*) AS person_driver_rows
FROM individual AS i
INNER JOIN drivers AS d
  ON i.driver_id = d.id;

-- Fan-out checkpoint: 1,002
SELECT COUNT(*) AS person_event_rows
FROM individual AS i
LEFT JOIN facebook_event AS f
  ON i.id = f.individual_id;

-- Q2 checkpoint: 4
SELECT
  i.name,
  d.age,
  d.gender,
  d.hair_color,
  d.eye_color,
  d.plate,
  d.car_make,
  d.car_model
FROM individual AS i
INNER JOIN drivers AS d
  ON i.driver_id = d.id
WHERE i.id IN (45, 146, 647, 981);

-- Q3
SELECT
  i.name,
  interrogation.description
FROM individual AS i
INNER JOIN interrogation
  ON i.id = interrogation.individual_id
WHERE i.name = 'Tris MacVagh';

-- Q4 checkpoint: 3
SELECT
  i.id,
  i.name,
  d.gender,
  d.hair_color,
  d.eye_color,
  d.car_make,
  d.plate
FROM individual AS i
INNER JOIN drivers AS d
  ON i.driver_id = d.id
WHERE d.gender = 'Female'
  AND d.hair_color = 'blonde'
  AND d.eye_color = 'green'
  AND d.car_make = 'Pontiac';

-- Q5 checkpoint: 1
SELECT
  i.name,
  d.gender,
  d.hair_color,
  d.eye_color,
  d.car_make,
  f.event_description,
  f.date
FROM individual AS i
INNER JOIN drivers AS d
  ON i.driver_id = d.id
INNER JOIN facebook_event AS f
  ON f.individual_id = i.id
WHERE d.gender = 'Female'
  AND d.hair_color = 'blonde'
  AND d.eye_color = 'green'
  AND d.car_make = 'Pontiac'
  AND f.event_description LIKE '%rock%'
  AND f.date LIKE '%2016%';

-- Q6
SELECT
  i.id,
  i.name
FROM individual AS i
INNER JOIN drivers AS d
  ON i.driver_id = d.id
INNER JOIN facebook_event AS f
  ON f.individual_id = i.id
WHERE d.gender = 'Female'
  AND d.hair_color = 'blonde'
  AND d.eye_color = 'green'
  AND d.car_make = 'Pontiac'
  AND f.event_description LIKE '%rock%'
  AND f.date LIKE '%2016%';

-- Final finding: Berry Esmead is the culprit.
-- Evidence: The driver profile and the 2016 private rock-concert event both match Tris's statement.

-- Stretch
SELECT
  i.id,
  i.name,
  d.plate,
  d.car_make,
  d.car_model,
  f.event_description,
  f.date
FROM individual AS i
INNER JOIN drivers AS d
  ON i.driver_id = d.id
INNER JOIN facebook_event AS f
  ON f.individual_id = i.id
WHERE i.name = 'Berry Esmead';
