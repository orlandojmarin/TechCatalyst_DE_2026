"""Student Do: SQLite basics with the standard library.

Create a claims table, insert rows, and query it with SQL. Run from inside this
drill folder; the script creates claims.db there.
"""
import sqlite3
from pathlib import Path

DB = Path("claims.db")

# Start fresh each run so the drill is repeatable
if DB.exists():
    DB.unlink()

rows = [
    ("CLM-1001", "auto", 5000.0, 1200.0),
    ("CLM-1002", "property", 12000.0, 11800.0),
    ("CLM-1003", "liability", 20000.0, 4000.0),
    ("CLM-1004", "auto", 3000.0, 500.0),
    ("CLM-1005", "property", 15000.0, 16200.0),
]

# TODO: connect to DB and get a cursor


# TODO: CREATE TABLE claims (claim_id TEXT PRIMARY KEY, policy_type TEXT,
#       reserve REAL, paid REAL)


# TODO: insert the rows with executemany and ? placeholders, then commit


# TODO: query and print the auto claims (claim_id, reserve) with a parameter


# TODO: query and print total reserve per policy type with GROUP BY


# TODO: close the connection
