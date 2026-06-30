# Advanced Track A3: Classes to Dataclasses

**Optional, for fast finishers. Targets Python 3.13.**

**Prerequisite:** the core drill `Python Drills/10-Stu_Classes` introduces classes
and the class-versus-function decision. This drill builds on it.

You have modeled a claim as a `dict` and as a plain class. A **dataclass** is a
modern shortcut that writes the repetitive parts of a class for you. You will
build the plain class first, then the dataclass, so the improvement is obvious.

## Class basics

```python
class ClaimPlain:
    def __init__(self, claim_id, policy_type, reserve, paid):
        # __init__ runs when you create the object. self is the object itself.
        self.claim_id = claim_id
        self.reserve = reserve
        self.paid = paid

    def reserve_burn(self):
        # A method is a function that lives on the object and uses self.
        return round(self.paid / self.reserve * 100, 1)
```

You create one with `c = ClaimPlain("CLM-5001", "auto", 5000.0, 1200.0)` and call
its method with `c.reserve_burn()`.

## Before and after

```python
# Before: a plain class. You hand-write __init__ and __repr__.
class ClaimPlain:
    def __init__(self, claim_id, policy_type, reserve, paid):
        self.claim_id = claim_id
        ...
    def __repr__(self):
        return f"ClaimPlain({self.claim_id!r}, ...)"

# After: a dataclass. @dataclass writes __init__, __repr__, and __eq__ for you.
from dataclasses import dataclass

@dataclass
class Claim:
    claim_id: str
    policy_type: str
    reserve: float
    paid: float = 0.0          # typed field with a default
    def reserve_burn(self) -> float:
        return round(self.paid / self.reserve * 100, 1)
```

The dataclass needs **type hints** on its fields (`claim_id: str`), and in return
it generates the constructor, a readable `repr`, and field-by-field `==`. Less
boilerplate, fewer bugs.

## Methods versus functions

A **method** is called on the object and uses `self`:
`claim.reserve_burn()`. A **function** is standalone and takes the data as an
argument: `reserve_burn_fn(claim)`. Same result, different call style. Methods keep
behavior next to the data it works on.

## Instructions

Copy `Unsolved/claim_model.py` into your project.

### Core

1. Complete the `ClaimPlain` class: write `__init__` to store the four fields,
   the `reserve_burn` method, and a `__repr__`.

### Challenge

2. Write the `Claim` dataclass with typed fields and a `paid` default of `0.0`,
   plus the `reserve_burn` method.

3. Write the standalone `reserve_burn_fn(claim)` function and confirm it returns
   the same value as the method.

## Expected Output

```text
plain class: ClaimPlain('CLM-5001', 'auto', 5000.0, 1200.0)
plain burn: 24.0
dataclass: Claim(claim_id='CLM-5001', policy_type='auto', reserve=5000.0, paid=1200.0)
dataclass burn: 24.0
c2 == c3: True
with default: Claim(claim_id='CLM-5002', policy_type='property', reserve=12000.0, paid=0.0)
default burn: 0.0
via method: 24.0
via function: 24.0
```

## Success Criteria

- `ClaimPlain` and `Claim` both produce a burn of `24.0` for the same inputs.
- The dataclass version is shorter and you did not write its `__init__` or
  `__repr__`.
- You can explain the difference between `c2.reserve_burn()` and
  `reserve_burn_fn(c2)`.

## Hint

<details>
<summary>Why does `c2 == c3` print True?</summary>

`@dataclass` generates an `__eq__` that compares the objects field by field. Two
`Claim` objects with the same `claim_id`, `policy_type`, `reserve`, and `paid` are
considered equal. A plain class without `__eq__` would compare by identity and
print False.

</details>
