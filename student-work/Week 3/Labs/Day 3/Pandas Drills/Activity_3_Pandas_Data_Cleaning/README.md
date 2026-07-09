# Activity 3: Pandas Data Cleaning

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 25 minutes  
**Difficulty:** Beginner to Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel. Do not run `uv init` inside this activity folder.

## Objective

In this activity, you will load, inspect, clean, and summarize a messy stock dataset with pandas.

## Concepts Covered

| Concept | Where it appears |
|---|---|
| CSV loading and inspection | `read_csv`, `.head()`, `.shape`, `.dtypes` |
| Missing data profiling | `.isna().sum()`, `.isna().mean()` |
| Type conversion | `pd.to_numeric` on currency-like text |
| Cleaning policy | `fillna`, `dropna` |
| Aggregation | `groupby` and `agg` |

## Background

This is a focused cleaning drill. The goal is not finance knowledge. The goal is to practice the same inspection and cleanup sequence you will use in pipeline work.

## Setup

From the repo root, copy this whole activity folder into your day workspace:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_3_Pandas_Data_Cleaning" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_3_Pandas_Data_Cleaning/`. Use the repo-root `.venv` as the kernel. If VS Code shows a `VIRTUAL_ENV does not match` warning, run `deactivate` in the terminal and keep using `uv run` from the repo root.

Weeks 1 to 4 are still an AI-Free Zone. Write the pandas code yourself, ask a partner, or ask the instructor.

## Instructions

1. Copy the activity folder into `student-work/week3/day3/`.
2. Open `pandas_data_cleaning.ipynb` from your copied folder.
3. Read the CSV, inspect shape and dtypes, and profile missing values.
4. Clean money columns and missing EBITDA values.
5. Build a sector summary and write the reflection.

## Starter Code

Use `pandas_data_cleaning.ipynb` in this folder. The notebook has imports, data paths, and TODO cells.

## Expected Output

```text
A sector summary appears with one row per sector, numeric averages, and a company count.
```

## Success Criteria

- The notebook runs top to bottom without errors.
- You can explain which rows were dropped and why.
- Your summary table uses numeric columns, not dollar-string columns.

## Hints

<details>
<summary>Hint 1</summary>

Use `df.isna().sum()` for missing counts and `df.isna().mean() * 100` for missing percent.

</details>

<details>
<summary>Hint 2</summary>

Use `pd.to_numeric(..., errors="coerce")` when a column may contain bad numeric strings.

</details>

## Stretch Goals

- Sort the sector summary by company count or average price.
- Add one validation cell that confirms no critical fields are missing.

## Instructor Notes

- Common mistakes: converting a dollar string without removing `$`, dropping all rows before filling EBITDA, or forgetting to assign the result of `dropna`.
- Debrief question: which cleaning decisions preserve data, and which remove data?
