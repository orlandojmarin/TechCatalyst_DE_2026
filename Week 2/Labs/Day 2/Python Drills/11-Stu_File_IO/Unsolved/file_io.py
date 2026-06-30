"""Student Do: File I/O.

Read a text file of daily claim counts, total and count them, then write a
summary file. Run from inside this drill folder so Resources/ resolves.
"""
from pathlib import Path

DATA = Path("Resources/daily_claims.txt")
OUT = Path("claims_summary.txt")

# TODO: initialize total and day_count


# TODO: open DATA, iterate lines, strip and skip blanks, convert to int,
# and accumulate total and day_count


# TODO: compute daily_average = round(total / day_count, 2)


# TODO: open OUT in write mode and write the three values, one per line


# TODO: print Total claims, Days, Daily average, and a "Wrote ..." line
