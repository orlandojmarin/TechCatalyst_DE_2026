# Activity 9: Concat DataFrames

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 30 minutes  
**Difficulty:** Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel. Do not run `uv init` inside this activity folder.

## Objective

In this activity, you will combine multiple related CSV files with `pd.concat` and `merge`.

## Concepts Covered

| Concept | Where it appears |
|---|---|
| Multiple CSV inputs | four related files |
| Row-wise concat | `pd.concat(..., ignore_index=True)` |
| Key discipline | organization label before combining |
| Merge | join dues to membership status |
| Aggregation | balance summary by organization |

## Background

This is the strongest bridge from pandas review into SQL. Row-wise concat behaves like stacking similar tables. The merge step behaves like joining related tables.

## Setup

From the repo root, copy this whole activity folder into your day workspace:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_9_Concat_Dataframes" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_9_Concat_Dataframes/`. Use the repo-root `.venv` as the kernel. If VS Code shows a `VIRTUAL_ENV does not match` warning, run `deactivate` in the terminal and keep using `uv run` from the repo root.

Weeks 1 to 4 are still an AI-Free Zone. Write the pandas code yourself, ask a partner, or ask the instructor.

## Instructions

1. Copy the activity folder into `student-work/week3/day3/`.
2. Open `concat_dataframes.ipynb` from your copied folder.
3. Inspect the four source CSVs.
4. Add organization labels before combining data.
5. Concat dues tables, concat member-status tables, then merge into a master ledger.
6. Create a balance check by organization.

## Starter Code

Use `concat_dataframes.ipynb` in this folder. The notebook has imports, data paths, and TODO cells.

## Expected Output

```text
A master ledger appears with dues, payment, membership status, organization, and balance due.
```

## Success Criteria

- The combined tables preserve organization labels.
- `all_dues_df` and `all_members_df` stack rows correctly.
- The final ledger uses both `MemberName` and `Organization` as merge keys.
- The balance summary is grouped by organization.

## Hints

<details>
<summary>Hint 1</summary>

Use `pd.concat([df1, df2], ignore_index=True)` for row-wise stacking.

</details>

<details>
<summary>Hint 2</summary>

Use `pd.merge(..., on=["MemberName", "Organization"], how="inner")` for the final combination.

</details>

## Stretch Goals

- Try an outer merge and inspect unmatched rows.
- Write the master ledger to `Output/master_ledger.csv`.

## Instructor Notes

- Common mistakes: losing source organization before concat, or merging only on `MemberName` and accidentally matching people across organizations.
- Debrief question: why are keys more important than function names when combining tables?
