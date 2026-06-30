# Week 2 Day 2: Student Resources for Python Foundations

**AI-Free Zone:** no Copilot, no ChatGPT, and no copying from `solutions/`. Start from the provided `Unsolved` scaffold and write the logic yourself. Today is about building real fluency, not autocompleting it.

## Core References

| Resource | Why it helps |
|----------|-------------|
| [Python 3 Built-in Types](https://docs.python.org/3/library/stdtypes.html) | Complete reference for str, list, dict, set, and tuple methods |
| [Python 3 Built-in Functions](https://docs.python.org/3/library/functions.html) | `type()`, `len()`, `enumerate()`, `zip()`, `round()`, `sorted()`, and `isinstance()` |
| [UV Documentation](https://docs.astral.sh/uv/) | Local Python project workflow for `uv init`, `uv run`, `uv sync`, and `uv lock` |
| [Python Tutor](https://pythontutor.com) | Visualize exactly what Python is doing step by step |

## Strings and f-Strings

- [Real Python: f-Strings](https://realpython.com/python-f-strings/) covers `:,` (thousands separator), `:.2f` (two decimal places), `!r`, and nested expressions.
- [PEP 498: Format Specifiers](https://peps.python.org/pep-0498/#format-specifiers) is the official spec, useful for the Challenge in 01-Variables.

Quick reminder:

```python
reserve = 18420.50
claims = 3_421
print(f"${reserve:,.2f} across {claims:,} claims")
# $18,420.50 across 3,421 claims
```

## Collections: Lists and Dictionaries

- [Real Python: Python Dictionaries](https://realpython.com/python-dicts/) covers `.get()`, `.items()`, `.update()`, and dict comprehensions.
- [Real Python: Lists and Tuples](https://realpython.com/python-lists-tuples/) covers indexing, slicing, `.append()`, and `.extend()`.

Key pattern for 06-Dictionaries and 09-Nesting:

```python
# Safe dict access returns the default if the key is missing
value = my_dict.get("key", default_value)

# Extract one field from a list of dicts
policy_types = [claim["policy_type"] for claim in claims]
```

## Loops

- [Real Python: Python for Loops](https://realpython.com/python-for-loop/) covers `for`, `range()`, `enumerate()`, and `zip()`.

```python
# enumerate when you need index and value
for i, amount in enumerate(amounts):
    print(f"row {i}: {amount}")

# zip when iterating two lists together
for amount, policy_type in zip(amounts, policy_types):
    print(f"{policy_type}: ${amount:,.2f}")
```

## Functions

- [Real Python: Defining Functions](https://realpython.com/defining-your-own-python-function/) covers default args, docstrings, and scope.
- [Python Built-in Functions: round()](https://docs.python.org/3/library/functions.html#round) is the official reference used in 08-Functions.

Pattern from today's live build:

```python
def clean_amount(raw, max_amount=1_000_000.0):
    """Convert a raw claim amount string to float; return None if invalid."""
    try:
        amount = float(raw)
    except ValueError:
        return None
    if amount < 0 or amount > max_amount:
        return None
    return round(amount, 2)
```

This is the same idea as `parse_money()` in the mini-capstone.

## Debugging Tracebacks

- [Real Python: Python Traceback Guide](https://realpython.com/python-traceback/) covers all six errors from today's clinic.
- [Python Errors & Exceptions (Official Docs)](https://docs.python.org/3/tutorial/errors.html) is the authoritative reference.

**Read bottom-up:**

1. Last line = error type + message. This tells you what broke.
2. Walk up to find your file and line number. Ignore library internals at first.
3. Ask what value caused this. Add a `print()` just before that line to confirm.

Today's Big Six:

| Error | Typical cause |
|-------|--------------|
| `KeyError` | Dict key does not exist, often solved with `.get()` |
| `TypeError` | Wrong type in an operation, such as `"18" + 5` |
| `IndexError` | List index out of range |
| `NameError` | Variable not defined yet, usually typo or wrong scope |
| `ValueError` | Right type, wrong value, such as `float("N/A")` |
| `IndentationError` | Mixed tabs/spaces or wrong block depth |

## Style

- [PEP 8 Style Guide](https://peps.python.org/pep-0008/) covers 4-space indentation, snake_case names, and line length.

## Today's Drills: Quick Reference

| Drill | Scenario | Key concept |
|-------|----------|-------------|
| 01-Variables | Claim reserve variance | Variables, arithmetic, f-string format specifiers |
| 02-Conditionals | Triage logic | `if / elif / else`, comparison operators, truthiness |
| 03-Triage | Triage faceoff | `random` module, `input()`, nested conditionals |
| 04-Loops | Claim pipeline banner | `for` over a string and a `range()` |
| 05-Lists | The claim queue | List creation, slicing, indexing, mutation |
| 06-Dictionaries | Claim reserves by tier | Dict CRUD, `.get()`, iteration with `.items()` |
| 07-Iterate_Lists | Daily claims cash flow | Loop plus logic over a list |
| 08-Functions | Loss ratio | Define, call, default args, docstrings, `round()` |
| 09-Nesting | Claim payment rollup | Dict of lists of records, exactly what REST APIs return tomorrow |
| 10-Classes | Claims as classes | Classes, `__init__`, methods, object state, and class versus function |
| 11-File_IO | Daily claims file | Read and write text files with `pathlib` and `open` |
| 12-CSV_IO | Claims CSV | `csv.DictReader` and `csv.DictWriter` |
| 13-JSON_IO | Claims JSON | `json.load` and `json.dump`, nested data (the Day 3 API shape) |
| 14-Lambdas_Map_Filter | Transform claims | `lambda`, `map`, `filter`, `sorted(key=...)` (reused in PySpark) |
| 15-SQLite | Claims database | `sqlite3`: `CREATE`, `INSERT`, `SELECT`, `GROUP BY` |
| 16-Error_Handling | Reject bad records | `try/except/else/finally`, custom exceptions, retry loop |
| 17-Collections | Group and count | `defaultdict`, `Counter` |
| 18-Datetime | Claim dates | `strptime`/`strftime`, `timedelta`, sorting by date |
| Mini-Capstone | Claims intake pipeline | All of the above, on messy claim data, tiered Core/Challenge/Stretch |
| Advanced Track | Modern Python (optional) | Comprehensions, `match`/`case`, classes and dataclasses, walrus, generators |

**Priority:** finish 09-Nesting before anything else in the afternoon block, then
move to the mini-capstone.

## Modern Python (Advanced Track)

Optional, for fast finishers. These features target the Python 3.13 on your VM.

| Resource | Why it helps |
|----------|-------------|
| [Comprehensions (official tutorial)](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) | list, dict, and set comprehensions |
| [match statement (official tutorial)](https://docs.python.org/3/tutorial/controlflow.html#match-statements) | structural pattern matching, 3.10+ |
| [dataclasses (official docs)](https://docs.python.org/3/library/dataclasses.html) | model records with less boilerplate |
| [Assignment expressions / walrus (PEP 572)](https://peps.python.org/pep-0572/) | assign and test in one expression |

## Lab Deliverable Checklist

| Done | Deliverable |
| :--- | :--- |
| ☐ | UV project created under `student-work/week2/day2/` |
| ☐ | Morning drills solved by hand (01-Variables, 02-Conditionals, 03-Triage) |
| ☐ | Afternoon drills solved (04, 05, 06, 07, 08) |
| ☐ | 09-Nesting completed (priority because APIs return this shape tomorrow) |
| ☐ | Mini-capstone `claims_pipeline.py` (Core and Challenge at minimum) |
| ☐ | Each traceback you defeated written down |
| ☐ | Solutions committed under `student-work/week2/day2/` in your course repo |
| ☐ | One "aha" note added to your repo README |
| ☐ | Exit ticket completed |
