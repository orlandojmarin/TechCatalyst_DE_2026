# Week 4 Day 1: SQL Foundations on SQLite

**Module:** Week 4, Day 1
**Estimated Time:** Full day
**Difficulty:** Beginner (in SQL; you are not beginners in data)
**Format:** Individual first, then partner check
**Platform:** DBeaver Community with SQLite (local files, zero cloud setup)

## Purpose

Welcome to the SQL week. Everything you learned in pandas (filtering, grouping, summarizing) exists in SQL under different names, and today you prove that to yourself. We start local: small SQLite database files opened in DBeaver, where every table is visible and every mistake is free. By Friday you will be loading and transforming data in Snowflake; today you learn to ask one table careful questions.

The goal is not to memorize syntax. The goal is to read a question, identify the columns you need, and write a clear query that answers only that question.

## Scope

Use only these SQL ideas today:

- `SELECT`, column lists, aliases with `AS`, `DISTINCT`
- `WHERE` with comparison and logical operators, `IN`, `BETWEEN`, `LIKE`
- `ORDER BY`, `LIMIT`
- `IS NULL` and `IS NOT NULL`
- Calculated columns
- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- `GROUP BY`, `HAVING`, simple `CASE`

Do not use these yet (each has its day this week):

- Joins (Day 2)
- Subqueries or `WITH` CTEs (Day 3)
- `CREATE TABLE`, views (Day 4)
- Window functions such as `ROW_NUMBER` (Week 5)
- AI assistants to write SQL. Weeks 1 to 4 are an AI-Free Zone.

## Today's Arc

| Sequence | Activity | Story |
|---|---|---|
| 1 | Kickoff Markdown Mash | Weeks 1 to 3 recap, quiz-show style |
| 2 | Warmup, Parts 1 and 2 (notebook) | Solve six business questions in pandas, then export the DataFrame to a SQLite database you create |
| 3 | SQL kickoff | Concepts and guided demo: query anatomy, execution order, the pandas dictionary |
| 4 | Activity 0 | Connect DBeaver to SQLite (your `warmup_claims.db` first, then `bron.db`) and run a first query |
| 5 | Warmup, Part 3 (DBeaver) | Answer the same six questions in SQL against your own database and compare |
| 6 | Activity 1 | Basketball game log: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, nulls |
| 7 | Activity 2 | Call center operations: aggregates, `GROUP BY`, `HAVING` |
| 8 | Activity 3 | Detective case file: filters, grouped counts, `CASE`, and a cliffhanger |
| 9 | Post-class quiz | Check the day's SQL landed |

## Datasets

| Dataset | File or table | Why we use it today |
|---|---|---|
| LeBron game logs | `data/bron.db`, table `king_james` | Friendly single-table practice for `SELECT`, `WHERE`, sorting, limits, and nulls |
| Call center | `data/call_center_database2.db`, tables `agent`, `call`, `customer` | Operational story for aggregates and grouped summaries |
| Sequel City investigation | `data/crime_database.db` | Evidence story for filters, grouped counts, and careful questioning. The case continues on Day 2 |

## Lab Index

### Provided Files

| # | File | Focus |
|---|---|---|
| Quiz | `quiz/W4D1_Monday_Markdown_Mash.md` | Kickoff recap of Weeks 1 to 3 |
| Warmup | `Warmup_Drill_Pandas_to_SQL.md` | Instructions for the two-sitting warmup (pandas, then SQL) |
| Warmup | `Warmup_Pandas_to_SQL.ipynb` | Starter notebook: solve six questions in pandas, export to SQLite |
| Reading | `Reading_SQL_Foundations.md` | Student explainer: query anatomy, execution order, the pandas dictionary |
| Resources | `Student_Resources.md` | Curated documentation links and the deliverable checklist |
| 0 | `Activity_0_DBeaver_SQLite_Setup.md` | Install or open DBeaver, connect to SQLite, run a first query |
| 1 | `Activity_1_SQLite_SELECT_WHERE_LeBron.md` | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `NULL` |
| 2 | `Activity_2_SQLite_Aggregates_Call_Center.md` | Aggregates, `GROUP BY`, `HAVING` |
| 3 | `Activity_3_SQLite_Investigation_Crime.md` | Filters, grouped counts, `CASE`, evidence trail |
| Starter | `starter/w4d1_sqlite_drills.sql` | Query template you copy into your own workspace |
| Solutions | `solutions/` | Instructor-only solution SQL |
| Homework | `Homework_BigQuery_Transfer/` | Optional evening transfer drills on BigQuery Sandbox (own starter and instructions inside) |
| Quiz | `quiz/W4D1_Post_Quiz.md` | End-of-day knowledge check |

### Deliverables

| # | Deliverable | Format |
|---|---|---|
| 0 | Kickoff Mash | Markdown Mash responses |
| 1 | Warmup pandas answers plus your database | Completed notebook and `warmup_claims.db` in `student-work/week4/day1/` |
| 2 | SQLite setup proof | A query result grid in DBeaver against `bron.db` |
| 3 | Warmup SQL twins | Six queries under `-- Warmup` in your drill file, matching the pandas outputs |
| 4 | SQLite answers | `student-work/week4/day1/w4d1_sqlite_drills.sql` with Activities 1 to 3 |
| 5 | Reflections | SQL comments at the bottom of your drill file (each activity lists its prompts) |
| 6 | Post-class quiz | Markdown Mash responses |

## Student Workspace

Keep your work in your personal student folder, never inside this provided lab folder.

```bash
mkdir -p student-work/week4/day1
cd student-work/week4/day1
```

The warmup notebook walks you through creating the UV project here (`uv init`, `uv add pandas ipykernel`; the `.venv` lands in this folder). Copy `Warmup_Pandas_to_SQL.ipynb` and `starter/w4d1_sqlite_drills.sql` into this folder and complete your answers there. After the warmup, DBeaver does the rest of the day's work.

## Check Yourself Culture

Each activity includes a Check Yourself table with expected counts. If your number differs, that is not failure, that is the job: read your `WHERE` clause and find out why. Debugging a filter is the most common SQL task in real data engineering.

## Homework (Optional)

`Homework_BigQuery_Transfer/` re-asks today's ideas against a real cloud table (US baby names) in the free BigQuery Sandbox. Same SQL thinking, new engine, plus cost-awareness habits (no `SELECT *`, check the estimate before running). Recommended if today felt comfortable; skip guilt-free if you want the evening off. Wednesday uses BigQuery either way.

## Success Criteria

- You can explain what rows your `WHERE` clause keeps.
- You can use `COUNT`, `SUM`, and `AVG` without changing the original data.
- You can group rows and filter grouped results with `HAVING`, and say why that is not `WHERE`.
- You use `IS NULL`, never `= NULL`.
- Your Check Yourself numbers match, or you can explain why they did not at first.
- You did not use joins, CTEs, subqueries, window functions, or AI assistants.
