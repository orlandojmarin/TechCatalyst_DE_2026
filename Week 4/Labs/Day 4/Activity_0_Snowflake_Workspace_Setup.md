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

2. Create your Day 4 work folder, then copy in the notebooks and the load-review template. Do not edit files under `Week 4/Labs/Day 4/`.

   ```bash
   mkdir -p student-work/week4/day4
   cp "Week 4/Labs/Day 4/Activity_4_Pandas_ETL_to_Snowflake.ipynb" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/Activity_5_Pandas_Mirror.ipynb" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/Activity_6_Pandas_Parallel.ipynb" student-work/week4/day4/
   cp "Week 4/Labs/Day 4/day4_load_review_template.md" student-work/week4/day4/day4_load_review.md
   cd student-work/week4/day4
   ```

   The SQL lessons and activities keep their SQL inline in the instructions. You copy those code blocks straight into a Snowsight worksheet, so there are no `.sql` files to copy.

3. In VS Code, select `<repo-root>/.venv/bin/python` as the interpreter. The pandas activities (4, 5, 6) are notebooks, so select that same root environment as their Jupyter kernel after installing the packages from the repository root.

4. If you see `VIRTUAL_ENV does not match the project environment`, run `deactivate`, return to the repository root, and run `uv sync`.

5. Create `student-work/week4/day4/snow.cfg` with this content, filling in your own values:

   ```ini
   [DEV]
   account = <your_snowflake_account_identifier>
   user = <your_snowflake_username>
   password = <your_snowflake_password>
   role = DE
   warehouse = COMPUTE_WH
   database = TECHCATALYST
   schema = <your_assigned_schema>
   ```

   Your instructor provides the `account` identifier. The repository-root `.gitignore` already ignores `**/snow.cfg`, so your password stays on your machine. Keep the password in `snow.cfg` only, never in a notebook or script, and do not create another `.gitignore`. If your password sign-in fails (some accounts use SSO), remove the `password` line and add `authenticator = externalbrowser` instead.

6. In Snowsight, open **Projects, Workspaces**, then create a SQL worksheet for your Day 4 work. Use the same role, warehouse, database, and schema you put in `snow.cfg`.

7. Run this context block in your Snowsight worksheet, then copy the returned values into `day4_load_review.md`:

   ```sql
   USE ROLE DE;
   USE WAREHOUSE COMPUTE_WH;
   USE DATABASE TECHCATALYST;
   USE SCHEMA TECHCATALYST.<YOUR_NAME>;

   SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
   ```

## Expected output

```text
student-work/week4/day4/
├── day4_load_review.md
├── Activity_4_Pandas_ETL_to_Snowflake.ipynb
├── Activity_5_Pandas_Mirror.ipynb
├── Activity_6_Pandas_Parallel.ipynb
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
