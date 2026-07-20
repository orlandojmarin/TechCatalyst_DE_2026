# Student Resources: Week 5 Day 1

**AI allowed, review required.** This week you may use an AI assistant to explain or draft, but you must read, run, and be able to defend every line you submit. Do not paste credentials or private data into an assistant.

## Core Documentation

| Topic | Link | Why it matters today |
|---|---|---|
| Data loading overview | [Snowflake data loading](https://docs.snowflake.com/en/user-guide/data-load-overview) | The big picture of stages, formats, and `COPY INTO`. |
| `COPY INTO` table | [COPY INTO](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table) | The load command and its options (`FILES`, `MATCH_BY_COLUMN_NAME`). |
| `CREATE FILE FORMAT` | [File formats](https://docs.snowflake.com/en/sql-reference/sql/create-file-format) | CSV, JSON, and Parquet parsing contracts. |
| Semi-structured data | [Querying VARIANT](https://docs.snowflake.com/en/user-guide/querying-semistructured) | Keep raw JSON, then flatten with path syntax. |
| Window functions | [Analytic functions](https://docs.snowflake.com/en/sql-reference/functions-analytic) | Ranking, `LAG`/`LEAD`, running totals, moving averages. |
| `QUALIFY` | [QUALIFY](https://docs.snowflake.com/en/sql-reference/constructs/qualify) | Filter on a window function without a CTE: `HAVING` for windows. |
| Snowpark Python | [Snowpark](https://docs.snowflake.com/en/developer-guide/snowpark/python/index) | DataFrame API that runs inside Snowflake. |
| Snowpark DataFrames | [Working with DataFrames](https://docs.snowflake.com/en/developer-guide/snowpark/python/working-with-dataframes) | `session.table`, transformations, actions, and writing back. |
| Polars | [Polars user guide](https://docs.pola.rs/) | Fast single-machine DataFrames for the review drills. |

## Concepts, in one line each

- **Stage**: a named pointer to files in cloud storage; it holds no rows.
- **File format**: how to parse a file (CSV delimiter and header, JSON, Parquet).
- **`COPY INTO`**: loads staged files through a file format into a table.
- **`VARIANT`**: a column type that holds raw JSON so you can flatten it later.
- **Window function**: keeps every row and adds a value computed over a related window.
- **`PARTITION BY` / `ORDER BY` / frame**: choose the window (group, order, nearby rows).
- **`QUALIFY`**: filters rows on a window result, after the windows are computed.
- **Snowpark**: DataFrame code that Snowflake runs as SQL, without moving data to your machine.
- **Lazy evaluation**: transformations build a plan; nothing runs until an action asks for results.

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Load pulls the wrong file | You loaded a whole prefix | Name the exact file with `FILES = ('...')`. |
| CSV columns land in the wrong place | Header not matched | Use `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` with a header-aware format. |
| JSON load fails or is unusable | Loading into typed columns | Load into one `VARIANT` column, then flatten with path syntax. |
| Ranking skips numbers on ties | `RANK` leaves gaps | Use `DENSE_RANK` when you do not want gaps. |
| Running total looks wrong | Missing `ORDER BY` in `OVER` | Accumulation needs an ordered window. |
| Share-of-total becomes a running share | `ORDER BY` inside `OVER` out of habit | A whole-partition window takes no `ORDER BY`. |
| Snowpark `session.table` fails | The table was never created | Run the setup block from the matching activity first. |
| Notebook is slow or memory spikes | `to_pandas` before aggregating | Aggregate in Snowflake, then convert the small result. |

## Lab Deliverable Checklist

| Done | Deliverable |
|---|---|
| [ ] | Week 5 Day 1 work folder created under `student-work/week5/day1/` |
| [ ] | Kickoff drills notebook completed, all seven checkpoints matched (Activity 1) |
| [ ] | Parquet and CSV files loaded, before/after counts prove no duplicates, cross-format totals match (Activity 2) |
| [ ] | RAW to CLEAN to FINAL built with zero rule violations and exact reconciliation (Activity 3) |
| [ ] | Window drills W1 through W5 match the checkpoints (Activity 4) |
| [ ] | TPC-H S1 and S2 completed, with S2 ranking top three (descending) |
| [ ] | Time series window drills: all checkpoints matched, W4 uses `QUALIFY` (Activity 5) |
| [ ] | Pandas twin completed and agrees with the Activity 5 SQL grids (Activity 6) |
| [ ] | Snowpark first flight completed, `W5D1_CLAIMS_ENRICHED` verified in Snowsight (Activity 7) |
| [ ] | Wrap-up questions from Activity 7 answered in a markdown cell |
