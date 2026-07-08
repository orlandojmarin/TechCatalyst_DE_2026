## Finally Functioning

In this activity, you will define a function to calculate the loss ratio for a
book of insurance business. You are encouraged to work with a partner.

## Background

You have been calculating the loss ratio by hand for three years in a row: once
for 2024, once for 2025, and once for 2026. You wrote the same formula three
times. That is hard to maintain: if the formula ever changes, you have to fix it
in three places. You decide to refactor the logic into one reusable function.

The loss ratio is the classic insurance performance metric. It tells you how much
of every premium dollar is going back out as claims. A lower loss ratio is better
for the insurer.

Loss ratio formula:

```text
loss_ratio = incurred_losses / earned_premium * 100
```

In this activity, define a function named `calculate_loss_ratio` that accepts:

* `incurred_losses`
* `earned_premium`
* `round_to` (with a default value of `2`)

The function should return the loss ratio as a float percentage.

## Instructions

Use `Unsolved/loss_ratio.py` to complete the following steps:

1. Define `calculate_loss_ratio(incurred_losses, earned_premium, round_to=2)` that
   returns the loss ratio as a percentage.

2. For 2024, set `incurred_losses` to 2900 and `earned_premium` to 4500.

3. Call `calculate_loss_ratio()` and capture the result as `year_2024`.

4. For 2025, set `incurred_losses` to 3600 and `earned_premium` to 4800, then call
   the function and capture `year_2025`.

5. For 2026, set `incurred_losses` to 4200 and `earned_premium` to 5000, then call
   the function and capture `year_2026`.

6. Print `year_2024`, `year_2025`, and `year_2026` as percentages.

7. Identify the worst (highest) loss ratio of the three years.

## Challenge

Instead of returning each loss ratio into a variable, append it to a global list
named `loss_ratios`. Write this logic in a new function
`calculate_loss_ratio_list`, then call it for all three years and print the list.

## Hints

* The `round_to=2` default means a caller can write
  `calculate_loss_ratio(2900, 4500)` and still get two decimals.
* Refer to the official [`round()` documentation](https://docs.python.org/3/library/functions.html#round).
* Expected output:

```text
Loss Ratio for 2024: 64.44%
Loss Ratio for 2025: 75.0%
Loss Ratio for 2026: 84.0%
Worst loss ratio: 84.0%
Loss ratios: [64.44, 75.0, 84.0]
```
