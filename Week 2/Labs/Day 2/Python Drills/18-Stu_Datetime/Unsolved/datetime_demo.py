"""Student Do: datetime.

Parse, format, and do arithmetic on claim dates.
"""
from datetime import datetime, timedelta

claims = [
    {"claim_id": "CLM-1", "opened": "2026-05-02", "closed": "2026-05-20"},
    {"claim_id": "CLM-2", "opened": "2026-05-10", "closed": "2026-06-01"},
    {"claim_id": "CLM-3", "opened": "2026-05-15", "closed": "2026-05-18"},
]

# TODO 1: parse claims[0]["opened"] with strptime; print it, .year, and weekday (%A)


# TODO 2: format that date as MM/DD/YYYY with strftime


# TODO 3: for each claim, print how many days it was open ((closed - opened).days)


# TODO 4: sort claims by opened date (parse inside the key); print the ids


# TODO 5: compute a follow-up date 30 days after the first claim opened


# TODO 6 (Challenge): build {claim_id: days_open}, print average and longest
