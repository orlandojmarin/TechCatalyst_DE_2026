"""Optional helper: create a populated claims.db.

You do NOT need this for the drill. The drill itself creates claims.db when you
run your script (connecting creates the file, then CREATE TABLE and INSERT fill
it). This helper just gives you a ready-made, populated database, for example if
you want to practice only the query part.

Run it from the drill folder:
    uv run python Resources/create_claims_db.py
"""
import sqlite3
from pathlib import Path

DB = Path("claims.db")
if DB.exists():
    DB.unlink()

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE claims (
        claim_id TEXT PRIMARY KEY,
        policy_type TEXT,
        reserve REAL,
        paid REAL
    )
""")
cur.executemany("INSERT INTO claims VALUES (?, ?, ?, ?)", [
    ("CLM-1001", "auto", 5000.0, 1200.0),
    ("CLM-1002", "property", 12000.0, 11800.0),
    ("CLM-1003", "liability", 20000.0, 4000.0),
    ("CLM-1004", "auto", 3000.0, 500.0),
    ("CLM-1005", "property", 15000.0, 16200.0),
])
conn.commit()
count = cur.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
conn.close()
print(f"Created {DB} with {count} claims.")
