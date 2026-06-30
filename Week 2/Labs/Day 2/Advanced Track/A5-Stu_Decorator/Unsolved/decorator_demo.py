"""Advanced Track: a decorator (the @timer teaser).

Write a timer decorator that prints how long a function took.
"""
import time
from functools import wraps


# TODO: write timer(func) that returns wrapper(*args, **kwargs).
# The wrapper times func, prints "  {func.__name__} took {elapsed:.4f}s",
# and returns the result. Use @wraps(func) on the wrapper.
def timer(func):
    pass


# TODO: decorate total_paid with @timer
def total_paid(claims):
    """Sum the paid amount across claims."""
    return sum(c["paid"] for c in claims)


claims = [{"claim_id": f"CLM-{i}", "paid": float(i * 100)} for i in range(1, 1001)]
print("total:", total_paid(claims))
