# Lesson 3: Choosing the Right Table or View in Snowflake

**Module:** Week 4 Day 4  
**Estimated Time:** 40 to 55 minutes  
**Format:** Guided journey. Read, run, and predict, then explain your choice to a partner.  
**Prerequisites:** Lesson 1 complete. You have `policyholders` and `claims` in your own schema.

## Why this lesson exists

In Lesson 1 you created tables and a view without thinking much about the **type**. A senior engineer picks the type on purpose, because the type decides three things:

1. **How long the object lives.**
2. **How much recovery you get if something goes wrong.**
3. **How much it costs to store.**

Picking well is part of designing a warehouse, not an afterthought. This lesson gives you the short, practical menu you will actually reach for, plus the two questions that pick the right item every time.

This is an AI-Free Zone lesson. Set your context first.

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;
```

## Part 1: The table menu

### The three you will use constantly

| Type | Lives until | Recovery (Time Travel / Fail-safe) | Storage cost | Reach for it when |
|---|---|---|---|---|
| **Permanent** (default) | You drop it | Time Travel (up to 90 days on Enterprise) plus 7-day Fail-safe | Highest | Real data the business depends on and cannot lose |
| **Transient** | You drop it | Time Travel (0 or 1 day), no Fail-safe | Lower | Staging, reproducible, or class data you could rebuild |
| **Temporary** | Your session ends | Session only, no Fail-safe | Cheapest | Scratch results only you need, right now |

Two terms in that table:

- **Time Travel** lets you look at or recover data as it was a moment ago (a dropped table, a bad `UPDATE`). You will try it below.
- **Fail-safe** is a 7-day, Snowflake-managed safety net after Time Travel ends. You cannot query it; only Snowflake can recover from it. It is why permanent tables cost the most to store.

### Two you should recognize, not create today

| Type | What it is | You will meet it |
|---|---|---|
| **External table** | A table whose rows stay in files in cloud storage (S3). Snowflake reads them in place. | Day 5, with stages |
| **Dynamic table** | A table you define with a query, and Snowflake keeps it refreshed automatically. The modern way to build a pipeline step. | Later, when we build pipelines that update themselves |

### Feel the difference

You already saw transient and temporary in Lesson 1. Now watch the recovery difference with Time Travel. Create a transient table, drop it, and bring it back:

```sql
CREATE OR REPLACE TRANSIENT TABLE recovery_demo AS
SELECT * FROM claims;

DROP TABLE recovery_demo;

-- Time Travel: undo the drop.
UNDROP TABLE recovery_demo;

SELECT COUNT(*) AS rows_back FROM recovery_demo;   -- your claims are back
```

Now a bad edit, undone by reading the past:

```sql
-- A careless update with no WHERE hits every row.
UPDATE recovery_demo SET amount = 0;

-- Look at the table as it was one minute ago, before the mistake.
SELECT COUNT(*) AS nonzero_before
FROM recovery_demo AT(OFFSET => -60)
WHERE amount > 0;

-- Rebuild the good data from the past.
CREATE OR REPLACE TRANSIENT TABLE recovery_demo AS
SELECT * FROM recovery_demo AT(OFFSET => -60);

DROP TABLE IF EXISTS recovery_demo;
```

> The lesson: recovery is not magic, it is a table property you chose. A temporary table gives you the least of it, a permanent table the most (and charges you for it).

## Part 2: The view menu

A view stores query logic, not rows (you built one in Lesson 1). There are three kinds worth knowing.

| View type | What it stores | Cost and behavior | Reach for it when |
|---|---|---|---|
| **Standard view** | Just the query. Re-runs every read. | Free to store, pays compute on every read. Always current. | Almost always. Your default. |
| **Materialized view** | The query **and** its precomputed results, auto-maintained. | Costs storage plus serverless maintenance. Restricted (single table, no joins, limited aggregates). | A slow, frequently read aggregate over one big table. |
| **Secure view** | The query, with the definition hidden and some optimizations disabled for privacy. | Slightly slower, but the logic and underlying data are protected. | Sharing data outside your team, or hiding sensitive logic. |

### Build one of each

A standard view (your default):

```sql
CREATE OR REPLACE VIEW v_claims_by_state AS
SELECT
  p.state,
  COUNT(*) AS claim_count,
  SUM(c.amount) AS total_amount
FROM claims AS c
JOIN policyholders AS p
  ON c.policyholder_id = p.policyholder_id
GROUP BY p.state;

SELECT * FROM v_claims_by_state ORDER BY total_amount DESC;
```

A secure view (same query, protected definition):

```sql
CREATE OR REPLACE SECURE VIEW v_claims_by_state_secure AS
SELECT
  p.state,
  COUNT(*) AS claim_count,
  SUM(c.amount) AS total_amount
FROM claims AS c
JOIN policyholders AS p
  ON c.policyholder_id = p.policyholder_id
GROUP BY p.state;
```

Compare what each reveals about its own definition:

```sql
-- The standard view shows its text.
SELECT GET_DDL('VIEW', 'v_claims_by_state');

-- The secure view hides its text from users who do not own it.
SELECT GET_DDL('VIEW', 'v_claims_by_state_secure');
```

> A materialized view has real restrictions (one table, no joins, a limited set of aggregations) and it costs money to keep fresh. That is why you do not reach for it first. Our `v_claims_by_state` joins two tables, so it could not be a materialized view anyway. Know it exists; use a standard view until a measured performance problem tells you otherwise.

### Clean up the demo views

```sql
DROP VIEW IF EXISTS v_claims_by_state;
DROP VIEW IF EXISTS v_claims_by_state_secure;
```

> Keep `policyholders`, `claims`, and anything from Lesson 2. Only the demo objects created in this lesson are safe to drop.

## Part 3: The two questions that pick the type

Before you create anything, ask:

1. **How long must this outlive me?** Only this session, so temporary. Longer, so transient or permanent.
2. **What happens if it is lost?** Rebuildable from source, so transient is fine and cheaper. Irreplaceable, so permanent for the Fail-safe net.

For views, ask instead:

1. **Do I want it always live?** Yes, so a standard view.
2. **Is this a proven-slow aggregate over one big table, read constantly?** Only then consider a materialized view.
3. **Am I sharing this outside my team or hiding logic?** Then a secure view.

## What you can now do

- [ ] Name the three table types and say what each costs you in persistence and recovery.
- [ ] Explain Time Travel and Fail-safe, and which table types have them.
- [ ] Use `UNDROP` and `AT(OFFSET => ...)` to recover from a mistake.
- [ ] Name the three view types and when each is the right call.
- [ ] Explain why a standard view is the default and a materialized view is the exception.
- [ ] Give the two questions you ask before choosing a table type.

## Quick reference

```sql
-- Tables
CREATE TABLE t (...);                    -- permanent (default): Time Travel + Fail-safe
CREATE TRANSIENT TABLE t (...);          -- no Fail-safe, cheaper
CREATE TEMPORARY TABLE t (...);          -- session only, cheapest
UNDROP TABLE t;                          -- recover a dropped table (Time Travel)
SELECT * FROM t AT(OFFSET => -60);       -- read t as it was 60 seconds ago

-- Views
CREATE VIEW v AS SELECT ...;             -- standard: live, stores only logic
CREATE SECURE VIEW v AS SELECT ...;      -- protected definition, for sharing
-- MATERIALIZED VIEW: stored + auto-maintained, single table, costs money. Use rarely.
```

Next you will apply all of this in **Activity 4**, where the pipeline pre-creates transient tables in your schema on purpose, so you can rebuild them cheaply while you iterate.
