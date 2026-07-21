# SQL Deep Dive: Dates, Conversions, and Conditionals

**In-Class Demo**

Today we go beyond basic `SELECT` and `WHERE`. Three families of functions come up constantly in real data engineering work: **date/time manipulation**, **type conversion**, and **conditional logic**. Snowflake gives you several ways to do each — knowing which to reach for (and when one silently fails vs. loudly errors) is the actual skill.

---

## Part 1: Date and Time Functions

Every date has components hiding inside it, and Snowflake lets you extract, shift, and compare them without ever touching a string.

```sql
SELECT
    CURRENT_DATE()                       AS today_date,
    YEAR(CURRENT_DATE())                 AS year,
    MONTH(CURRENT_DATE())                AS month,
    QUARTER(CURRENT_DATE())              AS quarter,
    WEEK(CURRENT_DATE())                 AS week,
    DAYNAME(CURRENT_DATE())              AS name_of_day,
    NEXT_DAY(CURRENT_DATE(), 'WE')        AS next_wednesday,
    PREVIOUS_DAY(CURRENT_DATE(), 'WE')    AS prev_wednesday,
    DATEADD('month', 1, CURRENT_DATE())   AS next_month,
    DATEADD('quarter', 1, CURRENT_DATE()) AS next_quarter,
    DATEDIFF('day', CURRENT_DATE(), NEXT_DAY(CURRENT_DATE(), 'WE'))     AS days_to_wed,
    DATEDIFF('month', CURRENT_DATE(), DATEADD('quarter', 1, CURRENT_DATE())) AS months_to_next_q
;
```

**Note:** a column alias (like `today_date`) is not visible inside the same `SELECT` statement — that's why every reference above repeats `CURRENT_DATE()` instead of reusing an alias. This is a common gotcha; the fix, when the repetition gets ugly, is a CTE.

### DATEDIFF vs. TIMESTAMPDIFF

Both exist in Snowflake:

- `DATEDIFF(unit, start, end)` — Snowflake's native spelling, works on dates or timestamps.
- `TIMESTAMPDIFF(unit, start, end)` — ANSI-style spelling, same behavior for timestamps.

They're interchangeable for timestamp math. Pick one and be consistent within a codebase.

### Timestamps, UTC, and EPOCH

```sql
SELECT
    CURRENT_TIMESTAMP()                              AS local_ts,
    CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())      AS utc_ts,
    CONVERT_TIMEZONE('Asia/Amman', CURRENT_TIMESTAMP()) AS amman_ts,
    CONVERT_TIMEZONE('America/New_York', 'UTC', CURRENT_TIMESTAMP()) AS ny_to_utc,
    DATE_PART(EPOCH_SECOND, CURRENT_TIMESTAMP())      AS epoch_seconds,
    TO_TIMESTAMP(1721568000)                          AS from_epoch_seconds,
    TO_TIMESTAMP(1721568000000, 3)                    AS from_epoch_millis
;
```

- `CONVERT_TIMEZONE` shifts a timestamp between zones; give it a source zone, or omit it to assume the session's current zone.
- `DATE_PART(EPOCH_SECOND, ts)` turns a timestamp into Unix epoch seconds — useful when writing to systems that expect epoch, not `TIMESTAMP` types.
- `TO_TIMESTAMP(n)` reverses that: it reads an epoch integer and rebuilds a timestamp. The second argument (`6` or `3`) tells Snowflake whether the input is microseconds, milliseconds, or seconds — this is exactly the trick used for raw Parquet timestamp columns that land as `NUMBER`.

---

## Part 2: Conversion Functions

Same destination type, several roads. The difference matters once bad data shows up.

**String to decimal:**

```sql
SELECT
    CAST('124' AS DECIMAL(5,2))      AS via_cast,
    '124'::DECIMAL(5,2)              AS via_shorthand,
    TO_DECIMAL('123', 5, 2)          AS via_to_decimal,
    TRY_TO_DECIMAL('12A', 5, 2)      AS via_try_to_decimal  -- returns NULL, not an error
;
```

**String to date / timestamp:**

```sql
SELECT
    CAST('2023-10-25' AS DATE)       AS date_via_cast,
    '2023-10-25'::DATE               AS date_via_shorthand,
    TO_DATE('2023-10-25')            AS date_via_to_date,
    CAST('2023-10-25' AS TIMESTAMP)  AS ts_via_cast,
    TO_TIMESTAMP('2023-10-25')       AS ts_via_to_timestamp
;
```

