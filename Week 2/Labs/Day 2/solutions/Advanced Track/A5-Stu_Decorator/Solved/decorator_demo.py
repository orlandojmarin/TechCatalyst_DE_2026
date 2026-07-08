"""Advanced Track: a decorator (the @timer teaser).

A decorator wraps a function to add behavior without changing the function itself.
Here we time how long a function runs. You will use decorators to instrument
pipelines (timing, logging, retries) in later weeks.
"""
import time
from functools import wraps


def timer(func):
    @wraps(func)                      # keeps func's name and docstring
    def wrapper(*args, **kwargs):     # accepts any arguments
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


@timer
def total_paid(claims):
    """Sum the paid amount across claims."""
    return sum(c["paid"] for c in claims)


claims = [{"claim_id": f"CLM-{i}", "paid": float(i * 100)} for i in range(1, 1001)]
print("total:", total_paid(claims))
print("function name preserved:", total_paid.__name__)
