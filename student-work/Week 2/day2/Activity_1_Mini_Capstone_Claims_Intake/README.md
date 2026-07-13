# Mini Project 1: Claims Intake Pipeline

**This is Mini Project 1 of today's two mini projects** (the other is
`Activity_2_No_Show_Analysis/`). The 18 numbered drills build individual Python
skills; this mini project is where you chain those skills into one small,
realistic pipeline.

**Module:** Week 2 Day 2, Python Foundations
**Estimated Time:** 45 to 60 minutes
**Difficulty:** Intermediate (Core), Advanced (Stretch)
**Format:** Individual build, table review
**Prerequisites:** Activity 0 (UV project), and the Block 1 and Block 2 drills

## Objective

In this mini-capstone you will pull the whole day together. You will build a
small data pipeline that reads messy insurance claim records, cleans and
validates them, aggregates them, and writes report files. You will use only the
Python standard library: `csv`, `json`, and `pathlib`.

## Background

You are a data engineering intern at Charter Oak Mutual, a fictional property and
casualty insurer. Claims arrive from several intake systems, so the raw export is
messy: money fields have dollar signs and commas, some are blank or say `N/A`,
statuses are in mixed case, a few rows are missing a claim id, and one claim id
is duplicated. Your job is to turn that raw file into trustworthy numbers the
business can act on.

This is the same shape of work you will do tomorrow on Day 3, except the records
will arrive from a live REST API instead of a local file. The clean, validate,
flatten, and write pipeline you build here is exactly what runs on an API
response.

## Provided Files

| File | Purpose |
|---|---|
| `data/claims_raw.csv` | 22 raw claim rows with realistic data quality problems |
| `data/claim_payments.json` | Nested payment events per claim (dict of lists of dicts) |
| `starter/claims_pipeline.py` | Scaffold with TODO markers for each tier |
| `solutions/claims_pipeline_solution.py` | Instructor reference (open only at debrief) |
| `solutions/expected_output.txt` | Canonical expected console output |

## Setup

Copy this activity folder into your `student-work/week2/day2` project, or work in
place. Run everything from the folder that contains `data/`.

```bash
uv run python starter/claims_pipeline.py
```

## Instructions

Work one tier at a time. Run after each tier and compare to the expected output.

### Core: clean and validate (everyone)

1. Implement `parse_money()` so it strips spaces, a leading `$`, and thousands
   commas, returns `None` for empty, `N/A`, non-numeric, or negative values, and
   rounds valid values to two decimals.
2. Implement `load_clean_claims()` so it rejects rows with no claim id, an
   invalid `reserve` or `paid`, or a duplicate claim id. Normalize `policy_type`
   and `status` to lowercase and `state` to uppercase.
3. In `main()`, print the valid count, rejected count, total reserve, and total
   paid.

### Challenge: aggregate by policy type

4. Implement `loss_ratio()` (paid divided by reserve, as a percentage).
5. Implement `summarize_by_policy()` to total `count`, `reserve`, and `paid` per
   policy type.
6. Print the loss-ratio table and write `outputs/policy_summary.csv` with a
   header row.

### Stretch: nested payments and SIU review

7. Load `data/claim_payments.json`. For each claim, sum its payment amounts.
8. Implement `find_reserve_breaches()` to flag claims whose total payments exceed
   their reserve. Capture `claim_id`, `reserve`, `total_paid`, `overage`, and
   `payment_count`.
9. Print the breaches and write `outputs/siu_review.json`. These are the claims
   the Special Investigations Unit should look at first.

## Expected Output

```text
=== CORE: Intake summary ===
Valid claims:    16
Rejected rows:   6
Total reserve:   $144,000.00
Total paid:      $87,900.50

=== CHALLENGE: Loss ratio by policy type ===
policy_type  count       reserve          paid  loss_ratio
auto             8     31,500.00     17,900.00      56.83%
liability        3     39,000.00     12,300.00      31.54%
property         4     69,500.00     57,200.50      82.30%
unknown          1      4,000.00        500.00      12.50%
Wrote outputs/policy_summary.csv

=== STRETCH: SIU reserve-breach review ===
Claims breaching reserve: 2
  CLM-1009: paid $26,500.00 vs reserve $25,000.00 (overage $1,500.00)
  CLM-1016: paid $19,250.00 vs reserve $18,000.00 (overage $1,250.00)
Wrote outputs/siu_review.json
```

`outputs/policy_summary.csv`:

```text
policy_type,count,total_reserve,total_paid,loss_ratio_pct
auto,8,31500.0,17900.0,56.83
liability,3,39000.0,12300.0,31.54
property,4,69500.0,57200.5,82.3
unknown,1,4000.0,500.0,12.5
```

## Success Criteria

- Your script runs with `uv run python` and produces the expected console output.
- You reject exactly 6 rows, and you can name why each one failed.
- `outputs/policy_summary.csv` and `outputs/siu_review.json` are created.
- Your Stretch flags CLM-1009 and CLM-1016 and no others.
- You can explain which Python data type you used at each step and why.

## Hints

<details>
<summary>How do I strip the dollar signs and commas?</summary>

String methods chain: `raw.strip().replace("$", "").replace(",", "")`. Do the
cleaning first, then try `float()` inside a `try` / `except ValueError`.

</details>

<details>
<summary>How do I detect a duplicate claim id?</summary>

Keep a `set()` of ids you have already accepted. Before appending a record,
check `if claim_id in seen`. Sets give you fast membership checks.

</details>

<details>
<summary>What is the cleanest way to accumulate per-policy totals?</summary>

`summary.setdefault(policy_type, {"count": 0, "reserve": 0.0, "paid": 0.0})`
returns the existing bucket or creates a fresh one, so you can add to it in one
line.

</details>

<details>
<summary>How do I sum the nested payment amounts?</summary>

Each value in `claim_payments.json` is a list of dicts. Use a generator:
`sum(event["amount"] for event in events)`.

</details>

## Stretch Goals (beyond the three tiers)

- Add a `denied` filter: report total reserve tied up in denied claims.
- Add a `--state` style summary: loss ratio by `state` instead of policy type.
- Reconcile the `paid` column in the CSV against the summed payments in the JSON
  and report any claim where they disagree. This is a real data quality check.

## Bridge to Day 3

Save your working `claims_pipeline.py`. On Day 3 you will write `ingest_api.py`,
which fetches JSON from a live REST API, paginates, saves a raw JSON page, then
cleans and writes a CSV. Notice the parallel: `claims_raw.csv` plus
`claim_payments.json` here become `data/raw_page1.json` there, and
`policy_summary.csv` here becomes `data/clean.csv` there. Same pipeline, new
source.
