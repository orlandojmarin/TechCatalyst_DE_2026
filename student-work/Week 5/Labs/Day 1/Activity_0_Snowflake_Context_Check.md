# Activity 0: Snowflake Context Check

**Module:** Week 5 Day 1  
**Estimated Time:** 10 minutes  
**Difficulty:** Beginner  
**Format:** Individual  
**Prerequisites:** Your Week 4 Snowflake access

## Objective

Confirm you are working in your own Snowflake schema and set up a Week 5 work folder. You already created `snow.cfg` in Week 4, so this is a quick check, not a new setup.

## Steps

1. From the repository root, make your Week 5 Day 1 work folder.

   ```bash
   mkdir -p student-work/week5/day1
   ```

2. If you will run the pandas or Polars drills, copy your Week 4 `snow.cfg` beside your Week 5 work so the notebooks can connect.

   ```bash
   cp student-work/week4/day4/snow.cfg student-work/week5/day1/snow.cfg
   ```

   The repository-root `.gitignore` already ignores every `snow.cfg`. Keep your password in that file only, never in a notebook or a worksheet.

3. Open a Snowsight worksheet and set your context:

   ```sql
   USE ROLE DE;
   USE WAREHOUSE COMPUTE_WH;
   USE DATABASE TECHCATALYST;
   USE SCHEMA TECHCATALYST.<YOUR_NAME>;

   SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
   ```

## Success Criteria

- `CURRENT_SCHEMA()` returns your own schema.
- Your Week 5 work folder exists under `student-work/week5/day1/`.
- No password appears in any worksheet or notebook.
