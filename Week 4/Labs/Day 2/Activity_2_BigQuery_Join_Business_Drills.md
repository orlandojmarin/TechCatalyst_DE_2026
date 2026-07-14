# Activity 2: BigQuery Join Business Drills

**Module:** Week 4 Day 2  
**Estimated Time:** 75 to 90 minutes for the core tier  
**Difficulty:** Beginner to early intermediate  
**Format:** Individual first, then partner review  
**Prerequisites:** Activity 1 join foundations

## Objective

In this activity, you will answer operational questions by joining Austin bikeshare trips to station details and then aggregating the result.

## Instructions

1. Continue in `student-work/week4/day2/w4d2_bikeshare_join_drills.sql`.
2. Add a business-question comment above each query.
3. Add a one-sentence plain-English answer below each completed query.
4. Check the BigQuery byte estimate before running.
5. Complete the core tier first. The stretch tier is optional.

## Translation Framework

Before writing each query, say these five things out loud or in a comment:

1. What business question am I answering?
2. What does one output row need to represent?
3. Which table is the event table?
4. Which lookup details do I need?
5. Which row count should I validate before trusting the result?

## Core Tier

### Q1: Busiest Start Stations

Which 10 stations launched the most trips? Use the station lookup name, count trips, and sort from most to fewest.

### Q2: Busiest End Stations

Which 10 stations received the most trips? Join using `end_station_id` and return station name with trip count.

### Q3: Average Trip Duration by Start Station

For each start station, calculate average trip duration in minutes. Return the 10 stations with the highest average duration.

### Q4: Station Status and Trip Volume

How many trip starts are associated with each station status? Return status and trip count.

### Q5: Dock Count and Usage

For each start station, return station name, number of docks, and trip count. Sort from most trips to fewest.

### Q6: Subscriber Type by Start Station

Which station and subscriber-type combinations have more than 1,000 trips? Return station name, subscriber type, and trip count. Use `HAVING` after grouping.

## Stretch Tier

Do these only after the core tier is complete.

### Q7: Missing Lookup Details

How many trips have no matching start-station lookup row? Use a left join and explain why this is a data-quality check.

### Q8: Active Stations With Few Starts

Find active stations with fewer than 100 matching trip starts. Preserve stations with zero starts and use `COUNT(trips.trip_id)`.

### Q9: Same Start and End Station

Find trips where the start-station lookup name and end-station lookup name are the same. Return trip id, station name, and duration. Limit to 25 rows.

### Q10: Two Station Lookups

Join the trips table to the stations table twice: once for the start station and once for the end station. Return trip id, start lookup name, end lookup name, and duration. Limit to 25 rows.

### Stretch Plus: Popular Station Pairs

Find the 10 most common start and end station pairs by trip count.

## Check Yourself

| Check | Expected relationship |
|---|---|
| Q1 and Q2 | Each output row represents one station, not one trip |
| Q3 | Average duration is measured over matched trips for each station |
| Q4 | The status count total should equal the matched trip count from Activity 1 when every matched row has one status |
| Q5 | One output row represents one station and its dock count |
| Q6 | `HAVING` filters station and subscriber-type groups after `COUNT(*)` is calculated |
| Q8 | A zero-trip station must show `0`, not `1` |

## Success Criteria

- You answer the six core questions with one clear query each.
- You choose the correct start or end join key for each business question.
- You group after joining when the question asks for counts or averages.
- You use aliases that make the query readable to a reviewer.
- You write a plain-English result comment for each core answer.
- You do not use CTEs, subqueries, window functions, or AI assistants.

## Hints

<details>
<summary>How do I join the stations table twice?</summary>

Give it two aliases, such as `start_stations` and `end_stations`, then use the matching key for each alias.

</details>

<details>
<summary>Why does the Q8 count use a column instead of a star?</summary>

After a left join, `COUNT(*)` counts the preserved station row even if no trip matched. `COUNT(trips.trip_id)` counts only real trip rows.

</details>

