# Claims as Classes

So far you have modeled a claim as a `dict` and written functions that act on it.
A **class** lets you bundle the claim's data and the behavior that goes with it
into one object. Knowing when to reach for a class instead of a function is a
critical engineering skill, and this drill is about exactly that.

## A class in three parts

```python
class Claim:
    def __init__(self, claim_id, reserve, paid):
        # __init__ runs when you create the object. self is this claim.
        self.claim_id = claim_id      # attribute (data on the object)
        self.reserve = reserve
        self.paid = paid

    def reserve_burn(self):           # method (behavior on the object)
        return round(self.paid / self.reserve * 100, 1)
```

- `__init__` is the constructor. It stores the starting data on `self`.
- Attributes (`self.reserve`) are the object's data.
- Methods (`reserve_burn`) are functions that live on the object and use `self`.

You create one with `c = Claim("CLM-6001", 5000.0, 1200.0)` and use it with
`c.reserve_burn()`.

## Class versus function: when to use each

This is the judgment call.

| Use a function when... | Use a class when... |
|---|---|
| You transform inputs into an output | You have a "thing" with data and behavior |
| There is no state to remember | The thing carries state that changes over time |
| One operation, no related data | Several operations naturally belong together |

Example: `loss_ratio(losses, premium)` is a pure calculation, so a **function**
is right. A claim, on the other hand, has data (reserve, paid) and behavior
(burn, add a payment) that change over its life, so a **class** is the better
fit. In this drill, `add_payment` is the tell: the claim remembers its new
`paid` total. A plain function cannot remember anything between calls.

## Instructions

Copy `Unsolved/claim_class.py` into your `student-work/week2/day2` project.

### Core

1. Write the `Claim` class with `__init__(self, claim_id, policy_type, reserve,
   paid)` storing each value on `self`.
2. Add a `reserve_burn(self)` method returning `round(self.paid / self.reserve *
   100, 1)`.
3. Add an `is_over_reserve(self)` method returning `self.paid > self.reserve`.
4. Add a `summary(self)` method returning a readable one-line string.
5. Create the three claims, print each summary.

### Challenge

6. Add an `add_payment(self, amount)` method that increases `self.paid`.
7. Post a `$4,200` payment to `CLM-6001`, print its new summary, and count how
   many claims are over their reserve.

## Expected Output

```text
Initial claims:
  CLM-6001 (auto): burn 24.0%
  CLM-6002 (property): burn 112.5% OVER RESERVE
  CLM-6003 (liability): burn 20.0%

After a $4,200 payment on CLM-6001:
  CLM-6001 (auto): burn 108.0% OVER RESERVE

Claims over reserve: 2
```

## Success Criteria

- `Claim` has an `__init__` plus the four methods.
- Calling `add_payment` changes the object's `paid` and its later `reserve_burn`.
- You can explain, in one sentence, why a claim is a class but `loss_ratio` is a
  function.

## Hint

<details>
<summary>Why does CLM-6001 flip to OVER RESERVE after the payment?</summary>

`add_payment` changes `self.paid` on that one object. The next call to
`reserve_burn` and `is_over_reserve` reads the updated `paid`, so the claim
"remembers" the payment. That memory of state is the main reason to use a class
instead of a function.

</details>

## Next step

The Advanced Track drill `A3-Stu_Classes_to_Dataclasses` builds directly on this:
it shows how `@dataclass` writes the `__init__` and `__repr__` for you.
