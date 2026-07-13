# Warmup Drill: Pandas to SQL (Notebook + DBeaver)

**Module:** Week 4 Day 1
**Estimated Time:** 30 to 40 minutes (Parts 1 and 2 now; Part 3 right after Activity 0)
**Difficulty:** Beginner
**Format:** Individual, then partner check
**Prerequisites:** Weeks 2 and 3 pandas; VS Code with Jupyter support

## Objective

Solve six business questions in pandas on your own, export the DataFrame into a real SQLite database, then, after the SQL kickoff, answer the same six questions in SQL against your own database in DBeaver. By the end you have built the smallest possible pipeline (pandas in, database out) and proven that SQL is a second notation for thinking you already own.

## The Notebook

Everything happens in `Warmup_Pandas_to_SQL.ipynb`, which you copy into your own workspace:

```bash
mkdir -p student-work/week4/day1
cp "Week 4/Labs/Day 1/Warmup_Pandas_to_SQL.ipynb" student-work/week4/day1/
cd student-work/week4/day1
```

The `.venv` lands in `student-work/week4/day1/.venv`. Select it as the notebook kernel in VS Code (Select Kernel, Python Environments). If you see a `VIRTUAL_ENV does not match` warning, run `deactivate` first, and keep `.venv/` gitignored.

## The Three Parts

| Part | When | What you do |
|---|---|---|
| 1 | Morning opener, before any SQL | Solve six business questions (D1 to D6) in pandas yourself. Retrieval practice: you have used every move since Week 2. |
| 2 | Right after Part 1 | Run the given export cell: `claims.to_sql(...)` creates `warmup_claims.db` with a `claims` table, then read it back with `pd.read_sql` to prove the round trip. |
| 3 | After the SQL kickoff, demo, and Activity 0 | Connect DBeaver to `student-work/week4/day1/warmup_claims.db`, write the SQL for the same six questions under a `-- Warmup` header in `w4d1_sqlite_drills.sql`, and compare each result grid with your pandas output. |

## The Six Questions

| # | Business question | pandas move you already know |
|---|---|---|
| D1 | Show only the Connecticut claims | boolean filter |
| D2 | Claim id and amount for claims over 2,000 | filter plus column selection |
| D3 | How many claims per state? | `groupby` and size |
| D4 | Average claim amount for auto vs home | `groupby` and mean |
| D5 | Top three claims by amount, biggest first | sort and head |
| D6 | Find the claim with no recorded amount | `isna` |

## Worth Noticing

- The missing amount is `NaN` in pandas and `NULL` in the database. Same idea, two spellings, and D6 needs `IS NULL`, not `= NULL`.
- `to_sql` is a real data engineering move: you just loaded a database from a DataFrame. Friday you do the industrial version of this with `COPY INTO` on Snowflake.
- SQL results have no index column and no guaranteed row order. If D5 looks shuffled, that is what `ORDER BY` is for.

## Success Criteria

- The notebook runs top to bottom in your day 1 `.venv`.
- `warmup_claims.db` exists in `student-work/week4/day1/` and DBeaver can open it.
- All six pandas answers run, and all six SQL twins run in DBeaver and match them.
- You can name at least three pandas operations and their SQL twins from memory.
- You did not use AI assistants; solving it yourself is the exercise.
