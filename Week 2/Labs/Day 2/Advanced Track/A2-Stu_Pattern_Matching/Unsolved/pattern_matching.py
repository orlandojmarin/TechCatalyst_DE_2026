"""Advanced Track: Structural pattern matching (match/case, Python 3.10+).

Implement each function with match/case, not if/elif.
"""

claims = [
    {"claim_id": "CLM-4001", "policy_type": "auto", "status": "open", "reserve": 5000.0},
    {"claim_id": "CLM-4002", "policy_type": "property", "status": "closed", "reserve": 12000.0},
    {"claim_id": "CLM-4003", "policy_type": "auto", "status": "denied", "reserve": 8000.0},
    {"claim_id": "CLM-4004", "policy_type": "liability", "status": "open", "reserve": 28000.0},
    {"claim_id": "CLM-4005", "policy_type": "property", "status": "open", "reserve": 15000.0},
    {"claim_id": "CLM-4006", "policy_type": "auto", "status": "open", "reserve": 3000.0},
    {"claim_id": "CLM-4007", "policy_type": "auto", "status": "open", "reserve": 30000.0},
]


# ---- Core: route a claim by its shape ----
def route_claim(claim):
    # TODO: match on claim with mapping patterns and a guard.
    # Order the cases from most specific to least specific.
    pass


print("Claim routing:")
for c in claims:
    print(f"  {c['claim_id']}: {route_claim(c)}")


# ---- Core: destructure a nested payment record ----
def describe_payment(record):
    # TODO: match a [date, kind, amount] sequence; return "unknown record" otherwise.
    pass


print("\nPayment records:")
records = [
    ["2026-06-01", "medical", 800.0],
    ["2026-06-05", "liability", 4000.0],
    ["bad record"],
]
for r in records:
    print(f"  {describe_payment(r)}")


# ---- Challenge: tuple patterns with OR and wildcard ----
def priority(status, policy_type):
    # TODO: match the tuple (status, policy_type). Use a wildcard and an OR pattern.
    pass


print("\nPriority by (status, policy_type):")
for c in claims:
    print(f"  {c['claim_id']}: {priority(c['status'], c['policy_type'])}")