**The `TRY_` family — the important part:**

```sql
SELECT
    TRY_CAST('202A-10-25' AS DATE)   AS try_cast_bad_date,     -- NULL
    TRY_TO_DATE('202A-10-25')        AS try_to_date_bad,       -- NULL
    TRY_TO_TIMESTAMP('202A-10-25')   AS try_to_timestamp_bad,  -- NULL
    TRY_TO_DECIMAL('12A', 5, 2)      AS try_decimal_bad        -- NULL
;
```

`CAST` and `TO_X` raise an error on bad input and kill the query. `TRY_CAST` and `TRY_TO_X` swallow the error and return `NULL` instead. In production pipelines, `TRY_` versions are usually the right default for messy source data — you want the row to survive with a `NULL`, not the whole batch to fail.

---

## Part 3: Conditional Functions

```sql
SELECT
    IFF(1 + 1 = 2, 'Correct', 'Wrong')              AS logic_1,
    IFF(100 > 5, TRUE, FALSE)                       AS logic_2,
    IFF('0050'::INT = 50, 'Integer', 'Not Integer') AS logic_3,
    IS_INTEGER(5.2)                                 AS check_int,
    IS_DECIMAL(5.2)                                 AS check_decimal
;
```

`IFF(condition, true_result, false_result)` is Snowflake's inline if/else — shorthand for a two-branch `CASE`. Reach for `CASE WHEN` once you need three or more branches; `IFF` nested three levels deep is unreadable.

## Part 4: Additional Functions Worth Knowing

The three families above cover most day-to-day SQL, but a handful of other functions show up constantly in real pipelines. These round out your toolkit.

| Category      | Function                   | Why it matters                                               |
| ------------- | -------------------------- | ------------------------------------------------------------ |
| NULL handling | `COALESCE`                 | First non-NULL in a list; core to consolidating messy source columns |
| NULL handling | `NULLIF(a, b)`             | Returns NULL if `a = b`; turns placeholder values like `'N/A'` into true NULLs |
| NULL handling | `NVL(a, b)` / `NVL2`       | Two/three-arg NULL substitution, equivalent to COALESCE for simple cases |
| Conditional   | `MOD(a, b)`                | Remainder after division; needed for even/odd checks, cyclical bucketing |
| Conditional   | `CASE WHEN`                | Multi-branch logic once `IFF` nesting gets unreadable        |
| Date/Time     | `DATE_TRUNC(unit, ts)`     | Rounds a timestamp down to the start of a unit (day, month, hour) — the standard way to group timestamps cleanly |
| Date/Time     | `LAST_DAY(date)`           | Returns the last calendar day of the month                   |
| String        | `TRIM` / `LTRIM` / `RTRIM` | Strips whitespace; the most common "why isn't my join matching" fix |
| String        | `SPLIT_PART` / `SPLIT`     | Breaks delimited strings into parts, common for parsing raw text fields |
| Aggregation   | `LISTAGG`                  | Concatenates grouped values into one string, useful for readable summary rows |

### NULL handling: COALESCE

**Example 1: fill a single NULL with a default**

```sql
SELECT
    NULL AS raw_value,
    COALESCE(NULL, 'default') AS filled_value;
```

Returns `'default'`, because the first argument is NULL, so COALESCE moves to the next one.

**Example 2: pick the first available value from several options**

```sql
SELECT
    COALESCE(NULL, NULL, 'first_real_value', 'never_reached') AS result;
```

Returns `'first_real_value'`. COALESCE scans its arguments left to right and returns the first one that isn't NULL — if every argument were NULL, the result would be NULL too [web:16][web:29].

### How data engineers actually use COALESCE

Data engineers reach for COALESCE constantly when consolidating messy or incomplete source data, and it shows up in three recurring patterns:

- **Default values for missing data**: replacing a NULL `phone` or `email` column with a placeholder like `'Unknown'` before it hits a report, so downstream tools never choke on a blank field [web:22].
- **Fallback chains across columns**: trying a primary column first, then a backup column, then a hardcoded default — for example `COALESCE(email, alternate_email, 'no_email')`, common when merging records from multiple source systems that don't always populate the same fields [web:22][web:25].
- **Safe aggregation**: turning NULL into `0` before summing or averaging numeric columns, since a single NULL in a sum can silently propagate and null out the entire calculation — this is the exact reason COALESCE shows up before adding numeric columns together in ETL logic [web:27].

