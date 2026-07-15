# Activity 0: SQL Workspace Setup

**Module:** Week 4 Day 3  
**Estimated Time:** 20 minutes  
**Difficulty:** Beginner  
**Format:** Individual, then pair check  
**Prerequisites:** Day 2 joins complete

## Objective

Create a clean Day 3 work folder under `student-work/week4/day3/` and copy the SQL starters. Day 3 does not create another Python project or virtual environment.

## Background

Most of today's work happens in BigQuery, SQLite, and Snowflake. Your editable SQL files and notes belong under `student-work/`, while the repository-root `.venv`, `pyproject.toml`, `uv.lock`, and `.gitignore` remain shared.

## Instructions

1. Start at the repository root and verify the shared Python project.

   ```bash
   pwd
   ls pyproject.toml
   uv sync
   uv run python --version
   ```

   Do not run `uv init`. The repository project already exists.

2. Create the Day 3 work folder.

   ```bash
   mkdir -p student-work/week4/day3
   ```

3. Copy the starter files from the repository root.

   ```bash
   cp "Week 4/Labs/Day 3/starter/day3_gtfs_setup.sql" student-work/week4/day3/gtfs_setup.sql
   cp "Week 4/Labs/Day 3/starter/day3_gtfs_warmup.sql" student-work/week4/day3/gtfs_warmup.sql
   cp "Week 4/Labs/Day 3/starter/day3_public_taxi_cte_drills.sql" student-work/week4/day3/
   cp "Week 4/Labs/Day 3/starter/day3_public_taxi_business_challenge.sql" student-work/week4/day3/
   cp "Week 4/Labs/Day 3/starter/day3_sqlite_ddl_fast_finisher.sql" student-work/week4/day3/
   cp "Week 4/Labs/Day 3/starter/day3_snowflake_ddl_mirror.sql" student-work/week4/day3/
   cp "Week 4/Labs/Day 3/starter/w4d3_snowflake_tpch_transfer.sql" student-work/week4/day3/
   cp "Week 4/Labs/Day 3/starter/day3_query_review_template.md" student-work/week4/day3/day3_query_review.md
   ```

4. Enter the work folder and inspect the copies.

   ```bash
   cd student-work/week4/day3
   ls -la
   ```

5. If VS Code requests a Python interpreter, select `<repo-root>/.venv/bin/python`. If you create a notebook for notes, select the same root environment as the Jupyter kernel.

6. Open `day3_query_review.md` and record the approved BigQuery public table and partner name.

7. In BigQuery, confirm that GoogleSQL is selected. Preview the approved public table's schema and record its fully qualified name.

## Expected output

```text
student-work/week4/day3/
├── day3_query_review.md
├── gtfs_setup.sql
├── gtfs_warmup.sql
├── day3_public_taxi_cte_drills.sql
├── day3_public_taxi_business_challenge.sql
├── day3_sqlite_ddl_fast_finisher.sql
├── day3_snowflake_ddl_mirror.sql
└── w4d3_snowflake_tpch_transfer.sql
```

The `.venv`, `pyproject.toml`, `uv.lock`, and `.gitignore` remain at the repository root and do not appear in this tree.

## Success criteria

- Your editable files are under `student-work/week4/day3/`.
- VS Code uses `<repo-root>/.venv/bin/python` if Python is needed.
- No nested `.venv`, `pyproject.toml`, `uv.lock`, or `.gitignore` was created.
- You copied the GTFS setup, six learner SQL starters, and the review template.
- You recorded the approved public table.
- You can explain why provided files remain untouched under `Week 4/Labs/Day 3/`.

## Hints

<details>
<summary>I accidentally created Python project files in the Day 3 folder</summary>

Stop and show the folder contents to the instructor before deleting anything. Day 3 should use the repository-root project only.

</details>

<details>
<summary>I cannot access the public table</summary>

Ask the instructor to confirm the classroom project and approved public table. Continue with the GTFS and SQLite activities while access is checked.

</details>

<details>
<summary>I see a `VIRTUAL_ENV does not match` warning</summary>

Run `deactivate`, return to the repository root, then run `uv sync`.

</details>

## Stretch goals

- Create a `screenshots/` folder for query results.
- Add a short note explaining why Day 2 table design matters for today's SQL costs.
