"""Advanced Track: itertools pipelines.

Use chain, islice, accumulate, and groupby on the claim batches.
"""
from itertools import chain, islice, accumulate, groupby

batch1 = [{"claim_id": "CLM-1", "paid": 1200.0}, {"claim_id": "CLM-2", "paid": 5000.0}]
batch2 = [{"claim_id": "CLM-3", "paid": 800.0}, {"claim_id": "CLM-4", "paid": 4000.0}]

# TODO 1: chain batch1 and batch2 into one stream; print the claim ids


# TODO 2: islice the first two from the chained stream


# TODO 3: accumulate a running total of paid across all claims


claims = [
    {"claim_id": "CLM-1", "policy_type": "auto"},
    {"claim_id": "CLM-2", "policy_type": "property"},
    {"claim_id": "CLM-3", "policy_type": "auto"},
]

# TODO 4 (Challenge): sort claims by policy_type, then groupby and print each group
