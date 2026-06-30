# JSON Read and Write

**Label: Core.** JSON is the format a REST API returns, so this drill is the direct
bridge to the Day 3 API lab. You read a nested JSON file, walk the structure, and
write a flat JSON summary.

## Background

`Resources/claims.json` is a list of claim objects, each with a nested list of
`payments`. You will total each claim's payments and write the result to
`claims_totals.json`.

## Instructions

Copy this drill folder (including `Resources/`) into your `student-work/week2/day2`
project, then run from the drill-folder root (the folder that contains
`Resources/`):

```bash
uv run python Unsolved/json_io.py
```

### Core

1. Open `Resources/claims.json` and load it with `json.load`. You get back Python
   lists and dicts.
2. For each claim, sum the `amount` of every record in its `payments` list.
3. Print each `claim_id` and its total.
4. Build a list of `{"claim_id": ..., "total_paid": ...}` dicts and write it to
   `claims_totals.json` with `json.dump(..., indent=2)`.

### Stretch

5. Skip claims with no payments, or add the `policy_type` to each output record.

## Expected Output

```text
CLM-8001: $1,200.00
CLM-8002: $7,500.00
CLM-8003: $0.00
CLM-8004: $1,500.00
CLM-8005: $4,000.00
Wrote claims_totals.json
```

`claims_totals.json` (first record):

```json
[
  {
    "claim_id": "CLM-8001",
    "total_paid": 1200
  },
  ...
]
```

## Success Criteria

- You load with `json.load` and write with `json.dump`.
- You walk the nested `payments` list to total each claim (this is the same skill
  as drill 09-Nesting).
- The output file is valid JSON.

## Hint

<details>
<summary>How is this different from the CSV drill?</summary>

CSV is flat (rows and columns). JSON can nest: here each claim holds a list of
payment dicts. `json.load` rebuilds that nesting as Python lists and dicts, so you
loop over them the same way you did in 09-Nesting. Tomorrow an API hands you this
exact shape.

</details>
