# Activity 3: SQL Detective Investigation

**Module:** Week 4 Day 1
**Estimated Time:** 60 to 75 minutes
**Difficulty:** Beginner
**Format:** Guided investigation in pairs
**Prerequisites:** Basic `SELECT`, `WHERE`, and aggregate practice

## Objective

In this activity, you will use beginner SQL to inspect clues in a small investigation database. The goal is not to solve the whole mystery with advanced SQL. The goal is to ask careful questions and retrieve evidence.

## Story

You have inherited a detective case file from Sequel City. The database contains crime scenes, people, drivers, gym records, social events, and interviews. Today you are learning how to inspect evidence one table at a time. Later, joins and advanced SQL will make the investigation deeper.

## Database

Open this SQLite database in DBeaver:

```text
Week 4/Labs/Day 1/data/crime_database.db
```

Useful tables:

| Table | What it contains |
|---|---|
| `crime_scene` | Reported incidents and descriptions |
| `individual` | People, addresses, and income |
| `drivers` | Driver demographics and vehicle details |
| `interrogation` | Interview descriptions by person |
| `gym_affiliated` | Gym memberships |
| `gym_record` | Gym check-ins |
| `facebook_event` | Event attendance records |

## Instructor Demo: Find Murder Reports

Run this together:

```sql
SELECT
  date,
  city,
  country,
  description
FROM crime_scene
WHERE type = 'murder'
LIMIT 10;
```

Discuss:

- Which table holds incident reports?
- Which rows did `WHERE type = 'murder'` keep?
- Why should we read descriptions carefully before writing more filters?

## Instructor Demo: Count By Category

Run this together:

```sql
SELECT
  type,
  COUNT(*) AS incident_count
FROM crime_scene
GROUP BY type
ORDER BY incident_count DESC;
```

Discuss:

- What does one row in this result represent?
- How is this different from reading individual crime reports?

## Your Turn

Write each answer in `student-work/week4/day1/w4d1_sqlite_drills.sql`.

### Q1: Inspect Crime Scenes

Show 10 rows from `crime_scene` with `date`, `type`, `city`, `country`, and `description`.

### Q2: Murder Reports

Show all murder reports. Return `date`, `city`, `country`, and `description`.

### Q3: Incident Counts

Count incidents by `type`. Sort from most common to least common.

### Q4: City Counts

Count incidents by `city`. Show only cities with more than `2` incidents. Use `HAVING`.

### Q5: Driver Profile Filter

From the `drivers` table, find drivers with `hair_color = 'white'`. Return `id`, `age`, `gender`, `height`, `hair_color`, `eye_color`, and `plate`.

### Q6: Vehicle Filter

Find drivers with `car_make = 'Maserati'`. Return `id`, `age`, `gender`, `plate`, `car_make`, `car_model`, and `car_model_year`.

### Q7: Income Categories

Use the `individual` table to count people by income group:

| Group | Rule |
|---|---|
| `Low` | income less than 35000 |
| `Medium` | income from 35000 through 50000 |
| `High` | income greater than 50000 |

Use `CASE`, `COUNT`, and `GROUP BY`.

### Q8: Existing Suspect View

The database already includes a view named `v_suspects`. Query it and return `name`, `age`, `gender`, `hair_color`, `eye_color`, `car_make`, and `car_model`.

## Check Yourself

| Check | Expected |
|---|---|
| Murder reports (Q2) | 31 rows |
| Cities with more than 2 incidents (Q4) | 15 rows |
| Rows in `v_suspects` (Q8) | 4 |

## Stretch

Search interrogation descriptions for the word `Poirot`. Return `individual_id` and `description`.

## To Be Continued

You are getting closer, but the case is not closed yet.

At the end of Day 1, your job is to leave a clean evidence trail:

- Which suspects did you identify?
- Which vehicle and profile clues seem important?
- Which table do you think needs to connect to another table next?

On Day 2, you will return to this same database and use joins to finish the investigation. The suspect list from today is not the final answer. It is the trailhead.

## Reflection

At the bottom of your SQL file, add comments answering:

```sql
-- Which table felt most like raw evidence?
-- Which query summarized evidence instead of listing it?
-- What question would require a join later?
-- What clue should we continue with on Day 2?
```

## Success Criteria

- You use `SELECT` to inspect evidence.
- You use `WHERE` to filter relevant rows.
- You use `GROUP BY` and `HAVING` to summarize categories.
- You can explain the difference between reading records and summarizing records.
- You do not create views, use CTEs, write subqueries, or use window functions.

## Instructor Notes

- The source material includes CTEs and views, but those are intentionally not today's focus.
- The existing `v_suspects` view is safe to query as a table-like object. Do not ask students to create it.
- This activity is meant to create curiosity for Day 2 joins and later advanced SQL.
- Do not reveal the culprit on Day 1. The case closes in the Day 2 join activity.
