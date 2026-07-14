---
title: "Joins and Relationships: Connecting Tables Without Losing the Truth"
module: "Week 4 Day 2"
type: explainer
audience: "TechCatalyst Data Engineering learners"
---

# Joins and Relationships: Connecting Tables Without Losing the Truth

## Why This Matters

Operational systems split facts into tables. A bike trip is stored once in a trips table. Details about the station belong in a stations table. That separation prevents repetitive data, but it means useful questions require a join.

The important skill is not memorizing `INNER JOIN`. It is deciding whether two columns describe the same thing, predicting what one output row will mean, and proving that the result did not silently lose or multiply data.

## Keys Describe the Relationship

A **primary key** uniquely identifies one row in its table. In a station lookup, `station_id` should identify one station record. A **foreign key** is a column that points to the primary key in another table. In a trips table, `start_station_id` points to a station.

```text
bikeshare_stations                    bikeshare_trips
one row per station                   one row per trip
station_id  <----------------------   start_station_id
```

This is usually a one-to-many relationship: one station can appear on many trip rows. A person can also have many event-attendance rows. That second example is why joins can make a result longer.

## Inner Join: Keep Only Matches

An inner join keeps rows where the join condition finds a match on both sides.

```sql
SELECT
  trips.trip_id,
  stations.name AS station_name
FROM trips
INNER JOIN stations
  ON trips.start_station_id = stations.station_id;
```

Use it when a result only makes sense for matched records. The risk is that unmatched event rows disappear. That is sometimes right, but it must be intentional.

## Left Join: Preserve the Left Table

A left join keeps every row from the table on the left. When no lookup match exists, right-side columns are `NULL`.

```sql
SELECT
  trips.trip_id,
  stations.name AS station_name
FROM trips
LEFT JOIN stations
  ON trips.start_station_id = stations.station_id;
```

Use a left join when the business question says "keep every trip" or "show every station." The position matters. If you want every station, start from `stations` and put it on the left.

## The Fan-Out Problem

A **fan-out** happens when one input row matches more than one row on the other side. It is not automatically wrong. It is correct when the relationship is truly one-to-many. It becomes dangerous when you expected a lookup to be one-to-one.

In the Sequel City database, joining 1,000 people to the driver lookup returns 1,000 rows. A left join from people to event attendance returns 1,002 rows because two people attended two events and every person is preserved. If you add `COUNT(*)` after that join without thinking, you may count attendance records when you intended to count people.

Before joining a lookup, test whether the lookup key is unique:

```sql
SELECT
  COUNT(*) AS station_rows,
  COUNT(DISTINCT station_id) AS distinct_station_ids
FROM stations;
```

If the two values match, the key is unique in that snapshot. If not, stop and investigate before interpreting any joined totals.

## A Reliable Join Workflow

1. Write the business question in one sentence.
2. State the grain of each table, meaning what one row represents.
3. Identify the primary key and foreign key.
4. Choose the table whose rows must be preserved.
5. Predict the output grain and expected row-count relationship.
6. Run a small `LIMIT` query to inspect the joined columns.
7. Run a count query and explain any difference.

This workflow protects you from a common failure mode: a query that has valid syntax and plausible output, but represents the wrong business fact.

## Counting After a Left Join

This detail matters when you want to find stations with zero trips.

```sql
SELECT
  stations.name,
  COUNT(trips.trip_id) AS trip_count
FROM stations
LEFT JOIN trips
  ON stations.station_id = trips.start_station_id
GROUP BY stations.name;
```

`COUNT(*)` counts the preserved station row even when no trip matched, so it can produce `1` for a zero-trip station. `COUNT(trips.trip_id)` counts only rows where a real trip id exists.

## Right Joins Are a Reading Problem

GoogleSQL supports `RIGHT JOIN`, but it is the same row-preservation idea as a left join written backward. This course uses left joins so you can read the preserved table first. If you see a right join, swap the table order and rewrite it as a left join before reasoning about it.

## Common Mistakes

- Joining on descriptive names when stable ids are available.
- Assuming a lookup key is unique without checking it.
- Using an inner join when the question requires all records from one table.
- Counting `*` after preserving rows with a left join.
- Adding `DISTINCT` just to hide a fan-out. Find the relationship cause first.
- Treating a successful query run as proof that the business answer is correct.

## Key Takeaways

- A join is a data-model claim, not just a SQL clause.
- Primary keys identify rows. Foreign keys connect them.
- Inner joins keep matches. Left joins preserve the table on the left.
- Counts and uniqueness checks are part of the answer.
- Fan-out can be correct, but it must be expected and explained.
