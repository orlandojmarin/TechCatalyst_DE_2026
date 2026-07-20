# Lesson 1: Build Your Own Snowflake Warehouse (DDL, Data Types, Tables, Views, CTAS)

**Module:** Week 4 Day 4  
**Estimated Time:** 60 to 90 minutes  
**Format:** Guided journey. Read a little, run a little, predict the result before you look.  
**Where you work:** Snowsight, in your own personal schema. No SQLite today.

## The story

You are the new data engineer for a small insurance office. By the end of this lesson you will have built a tiny warehouse from nothing: two tables, a snapshot, and a live view. You will fill them, fix them, reshape them, and clean them up, using the same commands real engineers use every day.

This is an AI-Free Zone lesson. Read each block, predict what it does, then run it. Learning happens in the gap between your prediction and the result.

> How to use this file: every code block is meant to be copied into a Snowsight worksheet and run. Run them in order. Do not skip the context block at the top.

## Step 0: Set your context

Snowflake always runs a command inside four settings: a **role** (what you are allowed to do), a **warehouse** (the compute that runs the query), a **database**, and a **schema** (where your objects live). Set all four before you do anything else.

```sql
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.<YOUR_NAME>;   -- replace <YOUR_NAME> with your assigned schema
```

Confirm you landed in the right place:

```sql
SELECT
  CURRENT_ROLE()      AS my_role,
  CURRENT_WAREHOUSE() AS my_warehouse,
  CURRENT_DATABASE()  AS my_database,
  CURRENT_SCHEMA()    AS my_schema;
```

> Stop and check: `my_schema` must be your own name. Everything you create in this lesson lands in that schema and nobody else's. If it says something else, fix your `USE SCHEMA` line before continuing.

## Step 1: What is DDL, and how does it fit with the rest of SQL?

SQL commands fall into a few families. You do not need every acronym, but this map keeps you oriented all day.

| Family | Full name | Commands | What it touches |
|---|---|---|---|
| **DDL** | Data Definition Language | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | The **structure**: tables, views, schemas |
| **DML** | Data Manipulation Language | `INSERT`, `UPDATE`, `DELETE`, `MERGE` | The **rows** inside a table |
| **DQL** | Data Query Language | `SELECT` | **Reading** data back out |

One sentence to remember:

> DDL builds the shelves. DML puts boxes on the shelves and moves them around. DQL reads the labels.

Today is mostly DDL and DML. You already know DQL (`SELECT`) from Days 1 through 3, and you will use it at the end to answer business questions.

## Step 2: Data types you will actually use in Snowflake

Before you create a table, you pick a **type** for each column. The type is a promise about what that column holds. Snowflake has many types, but this short list covers almost everything you will do this bootcamp.

| Type | Use it for | Example value |
|---|---|---|
| `NUMBER(p, s)` | Whole numbers and decimals. `p` = total digits, `s` = digits after the point. | `NUMBER(12,2)` holds `9900.00` |
| `INT` / `INTEGER` | Whole numbers. Snowflake stores this as `NUMBER(38,0)`. | `42` |
| `FLOAT` | Approximate decimals for scientific or ratio data. | `3.14159` |
| `VARCHAR` / `STRING` / `TEXT` | Text. These three are the same thing in Snowflake. | `'auto'` |
| `BOOLEAN` | True or false. | `TRUE` |
| `DATE` | A calendar date, no time. | `'2026-01-05'` |
| `TIMESTAMP_NTZ` | A date and time with no time zone. | `'2026-01-05 14:30:00'` |
| `VARIANT` | Semi-structured data (JSON). You will meet this on Day 5. | `{"tier":"Gold"}` |

> Good to know: Snowflake quietly normalizes some types. If you write `INT`, it becomes `NUMBER(38,0)`. If you write `STRING`, it becomes `VARCHAR`. So do not be surprised when the column shows a slightly different type name than you typed.

## Step 3: Your first table with CREATE TABLE

Let's build the customer list for the office: the **policyholders**.

