"""Advanced Track: Structural pattern matching (match/case, Python 3.10+).

match/case reads the shape of data, not just a single value. It is a clean way to
route records and to destructure nested structures like API responses.
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
    match claim:
        case {"status": "denied"}:
            return "closed"
        case {"policy_type": "auto", "reserve": reserve} if reserve > 25000:
            return "SIU"
        case {"status": "open", "reserve": reserve} if reserve >= 20000:
            return "senior adjuster"
        case {"status": "open"}:
            return "standard queue"
        case _:
            return "manual review"


print("Claim routing:")
for c in claims:
    print(f"  {c['claim_id']}: {route_claim(c)}")


# ---- Core: destructure a nested payment record ----
def describe_payment(record):
    match record:
        case [date, kind, amount]:
            return f"{date}: {kind} payment of ${amount:,.2f}"
        case _:
            return "unknown record"


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
    match (status, policy_type):
        case ("denied", _):
            return "none"
        case ("open", "liability"):
            return "high"
        case ("open", "auto" | "property"):
            return "normal"
        case _:
            return "low"


print("\nPriority by (status, policy_type):")
for c in claims:
    print(f"  {c['claim_id']}: {priority(c['status'], c['policy_type'])}")