### NULL handling: COALESCE, NULLIF, NVL, NVL2

Four functions, one shared theme: NULL values need explicit handling, or they silently break calculations, joins, and reports downstream.

**COALESCE — return the first non-NULL value in a list**

```sql
SELECT COALESCE(NULL, NULL, 'fallback', 'never reached') AS coalesce_demo;
```

Scans left to right and stops at the first non-NULL argument — here that's `'fallback'`, at position three. Everything after it, including `'never reached'`, is ignored. If every argument were NULL, the result would be NULL too.

**NULLIF — turn a specific value into NULL**

```sql
SELECT
    NULLIF('N/A', 'N/A')    AS nullif_demo,     -- returns NULL
    NULLIF('active', 'N/A') AS nullif_no_match;  -- returns 'active'
```

`NULLIF(a, b)` compares its two arguments: if they're equal, it returns NULL; if they're different, it returns `a` unchanged. In the first line, `'N/A'` equals `'N/A'`, so the result is NULL. In the second line, `'active'` does not equal `'N/A'`, so `'active'` passes through untouched.

This is the reverse job of COALESCE — instead of filling a NULL with a real value, NULLIF hunts for a fake "looks real but actually means missing" value and converts it into a true NULL. Source systems frequently use placeholder strings like `'N/A'`, `'-1'`, `'0000-00-00'`, or `'UNKNOWN'` to mean "no data," and those placeholders are invisible to NULL-aware logic unless you convert them first.

**NVL — a simpler two-argument COALESCE**

```sql
SELECT NVL(NULL, 'default') AS nvl_demo;
```

`NVL(a, b)` returns `a` if it's not NULL, otherwise returns `b`. It behaves exactly like `COALESCE(a, b)` but only accepts two arguments — useful shorthand when you only ever need one fallback, though COALESCE is more portable across database platforms.

**NVL2 — branch on whether a value is NULL, not just fill it**

```sql
SELECT NVL2(NULL, 'if_not_null', 'if_null') AS nvl2_demo;
```

`NVL2(a, b, c)` checks whether `a` is NULL: if `a` is NOT NULL, it returns `b`; if `a` IS NULL, it returns `c`. Here the first argument is NULL, so the result is `'if_null'`. This is a step beyond COALESCE and NVL — instead of just substituting a fallback value, NVL2 lets you return a completely different result depending on which branch you're in, similar in spirit to `IFF` but specifically triggered by NULL-ness.

**All together, for comparison**

```sql
SELECT
    COALESCE(NULL, NULL, 'fallback', 'never reached')  AS coalesce_demo,
    NULLIF('N/A', 'N/A')                                AS nullif_demo,
    NULLIF('active', 'N/A')                             AS nullif_no_match,
    NVL(NULL, 'default')                                AS nvl_demo,
    NVL2(NULL, 'if_not_null', 'if_null')                AS nvl2_demo
;
```

| Function   | Job                                             | This example returns    |
| ---------- | ----------------------------------------------- | ----------------------- |
| `COALESCE` | First non-NULL value in a list                  | `'fallback'`            |
| `NULLIF`   | Converts a matching value into NULL             | `NULL`, then `'active'` |
| `NVL`      | Two-argument fallback (like a mini-COALESCE)    | `'default'`             |
| `NVL2`     | Different result depending on NULL vs. not-NULL | `'if_null'`             |

### Conditional: MOD

```sql
SELECT
    -7 AS number_val,
    MOD(-7, 2)                         AS remainder,
    IFF(MOD(-7, 2) = 0, 'Even', 'Odd') AS even_odd
UNION ALL
SELECT
    4,
    MOD(4, 2),
    IFF(MOD(4, 2) = 0, 'Even', 'Odd');
```

`MOD(a, b)` returns the remainder of `a / b`. It's the standard trick for even/odd checks, but it also shows up anywhere you need cyclical logic — bucketing rows into groups of N, or checking "is this the Nth row.”

__Note__ You can try this query once you create the `lab_date` below.

```sql
SELECT
    number_val,
    MOD(number_val, 2)                         AS remainder,
    IFF(MOD(number_val, 2) = 0, 'Even', 'Odd') AS even_odd
FROM lab_data;
```



### Date/Time: DATE_TRUNC and LAST_DAY

