-- ACTIVITY 1: BIGQUERY JOIN FOUNDATIONS
-- Q1: Inspect the Event Table
SELECT t.trip_id, t.start_station_id, t.start_station_name, t.end_station_id, t.end_station_name, t.duration_minutes
FROM bigquery-public-data.austin_bikeshare.bikeshare_trips as t
LIMIT 20;


-- Q2: Inspect the Lookup Table
SELECT s.station_id, s.name, s.status, s.number_of_docks
FROM bigquery-public-data.austin_bikeshare.bikeshare_stations as s
LIMIT 20;


-- Q3: Validate the Lookup Key
-- Answer: the lookup is safe to treat as one row per station because the total station rows and distinct station ids are equal
SELECT COUNT(s.station_id) as total_station_rows, COUNT(DISTINCT station_id) as distinct_station_ids
FROM bigquery-public-data.austin_bikeshare.bikeshare_stations as s;


-- Q4: First Inner Join
SELECT t.trip_id, t.start_station_name, s.name, s.status, s.number_of_docks
FROM bigquery-public-data.austin_bikeshare.bikeshare_trips as t
INNER JOIN bigquery-public-data.austin_bikeshare.bikeshare_stations as s
ON t.start_station_id = s.station_id
LIMIT 20;


-- Q5: Find Missing Start-Station Lookups
SELECT COUNT(*) as mission_station_lookups
FROM bigquery-public-data.austin_bikeshare.bikeshare_trips as t
LEFT JOIN bigquery-public-data.austin_bikeshare.bikeshare_stations as s
ON t.start_station_id = s.station_id
WHERE s.station_id is null;


-- Q6: Preserve Every Station
SELECT s.station_id, s.name, COUNT(t.trip_id) as trip_count
FROM bigquery-public-data.austin_bikeshare.bikeshare_stations as s
LEFT JOIN bigquery-public-data.austin_bikeshare.bikeshare_trips as t
ON t.start_station_id = s.station_id
GROUP BY s.station_id, s.name
ORDER BY trip_count ASC
LIMIT 25;