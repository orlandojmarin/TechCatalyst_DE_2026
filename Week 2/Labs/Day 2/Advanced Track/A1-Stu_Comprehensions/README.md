# Advanced Track A1: Comprehensions

**Optional, for fast finishers. Targets Python 3.13.**

Comprehensions build a list, dict, or set in one readable line, replacing many
simple for-loops. They are a must-know modern Python skill and you will see them
constantly in real data engineering code.

## Before and after

```python
# Before: a loop that builds a list
open_ids = []
for c in claims:
    if c["status"] == "open":
        open_ids.append(c["claim_id"])

# After: the same thing as a list comprehension
open_ids = [c["claim_id"] for c in claims if c["status"] == "open"]
```

The pattern is `[expression for item in iterable if condition]`. Swap the brackets
for `{}` to build a set, or `{key: value for ...}` to build a dict.

## Instructions

Copy `Unsolved/comprehensions.py` into your `student-work/week2/day2` project. The
claims list is provided. Write each comprehension.

### Core

1. `all_ids`: a list of every `claim_id`.
2. `open_ids`: a list of `claim_id` for claims whose `status` is `open`.
3. `reserve_by_id`: a dict mapping `claim_id` to `reserve`.
4. `policy_types`: a set of the distinct `policy_type` values.
5. `burn_by_id`: a dict mapping `claim_id` to reserve burn percent
   (`paid / reserve * 100`, rounded to 1 decimal), only for claims where
   `paid > 0`.

### Challenge

A. `all_amounts`: a flat list of every payment amount across all claims in the
   `payments` dict (a nested comprehension over a dict of lists of records).

B. `labels`: a dict mapping `claim_id` to `"over"` if `paid > reserve`, else
   `"within"` (a conditional expression inside a comprehension).

## Expected Output

```text
All ids: ['CLM-4001', 'CLM-4002', 'CLM-4003', 'CLM-4004', 'CLM-4005', 'CLM-4006']
Open ids: ['CLM-4001', 'CLM-4004', 'CLM-4005', 'CLM-4006']
Reserve by id: {'CLM-4001': 5000.0, 'CLM-4002': 12000.0, 'CLM-4003': 8000.0, 'CLM-4004': 28000.0, 'CLM-4005': 15000.0, 'CLM-4006': 3000.0}
Policy types: ['auto', 'liability', 'property']
Burn by id: {'CLM-4001': 24.0, 'CLM-4002': 98.3, 'CLM-4004': 14.3, 'CLM-4005': 108.0, 'CLM-4006': 16.7}
All amounts: [800.0, 400.0, 4000.0, 16200.0]
Labels: {'CLM-4001': 'within', 'CLM-4002': 'within', 'CLM-4003': 'within', 'CLM-4004': 'within', 'CLM-4005': 'over', 'CLM-4006': 'within'}
```

## Success Criteria

- Every value is built with a comprehension, not an explicit `for` loop with
  `.append()`.
- Your output matches the expected output.
- You can read each comprehension out loud as "expression, for item, where
  condition."

## Hint

<details>
<summary>How does the nested comprehension in Challenge A work?</summary>

Read it left to right as nested loops: `[rec[2] for events in payments.values()
for rec in events]` is the same as looping over each claim's list of events, then
over each record in that list, taking `rec[2]` (the amount).

</details>
