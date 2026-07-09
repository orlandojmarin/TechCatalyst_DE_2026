# Activity 8: Comic Books Summary

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 20 minutes  
**Difficulty:** Beginner to Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel. Do not run `uv init` inside this activity folder.

## Objective

In this activity, you will turn a cleaned dataset into summary metrics and a grouped count table.

## Concepts Covered

| Concept | Where it appears |
|---|---|
| Summary metrics | `nunique`, `min`, `max`, row count |
| DataFrame construction | one-row summary table |
| Frequency counts | `value_counts` |
| Grouped thinking | scalar metric vs grouped metric |

## Background

This is a compact aggregation drill. It pairs well after Activity 7, but it also includes a provided clean CSV so it can stand alone.

## Setup

From the repo root, copy this whole activity folder into your day workspace:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_8_Comic_Books_Summary" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_8_Comic_Books_Summary/`. Use the repo-root `.venv` as the kernel. If VS Code shows a `VIRTUAL_ENV does not match` warning, run `deactivate` in the terminal and keep using `uv run` from the repo root.

Weeks 1 to 4 are still an AI-Free Zone. Write the pandas code yourself, ask a partner, or ask the instructor.

## Instructions

1. Copy the activity folder into `student-work/week3/day3/`.
2. Open `comic_books_summary.ipynb` from your copied folder.
3. Inspect the cleaned data.
4. Calculate one-row summary metrics.
5. Build a top-10 country count table.

## Starter Code

Use `comic_books_summary.ipynb` in this folder. The notebook has imports, data paths, and TODO cells.

## Expected Output

```text
A one-row summary table appears, plus a top-10 country count table.
```

## Success Criteria

- The summary table contains counts and year range metrics.
- The country table is sorted from most publications to fewest.
- You can explain the difference between a scalar metric and a grouped table.

## Hints

<details>
<summary>Hint 1</summary>

Use `.nunique()` for unique counts.

</details>

<details>
<summary>Hint 2</summary>

Use `.value_counts().head(10)` for the country count table.

</details>

## Stretch Goals

- Add a publisher count table.
- Compare earliest and latest publication years by country.

## Instructor Notes

- Common mistakes: counting rows instead of unique values, or leaving numeric year values as strings.
- Debrief question: when should a pipeline produce a summary table instead of only a cleaned table?
