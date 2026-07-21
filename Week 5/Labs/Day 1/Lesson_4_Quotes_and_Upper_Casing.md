# Lesson 4: Quotes and Upper-Casing, What Snowflake Actually Does

**Module:** Week 5 Day 4
**Format:** In-class walkthrough. Your instructor drives; run every statement yourself in Snowsight as you go.
**Dataset:** The same `raw_yellow_tripdata_csv` and `raw_yellow_tripdata_parquet` tables from Lessons 1 through 3.

## The question this lesson answers

Why does a `SELECT vendorid` sometimes work fine, and sometimes throw "invalid identifier"? Why did some of you build a table from `INFER_SCHEMA` and suddenly every single column needs double quotes to query? This is not random. Snowflake has one exact, consistent rule for identifier casing, and once you see the rule, the "surprises" disappear. This is a critical lesson: get this wrong in a production pipeline and you get silent data corruption, not just an error message.

## 1. The one rule that explains everything

Snowflake has exactly one rule for identifiers (table names, column names, stage names, anything you name):

- **Unquoted identifier** -> Snowflake folds it to UPPERCASE, no matter how you typed it.
- **Quoted identifier** (wrapped in `"..."`) -> Snowflake stores and matches it EXACTLY as typed, case included.

That's it. Everything in this lesson is a consequence of that one rule.

```sql
CREATE OR REPLACE TRANSIENT TABLE raw_yellow_tripdata_csv (
  vendorid              NUMBER,
  tpep_pickup_datetime  TIMESTAMP_NTZ,
  tpep_dropoff_datetime TIMESTAMP_NTZ,
  passenger_count       NUMBER
);
```

None of these column names are quoted, so Snowflake stores all of them as `VENDORID`, `TPEP_PICKUP_DATETIME`, etc. Prove it:

```sql
DESCRIBE TABLE raw_yellow_tripdata_csv;
```

Read the `name` column in the output. Every name comes back uppercase, even though you typed lowercase in the DDL.

Because the identifiers are unquoted, all of these are equivalent and all of them work:

```sql
SELECT vendorid FROM raw_yellow_tripdata_csv;
SELECT VENDORID FROM raw_yellow_tripdata_csv;
SELECT VendorId FROM raw_yellow_tripdata_csv;
```

Unquoted references are matched case-insensitively, and Snowflake uppercases whatever you type before comparing it to the stored (also uppercase) name.

## 2. What happens the moment you add quotes

Now watch what one pair of double quotes does. Run this variant:

```sql
CREATE OR REPLACE TRANSIENT TABLE raw_yellow_tripdata_csv (
  "vendorid"             NUMBER,
  tpep_pickup_datetime  TIMESTAMP_NTZ,
  tpep_dropoff_datetime TIMESTAMP_NTZ,
  passenger_count       NUMBER
);
```

Only the first column is quoted, and it is quoted in lowercase. Run `DESCRIBE TABLE` again:

```sql
DESCRIBE TABLE raw_yellow_tripdata_csv;
```

The first column now shows up as `vendorid`, lowercase, while the rest are still uppercase. That single column is now permanently case-sensitive. Try both of these:

```sql
SELECT "vendorid" FROM raw_yellow_tripdata_csv;   -- works
SELECT vendorid   FROM raw_yellow_tripdata_csv;   -- SQL compilation error: invalid identifier 'VENDORID'
```

The second statement fails because Snowflake uppercases the unquoted `vendorid` to `VENDORID` before looking it up, and the stored name is the lowercase `vendorid`, exact case, from the quotes. They do not match.

Now compare this against the DDL from the first section of Lesson 1's build, which used `"VENDORID"` (quoted, but already uppercase):

```sql
CREATE OR REPLACE TRANSIENT TABLE raw_yellow_tripdata_csv (
  "VENDORID"             NUMBER,
  tpep_pickup_datetime  TIMESTAMP_NTZ,
  tpep_dropoff_datetime TIMESTAMP_NTZ,
  passenger_count       NUMBER
);
```

