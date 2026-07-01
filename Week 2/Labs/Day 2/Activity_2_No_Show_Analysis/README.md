# Mini Project 2: Appointment No-Show Analysis

**This is Mini Project 2 of today's two mini projects** (the other is
`Activity_1_Mini_Capstone_Claims_Intake/`). Where Mini Project 1 builds a
pipeline, this one builds the interpretation muscle: reading real output and
deciding what it means for the business.

**Module:** Week 2 Day 2, Python Foundations
**Estimated Time:** 60 to 90 minutes
**Difficulty:** Intermediate
**Format:** Individual, can pair for the interpretation
**Label: Homework** (or in-class if time allows)
**Prerequisites:** the CSV drill (12-Stu_CSV_IO) and functions (08-Stu_Functions)

## Objective

This activity is about thinking, not just coding. You will read a real
appointments dataset, compute no-show rates by several factors, and then interpret
what the numbers mean for the business. A data engineer who can only produce
numbers is half a data engineer; the other half is reading them.

## Background

A health plan wants to reduce appointment no-shows (patients who book and do not
attend). You have a file of past appointments with patient attributes, whether a
reminder SMS was sent, and whether the patient showed up. Your job: quantify the
no-show problem, then advise the plan.

## Provided Files

| File | Purpose |
|---|---|
| `data/no_shows.csv` | ~12,500 appointment records |
| `starter/no_show_analysis.py` | Scaffold with TODOs |
| `solutions/no_show_analysis_solution.py` | Instructor reference (open at debrief) |
| `solutions/expected_output.txt` | Canonical expected console output |

Columns include `Age`, `Neighborhood`, `Scholarship`, `Hypertension`, `Diabetes`,
`SMS_received`, and `No-show` (the target: `Y` means the patient did not show up).

## Setup

Copy this activity folder into your `student-work/week2/day2` project, then run
from the folder that contains `data/`:

```bash
uv run python starter/no_show_analysis.py
```

## Instructions

### Core: compute the rates

1. Read `data/no_shows.csv` with `csv.DictReader`.
2. Write a `rate(rows)` helper returning `(appointments, no_shows, percent)`.
3. Print the overall no-show rate.
4. Print the no-show rate for **SMS received** vs **no SMS**.
5. Print the no-show rate for **scholarship** vs **no scholarship**.
6. Print the no-show rate by **age group** (18-34, 35-54, 55+).

### Challenge: go deeper

7. Print the no-show rate for patients with **hypertension** and with **diabetes**.
8. Find the **neighborhoods** with the highest no-show rate among those with at
   least 50 appointments, and print the top 3.

### Analyze: write your findings

Create `findings.md` and answer these in a few sentences each. Use your numbers.

1. **The SMS surprise.** Compare the no-show rate for appointments that received an
   SMS reminder versus those that did not. The result is probably the opposite of
   what you expected. Give a plausible explanation. What could make a reminder
   correlate with *more* no-shows? (Think about which appointments get reminders.)
2. **The flat factors.** Which factors in this data barely move the no-show rate?
   What does that tell you about where *not* to spend effort?
3. **Your recommendation.** If you were advising the health plan, what is one thing
   you would test next, and what extra data would you ask for to be more confident?

## Expected Output (Core + Challenge)

See `solutions/expected_output.txt`. Key numbers:

```text
Overall no-show rate: 20.1%
  SMS received   ...  27.5%
  no SMS         ...  16.4%
```

## Success Criteria

- Your script reads the CSV and prints the rates above (your numbers match the
  expected output).
- Your `rate()` helper is a single function reused for every breakdown.
- `findings.md` answers all three questions using your own numbers, and your SMS
  explanation shows you did not just assume reminders reduce no-shows.

## Hints

<details>
<summary>How do I compute a rate for a subset?</summary>

Filter the rows first (a list comprehension is perfect), then pass that smaller
list to your `rate()` function. For example, the SMS group is
`[r for r in rows if is_yes(r["SMS_received"])]`.

</details>

<details>
<summary>Why might SMS reminders correlate with more no-shows?</summary>

Correlation is not cause. Reminders are often sent for appointments booked far in
advance, and appointments booked far ahead are more likely to be forgotten or to
become inconvenient. The SMS is a marker of "booked long ago," not the cause of the
no-show. This is a confounding variable, and spotting it is the real skill here.

</details>
