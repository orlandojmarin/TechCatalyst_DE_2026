-- Activity 0
-- Q1: Attach Driver Details to People
SELECT i.id, i.name, d.gender, d.hair_color, d.eye_color, d.car_make, d.car_model, d.plate
FROM individual as i
INNER JOIN drivers as d
ON i.driver_id = d.id
LIMIT 20;

-- Q2: Rebuild Yesterday's Suspect Board
SELECT i.id, i.name, d.age, d.gender, d.hair_color, d.eye_color, d.plate, d.car_make, d.car_model
FROM individual as i
INNER JOIN drivers as d
ON i.driver_id = d.id
WHERE i.id in (45, 146, 647, 981);

-- Q3: Read the Witness Statement
SELECT i.name, i2.description 
FROM individual as i
INNER JOIN interrogation as i2
ON i.id = i2.individual_id
WHERE i.name = "Tris MacVagh";

-- Q4: Translate the Statement Into a Profile
SELECT i.id, i.name, d.gender, d.hair_color, d.eye_color, d.car_make, d.plate
FROM individual as i
INNER JOIN drivers as d
ON i.driver_id = d.id
WHERE d.hair_color = "blonde" and d.eye_color = "green" and d.car_make = "Pontiac";

-- Q5: Add the Event Evidence
SELECT i.id, i.name, d.gender, d.hair_color, d.eye_color, d.car_make, d.plate, fe.event_description, fe.date 
FROM individual as i
INNER JOIN drivers as d
ON i.driver_id = d.id
INNER JOIN facebook_event as fe
ON i.id = fe.individual_id 
WHERE d.hair_color = "blonde" and d.eye_color = "green" and d.car_make = "Pontiac" and fe.event_description LIKE "%rock%" and fe.date LIKE "%2016%";

-- Q6: Case Close
SELECT i.id, i.name
FROM individual as i
INNER JOIN drivers as d
ON i.driver_id = d.id
INNER JOIN facebook_event as fe
ON i.id = fe.individual_id 
WHERE d.hair_color = "blonde" and d.eye_color = "green" and d.car_make = "Pontiac" and fe.event_description LIKE "%rock%" and fe.date LIKE "%2016%";

-- Final finding: Berry Esmead, ID number 402
-- Evidence: They are the only person who fits the descriptions provided in Q4 and Q5