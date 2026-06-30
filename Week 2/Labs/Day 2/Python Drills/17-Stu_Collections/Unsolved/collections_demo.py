"""Student Do: collections (defaultdict and Counter).

Group and count the claims with Counter and defaultdict instead of setdefault.
"""
from collections import defaultdict, Counter

claims = [
    {"claim_id": "CLM-1", "policy_type": "auto", "paid": 1200.0},
    {"claim_id": "CLM-2", "policy_type": "property", "paid": 5000.0},
    {"claim_id": "CLM-3", "policy_type": "auto", "paid": 800.0},
    {"claim_id": "CLM-4", "policy_type": "liability", "paid": 4000.0},
    {"claim_id": "CLM-5", "policy_type": "property", "paid": 2200.0},
    {"claim_id": "CLM-6", "policy_type": "auto", "paid": 3100.0},
]

# TODO 1: use Counter to count claims per policy_type; print dict(counts) and
# counts.most_common(1)


# TODO 2: use defaultdict(float) to sum paid per policy type; print it


# TODO 3: use defaultdict(list) to group claim ids per policy type; print it


# TODO 4 (Challenge): print the average paid per policy type
