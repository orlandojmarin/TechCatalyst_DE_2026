# Advanced Track A2: Pattern Matching (match/case)

**Optional, for fast finishers. Targets Python 3.13.**

`match/case` (added in Python 3.10) matches the **shape** of data, not just one
value. It is a clean replacement for long `if/elif` chains when you are routing
records or pulling fields out of a nested structure, which is exactly what you do
with API responses.

## Before and after

```python
# Before: if/elif on a claim dict
if claim["status"] == "denied":
    route = "closed"
elif claim["policy_type"] == "auto" and claim["reserve"] > 25000:
    route = "SIU"
else:
    route = "standard queue"

# After: match on the shape, capturing fields and using a guard
match claim:
    case {"status": "denied"}:
        route = "closed"
    case {"policy_type": "auto", "reserve": reserve} if reserve > 25000:
        route = "SIU"
    case _:
        route = "standard queue"
```

Key pieces: **mapping patterns** `{"key": value}`, **capture** (`"reserve":
reserve` binds the value to a variable), **guards** (`if reserve > 25000`),
**sequence patterns** (`[date, kind, amount]`), **OR patterns** (`"auto" |
"property"`), and the **wildcard** `case _`.

## Instructions

Copy `Unsolved/pattern_matching.py` into your project. Implement the three
functions with `match/case`.

### Core

1. `route_claim(claim)`: return a route string using mapping patterns and a guard.
   - `denied` status returns `"closed"`.
   - `auto` with `reserve > 25000` returns `"SIU"`.
   - `open` with `reserve >= 20000` returns `"senior adjuster"`.
   - any other `open` claim returns `"standard queue"`.
   - anything else returns `"manual review"`.

2. `describe_payment(record)`: match a `[date, kind, amount]` sequence and return a
   formatted string; return `"unknown record"` for anything else.

### Challenge

3. `priority(status, policy_type)`: match the tuple `(status, policy_type)`.
   - `("denied", _)` returns `"none"`.
   - `("open", "liability")` returns `"high"`.
   - `("open", "auto" | "property")` returns `"normal"`.
   - anything else returns `"low"`.

## Expected Output

```text
Claim routing:
  CLM-4001: standard queue
  CLM-4002: manual review
  CLM-4003: closed
  CLM-4004: senior adjuster
  CLM-4005: standard queue
  CLM-4006: standard queue
  CLM-4007: SIU

Payment records:
  2026-06-01: medical payment of $800.00
  2026-06-05: liability payment of $4,000.00
  unknown record

Priority by (status, policy_type):
  CLM-4001: normal
  CLM-4002: low
  CLM-4003: none
  CLM-4004: high
  CLM-4005: normal
  CLM-4006: normal
  CLM-4007: normal
```

## Success Criteria

- All three functions use `match/case`, not `if/elif`.
- Order matters: the first matching case wins, so the most specific cases come
  first.
- Your output matches the expected output.

## Hint

<details>
<summary>Why does CLM-4007 route to SIU but CLM-4004 to senior adjuster?</summary>

Both are open with a large reserve, but CLM-4007 is `auto` with `reserve > 25000`,
and that case is listed before the `reserve >= 20000` case. The first match wins,
so case order encodes your routing priority.

</details>
