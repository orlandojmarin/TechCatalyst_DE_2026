# Activity 12: Rolling Windows and Time-Series Signals

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 30 minutes  
**Difficulty:** Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel.

## Objective

In this activity, you will smooth noisy daily data with rolling averages, compare today to yesterday with `shift`, and create simple signal flags.

## Documentation

| Resource | Why it helps |
|---|---|
| [pandas `DataFrame.rolling`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html) | Reference for rolling calculations such as moving averages. |
| [pandas `DataFrame.shift`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html) | Reference for comparing a row with a prior row. |
| [pandas `DataFrame.pct_change`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html) | Reference for percent change calculations. |

## Setup

From the repo root:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_12_Rolling_Window_Signals" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_12_Rolling_Window_Signals/`. Use the repo-root `.venv` as the kernel.

## Instructions

1. Read the assignment at the top of the notebook.
2. Run the worked rolling and shift examples.
3. Parse the daily claims data and sort by date.
4. Add a 7-day rolling average for claims filed.
5. Add day-over-day difference and percent change columns.
6. Create a signal flag for days that are above the rolling average by a meaningful amount.

## Expected Output

```text
a daily DataFrame with rolling average, prior-day comparison, percent change, and signal flag columns
```

## Success Criteria

- Your date column is parsed as datetime.
- Your rolling average uses the sorted date order.
- Your signal flag is based on a clear rule.
- You can explain why a rolling average is different from a raw daily count.

## Hints

<details>
<summary>Hint 1</summary>

Use `rolling(window=7, min_periods=3).mean()` so the first few rows can still produce values.

</details>

<details>
<summary>Hint 2</summary>

Use `shift(1)` to pull yesterday's value next to today's value.

</details>

## Stretch Goals

- Add a rolling average for total claim amount.
- Create a plot of raw claims and the rolling average.

## Instructor Notes

- Common mistakes: calculating rolling averages before sorting by date, or interpreting percent change without checking the denominator.
- Debrief question: what business question is a rolling average better at answering than a raw daily count?
