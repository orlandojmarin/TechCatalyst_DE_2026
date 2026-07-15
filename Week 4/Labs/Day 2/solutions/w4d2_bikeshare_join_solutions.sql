-- Week 4 Day 2: Austin Bikeshare Join Solutions
-- Instructor-only. Run in BigQuery Sandbox with GoogleSQL selected.
-- Public dataset totals are intentionally not frozen in this file.

-- Activity 1, Q1
SELECT
  trip_id,
  start_station_id,
  start_station_name,
  end_station_id,
  end_station_name,
  duration_minutes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
LIMIT 20;

-- Activity 1, Q2
SELECT
  station_id,
  name,
  status,
  number_of_docks
FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations`
LIMIT 20;

-- Activity 1, Q3
SELECT
  COUNT(*) AS station_rows,
  COUNT(DISTINCT station_id) AS distinct_station_ids
FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations`;

-- Activity 1, Q4
SELECT
  trips.trip_id,
  trips.start_station_name,
  stations.name AS station_lookup_name,
  stations.status,
  stations.number_of_docks
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
LIMIT 20;

-- Activity 1, Q5
SELECT COUNT(*) AS trips_missing_start_station_lookup
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
LEFT JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
WHERE stations.station_id IS NULL;

-- Activity 1, Q6
SELECT
  stations.station_id,
  stations.name AS station_name,
  COUNT(trips.trip_id) AS trip_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
LEFT JOIN `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
  ON stations.station_id = trips.start_station_id
GROUP BY stations.station_id, stations.name
ORDER BY trip_count, station_name
LIMIT 25;

-- Activity 1, stretch
SELECT
  trips.trip_id,
  trips.end_station_name,
  stations.name AS station_lookup_name,
  stations.status,
  stations.number_of_docks
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.end_station_id = stations.station_id
LIMIT 20;

SELECT COUNT(*) AS trips_missing_end_station_lookup
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
LEFT JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.end_station_id = stations.station_id
WHERE stations.station_id IS NULL;

-- Activity 2 core, Q1
SELECT
  stations.name AS station_name,
  COUNT(*) AS trip_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
GROUP BY station_name
ORDER BY trip_count DESC
LIMIT 10;

-- Activity 2 core, Q2
SELECT
  stations.name AS station_name,
  COUNT(*) AS trip_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.end_station_id = stations.station_id
GROUP BY station_name
ORDER BY trip_count DESC
LIMIT 10;

-- Activity 2 core, Q3
SELECT
  stations.name AS station_name,
  AVG(trips.duration_minutes) AS average_duration_minutes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
GROUP BY station_name
ORDER BY average_duration_minutes DESC
LIMIT 10;

-- Activity 2 core, Q4
SELECT
  stations.status,
  COUNT(*) AS trip_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
GROUP BY stations.status
ORDER BY trip_count DESC;

-- Activity 2 core, Q5
SELECT
  stations.name AS station_name,
  stations.number_of_docks,
  COUNT(*) AS trip_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
GROUP BY station_name, stations.number_of_docks
ORDER BY trip_count DESC;

-- Activity 2 core, Q6
SELECT
  stations.name AS station_name,
  trips.subscriber_type,
  COUNT(*) AS trip_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
GROUP BY station_name, trips.subscriber_type
HAVING COUNT(*) > 1000
ORDER BY station_name, trip_count DESC;

-- Activity 2 stretch, Q7
SELECT COUNT(*) AS trips_missing_start_station_lookup
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
LEFT JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
WHERE stations.station_id IS NULL;

-- Activity 2 stretch, Q8
SELECT
  stations.station_id,
  stations.name AS station_name,
  stations.status,
  COUNT(trips.trip_id) AS trip_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
LEFT JOIN `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
  ON stations.station_id = trips.start_station_id
WHERE stations.status = 'active'
GROUP BY stations.station_id, station_name, stations.status
HAVING COUNT(trips.trip_id) < 100
ORDER BY trip_count, station_name;

-- Activity 2 stretch, Q9
SELECT
  trips.trip_id,
  start_stations.name AS station_name,
  trips.duration_minutes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS start_stations
  ON trips.start_station_id = start_stations.station_id
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS end_stations
  ON trips.end_station_id = end_stations.station_id
WHERE start_stations.name = end_stations.name
LIMIT 25;

-- Activity 2 stretch, Q10
SELECT
  trips.trip_id,
  start_stations.name AS start_station_lookup_name,
  end_stations.name AS end_station_lookup_name,
  trips.duration_minutes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
LEFT JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS start_stations
  ON trips.start_station_id = start_stations.station_id
LEFT JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS end_stations
  ON trips.end_station_id = end_stations.station_id
LIMIT 25;

-- Stretch plus
SELECT
  start_stations.name AS start_station_lookup_name,
  end_stations.name AS end_station_lookup_name,
  COUNT(*) AS trip_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS start_stations
  ON trips.start_station_id = start_stations.station_id
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS end_stations
  ON trips.end_station_id = end_stations.station_id
GROUP BY start_station_lookup_name, end_station_lookup_name
ORDER BY trip_count DESC
LIMIT 10;
