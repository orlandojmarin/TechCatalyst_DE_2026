# CSV Read and Write

**Label: Core.** The `csv` module is how you read and write tabular files with the
standard library. You used it inside the mini-capstone; here you practice it on
its own, which is the direct on-ramp to pandas on Day 4.

In this drill you read a clean claims CSV, aggregate by policy type, and write a
summary CSV.

## Background

`Resources/claims.csv` has one row per claim with `claim_id, policy_type, reserve,
paid`. You will total the reserve and paid amounts per policy type and write the
result to `policy_summary.csv`.

## Instructions

Copy this drill folder (including `Resources/`) into your `student-work/week2/day2`
project, then run from the drill-folder root (the folder that contains
`Resources/`):

```bash
uv run python Unsolved/csv_io.py
```

### Core

1. Open `Resources/claims.csv` and read it with `csv.DictReader`, which yields each
   row as a dict keyed by the header names.
2. For each row, convert `reserve` and `paid` to `float` and accumulate a per
   `policy_type` total (count, reserve, paid). `dict.setdefault` helps.
3. Print the summary, sorted by policy type.
4. Write `policy_summary.csv` with `csv.DictWriter`, columns `policy_type, count,
   total_reserve, total_paid`, with a header row.

### Stretch

5. Add a `loss_ratio` column (`paid / reserve * 100`, rounded) to the output.

## Expected Output

```text
Policy summary:
  auto: 4 claims, reserve $18,700.00, paid $9,300.00
  liability: 3 claims, reserve $49,000.00, paid $16,300.00
  property: 3 claims, reserve $36,000.00, paid $30,200.00
Wrote policy_summary.csv
```

`policy_summary.csv`:

```text
policy_type,count,total_reserve,total_paid
auto,4,18700.0,9300.0
liability,3,49000.0,16300.0
property,3,36000.0,30200.0
```

## Success Criteria

- You read with `csv.DictReader` and write with `csv.DictWriter`.
- Values from a CSV are strings, so you convert `reserve` and `paid` before doing
  math.
- The output file has a header and one row per policy type.

## Hint

<details>
<summary>Why pass `newline=""` to open?</summary>

The `csv` module handles line endings itself. Opening with `newline=""` prevents
blank lines from appearing between rows on some platforms. It is the documented way
to open a file for the `csv` module.

</details>
