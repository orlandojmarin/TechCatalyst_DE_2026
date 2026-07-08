"""Student Do: Error Handling.

Real data and real APIs fail: bad values, missing fields, dropped connections.
Robust code catches the failure, decides what to do, and keeps going. This is the
foundation for resilient API ingestion on Day 3.
"""
import random

raw_claims = [
    {"claim_id": "CLM-1", "amount": "1200.50"},
    {"claim_id": "CLM-2", "amount": "N/A"},
    {"claim_id": "CLM-3"},                 # missing 'amount'
    {"claim_id": "CLM-4", "amount": "-50"},
]


class InvalidAmountError(ValueError):
    """Raised when an amount is present but not a valid non-negative number."""


def parse_amount(raw):
    # raw may be None (missing key) or a non-numeric string
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise InvalidAmountError(f"cannot parse amount: {raw!r}")
    if value < 0:
        raise InvalidAmountError(f"negative amount: {value}")
    return round(value, 2)


# ---- Core: try / except / else / finally, catching specific exceptions ----
clean = []
errors = 0
for claim in raw_claims:
    cid = claim["claim_id"]
    try:
        amount = parse_amount(claim.get("amount"))  # .get returns None if missing
    except InvalidAmountError as exc:
        print(f"  {cid}: rejected ({exc})")
        errors += 1
        continue
    else:
        # runs only if no exception was raised
        clean.append({"claim_id": cid, "amount": amount})
    finally:
        # always runs (here just a marker; in real code, close a file or connection)
        pass

print("clean:", clean)
print("errors:", errors)


# ---- Challenge: retry a flaky call (foreshadows Day 3 API retries) ----
def flaky_fetch(claim_id):
    if random.random() < 0.5:
        raise ConnectionError("temporary network error")
    return {"claim_id": claim_id, "status": "ok"}


def fetch_with_retry(claim_id, max_tries=3):
    for attempt in range(1, max_tries + 1):
        try:
            return flaky_fetch(claim_id)
        except ConnectionError as exc:
            print(f"  attempt {attempt} failed: {exc}")
    raise RuntimeError(f"gave up on {claim_id} after {max_tries} tries")


print("\nRetry demo:")
try:
    print("  fetched:", fetch_with_retry("CLM-1"))
except RuntimeError as exc:
    print(" ", exc)