```sql
CREATE OR REPLACE TABLE policyholders (
  policyholder_id VARCHAR       NOT NULL,
  full_name       VARCHAR       NOT NULL,
  state           VARCHAR(2)    NOT NULL,
  plan_tier       VARCHAR       NOT NULL,
  PRIMARY KEY (policyholder_id)
);
```

Three things to notice:

- `NOT NULL` is a **constraint**. It says this column may never be empty. If you try to insert a row without a `full_name`, Snowflake rejects it.
- `PRIMARY KEY` documents that `policyholder_id` uniquely identifies a row. Important: Snowflake **records** primary and foreign keys but does not **enforce** them (except `NOT NULL`). They are documentation for humans and tools, not a guard rail. You still design as if they mattered, because they describe intent.
- `CREATE OR REPLACE` means "if this table already exists, drop it and build it fresh." Handy while learning. Dangerous on real data, because it deletes what was there. More on that in Step 5.

## Step 4: Put rows in with INSERT INTO

An empty table is a shelf with no boxes. Fill it with `INSERT INTO`.

```sql
INSERT INTO policyholders (policyholder_id, full_name, state, plan_tier) VALUES
  ('P01', 'Ava',  'CT', 'Gold'),
  ('P02', 'Ben',  'CT', 'Silver'),
  ('P03', 'Cara', 'NY', 'Gold'),
  ('P04', 'Dan',  'MA', 'Silver'),
  ('P05', 'Eve',  'NY', 'Bronze'),
  ('P06', 'Finn', 'CT', 'Bronze');
```

Read it back:

```sql
SELECT * FROM policyholders ORDER BY policyholder_id;
```

> You should see: 6 rows. Finn (P06) will matter later, because Finn is the one policyholder who never files a claim.

## Step 5: Three ways to create a table, and when to use each

This is one of the most useful things to understand clearly. There are three creation modes, and they behave very differently when the table already exists.

| Command | If the table already exists | Use it when |
|---|---|---|
| `CREATE TABLE foo (...)` | **Errors.** Snowflake refuses to overwrite. | You want to be told if you are about to clobber something. |
| `CREATE TABLE IF NOT EXISTS foo (...)` | **Does nothing.** Keeps the existing table and its data. | Safe setup scripts you might run more than once. |
| `CREATE OR REPLACE TABLE foo (...)` | **Drops it and rebuilds it empty.** Data is gone. | Quick iteration while learning, or a deliberate full reset. |

Feel the difference. Run these one at a time and read the message each returns:

```sql
-- 1. This errors, because policyholders already exists.
CREATE TABLE policyholders (policyholder_id VARCHAR);
```

```sql
-- 2. This does nothing and keeps your 6 rows. Safe.
CREATE TABLE IF NOT EXISTS policyholders (policyholder_id VARCHAR);
SELECT COUNT(*) AS row_count FROM policyholders;   -- still 6
```

```sql
-- 3. Do NOT run this one yet. It would wipe your 6 rows.
-- CREATE OR REPLACE TABLE policyholders (policyholder_id VARCHAR);
```

> The lesson: `CREATE OR REPLACE` is convenient but it silently deletes. On real data, prefer `CREATE TABLE IF NOT EXISTS`, or create the table once and never re-run the create.

## Step 6: The claims table (and a deliberate gap)

Now the second table: the **claims** filed by those policyholders. Each claim points back to a policyholder through `policyholder_id`. That shared column is what lets you `JOIN` the two tables later.

```sql
CREATE OR REPLACE TABLE claims (
  claim_id        VARCHAR       NOT NULL,
  policyholder_id VARCHAR       NOT NULL,
  claim_type      VARCHAR       NOT NULL,
  amount          NUMBER(12, 2),
  status          VARCHAR       NOT NULL,
  filed_date      DATE          NOT NULL,
  PRIMARY KEY (claim_id),
  FOREIGN KEY (policyholder_id) REFERENCES policyholders (policyholder_id)
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

```sql
SELECT * FROM claims ORDER BY claim_id;
```

> Notice `CL08` has a `NULL` amount. That is a real thing: a claim was filed but the dollar figure has not been entered yet. `amount` has no `NOT NULL` constraint, so Snowflake accepts it. You will handle that gap in the next step, and again when you aggregate later.

## Step 7: DML, editing the rows you already have

Tables are not frozen. `INSERT`, `UPDATE`, and `DELETE` change the rows inside them.

### Insert one more row

A new claim just came in:

```sql
INSERT INTO claims (claim_id, policyholder_id, claim_type, amount, status, filed_date)
VALUES ('CL12', 'P05', 'auto', 300, 'open', '2026-01-31');
```

### Update a row

The adjuster finally entered the dollar amount for `CL08`, and closed it:

```sql
UPDATE claims
SET amount = 640,
    status = 'closed'
