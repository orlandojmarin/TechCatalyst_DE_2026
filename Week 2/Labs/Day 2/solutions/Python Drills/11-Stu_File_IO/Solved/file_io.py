"""Student Do: File I/O.

Read a text file of daily claim counts, total and count them, then write a
summary file. File reading and writing is the foundation for everything you do
with data files, including the CSV work coming next and the pandas work on Day 4.
"""
from pathlib import Path

DATA = Path("Resources/daily_claims.txt")
OUT = Path("claims_summary.txt")

# Read: open the file and accumulate
total = 0
day_count = 0
with open(DATA) as f:
    for line in f:
        line = line.strip()
        if line == "":
            continue
        total += int(line)
        day_count += 1

daily_average = round(total / day_count, 2)

# Write: open in write mode and save a summary
with open(OUT, "w") as f:
    f.write(f"Total claims: {total}\n")
    f.write(f"Days: {day_count}\n")
    f.write(f"Daily average: {daily_average}\n")

print(f"Total claims: {total}")
print(f"Days: {day_count}")
print(f"Daily average: {daily_average}")
print(f"Wrote {OUT}")
