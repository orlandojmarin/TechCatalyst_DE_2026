"""Student Do: SQLite basics with the standard library.

sqlite3 ships with Python, so you can create a real database, write to it, and
query it with SQL, all with no install. This is your first taste of the SQL you
will use heavily in the BigQuery and SQL weeks.
"""
import sqlite3
from pathlib import Path

DB = Path("claims.db")

# Start fresh each run so the drill is repeatable
if DB.exists():
    DB.unlink()

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Create a table
cur.execute("""
    CREATE TABLE claims (
        claim_id TEXT PRIMARY KEY,
        policy_type TEXT,
        reserve REAL,
        paid REAL
    )
""")

# Insert rows. The ? placeholders are the safe way to pass values.
rows = [
    ("CLM-1001", "auto", 5000.0, 1200.0),
    ("CLM-1002", "property", 12000.0, 11800.0),
    ("CLM-1003", "liability", 20000.0, 4000.0),
    ("CLM-1004", "auto", 3000.0, 500.0),
    ("CLM-1005", "property", 15000.0, 16200.0),
]
cur.executemany("INSERT INTO claims VALUES (?, ?, ?, ?)", rows)
conn.commit()

# Query: a filtered SELECT with a parameter
print("Auto claims:")
for row in cur.execute("SELECT claim_id, reserve FROM claims WHERE policy_type = ?", ("auto",)):
    print(" ", row)

# Query: an aggregate with GROUP BY
print("\nTotal reserve by policy type:")
for row in cur.execute(
    "SELECT policy_type, SUM(reserve) FROM claims GROUP BY policy_type ORDER BY policy_type"
):
    print(f"  {row[0]}: {row[1]}")

conn.close()
print(f"\nWrote database {DB}")