WHERE claim_id = 'CL08';
```

```sql
SELECT claim_id, amount, status FROM claims WHERE claim_id = 'CL08';
```

### Delete a row

`CL12` turned out to be a duplicate entry. Remove it:

```sql
DELETE FROM claims WHERE claim_id = 'CL12';
```

> Safety rule, burn it into memory: `UPDATE` and `DELETE` without a `WHERE` clause hit **every row in the table**. `DELETE FROM claims;` empties the whole table. Always write the `WHERE` first, then the rest.

> Reset note: for the practice in Lesson 2, the checkpoint answers assume `CL08` has amount `640` and status `closed`, and that `CL12` has been deleted. That is exactly the state you are in now. If you experimented and lost track, re-run Step 6 to rebuild `claims`, then re-apply the `CL08` update.

## Step 8: Views, a saved query that stays live

A **view** is a named `SELECT`. It stores the **query logic**, not a copy of the data. Every time you read the view, it re-runs its query against the current tables. So a view is always up to date.

Create a view of open claims with the policyholder's name and state attached:

```sql
CREATE OR REPLACE VIEW v_open_claims AS
SELECT
  c.claim_id,
  p.full_name,
  p.state,
  c.claim_type,
  c.amount,
  c.filed_date
FROM claims AS c
JOIN policyholders AS p
  ON c.policyholder_id = p.policyholder_id
WHERE c.status = 'open';
```

```sql
SELECT * FROM v_open_claims ORDER BY claim_id;
```

Now prove that a view is live. Insert a new open claim, then read the view again **without changing the view**:

```sql
INSERT INTO claims (claim_id, policyholder_id, claim_type, amount, status, filed_date)
VALUES ('CL13', 'P06', 'home', 4000, 'open', '2026-02-02');

SELECT * FROM v_open_claims ORDER BY claim_id;   -- CL13 now appears
```

> The view changed even though you never touched the view. That is the whole point: a view reflects the tables underneath it, right now.

## Step 9: CTAS, a snapshot frozen in time

`CREATE TABLE AS SELECT`, said as "CTAS", runs a query **once** and stores the **result rows** as a real, new table. Unlike a view, a CTAS table does not update when the source changes. It is a photograph, not a live feed.

```sql
CREATE OR REPLACE TABLE open_claims_snapshot AS
SELECT
  c.claim_id,
  p.full_name,
  p.state,
  c.amount
FROM claims AS c
JOIN policyholders AS p
  ON c.policyholder_id = p.policyholder_id
WHERE c.status = 'open';
```

```sql
SELECT * FROM open_claims_snapshot ORDER BY claim_id;
```

Now change the source and compare the view against the snapshot:

```sql
INSERT INTO claims (claim_id, policyholder_id, claim_type, amount, status, filed_date)
VALUES ('CL14', 'P04', 'auto', 275, 'open', '2026-02-03');

SELECT COUNT(*) AS live_view_rows  FROM v_open_claims;         -- includes CL14
SELECT COUNT(*) AS snapshot_rows   FROM open_claims_snapshot;  -- does NOT include CL14
```

> The single most important idea of the day: a **view** re-runs its query every time (always current, stores no data). A **CTAS table** stores the result once (fast to read, but frozen until you rebuild it). Choose based on whether you want "always live" or "a stable copy."

## Step 10: The table types, permanent, transient, temporary

Every table you create has a **type** that controls how long it lives and how much recovery Snowflake gives you. So far you have been creating permanent tables (the default). Here is the full picture.

| Type | Lives until | Time Travel and recovery | Cost profile | Use it for |
|---|---|---|---|---|
| **Permanent** (default) | You drop it | Time Travel plus a 7-day Fail-safe | Highest storage | Production data you must not lose |
| **Transient** | You drop it | Time Travel only, no Fail-safe | Lower storage | Reproducible or staging data, class work |
| **Temporary** | Your session ends | Session only | Cheapest | Scratch results only you need, right now |

Feel the difference between transient and temporary:

```sql
-- Transient: survives after this worksheet session ends, until you drop it.
CREATE OR REPLACE TRANSIENT TABLE claims_staging AS
SELECT * FROM claims WHERE status = 'open';