```sql
SELECT
    '2026-07-21 09:15:00'::TIMESTAMP AS event_ts,
    DATE_TRUNC('day', '2026-07-21 09:15:00'::TIMESTAMP)   AS truncated_to_day,
    DATE_TRUNC('month', '2026-07-21 09:15:00'::TIMESTAMP) AS truncated_to_month,
    LAST_DAY('2026-07-21'::DATE)                           AS last_day_of_month;
```

`DATE_TRUNC` rounds a timestamp *down* to the start of whatever unit you specify — truncating to `'month'` turns any timestamp in July into `2026-07-01 00:00:00`. This is the cleanest way to group timestamps by day, month, or hour without manually extracting and reassembling parts, and it's a more production-grade alternative to the `DATE()` + `HOUR()` combo used in this week's taxi CLEAN table.

**A quick note on `::`**

You've already seen `::` used for type conversion — `'124'::DECIMAL(5,2)` is shorthand for `CAST('124' AS DECIMAL(5,2))`. The two are functionally identical; `::` is just Snowflake's (and Postgres's) more compact syntax, and `CAST` is the ANSI-standard, more portable spelling. In the examples below, `'2026-07-21 09:15:00'::TIMESTAMP` converts a literal string into an actual `TIMESTAMP` value, the same way `CAST('2026-07-21 09:15:00' AS TIMESTAMP)` would — pick whichever reads clearer to you, but recognize both when reading other people's code.

__Note__ You can try this query once you create the `lab_date` below.

```sql
SELECT
    event_ts,
    DATE_TRUNC('day', event_ts)   AS truncated_to_day,
    DATE_TRUNC('month', event_ts) AS truncated_to_month,
    LAST_DAY(event_date)          AS last_day_of_month
FROM lab_data;
```

### String cleanup: TRIM, SPLIT_PART

```sql
SELECT
    '  messy value  '                    AS raw,
    TRIM('  messy value  ')              AS trimmed,
    SPLIT_PART('2026-07-21', '-', 1)     AS year_part,
    SPLIT_PART('2026-07-21', '-', 2)     AS month_part
;
```

`TRIM` (and its one-sided cousins `LTRIM`/`RTRIM`) strips leading/trailing whitespace — a frequent culprit when joins silently fail because one side has a trailing space. `SPLIT_PART` pulls out one piece of a delimited string by position, useful for parsing loosely structured text fields before they're properly typed.

### Aggregation: LISTAGG

```sql
SELECT
    pickup_dow,
    LISTAGG(DISTINCT vendorid, ', ') AS vendors_seen
FROM clean_yellow_taxi
GROUP BY pickup_dow;
```

`LISTAGG` flattens a group of rows into a single delimited string — handy for readable summary output, like listing which vendors appeared on each day of week in one line instead of one row per vendor.

---

# Lab: Try It Yourself

Run this setup once. It creates a small temp table with messy, realistic values — some clean, some intentionally broken — so you can practice conversions and date logic against known data with known answers.

## Setup

```sql
CREATE OR REPLACE TEMP TABLE lab_data (
    row_id            INT,
    event_date        DATE,
    event_ts          TIMESTAMP,
    amount_str        VARCHAR,
    date_str          VARCHAR,
    number_val        INT
);

INSERT INTO lab_data VALUES
    (1, '2026-07-21', '2026-07-21 09:15:00', '124',   '2023-10-25', -7),
    (2, '2026-08-15', '2026-08-15 14:30:00', '99',    '2024-02-30', 17),
    (3, '2026-12-01', '2026-12-01 23:59:59', '12A',   '2026-07-21', 0),
    (4, '2027-01-10', '2027-01-10 00:00:00', '0050',  '202A-10-25', 4),
    (5, '2026-09-30', '2026-09-30 18:45:22', '3.14',  '2026-12-25', -3);

SELECT * FROM lab_data;
```

Every activity below reads from `lab_data`. Because the dates and numbers are fixed, your output should match the expected results listed under each activity — if it doesn't, that's your signal to debug, not a screenshot to chase.

---

### Activity 1: Date Components

For each row, extract the year, month, quarter, week number, and day name from `event_date`.

```sql
SELECT
    row_id,
    event_date,
    -- YOUR CODE: year, month, quarter, week, day name
FROM lab_data;
```

**Expected for row 1** (`2026-07-21`): year `2026`, month `7`, quarter `3`, week `30`, and day name `Tue`.

---

### Activity 2: Next/Previous Day

For each row's `event_date`, find the next Friday and the previous Friday.

```sql
SELECT
    row_id,
    event_date,
    -- YOUR CODE: next Friday, previous Friday
FROM lab_data;
```

**Expected for row 1** (`2026-07-21`, a Tuesday): next Friday `2026-07-24`, previous Friday `2026-07-17`.

---

### Activity 3: Date Math

Add one quarter and subtract one week from `event_date`, in the same query.

```sql
SELECT
    row_id,
    event_date,
    -- YOUR CODE: plus one quarter, minus one week
FROM lab_data;
```

**Expected for row 1**: plus one quarter `2026-10-21`, minus one week `2026-07-14`.

---

### Activity 4: Date Differences

Find the number of days between `event_date` and the next Friday from that date, and the number of months between `event_date` and one quarter later.

```sql
SELECT
    row_id,
    event_date,
    -- YOUR CODE: days to next Friday, months to next quarter
FROM lab_data;
```

**Expected for row 1**: days to next Friday `3`, months to next quarter `3`.

---

### Activity 5: UTC and Epoch

Using `event_ts`, convert it to UTC, then to epoch seconds, then back to a timestamp — confirm the round trip matches.

```sql
SELECT
    row_id,
    event_ts,
    -- YOUR CODE: UTC version, epoch seconds, back to timestamp
FROM lab_data;
```

**Expected for row 1** (`2026-07-21 09:15:00`, assuming session timezone is UTC already): epoch seconds should be a large integer around `1784650500`, and converting it back should return the exact original timestamp `2026-07-21 16:15:00.000`.

---

### Activity 6: Conversions, the Safe Way

`amount_str` should convert cleanly to `DECIMAL(5,2)` for most rows — except row 3 (`'12A'`), which is invalid. `date_str` should convert cleanly to `DATE` for most rows — except row 2 (`'2024-02-30'`, an invalid calendar date) and row 4 (`'202A-10-25'`, invalid characters).

1. Convert `amount_str` to `DECIMAL(5,2)` using `CAST`, `::`, and `TO_DECIMAL`. What happens on row 3?
2. Convert `amount_str` using `TRY_TO_DECIMAL` instead. What changes on row 3?
3. Convert `date_str` to `DATE` using `CAST`. What happens on rows 2 and 4?
4. Convert `date_str` using `TRY_TO_DATE` instead. What changes?

```sql
-- Try CAST/TO_DECIMAL first — expect an error partway through row 3
SELECT row_id, amount_str,
    -- YOUR CODE
FROM lab_data;

-- Now try TRY_TO_DECIMAL and TRY_TO_DATE — expect NULLs instead of errors
SELECT row_id, amount_str, date_str,
    -- YOUR CODE
FROM lab_data;
```

**Expected:** rows 1, 2, 4, 5 convert `amount_str` cleanly; row 3 errors with `CAST`/`TO_DECIMAL` and returns `NULL` with `TRY_TO_DECIMAL`. For `date_str`, rows 1, 3, 5 convert cleanly; rows 2 and 4 error with `CAST` and return `NULL` with `TRY_TO_DATE`.

---

### Activity 7: Conditional Logic

Using `number_val`, label each row as `'Positive'`, `'Negative'`, or `'Zero'`, and separately as `'Even'` or `'Odd'`.

```sql
SELECT
    row_id,
    number_val,
    -- YOUR CODE: sign label, even/odd label
FROM lab_data;
```

**Expected:** row 1 (`-7`) → `Negative`, `Odd`. Row 3 (`0`) → `Zero`, `Even`. Row 4 (`4`) → `Positive`, `Even`.

---

### Activity 8: Combine Everything

1. Using `IFF` and `DAYNAME`, label each `event_date` as `'Weekday'` or `'Weekend'`.
2. Using `NEXT_DAY` and `DATEDIFF`, find how many days remain from each `event_date` until the next Saturday.
3. Bonus: convert that "days until Saturday" result into a `TRY_TO_DECIMAL` with two decimal places.

```sql
SELECT
    row_id,
    event_date,
    -- YOUR CODE: weekday/weekend label, days to next Saturday, decimal bonus
FROM lab_data;
```

**Expected for row 1** (`2026-07-21`, a Tuesday): `Weekday`, `4` days to next Saturday (`2026-07-25`), decimal bonus `4.00`.