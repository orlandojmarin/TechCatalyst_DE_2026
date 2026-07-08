# Activity 5: Groupby Time Series

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 30 minutes  
**Difficulty:** Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel. Do not run `uv init` inside this activity folder.

## Objective

In this activity, you will clean time-stamped price data and summarize it by group and month.

## Concepts Covered

| Concept | Where it appears |
|---|---|
| Date parsing | `parse_dates=["data_date"]` |
| Column cleanup | `drop` unused fields |
| Missing data | `dropna` on price |
| Datetime features | calendar month from `.dt` |
| Aggregation | `groupby`, `agg`, sorted range |

## Background

This activity modernizes the older groupby drill for pandas 3. Use `parse_dates` for the date column, then use `.dt` accessors and `groupby` to summarize.

## Setup

From the repo root, copy this whole activity folder into your day workspace:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_5_Groupby_Time_Series" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_5_Groupby_Time_Series/`. Use the repo-root `.venv` as the kernel. If VS Code shows a `VIRTUAL_ENV does not match` warning, run `deactivate` in the terminal and keep using `uv run` from the repo root.

Weeks 1 to 4 are still an AI-Free Zone. Write the pandas code yourself, ask a partner, or ask the instructor.

## Instructions

1. Copy the activity folder into `student-work/week3/day3/`.
2. Open `groupby_time_series.ipynb` from your copied folder.
3. Drop unused timestamp columns and remove missing prices.
4. Set and sort a datetime index.
5. Create coin-level and month-level summaries.

## Starter Code

Use `groupby_time_series.ipynb` in this folder. The notebook has imports, data paths, and TODO cells.

## Expected Output

```text
A summary table appears with average, minimum, maximum, and range by cryptocurrency.
```

## Success Criteria

- Dates are parsed as datetime values.
- Missing prices are removed before aggregation.
- The summary table correctly identifies the widest price range.

## Hints

<details>
<summary>Hint 1</summary>

Use `parse_dates=["data_date"]`; do not add older date-parser arguments.

</details>

<details>
<summary>Hint 2</summary>

Use `df.groupby("cryptocurrency")["data_priceUsd"].agg([...])`.

</details>

## Stretch Goals

- Plot monthly average prices for two coins.
- Add a count column so you can see how many observations support each summary.

## Instructor Notes

- Common mistakes: grouping before converting prices to numeric, or leaving missing prices in the dataset.
- Debrief question: why can min, max, and average tell different stories?