-- Temporary: visible only in THIS session. Open a new worksheet and it is gone.
CREATE OR REPLACE TEMPORARY TABLE claims_scratch AS
SELECT * FROM claims WHERE amount > 5000;

SELECT COUNT(*) AS staging_rows FROM claims_staging;
SELECT COUNT(*) AS scratch_rows FROM claims_scratch;
```

> Why we lean on transient tables in class: they behave like normal tables and persist across sessions, but they skip the extra 7-day Fail-safe storage, so they are cheaper and easier to reset. Temporary tables are perfect for a one-off scratch result you do not want cluttering your schema.

> There is also an **external table**, which points at files sitting in cloud storage (S3) instead of storing rows in Snowflake. You will meet stages and external data on Day 5. Note it exists; do not create one now.

## Step 11: Cleaning up with DROP and IF EXISTS

`DROP` removes an object entirely. Pair it with `IF EXISTS` so the command succeeds even if the object is already gone (no annoying error, which matters in reset scripts).

```sql
DROP TABLE IF EXISTS claims_scratch;
DROP TABLE IF EXISTS claims_staging;
```

Compare the two failure modes:

```sql
-- Errors if the view does not exist:
DROP VIEW some_view_that_is_not_here;
```

```sql
-- Succeeds quietly whether it exists or not:
DROP VIEW IF EXISTS some_view_that_is_not_here;
```

> `IF EXISTS` is the mirror image of `IF NOT EXISTS`. One protects you when creating ("only if it is missing"), the other protects you when dropping ("only if it is there").

> Keep for Lesson 2: do **not** drop `policyholders`, `claims`, `v_open_claims`, or `open_claims_snapshot`. You will query them next.

## What you can now do

Check yourself. You should be able to explain each of these in one sentence to your partner:

- [ ] The difference between DDL, DML, and DQL.
- [ ] When to use `NUMBER`, `VARCHAR`, `DATE`, and `BOOLEAN`.
- [ ] Why `CREATE OR REPLACE` is convenient and dangerous, and what `IF NOT EXISTS` protects.
- [ ] How to `INSERT`, `UPDATE`, and `DELETE` a specific row, and why `WHERE` is a safety rule.
- [ ] Why a **view** is always current but a **CTAS** table is frozen.
- [ ] The difference between permanent, transient, and temporary tables.
- [ ] What `DROP ... IF EXISTS` does and why you would want it.

## Quick reference

```sql
-- Structure (DDL)
CREATE TABLE t (...);                 -- errors if t exists
CREATE TABLE IF NOT EXISTS t (...);   -- skip if t exists
CREATE OR REPLACE TABLE t (...);      -- drop and rebuild (data lost)
CREATE OR REPLACE TRANSIENT TABLE t AS SELECT ...;   -- cheaper, persists
CREATE OR REPLACE TEMPORARY TABLE t AS SELECT ...;   -- session-only scratch
CREATE OR REPLACE VIEW v AS SELECT ...;              -- live, stores logic
CREATE OR REPLACE TABLE snap AS SELECT ...;          -- CTAS, frozen snapshot
DROP TABLE IF EXISTS t;
DROP VIEW  IF EXISTS v;

-- Rows (DML)
INSERT INTO t (...) VALUES (...);
UPDATE t SET col = val WHERE ...;     -- always write WHERE first
DELETE FROM t WHERE ...;              -- always write WHERE first
```

When your tables and view are in place, move on to **Lesson 2: SQL Practice** and put your `SELECT`, `JOIN`, `GROUP BY`, and CTE skills to work on the warehouse you just built.
