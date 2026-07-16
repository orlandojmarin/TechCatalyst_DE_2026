# Lesson 2: SQL Practice on Your Warehouse (SELECT, JOIN, GROUP BY, CTEs)

**Module:** Week 4 Day 4  
**Estimated Time:** 60 to 90 minutes  
**Format:** Solve, check against the expected result, then explain your reasoning to a partner.  
**Prerequisites:** Lesson 1 complete. You built `policyholders` and `claims` in your own schema.

## What you are doing

You built the warehouse in Lesson 1. Now you query it. These problems climb from simple reads to multi-step CTEs, the same "named intermediate result" thinking you practiced on Day 3. Write each query yourself. Predict the row count before you run it.

This is an AI-Free Zone lesson. Use your notes, the documentation, and your partner, not an AI assistant.

## Step 0: Reset to a known starting point

In Lesson 1 you inserted, updated, and deleted rows, so your `claims` table may be in any state. Run this once to reset `claims` to the exact rows every checkpoint below assumes. `policyholders` is unchanged, but the block recreates it too so Lesson 2 stands on its own.

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;   -- replace <YOUR_NAME>

CREATE OR REPLACE TABLE policyholders (
  policyholder_id VARCHAR NOT NULL,
  full_name       VARCHAR NOT NULL,
  state           VARCHAR(2) NOT NULL,
  plan_tier       VARCHAR NOT NULL,
  PRIMARY KEY (policyholder_id)
);

INSERT INTO policyholders (policyholder_id, full_name, state, plan_tier) VALUES
  ('P01', 'Ava',  'CT', 'Gold'),
  ('P02', 'Ben',  'CT', 'Silver'),
  ('P03', 'Cara', 'NY', 'Gold'),
  ('P04', 'Dan',  'MA', 'Silver'),
  ('P05', 'Eve',  'NY', 'Bronze'),
  ('P06', 'Finn', 'CT', 'Bronze');

CREATE OR REPLACE TABLE claims (
  claim_id        VARCHAR NOT NULL,
  policyholder_id VARCHAR NOT NULL,
  claim_type      VARCHAR NOT NULL,
  amount          NUMBER(12, 2),
  status          VARCHAR NOT NULL,
  filed_date      DATE NOT NULL,
  PRIMARY KEY (claim_id)
);

INSERT INTO claims (claim_id, policyholder_id, claim_type, amount, status, filed_date) VALUES
  ('CL01', 'P01', 'auto', 1200, 'closed', '2026-01-05'),
  ('CL02', 'P01', 'home', 5400, 'open',   '2026-01-12'),
  ('CL03', 'P02', 'auto',  800, 'open',   '2026-01-08'),
  ('CL04', 'P03', 'home', 3100, 'closed', '2026-01-15'),
  ('CL05', 'P03', 'auto', 9900, 'open',   '2026-01-20'),
  ('CL06', 'P04', 'auto',  450, 'closed', '2026-01-06'),
  ('CL07', 'P04', 'home', 2200, 'open',   '2026-01-22'),
  ('CL08', 'P01', 'auto', NULL, 'open',   '2026-01-25'),
  ('CL09', 'P05', 'home', 1500, 'open',   '2026-01-18'),
  ('CL10', 'P02', 'home', 2600, 'closed', '2026-01-28'),
  ('CL11', 'P03', 'auto',  700, 'open',   '2026-01-30');
```

> Starting point: 6 policyholders, 11 claims. `CL08` has a `NULL` amount on purpose. Finn (P06) has no claims on purpose. Both facts show up in the problems below.

## How to work each problem

1. Read the question and say out loud what one row of the answer represents.
2. Predict the number of rows.
3. Write the query. Run it.
4. Compare with the expected result. If it differs, the gap is the lesson.

Solutions live in `solutions/w4d4_ddl_practice_solutions.sql`. Try each problem before opening them.

## Part A: Read and filter (SELECT, WHERE, ORDER BY)

### Problem 1
List every open claim, showing `claim_id`, `claim_type`, and `amount`, ordered by `amount` from highest to lowest.

> Expected: 7 rows. `CL05` (9900) is first. The `NULL`-amount claim `CL08` sorts last.

### Problem 2
Count how many claims are `open` and how many are `closed`.

> Expected: open 7, closed 4.

## Part B: Aggregate (GROUP BY)

### Problem 3
For each `claim_type`, show the number of claims and the total `amount`.

> Expected: `auto` 6 claims, total 13050. `home` 5 claims, total 14800. The `NULL` amount on `CL08` is ignored by `SUM`, so `auto` totals 6 claims but only 5 contribute dollars.

### Problem 4
Show the overall average claim amount. In the same query, show `COUNT(*)` and `COUNT(amount)` side by side and explain why they differ.

> Expected: average 2785.00, `COUNT(*)` 11, `COUNT(amount)` 10. `COUNT(*)` counts rows; `COUNT(amount)` counts non-null amounts, so the `NULL` on `CL08` is the difference.

## Part C: Combine tables (JOIN)

### Problem 5
Total claim `amount` by `state`. Join `claims` to `policyholders`.

> Expected: CT 10000, NY 15200, MA 2650.

### Problem 6
List every open claim with the policyholder's `full_name` and `plan_tier`. Order by `amount` descending.

> Expected: 7 rows, each carrying the name and tier from `policyholders`.

### Problem 7
Which policyholders have filed no claims at all? Use a `LEFT JOIN` from `policyholders` and keep only the rows with no matching claim.

> Expected: Finn (P06), and only Finn.

## Part D: Multi-step reasoning (CTEs)

Use the planning habit from Day 3: name the intermediate result you wish existed, build it first, then build on it.

### Problem 8
Build `customer_totals` (one row per policyholder who has at least one claim, with a claim count and total amount). Then return only policyholders with at least two claims.

> Expected: Ava (3, 6600), Ben (2, 3400), Cara (3, 13700), Dan (2, 2650). Eve has one claim, so she is out.

### Problem 9
Starting from `customer_totals`, find the average per-policyholder total amount for each `plan_tier`, using only policyholders who have claims. Which tier has the highest average?

> Expected: Gold 10150.00, Silver 3025.00, Bronze 1500.00. Gold is highest.

### Problem 10 (stretch, ties the whole day together)
Find policyholders whose total claim amount is above the average total for their own tier (claimants only). This is the same "compare each row to its group benchmark" pattern from Activity 5 and Activity 6.

> Expected: exactly two people, Cara (Gold, 13700 above 10150) and Ben (Silver, 3400 above 3025).

## Success criteria

- [ ] You reset the tables and started from 6 policyholders and 11 claims.
- [ ] You can explain why `SUM(amount)` and `COUNT(amount)` treat the `NULL` on `CL08` the way they do.
- [ ] Your joins attach the right policyholder to each claim.
- [ ] Your `LEFT JOIN` finds Finn, the one policyholder with no claims.
- [ ] Your Problem 10 CTE returns Cara and Ben, and you can say what one row represents at each step.

## If you finish early

1. Rewrite Problem 10 with a subquery instead of CTEs, then decide which version you would rather hand to a teammate.
2. Add a `filed_date` angle: how many claims were filed in the last week of January (2026-01-24 through 2026-01-31)?
3. Turn Problem 9 into a permanent record: use CTAS to save the tier averages as a table `tier_benchmarks`, then a view `v_tier_benchmarks` over the same query. Change one claim amount and re-read both. Which one moved, and why?
