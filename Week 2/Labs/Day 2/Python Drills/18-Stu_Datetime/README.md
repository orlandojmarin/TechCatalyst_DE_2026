# datetime

**Label: Core.** Time is everywhere in data: claim dates, appointment times, taxi
timestamps. Parsing, formatting, and doing arithmetic on dates is essential before
pandas takes over on Day 4 and in the capstone.

## The two core moves

```python
from datetime import datetime, timedelta

# string -> datetime (parse)
d = datetime.strptime("2026-05-02", "%Y-%m-%d")

# datetime -> string (format)
d.strftime("%m/%d/%Y")        # '05/02/2026'

# arithmetic
(d2 - d1).days                # difference in days
d + timedelta(days=30)        # 30 days later
```

`%Y-%m-%d` is the format code: 4-digit year, 2-digit month, 2-digit day.

## Instructions

Copy `Unsolved/datetime_demo.py` into your `student-work/week2/day2` project.

### Core

1. Parse the first claim's `opened` date with `strptime`. Print it, its `.year`,
   and the weekday name (`strftime("%A")`).
2. Format that date as `MM/DD/YYYY` with `strftime`.
3. For each claim, compute how many days it was open (`(closed - opened).days`).
4. Sort the claims by `opened` date (parse inside the `key`).
5. Compute a follow-up date 30 days after the first claim opened.

### Challenge

6. Build a `{claim_id: days_open}` dict, then print the average days open and the
   claim id that was open the longest.

## Expected Output

```text
parsed: 2026-05-02 00:00:00 | year: 2026 | weekday: Saturday
formatted: 05/02/2026
days open:
  CLM-1: 18 days
  CLM-2: 22 days
  CLM-3: 3 days
by opened date: ['CLM-1', 'CLM-2', 'CLM-3']
follow-up due: 2026-06-01
average days open: 14.3
longest open: CLM-2
```

## Success Criteria

- You parse with `strptime` and format with `strftime`.
- You compute a duration with `timedelta` (the `.days` of a subtraction).
- You can read a format string like `%Y-%m-%d`.

## Hint

<details>
<summary>strptime vs strftime, which is which?</summary>

`strptime` = string parse time (string -> datetime). `strftime` = string format
time (datetime -> string). The "p" is parse; the "f" is format.

</details>
