# Activity 11: Pivot, Crosstab, and Melt Review

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 35 minutes  
**Difficulty:** Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel.

## Objective

In this activity, you will create spreadsheet-style summaries with `pivot_table`, count category combinations with `crosstab`, and reshape a wide table into a long table with `melt`.

## Documentation

| Resource | Why it helps |
|---|---|
| [pandas `pivot_table`](https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html) | Reference for spreadsheet-style summaries with rows, columns, values, and aggregation functions. |
| [pandas `crosstab`](https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html) | Reference for counting combinations of categories. |
| [pandas `melt`](https://pandas.pydata.org/docs/reference/api/pandas.melt.html) | Reference for changing wide data into long data. |

## Setup

From the repo root:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_11_Pivot_Crosstab_Melt" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_11_Pivot_Crosstab_Melt/`. Use the repo-root `.venv` as the kernel.

## Instructions

1. Read the assignment at the top of the notebook.
2. Run the worked pivot and melt examples.
3. Build a claim amount pivot table by region and claim type.
4. Build a channel-by-status crosstab.
5. Melt the monthly claims table from wide to long format.

## Expected Output

```text
a pivot table with regions as rows and claim types as columns
a crosstab with channels as rows and statuses as columns
a long monthly table with columns: region, month, claims
```

## Success Criteria

- You can say when to use `pivot_table` instead of `groupby`.
- You can use `crosstab` to count category combinations.
- You can explain why long format is useful for analysis and plotting.

## Hints

<details>
<summary>Hint 1</summary>

For `pivot_table`, choose `index`, `columns`, `values`, and `aggfunc`.

</details>

<details>
<summary>Hint 2</summary>

For `melt`, keep identifiers in `id_vars` and unpivot measurement columns with `value_vars`.

</details>

## Stretch Goals

- Add margins to the pivot table.
- Normalize the crosstab by row so each row sums to 1.

## Instructor Notes

- Common mistakes: using `pivot` when duplicate combinations require `pivot_table`, or forgetting to rename the melted value column.
- Debrief question: which shape is easier for a human to scan, and which shape is easier for a pipeline to process?
