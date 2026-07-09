# Activity 4: Crowdfunding Cleanup

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 30 minutes  
**Difficulty:** Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel. Do not run `uv init` inside this activity folder.

## Objective

In this activity, you will clean a campaign dataset and build a small outcome summary.

## Concepts Covered

| Concept | Where it appears |
|---|---|
| Column selection | working subset of campaign fields |
| Boolean filtering | `pledged > 0`, `country == "US"` |
| Derived columns | `average_pledge`, optional success flag |
| Aggregation | group by `staff_pick` |
| Business interpretation | evidence-based reflection |

## Background

Crowdfunding data is useful practice because it contains money, categories, boolean flags, and outcomes. Those are common ingredients in operational datasets.

## Setup

From the repo root, copy this whole activity folder into your day workspace:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_4_Crowdfunding_Cleanup" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_4_Crowdfunding_Cleanup/`. Use the repo-root `.venv` as the kernel. If VS Code shows a `VIRTUAL_ENV does not match` warning, run `deactivate` in the terminal and keep using `uv run` from the repo root.

Weeks 1 to 4 are still an AI-Free Zone. Write the pandas code yourself, ask a partner, or ask the instructor.

## Instructions

1. Copy the activity folder into `student-work/week3/day3/`.
2. Open `crowdfunding_cleanup.ipynb` from your copied folder.
3. Select only the working columns.
4. Filter to campaigns that raised money and then to US campaigns.
5. Create `average_pledge` and summarize outcomes by staff-pick status.

## Starter Code

Use `crowdfunding_cleanup.ipynb` in this folder. The notebook has imports, data paths, and TODO cells.

## Expected Output

```text
A staff-pick summary appears with counts, pledged totals, average pledge, and success rate.
```

## Success Criteria

- The filtered DataFrames have fewer rows for clear reasons.
- The `average_pledge` column is numeric.
- The staff-pick summary includes a readable success-rate measure.

## Hints

<details>
<summary>Hint 1</summary>

Use boolean masks such as `df[df["pledged"] > 0]`.

</details>

<details>
<summary>Hint 2</summary>

A success flag can be created with `(df["outcome"] == "successful").astype(int)`.

</details>

## Stretch Goals

- Break `category` into a top-level category before grouping.
- Compare staff-pick outcomes across the top five categories.

## Instructor Notes

- Common mistakes: filtering the original DataFrame after creating a cleaned copy, or calculating average pledge before removing zero-backer rows.
- Debrief question: what would you check before advising a business leader from this summary?
