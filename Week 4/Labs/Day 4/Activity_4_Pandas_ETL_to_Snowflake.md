# Activity 4: Pandas ETL to Snowflake

**Module:** Week 4 Day 4  
**Estimated Time:** 90 to 120 minutes  
**Difficulty:** Intermediate  
**Format:** Pairs, with individual code ownership  
**Prerequisites:** Python and pandas fundamentals, Activity 0 complete, Snowflake authentication preflight passed

## Objective

Build a complete ETL pipeline that reads a traffic-accident CSV from S3, profiles and cleans it with pandas, engineers analytical features, creates four business-facing DataFrames, publishes them as transient Snowflake tables, and reconciles the source and target row counts.

## Source

Use this file:

```text
s3://techcatalyst-de-2026/raw/accidents/accidents_2017_to_2023_english.csv
```

The validated source contains 463,152 rows and 27 columns. Do not substitute the NYC Taxi file in this activity. The second dataset gives you practice transferring the same engineering process to a new domain.

## Setup

1. From the repository root, add the notebook dependencies to the shared project.

   ```bash
   # If your terminal is still in student-work/week4/day4:
   cd ../../..
   ls pyproject.toml
   uv add pandas numpy s3fs pyarrow "snowflake-connector-python[pandas]" ipykernel
   uv run python -m ipykernel install --user --name techcatalyst-week4 --display-name "TechCatalyst 2026"
   ```

   These commands update the repository-root `pyproject.toml` and use the repository-root `.venv`. Do not run `uv init` in `student-work/week4/day4/`.

2. Enter your Day 4 work folder.

   ```bash
   cd student-work/week4/day4
   ```

3. Select `<repo-root>/.venv/bin/python` as the VS Code interpreter and select `TechCatalyst 2026` as the notebook kernel.

4. Open your copied `Activity_4_Pandas_ETL_to_Snowflake.ipynb`.

5. Open the `snow.cfg` file created in Activity 0. Complete its `[DEV]` section with the context supplied by your instructor.

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

   Use your own Snowflake username and password, the `DE` role, the `COMPUTE_WH` warehouse, and your personal schema (`TECHCATALYST.<your_name>`). Your instructor provides the account identifier. The notebook reads this section into a dictionary named `params` and connects with `snowflake.connector.connect(**params)`. The repository-root `.gitignore` already ignores every `snow.cfg`, so your password stays on your machine. Keep the password in `snow.cfg` only, never in the notebook, and do not create a nested `.gitignore`.

   Browser sign-in fallback: if your password sign-in fails (for example, your account uses SSO), remove the `password` line and add `authenticator = externalbrowser` instead. The connector then opens a browser for single sign-on rather than reading a password. The notebook explains this option in section 8 and accepts either style.

## Pipeline

| Phase | Provided scaffolding | You write |
|---|---|---|
| Extract | Imports, S3 URI, and the read call | Shape and schema assertions |
| Rename | The required source-to-target names and two dictionary examples | Complete the mapping dictionary, apply it, and verify required columns |
| Clean | One completed conversion example, method hints, and a guided function | Complete the remaining date, time, numeric, text, and required-row steps |
| Validate | Missing-value and integrity scaffolds plus a completed IQR algorithm | Complete the profile and integrity checks, run the IQR report, and interpret it |
| Engineer | Required feature definitions | Date parts, time bucket, weekend, fatal, multi-vehicle, and severity features |
| Analyze | Four business questions | Four grouped DataFrames with clear grain |
| Publish | A `snow.cfg` template, `ConfigParser` loader, one target DDL example, and write loop structure | Complete three target DDL statements, the `write_pandas` call, and reconciliation query |
| Explain | Reflection prompts | A concise comparison of pandas work and Snowflake work |

## Required Analytical Tables

| Snowflake table | One row represents | Required measures |
|---|---|---|
| `SEVERITY_ANALYSIS` | One weather and road-classification combination | Accident count and average severity score |
| `FATAL_TEMPORAL_PATTERNS` | One time-of-day and weekend combination | Number of fatal accidents |
| `CAUSE_VEHICLE_ANALYSIS` | One accident-cause and multi-vehicle combination | Accident count and average severity score |
| `QUARTERLY_HOTSPOT_ANALYSIS` | One state and quarter combination | Total accidents |

## Data-Quality Decisions

- Do not call `dropna()` on every column. Drop a row only when a field required for the four analyses is unusable.
- Rename `total_injured` to `total_injuries`. It equals minor plus serious injuries and does not include fatalities.
- Report IQR outliers. Do not delete them automatically. A severe crash can be rare and still valid.
- The notebook provides the IQR formula and implementation because memorizing that statistical method is not the objective. Your work is to run it, read the evidence, and explain whether an extreme value should be reviewed.
- Preserve the original row count whenever missing values occur only in fields that the analyses do not require.

## Expected Evidence

- Extracted shape: `(463152, 27)`.
- Cleaned row count: `463152`. Missing values occur only in fields not required by the four analyses.
- Missing-value profile: `reporting_station` 1,310; `highway_number` 990; `kilometer_marker` 990; `regional_office` 10.
- Zero mismatches for `minor_injuries + serious_injuries == total_injuries` after cleaning.
- Analysis row counts: `SEVERITY_ANALYSIS` 28; `FATAL_TEMPORAL_PATTERNS` 8; `CAUSE_VEHICLE_ANALYSIS` 167; `QUARTERLY_HOTSPOT_ANALYSIS` 108.
- Four successful `write_pandas` results.
- For every target table: DataFrame row count equals written row count equals Snowflake row count.
- Copy the final quality and reconciliation values into the Pandas ETL section of `day4_load_review.md`.

## Success Criteria

- Your notebook shows a complete extract, transform, validate, analyze, load, and reconcile process.
- Your cleaning code uses consistent final column names.
- Your pipeline does not discard rows because an unused reporting field is null.
- Your four analysis outputs answer different business questions.
- Your Snowflake tables are pre-created as transient tables with explicit schemas.
- No password, AWS key, token, or populated connection value appears in the notebook.
- Snowflake context is loaded from the root-ignored `snow.cfg` file and passed with `**params`.
- You can explain that `write_pandas` uses Parquet, a temporary stage, and `COPY INTO` behind the Python call.

## Hints

<details>
<summary>The S3 read fails</summary>

Stop and show the exact error. Do not paste cloud credentials into the notebook. The instructor will confirm S3 access or provide an approved local copy of the same file.

</details>

<details>
<summary>The Snowflake connection fails to authenticate</summary>

Confirm your `snow.cfg` has the right `account`, `user`, and `password`, and that `role = DE`, `warehouse = COMPUTE_WH`, `database = TECHCATALYST`, and `schema` is your own. Check for a stray space or a leftover `<placeholder>`. Keep the password in `snow.cfg` only, never in the notebook.

If the password still will not connect (some accounts require SSO), switch to the browser fallback: remove the `password` line and add `authenticator = externalbrowser`. A browser window opens for you to sign in, and no password is stored. If the browser flow cannot start in your environment, show the error to your instructor.

</details>

<details>
<summary>`write_pandas` reports an identifier error</summary>

Confirm that the DataFrame columns and target table columns use the same uppercase names, then use `quote_identifiers=False` as shown in the notebook guidance.

</details>

## Stretch Goals

1. Publish the cleaned row-level dataset to a fifth transient table in chunks, then compare its load time with the four small summaries.
2. Recreate one pandas analysis as a Snowflake SQL view and compare maintainability, compute location, and data movement.
3. Add one chart that communicates a decision, not only a distribution.
