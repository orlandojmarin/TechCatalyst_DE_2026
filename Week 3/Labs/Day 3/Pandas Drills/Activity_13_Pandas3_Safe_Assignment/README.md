# Activity 13: Pandas 3 Safe Assignment

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 25 minutes  
**Difficulty:** Beginner to Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel.

## Objective

In this activity, you will practice pandas 3 assignment habits: copy when you intend a separate DataFrame, and use `.loc[row_mask, column] = value` when you intend to update rows.

## Documentation

| Resource | Why it helps |
|---|---|
| [pandas Copy-on-Write guide](https://pandas.pydata.org/docs/user_guide/copy_on_write.html) | Explains the pandas 3 behavior behind safer assignment patterns. |
| [pandas `DataFrame.loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html) | Reference for label-based row and column assignment. |
| [pandas 3.0 release notes](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html) | Currentness reference for pandas 3 behavior changes. |

## Setup

From the repo root:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_13_Pandas3_Safe_Assignment" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_13_Pandas3_Safe_Assignment/`. Use the repo-root `.venv` as the kernel.

## Instructions

1. Read the assignment at the top of the notebook.
2. Run the worked example that shows a separate filtered copy.
3. Run the worked example that updates rows safely with `.loc`.
4. Complete the claim-review tasks.
5. Explain when you used `.copy()` and when you used `.loc`.

## Expected Output

```text
a review queue DataFrame with priority labels, escalation flags, and clean row updates
```

## Success Criteria

- You do not assign into a chained selection.
- You use `.copy()` when creating a separate working DataFrame.
- You use `.loc[row_mask, "column"] = value` for targeted updates.
- You can explain why pandas 3 makes this habit more important.

## Hints

<details>
<summary>Hint 1</summary>

Use `mask = df["claim_amount"] >= 5000`, then `df.loc[mask, "priority"] = "high"`.

</details>

<details>
<summary>Hint 2</summary>

Use `.copy()` after filtering when the filtered DataFrame is meant to become its own separate object.

</details>

## Stretch Goals

- Add a second flag based on both `status` and `review_score`.
- Create a small summary count by priority.

## Instructor Notes

- Common mistakes: assigning to `df[df["status"] == "open"]["priority"]`, or making a filtered DataFrame without `.copy()` and assuming it will update the original.
- Debrief question: how does explicit assignment make notebooks easier to debug?
