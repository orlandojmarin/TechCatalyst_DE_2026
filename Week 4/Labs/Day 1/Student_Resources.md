# Week 4 Day 1 Student Resources: SQL Foundations

> **AI-Free Zone (Weeks 1 to 4).** No Copilot, ChatGPT, or AI assistants to write your SQL today. The syntax you fumble now is exactly the fluency this week builds. Documentation is always allowed; that is what professionals read too.

## Core Documentation

| Resource | Why it helps |
|---|---|
| [SQLite SELECT syntax](https://www.sqlite.org/lang_select.html) | The official grammar for everything you write today |
| [SQLite core and aggregate functions](https://www.sqlite.org/lang_aggfunc.html) | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` behavior, including how nulls are skipped |
| [DBeaver SQL Editor basics](https://dbeaver.com/docs/dbeaver/SQL-Editor/) | Running statements, result grids, and keyboard shortcuts |
| [DBeaver SQLite connection guide](https://dbeaver.com/docs/dbeaver/Database-driver-SQLite/) | The exact connect-to-file flow from Activity 0 |
| [SQLite Tutorial: WHERE](https://www.sqlitetutorial.net/sqlite-where/) | Friendly walkthrough of comparison, `IN`, `BETWEEN`, `LIKE` |
| [SQLite Tutorial: GROUP BY](https://www.sqlitetutorial.net/sqlite-group-by/) | Grouped queries with worked examples |
| [pandas: comparison with SQL](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html) | The official version of today's pandas-to-SQL dictionary |
| [SQL style guide](https://www.sqlstyle.guide/) | Optional: how professionals format queries for review |

## Quick Patterns

Filter, sort, trim:

```sql
SELECT Date, Opp, PTS
FROM king_james
WHERE HomeAway = 'Away' AND PTS >= 25
ORDER BY PTS DESC
LIMIT 10;
```

Group, then filter the groups:

```sql
SELECT AgentID, COUNT(*) AS total_calls
FROM call
GROUP BY AgentID
HAVING COUNT(*) > 900
ORDER BY total_calls DESC;
```

Categorize with CASE:

```sql
SELECT
  CASE WHEN age < 18 THEN 'Under 18'
       WHEN age <= 34 THEN '18 to 34'
       ELSE '35 and older' END AS age_group,
  COUNT(*) AS customers
FROM customer
GROUP BY age_group;
```

Null checks:

```sql
SELECT COUNT(*) AS all_rows, COUNT(PTS) AS rows_with_points
FROM king_james;
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| DBeaver asks to download a driver | Normal on first SQLite connection; allow it |
| `no such table` | Wrong database connection is active; check which `.db` file the editor is attached to |
| `= NULL` returns nothing | That is how SQL works; use `IS NULL` |
| Aggregate query errors about a column | A selected column is missing from `GROUP BY` |
| Different row count than Check Yourself | Re-read your `WHERE` operators, especially `>` vs `>=` |

## Lab Deliverable Checklist

| Done | Deliverable |
|---|---|
| [ ] | Kickoff Mash completed |
| [ ] | Warmup notebook: six pandas answers, `warmup_claims.db` created |
| [ ] | Warmup SQL twins in DBeaver match the pandas outputs |
| [ ] | DBeaver connected to `bron.db` with a first query run |
| [ ] | Activity 1 queries in `student-work/week4/day1/w4d1_sqlite_drills.sql` |
| [ ] | Activity 2 queries added, Check Yourself numbers match |
| [ ] | Activity 3 queries added, evidence trail comments written |
| [ ] | Reflection comments at the bottom of the file |
| [ ] | Post-class quiz completed |
| [ ] | Optional: BigQuery transfer homework attempted |
