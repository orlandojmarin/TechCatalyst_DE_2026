# Activity 0: Snowflake Workspace and Context Setup

**Module:** Week 4 Day 4  
**Estimated Time:** 20 minutes  
**Difficulty:** Beginner  
**Format:** Individual, then partner check  
**Prerequisites:** Instructor-provided Snowflake account access

## Objective

Create a safe Day 4 work folder under `student-work/week4/day4/`, copy the starters, verify the repository-root Python environment, and record the Snowflake context used for object work.

## Instructions

1. Start at the repository root and synchronize the existing Python project.

   ```bash
   pwd
   ls pyproject.toml
   uv sync
   uv run python --version
   ```

   The environment is `<repo-root>/.venv`. Do not run `uv init` or create another `.venv`, `pyproject.toml`, `uv.lock`, or `.gitignore` in the Day 4 folder.

2. Create the work folder and copy the starter files. Do not edit files under `Week 4/Labs/Day 4/`.

   ```bash
   mkdir -p student-work/week4/day4
   cp "Week 4/Labs/Day 4/starter/w4d4_context_and_object_lifecycle.sql" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/starter/w4d4_stage_and_load.sql" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/starter/w4d4_snowflake_sql_drills.sql" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/starter/w4d4_mastery_dataset_setup.sql" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/starter/w4d4_sql_cte_mastery_drills.sql" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/starter/w4d4_pandas_mastery_drills.py" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/starter/Activity_4_Pandas_ETL_to_Snowflake.ipynb" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/starter/snow.cfg.example" student-work/week4/day4/snow.cfg
   cp "Week 4/Labs/Day 4/starter/day4_load_review_template.md" student-work/week4/day4/day4_load_review.md
   cd student-work/week4/day4
   ```

3. In VS Code, select `<repo-root>/.venv/bin/python` as the interpreter. Activity 4 uses a notebook, so select that same root environment as its Jupyter kernel after installing the Activity 4 packages from the repository root.

4. If you see `VIRTUAL_ENV does not match the project environment`, run `deactivate`, return to the repository root, and run `uv sync`.

5. Open `student-work/week4/day4/snow.cfg`. In `[DEV]`, fill in your own `user` and `password`, set `role = DE`, `warehouse = COMPUTE_WH`, `database = TECHCATALYST`, and `schema` to your personal schema. Your instructor provides the `account` identifier.

   The populated `.cfg` belongs in the Day 4 work folder. The repository-root `.gitignore` already ignores `**/snow.cfg`, so your password stays on your machine. Keep the password in `snow.cfg` only, never in a notebook or script, and do not create another `.gitignore`.

6. In Snowsight, open **Projects, Workspaces**, then create a SQL file named `day4_snowflake_objects.sql`. Use the same role, warehouse, database, and schema recorded in `snow.cfg`.

7. Run only the context block at the top of `w4d4_context_and_object_lifecycle.sql`. Copy the returned values into `day4_load_review.md`.

## Expected output

```text
student-work/week4/day4/
├── day4_load_review.md
├── w4d4_context_and_object_lifecycle.sql
├── w4d4_stage_and_load.sql
├── w4d4_snowflake_sql_drills.sql
├── w4d4_mastery_dataset_setup.sql
├── w4d4_sql_cte_mastery_drills.sql
├── w4d4_pandas_mastery_drills.py
├── Activity_4_Pandas_ETL_to_Snowflake.ipynb
└── snow.cfg
```

The `.venv`, `pyproject.toml`, `uv.lock`, and `.gitignore` remain at the repository root. The Snowflake context query returns one row with an active role, warehouse, database, and schema.

## Success criteria

- Your editable work is under `student-work/week4/day4/`.
- VS Code and Jupyter use `<repo-root>/.venv/bin/python`.
- No nested `.venv`, `pyproject.toml`, `uv.lock`, or `.gitignore` was created.
- You recorded all four Snowflake context values.
- Your folder-level `snow.cfg` contains `[DEV]` with your `account`, `user`, `password`, `role = DE`, `warehouse = COMPUTE_WH`, `database = TECHCATALYST`, and your `schema`.
- You know that the instructor provides the storage integration, not cloud credentials.

## Hints

<details>
<summary>I can see the database but cannot create an object</summary>

Visibility is not the same as permission. Record the exact error and ask the instructor to confirm your assigned role and schema. Do not change to an administrator role.

</details>

<details>
<summary>My warehouse is blank or suspended</summary>

Use the instructor-provided warehouse in the Workspaces context selector. If you cannot resume it, ask the instructor. Only roles with the right privilege can alter a warehouse.

</details>
