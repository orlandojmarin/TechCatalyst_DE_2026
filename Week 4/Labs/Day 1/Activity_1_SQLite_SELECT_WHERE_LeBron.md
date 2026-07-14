# Activity 1: Courtside SELECT And WHERE

**Module:** Week 4 Day 1
**Estimated Time:** 45 to 60 minutes
**Difficulty:** Beginner
**Format:** Guided examples, then student practice
**Prerequisites:** DBeaver connected to `bron.db`

## Objective

In this activity, you will investigate a basketball game log using `SELECT`, `WHERE`, `ORDER BY`, and `LIMIT`.

## Story

You are helping a sports desk prepare a quick segment on LeBron James game performance. Your editor does not want every row in the database. They want answers to specific questions: high-scoring games, home and away patterns, and games where the stat line is incomplete.

## Database

Open this SQLite database in DBeaver:

```text
Week 4/Labs/Day 1/data/bron.db
```

Use this table:

```text
king_james
```

Important columns:

| Column | Meaning |
|---|---|
| `G` | Row order for the game log |
| `Date` | Game date |
| `Month` | Month name |
| `Year` | Season year in this data extract |
| `HomeAway` | Home or away game |
| `Opp` | Opponent abbreviation |
| `REBS` | Rebounds |
| `AST` | Assists |
| `PTS` | Points |

## Guided Demo: Read The Table

Run this together:

```sql
SELECT
  G,
  Date,
  HomeAway,
  Opp,
  PTS
FROM king_james
LIMIT 10;
```

Discuss:

- Which columns did we ask for?
- Why did we avoid `SELECT *`?
- What does `LIMIT` control?

## Guided Demo: Filter Rows

Run this together:

```sql
SELECT
  G,
  Date,
  Opp,
  HomeAway,
  PTS
FROM king_james
WHERE HomeAway = 'Home'
ORDER BY PTS DESC
LIMIT 10;
```

Discuss:

- Which rows did `WHERE` keep?
- What did `ORDER BY PTS DESC` do?
- Why can a filtered query still return several rows?

## How To Translate a Question Into SQL

You do not know this data yet, and that is normal: data engineers rarely know a table before the first question arrives. Run the same five checks every time:

1. What does one row represent? (Here: one game.)
2. Which columns does the answer need? That is your `SELECT` list.
3. Which rows qualify? That is your `WHERE` clause.
4. Does the asker care about order? Only then add `ORDER BY`.
5. How many rows do they want? Only then add `LIMIT`.

Worked example. The editor asks: "Which road games did he score at least 20 in? I just need the date, the opponent, and the points."

One row is one game. Columns: `Date`, `Opp`, `PTS`. Rows: away games with 20 or more points. Order: not requested. Count: all of them.

```sql
SELECT Date, Opp, PTS
FROM king_james
WHERE HomeAway = 'Away' AND PTS >= 20;
```

## Your Turn

Each question below is how the sports desk would actually say it. Run the five checks, use the column glossary above to map words to columns, then write the SQL in `student-work/week4/day1/w4d1_sqlite_drills.sql`.

### Q1: First Look

"Before I trust you with segment stats, show me a sample of this data. Give me 15 games: game number, date, opponent, whether it was home or away, and the points."

*Translate: which five columns? Does the editor want specific games, or just a sample?*

### Q2: Away Games

"Our producer claims he travels well. Pull 15 road games so I can eyeball the scoring. Same columns as before."

*Translate: same `SELECT` as Q1. What one condition marks a road game? If you are unsure what values exist, check with `SELECT DISTINCT HomeAway FROM king_james;` first.*

### Q3: High Scoring Games

"The segment is called 30-Point Nights. Find every game where he scored 30 or more: date, opponent, home or away, and points, with the biggest night at the top."

*Translate: "biggest at the top" is an ordering instruction, and "every game" means no `LIMIT`.*

### Q4: Opponent Filter

"A rival network is running a Warriors special and we want a counter-piece. Pull every game against Golden State (the `Opp` code is `GSW`): date, home or away, opponent, points, rebounds, and assists."

### Q5: Missing Stat Lines

"The data vendor just admitted some game logs came in incomplete. Before anything airs, list every game with no points recorded (game number, date, opponent, home or away, points) so we can flag them for the vendor."

*Translate: "no points recorded" is not the same as zero points. Which null check did the reading say to use?*

### Q6: Combined Conditions

"We are building a 'dominant at home' graphic: home games with at least 25 points. Date, opponent, home or away, and points, ordered by date so it reads like a season timeline."

*Translate: two row conditions joined by which logical operator?*

### Q7: Complete Stat Lines Only

"The stat card graphic breaks if any number is missing. Give me up to 20 games where points, rebounds, and assists are all present: date, opponent, and those three stats."

## Check Yourself

Use these anchors to confirm your filters worked. If your numbers differ, re-read your `WHERE` clause.

| Check | Expected |
|---|---|
| Total rows in `king_james` | 82 |
| Away games in the table (Q2 filter, before LIMIT) | 41 |
| Games with `PTS >= 30` (Q3) | 34 rows |
| Games against `GSW` (Q4) | 4 rows |
| Rows where `PTS IS NULL` (Q5) | 26 rows |

## Stretch

"For the closer: his five best passing nights. Date, opponent, assists, and points, most assists first."

## Reflection

At the bottom of your SQL file, add comments answering:

```sql
-- Which question was easiest?
-- Which query needed the most careful filtering?
-- What does NULL mean in this database?
```

## Success Criteria

- Every query selects only the needed columns.
- Every filtered query has a clear `WHERE` clause.
- You use `IS NULL` for missing values, not `= NULL`.
- You use `ORDER BY` only when the question asks for sorted results.
- You do not use joins, CTEs, subqueries, or window functions.
