# Activity 6: Search For The Worst

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 15 minutes  
**Difficulty:** Beginner  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel. Do not run `uv init` inside this activity folder.

## Objective

In this activity, you will practice category inspection, filtering, sorting, and selecting the top row.

## Concepts Covered

| Concept | Where it appears |
|---|---|
| Category inspection | `unique` |
| Boolean filtering | two-condition mask |
| Sorting | `sort_values` |
| Index reset | `reset_index` |
| Row selection | `iloc[0]` |

## Background

This is a quick confidence rep. It overlaps with earlier filtering and sorting practice, so use it when students need another repetition before moving on.

## Setup

From the repo root, copy this whole activity folder into your day workspace:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_6_Search_For_The_Worst" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_6_Search_For_The_Worst/`. Use the repo-root `.venv` as the kernel. If VS Code shows a `VIRTUAL_ENV does not match` warning, run `deactivate` in the terminal and keep using `uv run` from the repo root.

Weeks 1 to 4 are still an AI-Free Zone. Write the pandas code yourself, ask a partner, or ask the instructor.

## Instructions

1. Copy the activity folder into `student-work/week3/day3/`.
2. Open `search_for_the_worst.ipynb` from your copied folder.
3. Inspect utility and owner categories.
4. Filter to one utility-owner slice.
5. Sort by usage and identify the highest-usage record.

## Starter Code

Use `search_for_the_worst.ipynb` in this folder. The notebook has imports, data paths, and TODO cells.

## Expected Output

```text
The notebook displays the highest-usage tenant electricity row.
```

## Success Criteria

- You inspected categories before filtering.
- Your filtered DataFrame contains only the requested utility and owner.
- Your top row comes from a descending sort by `Usage`.

## Hints

<details>
<summary>Hint 1</summary>

Use `.unique()` to inspect categories.

</details>

<details>
<summary>Hint 2</summary>

Use `(condition_one) & (condition_two)` for a two-part mask.

</details>

## Stretch Goals

- Repeat the workflow for another utility and compare the result.
- Create a function that returns the worst row for any utility-owner pair.

## Instructor Notes

- Common mistakes: missing parentheses around boolean conditions, or sorting ascending by mistake.
- Debrief question: what makes a metric actionable rather than merely large?