Here both of these work:

```sql
SELECT vendorid FROM raw_yellow_tripdata_csv;
SELECT VENDORID FROM raw_yellow_tripdata_csv;
```

This is the trap: quoting an identifier does not automatically make it case-sensitive-and-broken. It only breaks unquoted access when the quoted name is not already all-uppercase. Quote something in uppercase and it behaves exactly like an unquoted identifier, because the stored form matches what unquoted references get folded into anyway.

## 3. The escape hatch: QUOTED_IDENTIFIERS_IGNORE_CASE

Snowflake has a session (or account, or user) parameter that changes this behavior:

```sql
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE;
```

With this set to `TRUE`, quoted identifiers stop being case-sensitive; they get uppercased too, exactly like unquoted ones. So going forward, `"vendorid"` and `vendorid` and `VENDORID` all resolve to the same `VENDORID` object.

Two things to know that catch people off guard:

- This parameter only affects objects created **after** you set it. It does not retroactively fix a table that already exists with a lowercase quoted column. You must drop and recreate the object for it to take effect.
- The default value of `QUOTED_IDENTIFIERS_IGNORE_CASE` is `FALSE` at the account level. Some tools (dbt, certain ETL connectors) rely on this being `FALSE` to guarantee exact-case round-tripping, so flipping it account-wide can have side effects outside your own session; know what else is running before you change it globally.

For a training or sandbox environment, setting this to `TRUE` at the session or account level early is a reasonable defensive move, precisely because it prevents the lowercase-quote trap from ever locking in.

## 4. INFER_SCHEMA has the same trap, with its own switch

`INFER_SCHEMA` reads a file's embedded schema (Parquet, Avro, JSON, ORC, and now CSV) and reports back the exact field names it finds, case included. Its `IGNORE_CASE` parameter defaults to `FALSE`, which means the case from the file is preserved exactly as-is.

Feed that into `CREATE TABLE ... USING TEMPLATE` and you get every non-uppercase field name wrapped in quotes automatically:

```sql
CREATE OR REPLACE TABLE raw_yellow_tripdata_parquet
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
      INFER_SCHEMA(
        LOCATION => '@stages/parquet_stage',
        FILE_FORMAT => 'my_parquet_format'
      )
    )
  );
```

If the Parquet file's internal field names are lowercase (very common, since pandas and Spark both tend to write lowercase field names), you now have a table full of lowercase, quoted, case-sensitive columns, and every query needs `"vendorid"`, `"tpep_pickup_datetime"`, and so on, forever.

The fix is one parameter:

```sql
INFER_SCHEMA(
  LOCATION => '@stages/parquet_stage',
  FILE_FORMAT => 'my_parquet_format',
  IGNORE_CASE => TRUE
)
```

`IGNORE_CASE => TRUE` forces the inferred names to uppercase before they ever reach `USING TEMPLATE`, so the generated `CREATE TABLE` has clean, unquoted, uppercase columns from the start. **Rule of thumb: any time you call `INFER_SCHEMA`, set `IGNORE_CASE => TRUE` unless you have a specific reason not to.**

One more thing worth knowing: `INFER_SCHEMA` does not promise to return columns in the same order as the file. If you load into an inferred-schema table with a positional `COPY INTO`, confirm column order first, or better, use `MATCH_BY_COLUMN_NAME` so you are matching by name instead of position.

## 5. Python libraries follow the exact same rule, they just look different

This is the part that surprises engineers coming from a Python-heavy workflow: the Snowflake Connector for Python, Snowpark, and SQLAlchemy do not get special treatment. They generate SQL text (or an execution plan that becomes SQL), and that SQL is subject to the identical uppercase-folding rule described in Section 1.

Where this bites people in practice:

