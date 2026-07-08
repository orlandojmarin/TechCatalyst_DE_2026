# Activity 10: Duplicate and Key Quality Clinic

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 30 minutes  
**Difficulty:** Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel.

## Objective

In this activity, you will inspect duplicate rows, check whether a column is a safe key, deduplicate with a stated policy, and verify row counts before and after a join.

## Documentation

| Resource | Why it helps |
|---|---|
| [pandas `DataFrame.duplicated`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html) | Shows how to mark duplicate rows or duplicate business keys. |
| [pandas `DataFrame.drop_duplicates`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html) | Shows how to remove duplicates with `subset` and `keep`. |
| [pandas `merge`](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) | Reference for joins and row-count-sensitive merge behavior. |

## Setup

From the repo root:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_10_Duplicate_Key_Quality" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_10_Duplicate_Key_Quality/`. Use the repo-root `.venv` as the kernel.

Weeks 1 to 4 are still an AI-Free Zone. Write the pandas code yourself, ask a partner, or ask the instructor.

## Instructions

1. Read the assignment at the top of the notebook.
2. Run the worked examples for `duplicated` and `drop_duplicates`.
3. Complete the claim-key tasks using `claims_key_quality.csv`.
4. Check the policy lookup table for duplicate keys before joining.
5. Write a short explanation of which rows you kept and why.

## Expected Output

```text
claim_id duplicate rows found
business-key duplicates found
policy lookup key is not unique before cleanup
left join row count matches cleaned claims after lookup cleanup
```

## Success Criteria

- You can identify exact duplicate rows and duplicate business keys.
- You can explain the difference between a record identifier and a business key.
- You clean duplicates with an explicit `keep` policy.
- You check row counts before and after a join.

## Hints

<details>
<summary>Hint 1</summary>

Use `df.duplicated(subset=[...], keep=False)` when you want to see every row involved in a duplicate group.

</details>

<details>
<summary>Hint 2</summary>

Use `drop_duplicates(subset=[...], keep="last")` only after sorting by the timestamp that defines "last".

</details>

## Stretch Goals

- Try `pd.merge(..., validate="many_to_one")` after cleaning the lookup table.
- Create a small audit table that reports row counts at each stage.

## Instructor Notes

- Common mistakes: checking duplicates on all columns when the actual issue is the business key, or joining before checking the lookup table key.
- Debrief question: why can a join multiply rows even when the source table looks clean?
