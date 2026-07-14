# Activity 1: BigQuery Join Foundations

**Module:** Week 4 Day 2  
**Estimated Time:** 75 to 90 minutes  
**Difficulty:** Beginner  
**Format:** Individual first, then partner validation  
**Prerequisites:** Activity 0 and Day 1 filtering and aggregation

## Objective

In this activity, you will use GoogleSQL in BigQuery Sandbox to connect bike-trip events to station details. You will predict row preservation, then validate the prediction with counts.

## Dataset and Cost Guardrails

Use these public tables:

```text
bigquery-public-data.austin_bikeshare.bikeshare_trips
bigquery-public-data.austin_bikeshare.bikeshare_stations
```

Use BigQuery Sandbox, not a personal paid account. Choose your Sandbox project in the console, open a query tab, and confirm that **GoogleSQL** is selected. Before running a query, check the byte estimate. Select only columns you need and use `LIMIT` while inspecting rows.

> The public tables can change. The validation anchors below deliberately test relationships, not a frozen total. Record the actual totals you see in a SQL comment.

## Data Model

| Table | Grain | Key | Role |
|---|---|---|---|
| `bikeshare_trips` | One bike trip | `trip_id` | Event table, many trips can start at one station |
| `bikeshare_stations` | One station record | `station_id` | Lookup table, adds station status and dock count |

## Starter Pattern

```sql
-- Business question: add the lookup details for each trip's start station.
SELECT
  trips.trip_id,
  trips.start_station_id,
  trips.start_station_name,
  stations.name AS station_lookup_name,
  stations.status
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_stations` AS stations
  ON trips.start_station_id = stations.station_id
LIMIT 20;
```

## Your Turn

Write each answer in `student-work/week4/day2/w4d2_bikeshare_join_drills.sql`.

### Q1: Inspect the Event Table

The operations team wants to know what a trip record contains. Show 20 trip rows with `trip_id`, start station id and name, end station id and name, and `duration_minutes`.

### Q2: Inspect the Lookup Table

Show 20 station rows with `station_id`, `name`, `status`, and `number_of_docks`.

### Q3: Validate the Lookup Key

Before joining, check whether `station_id` is unique in the stations table. Return the total station rows and distinct station ids in one query. Add a SQL comment that says whether the lookup is safe to treat as one row per station.

### Q4: First Inner Join

Match trips to their start-station lookup record. Return trip id, the trip's start-station name, the lookup name, station status, and dock count. Limit to 20 rows.

### Q5: Find Missing Start-Station Lookups

Use a left join from trips to stations. Count trips whose lookup key did not match a station row.

### Q6: Preserve Every Station

The operations team asks which stations have no recorded trip starts. Start from `bikeshare_stations`, left join to trips on start station id, and return station id, station name, and `COUNT(trips.trip_id)` as `trip_count`. Sort from fewest starts to most. Limit to 25 rows.

## Check Yourself

| Checkpoint | Expected relationship | Why it matters |
|---|---|---|
| Q3 key check | `station_rows` equals `distinct_station_ids` | A lookup key must be unique before you expect one station row per trip |
| Q5 missing matches | A nonnegative count | Any positive result is a data-quality finding, not a reason to hide rows |
| Q6 zero-trip count | Use `COUNT(trips.trip_id)`, not `COUNT(*)` | A preserved station with no match still creates one output row |

## Footnote: Right Joins

GoogleSQL supports `RIGHT JOIN`, but it is not a new relationship concept. Swap the table order and use a left join instead. This course uses left joins because the preserved table is easier to see on the left side of the query.

## Stretch

Repeat Q4 and Q5 using `end_station_id = station_id`. In a SQL comment, state what changed and what did not.

## Success Criteria

- You inspect both tables before joining them.
- You state the event-table grain and lookup-table grain.
- You use an inner join for matches and a left join when you must preserve a named table.
- You prove the lookup-key assumption with a uniqueness check.
- You add a plain-English interpretation after each validation query.

## Hints

<details>
<summary>How can I count total and distinct station ids in one query?</summary>

Use `COUNT(*)` and `COUNT(DISTINCT station_id)` in the same `SELECT` statement.

</details>

<details>
<summary>How can I count only matched trips after a left join?</summary>

Use `COUNT(trips.trip_id)`. `COUNT(*)` also counts a preserved station row when no trip matched.

</details>
