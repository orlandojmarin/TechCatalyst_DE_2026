"""Advanced Track: Comprehensions on claims data.

list, dict, and set comprehensions replace many simple for-loops with one
readable line. This is a must-know modern Python skill.
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
all_ids = [c["claim_id"] for c in claims]
print("All ids:", all_ids)

# 2. List comprehension with a filter: ids of open claims only
open_ids = [c["claim_id"] for c in claims if c["status"] == "open"]
print("Open ids:", open_ids)

# 3. Dict comprehension: claim_id -> reserve lookup
reserve_by_id = {c["claim_id"]: c["reserve"] for c in claims}
print("Reserve by id:", reserve_by_id)

# 4. Set comprehension: the distinct policy types (printed sorted for stability)
policy_types = {c["policy_type"] for c in claims}
print("Policy types:", sorted(policy_types))

# 5. Dict comprehension with a transform and a filter:
#    claim_id -> reserve burn percent, only for claims that have paid out
burn_by_id = {
    c["claim_id"]: round(c["paid"] / c["reserve"] * 100, 1)
    for c in claims
    if c["paid"] > 0
}
print("Burn by id:", burn_by_id)

# ---- Challenge ----

payments = {
    "CLM-4001": [["2026-06-01", "medical", 800.0], ["2026-06-08", "rental", 400.0]],
    "CLM-4004": [["2026-06-05", "liability", 4000.0]],
    "CLM-4005": [["2026-06-02", "property", 16200.0]],
}

# A. Nested comprehension: flatten every payment amount across all claims
all_amounts = [rec[2] for events in payments.values() for rec in events]
print("All amounts:", all_amounts)

# B. Conditional expression inside a comprehension:
#    label each claim 'over' or 'within' its reserve
labels = {
    c["claim_id"]: ("over" if c["paid"] > c["reserve"] else "within")
    for c in claims
}
print("Labels:", labels)