- **`write_pandas`** (Snowflake Connector for Python): by default it writes your DataFrame's column names as unquoted identifiers, so a DataFrame column named `VendorID` lands as `VENDORID` in Snowflake, uppercased like any other unquoted identifier. If you pass `quote_identifiers=True`, it wraps every column name in quotes and preserves exact case, meaning `VendorID` stays `VendorID` and now needs quotes forever to query, same trap as Section 2.
- **Snowpark DataFrames**: column names coming from `session.table(...)` reflect whatever is actually stored (uppercase if unquoted at creation, exact case if quoted). If you build a DataFrame from a pandas source with mixed-case columns and write it back, Snowpark preserves that mixed case with quotes behind the scenes, and any raw SQL you write afterward (or `RESULT_SCAN`) needs matching quoted, exact-case references to touch those columns.
- **SQLAlchemy**: the Snowflake SQLAlchemy dialect quotes identifiers by default whenever a name is not already all-uppercase, for the same round-trip-fidelity reason dbt and Coalesce do it. This means model or table definitions written in mixed case in SQLAlchemy will generate quoted DDL in Snowflake, and you inherit the exact same lowercase-quote lock-in described above.

The underlying takeaway is: **case sensitivity is not a Snowflake-versus-Python thing. It is a quoted-versus-unquoted thing, and it is decided the moment an object is created, regardless of which tool issued the `CREATE`.** If you want consistent, quote-free, case-insensitive behavior across SQL worksheets, Python scripts, and BI tools alike, the fix is the same one lever in every case: make sure identifiers are created unquoted, or set `QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE` before those objects are created.

## 6. Field guide: symptoms and fixes

| Symptom | Cause | Fix |
|---|---|---|
| `SELECT vendorid` fails with "invalid identifier" | Column was created quoted, in a case other than all-uppercase | Recreate the table without quotes, or query it with the exact quoted case |
| Every column in an `INFER_SCHEMA`-built table needs quotes | `INFER_SCHEMA` defaulted `IGNORE_CASE` to `FALSE` and preserved file casing | Rerun with `IGNORE_CASE => TRUE`, then recreate the table |
| `ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE` "did not fix it" | The object already existed before the setting changed; the parameter is not retroactive | Drop and recreate the object after setting the parameter |
| A pandas DataFrame's columns come back quoted and case-locked after `write_pandas` | `quote_identifiers=True` was set, or default behavior in an older connector version preserved case | Rename DataFrame columns to uppercase before writing, or explicitly set `quote_identifiers=False` |
| Two tables that look identical (`Orders` and `ORDERS`) behave like separate objects | Both were created with quotes preserving different case, so they are genuinely different objects to Snowflake | `SHOW TABLES` to see the real stored names, and standardize your creation process going forward |

## 7. What to watch for in production

- **Standardize on unquoted, uppercase DDL.** Hand-write your `CREATE TABLE` statements without quotes whenever you can. This is the simplest way to guarantee case-insensitive behavior for the life of the object.
- **Always pair `INFER_SCHEMA` with `IGNORE_CASE => TRUE`**, unless you have a deliberate reason to preserve exact source casing (rare, but it happens with some legacy migrations).
- **Decide your `QUOTED_IDENTIFIERS_IGNORE_CASE` policy once, at the account or user level, before your team starts creating objects.** Changing it later does not retroactively fix anything already built.
- **Audit third-party tools before they touch your schema.** dbt, Coalesce, SQLAlchemy, and many BI/ETL connectors quote identifiers by default to guarantee fidelity across databases. That default is safe for those tools, but it is exactly the mechanism that creates the lock-in trap inside Snowflake.
- **If you inherit a table with quoted, mixed-case columns and cannot drop it,** you are not stuck: you can rename columns with `ALTER TABLE ... RENAME COLUMN "oldname" TO NEWNAME` (unquoted target), which recreates the column reference cleanly as uppercase.

## Key takeaway

Snowflake's identifier rule is simple and absolute: unquoted always folds to uppercase, quoted always preserves exact case, and that decision is locked in permanently the moment an object is created, no matter which tool, language, or interface issued the `CREATE` statement. Every "why do I need quotes for this one column" mystery in this course traces back to that single rule.
