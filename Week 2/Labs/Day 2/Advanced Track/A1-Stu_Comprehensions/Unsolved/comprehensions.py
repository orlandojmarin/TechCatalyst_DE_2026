"""Advanced Track: Comprehensions on claims data.

Replace each TODO with a single comprehension. Do not use an explicit for loop
with .append().
"""

claims = [
    {"claim_id": "CLM-4001", "policy_type": "auto", "status": "open", "state": "CT", "reserve": 5000.0, "paid": 1200.0},
    {"claim_id": "CLM-4002", "policy_type": "property", "status": "closed", "state": "MA", "reserve": 12000.0, "paid": 11800.0},
    {"claim_id": "CLM-4003", "policy_type": "auto", "status": "denied", "state": "CT", "reserve": 8000.0, "paid": 0.0},
    {"claim_id": "CLM-4004", "policy_type": "liability", "status": "open", "state": "RI", "reserve": 28000.0, "paid": 4000.0},
    {"claim_id": "CLM-4005", "policy_type": "property", "status": "open", "state": "CT", "reserve": 15000.0, "paid": 16200.0},
    {"claim_id": "CLM-4006", "policy_type": "auto", "status": "open", "state": "MA", "reserve": 3000.0, "paid": 500.0},
]

# ---- Core ----

# 1. List comprehension: every claim id
# all_ids = ...
# print("All ids:", all_ids)

# 2. List comprehension with a filter: ids of open claims only
# open_ids = ...

# 3. Dict comprehension: claim_id -> reserve
# reserve_by_id = ...

# 4. Set comprehension: distinct policy types (print sorted(...) for stable output)
# policy_types = ...

# 5. Dict comprehension with a transform and filter:
#    claim_id -> round(paid / reserve * 100, 1), only where paid > 0
# burn_by_id = ...

# ---- Challenge ----

payments = {
    "CLM-4001": [["2026-06-01", "medical", 800.0], ["2026-06-08", "rental", 400.0]],
    "CLM-4004": [["2026-06-05", "liability", 4000.0]],
    "CLM-4005": [["2026-06-02", "property", 16200.0]],
}

# A. Nested comprehension: flatten every payment amount across all claims
# all_amounts = ...

# B. Conditional expression inside a comprehension:
#    claim_id -> "over" if paid > reserve else "within"
# labels = ...
