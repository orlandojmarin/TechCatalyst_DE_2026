# Activity 0: Close the Murder Mystery With Joins

**Module:** Week 4 Day 2  
**Estimated Time:** 60 to 75 minutes  
**Difficulty:** Beginner  
**Format:** Pair investigation, then class debrief  
**Prerequisites:** Day 1 SQL Detective Investigation

## Objective

In this activity, you will reconnect the Day 1 evidence, validate each relationship, and close the Sequel City case with a short evidence trail.

## Story

Yesterday you found four people on the suspect board, but the board did not prove who committed the crime. Today, a join lets you attach a person's driver record, statement, and event attendance. Each connection is a claim about the data, so you will count before believing the story.

## Workspace and Database

Open the copy at `student-work/week4/day2/crime_database.db` in DBeaver. Write every answer in `student-work/week4/day2/w4d2_murder_mystery_joins.sql`.

| Table or view | Grain | Key used today |
|---|---|---|
| `individual` | One person | `id`, with `driver_id` pointing to a driver record |
| `drivers` | One driver record | `id` |
| `interrogation` | One statement | `individual_id` |
| `facebook_event` | One attendance record | `individual_id` |
| `v_suspects` | One Day 1 suspect | Existing view, not a table you create today |

## Five Checks Before You Trust a Join

1. State what one row means in the left table.
2. State what one row means in the right table.
3. Name the two columns that refer to the same thing.
4. Predict whether the output should keep the left-table row count or grow.
5. Count the result before interpreting it.

## Guided Demo: Reopen the Suspect Board

Run this together:

```sql
SELECT
  name,
  age,
  gender,
  hair_color,
  eye_color,
  plate,
  car_make,
  car_model
FROM v_suspects;
```

Ask: why are four rows useful, but not enough to close the case?

## Guided Demo: Validate a One-to-One Lookup

Run this count before looking at any individual people:

```sql
SELECT COUNT(*) AS person_driver_rows
FROM individual AS i
INNER JOIN drivers AS d
  ON i.driver_id = d.id;
```

This database has 1,000 `individual` rows and the join returns 1,000 rows. The driver lookup is one row per person here.

## Your Turn

### Q1: Attach Driver Details to People

The detective needs a people list with vehicle evidence. Join `individual` to `drivers` and return person id, name, gender, hair color, eye color, car make, car model, and plate. Limit to 20 rows.

### Q2: Rebuild Yesterday's Suspect Board

The four Day 1 suspect ids are `45`, `146`, `647`, and `981`. Join `individual` to `drivers`, filter to those ids, and return name, age, gender, hair color, eye color, plate, car make, and car model.

### Q3: Read the Witness Statement

The witness, Tris MacVagh, made a statement. Join `individual` to `interrogation` and return Tris's name and statement.

### Q4: Translate the Statement Into a Profile

Tris describes a woman with blonde hair, green eyes, and a Pontiac. Join `individual` to `drivers` and return the people who match that profile. Return person id, name, gender, hair color, eye color, car make, and plate.

### Q5: Add the Event Evidence

The final clue is event attendance. Join `individual`, `drivers`, and `facebook_event`. Keep people who match the Q4 profile, attended an event containing `rock`, and have an event date containing `2016`. Return name, profile fields, event description, and date.

### Q6: Case Close

Write one final query that returns only the culprit's id and name. Under it, add two SQL comments:

```sql
-- Final finding:
-- Evidence:
```

## Check Yourself

Run these as count checks, not as answers to copy.

| Checkpoint | Expected result | What it teaches |
|---|---:|---|
| Rows in `v_suspects` | 4 | Yesterday's board is a shortlist, not a verdict |
| `individual` joined to `drivers` | 1,000 rows | This lookup preserves the person count in this database |
| `individual` left joined to `facebook_event` | 1,002 rows | Two people have two attendance records, so preserving people exposes a one-to-many fan-out |
| Q2 shortlist | 4 rows | The relationship and filter recreate the Day 1 board |
| Q4 profile | 3 rows | The witness statement narrows the possibilities |
| Q5 event clue | 1 row | The evidence chain isolates one person |

If your left-join result is 1,000, check whether you accidentally used `DISTINCT` or grouped the result. The extra two rows are the point of the fan-out checkpoint.

## Stretch

Return the culprit's driver details and event details in one final evidence table. In a SQL comment, explain why the `facebook_event` table can produce more than one row for a person.

## Success Criteria

- You join people to driver records, statements, and event records using the listed keys.
- Your count checkpoints match the table.
- You can explain the 1,000 to 1,002 left-join fan-out without calling it a bug.
- You name the culprit and cite the evidence columns that support the conclusion.
- You do not use CTEs, subqueries, window functions, or AI assistants.
