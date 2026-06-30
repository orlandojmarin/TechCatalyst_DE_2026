# Error Handling

**Label: Core.** Real data and real APIs fail: bad values, missing fields, dropped
connections. Robust code catches the failure, decides what to do, and keeps going.
This is the foundation for the resilient API ingestion you build on Day 3.

## Background

You receive a batch of raw claim records. Some have bad amounts, some are missing
the amount entirely, some are negative. Instead of crashing on the first bad row,
you will reject the bad ones, keep the good ones, and report how many failed.

## Instructions

Copy `Unsolved/error_handling.py` into your `student-work/week2/day2` project.

### Core

1. Define `InvalidAmountError(ValueError)`, a custom exception.
2. Write `parse_amount(raw)`:
   - `try` to `float(raw)`; on `TypeError` or `ValueError`, `raise
     InvalidAmountError(...)`.
   - if the value is negative, `raise InvalidAmountError(...)`.
   - otherwise return it rounded to 2 places.
3. Loop the raw claims. Use `try / except InvalidAmountError / else / finally`:
   - `except`: print the rejection, count it, `continue`.
   - `else`: append the clean record (runs only when no exception).
   - `finally`: a marker for cleanup that always runs.
4. Print the clean records and the error count.

### Challenge

5. Write `fetch_with_retry(claim_id, max_tries=3)` that calls a flaky function
   (provided) which randomly raises `ConnectionError`. Retry up to `max_tries`,
   and `raise RuntimeError` if all attempts fail. This is the retry pattern you
   will use against a real API tomorrow.

## Expected Output (Core)

```text
  CLM-2: rejected (cannot parse amount: 'N/A')
  CLM-3: rejected (cannot parse amount: None)
  CLM-4: rejected (negative amount: -50.0)
clean: [{'claim_id': 'CLM-1', 'amount': 1200.5}]
errors: 3
```

The retry demo is random, so its output varies run to run.

## Success Criteria

- You catch **specific** exceptions, not a bare `except:`.
- `else` holds the success path; `finally` always runs.
- Your custom exception subclasses `ValueError`.
- One bad record never stops the whole batch.

## Hints

<details>
<summary>Why catch (TypeError, ValueError) together?</summary>

`float(None)` raises `TypeError` (missing key returns `None` via `.get`), while
`float("N/A")` raises `ValueError`. Catching both in one tuple handles both bad
cases with one rule.

</details>

<details>
<summary>Why a custom exception class?</summary>

`InvalidAmountError(ValueError)` lets callers catch exactly your business error
without also catching unrelated `ValueError`s. Naming your failures is how larger
pipelines stay debuggable.

</details>
