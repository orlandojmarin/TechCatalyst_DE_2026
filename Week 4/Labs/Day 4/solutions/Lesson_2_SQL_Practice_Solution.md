# Lesson 2 Solution: SQL Practice

Instructor reference. Replace `<YOUR_NAME>` with the student's schema. Copy blocks into Snowsight to verify.

```sql
-- Week 4 Day 4 Lesson 2 SQL practice solutions.
-- Answers assume the reset block in Lesson 2 ran: 6 policyholders, 11 claims,
-- CL08 amount is NULL, and Finn (P06) has no claims.

USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;


-- Problem 1. Open claims, highest amount first. 7 rows; CL08 (NULL) sorts last.
SELECT claim_id, claim_type, amount
FROM claims
WHERE status = 'open'
ORDER BY amount DESC NULLS LAST;

-- Problem 2. Claims by status. open 7, closed 4.
SELECT status, COUNT(*) AS claim_count
FROM claims
GROUP BY status
ORDER BY status;

-- Problem 3. Count and total by claim_type. auto 6 / 13050, home 5 / 14800.
SELECT
  claim_type,
  COUNT(*) AS claim_count,
  SUM(amount) AS total_amount
FROM claims
GROUP BY claim_type
ORDER BY claim_type;

-- Problem 4. Average amount, plus COUNT(*) vs COUNT(amount).
-- avg 2785.00, COUNT(*) 11, COUNT(amount) 10. The gap is the NULL on CL08.
SELECT
  ROUND(AVG(amount), 2) AS avg_amount,
  COUNT(*) AS row_count,
  COUNT(amount) AS amount_count
FROM claims;

-- Problem 5. Total amount by state. CT 10000, NY 15200, MA 2650.
SELECT
  p.state,
  SUM(c.amount) AS total_amount
FROM claims AS c
JOIN policyholders AS p
  ON c.policyholder_id = p.policyholder_id
GROUP BY p.state
ORDER BY total_amount DESC;

-- Problem 6. Open claims with policyholder name and tier. 7 rows.
SELECT
  c.claim_id,
  p.full_name,
  p.plan_tier,
  c.claim_type,
  c.amount
FROM claims AS c
JOIN policyholders AS p
  ON c.policyholder_id = p.policyholder_id
WHERE c.status = 'open'
ORDER BY c.amount DESC NULLS LAST;

-- Problem 7. Policyholders with no claims. Finn only.
SELECT
  p.policyholder_id,
  p.full_name
FROM policyholders AS p
LEFT JOIN claims AS c
  ON p.policyholder_id = c.policyholder_id
WHERE c.claim_id IS NULL
ORDER BY p.policyholder_id;

-- Problem 8. customer_totals, then policyholders with at least two claims.
-- Ava 3/6600, Ben 2/3400, Cara 3/13700, Dan 2/2650.
WITH customer_totals AS (
  SELECT
    p.policyholder_id,
    p.full_name,
    p.plan_tier,
    COUNT(c.claim_id) AS claim_count,
    SUM(c.amount) AS total_amount
  FROM policyholders AS p
  JOIN claims AS c
    ON p.policyholder_id = c.policyholder_id
  GROUP BY p.policyholder_id, p.full_name, p.plan_tier
)
SELECT *
FROM customer_totals
WHERE claim_count >= 2
ORDER BY total_amount DESC;

-- Problem 9. Average per-policyholder total by tier (claimants only).
-- Gold 10150.00, Silver 3025.00, Bronze 1500.00. Gold is highest.
WITH customer_totals AS (
  SELECT
    p.policyholder_id,
    p.plan_tier,
    SUM(c.amount) AS total_amount
  FROM policyholders AS p
  JOIN claims AS c
    ON p.policyholder_id = c.policyholder_id
  GROUP BY p.policyholder_id, p.plan_tier
)
SELECT
  plan_tier,
  ROUND(AVG(total_amount), 2) AS avg_total_amount
FROM customer_totals
GROUP BY plan_tier
ORDER BY avg_total_amount DESC;

-- Problem 10. Policyholders above their own tier average (claimants only).
-- Cara (Gold, 13700 > 10150) and Ben (Silver, 3400 > 3025).
WITH customer_totals AS (
  SELECT
    p.policyholder_id,
    p.full_name,
    p.plan_tier,
    SUM(c.amount) AS total_amount
  FROM policyholders AS p
  JOIN claims AS c
    ON p.policyholder_id = c.policyholder_id
  GROUP BY p.policyholder_id, p.full_name, p.plan_tier
),
tier_benchmarks AS (
  SELECT
    plan_tier,
    AVG(total_amount) AS tier_avg_total
  FROM customer_totals
  GROUP BY plan_tier
)
SELECT
  t.full_name,
  t.plan_tier,
  t.total_amount,
  ROUND(b.tier_avg_total, 2) AS tier_avg_total,
  ROUND(t.total_amount - b.tier_avg_total, 2) AS amount_above_tier_avg
FROM customer_totals AS t
JOIN tier_benchmarks AS b
  ON t.plan_tier = b.plan_tier
WHERE t.total_amount > b.tier_avg_total
ORDER BY amount_above_tier_avg DESC;
```
