"""Student Do: datetime.

Time is everywhere in data: claim dates, appointment times, taxi timestamps.
Parsing, formatting, and doing arithmetic on dates is essential before pandas
takes over on Day 4.
"""
from datetime import datetime, timedelta

claims = [
    {"claim_id": "CLM-1", "opened": "2026-05-02", "closed": "2026-05-20"},
    {"claim_id": "CLM-2", "opened": "2026-05-10", "closed": "2026-06-01"},
    {"claim_id": "CLM-3", "opened": "2026-05-15", "closed": "2026-05-18"},
]

# Parse a string into a datetime
opened = datetime.strptime(claims[0]["opened"], "%Y-%m-%d")
print("parsed:", opened, "| year:", opened.year, "| weekday:", opened.strftime("%A"))

# Format a datetime back to a string
print("formatted:", opened.strftime("%m/%d/%Y"))

# timedelta: how long was each claim open?
print("days open:")
for c in claims:
    o = datetime.strptime(c["opened"], "%Y-%m-%d")
    cl = datetime.strptime(c["closed"], "%Y-%m-%d")
    print(f"  {c['claim_id']}: {(cl - o).days} days")

# Sort claims by opened date (parse inside the key)
by_date = sorted(claims, key=lambda c: datetime.strptime(c["opened"], "%Y-%m-%d"))
print("by opened date:", [c["claim_id"] for c in by_date])

# Date arithmetic: a follow-up is due 30 days after opening
due = opened + timedelta(days=30)
print("follow-up due:", due.strftime("%Y-%m-%d"))

# Challenge: average days open, and the longest-running claim
durations = {
    c["claim_id"]: (datetime.strptime(c["closed"], "%Y-%m-%d")
                    - datetime.strptime(c["opened"], "%Y-%m-%d")).days
    for c in claims
}
print("average days open:", round(sum(durations.values()) / len(durations), 1))
print("longest open:", max(durations, key=durations.get))
