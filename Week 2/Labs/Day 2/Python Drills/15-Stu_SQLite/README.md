# SQLite: Create, Insert, Query

**Label: Core.** `sqlite3` ships with Python, so you can create a real database,
write to it, and query it with SQL, all with no install. This is your first taste
of the SQL you will use heavily in the BigQuery and SQL weeks.

In this drill you create a `claims` table, insert rows, and run two queries.

## Instructions

Copy `Unsolved/sqlite_claims.py` into your `student-work/week2/day2` project, then
run from inside the drill folder. You do not need a database file to start: your
script creates `claims.db` itself (connecting creates the file, then `CREATE
TABLE` and `INSERT` fill it). If you would rather start from a ready-made,
populated database (for example to practice only the query part), run
`Resources/create_claims_db.py` first.

### Core

1. Connect to `claims.db` with `sqlite3.connect`.
2. `CREATE TABLE claims (claim_id TEXT PRIMARY KEY, policy_type TEXT, reserve REAL,
   paid REAL)`.
3. Insert the five rows with `cur.executemany(...)` using `?` placeholders, then
   `conn.commit()`.
4. Query the auto claims with a parameterized `SELECT ... WHERE policy_type = ?`.
5. Query total reserve per policy type with `SELECT policy_type, SUM(reserve) ...
   GROUP BY policy_type`.
6. Close the connection.

### Stretch

7. Add a query for claims where `paid > reserve` (the reserve breaches).

## Expected Output

```text
Auto claims:
  ('CLM-1001', 5000.0)
  ('CLM-1004', 3000.0)

Total reserve by policy type:
  auto: 8000.0
  liability: 20000.0
  property: 27000.0

Wrote database claims.db
```

## Success Criteria

- The script creates `claims.db`, inserts rows, and queries them with SQL.
- You used `?` placeholders rather than building SQL strings by hand.
- You can name the SQL keywords you used: `CREATE TABLE`, `INSERT`, `SELECT`,
  `WHERE`, `GROUP BY`.

## Hint

<details>
<summary>Why use `?` placeholders instead of f-strings in SQL?</summary>

Placeholders let the database driver insert values safely. Building SQL with
f-strings or string concatenation is how SQL injection bugs happen. Always pass
values as parameters. You will see this again throughout the SQL weeks.

</details>

<details>
<summary>The script complains the table already exists</summary>

The solution deletes `claims.db` at the start so each run is fresh. If you skip
that, either delete the file or use `CREATE TABLE IF NOT EXISTS`.

</details>
