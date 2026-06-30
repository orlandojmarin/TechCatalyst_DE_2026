"""Student Do: Error Handling.

Reject bad claim records, keep the good ones, and never crash on one bad row.
"""
import random

raw_claims = [
    {"claim_id": "CLM-1", "amount": "1200.50"},
    {"claim_id": "CLM-2", "amount": "N/A"},
    {"claim_id": "CLM-3"},                 # missing 'amount'
    {"claim_id": "CLM-4", "amount": "-50"},
]


# TODO: define InvalidAmountError as a subclass of ValueError


# TODO: parse_amount(raw): try float(raw); on (TypeError, ValueError) raise
# InvalidAmountError; if negative raise InvalidAmountError; else return round(.,2)
def parse_amount(raw):
    pass


# TODO (Core): loop raw_claims with try / except InvalidAmountError / else / finally.
# On error: print, count, continue. On success (else): append a clean record.
clean = []
errors = 0

print("clean:", clean)
print("errors:", errors)


# ---- Challenge: retry a flaky call (provided) ----
def flaky_fetch(claim_id):
    if random.random() < 0.5:
        raise ConnectionError("temporary network error")
    return {"claim_id": claim_id, "status": "ok"}


# TODO (Challenge): fetch_with_retry(claim_id, max_tries=3) that retries flaky_fetch
# up to max_tries and raises RuntimeError if all attempts fail.
