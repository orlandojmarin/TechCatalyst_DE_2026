# Claim Reserve Variance

In this activity, you will create a Python program that calculates how far a
settled claim moved from its original reserve.

## Background

At Charter Oak Mutual, every open claim carries a reserve: the money set aside to
pay it. When the claim finally settles, the amount paid rarely matches the
reserve. Adjusters track the variance and the percent change so the finance team
can see whether reserves are being set too high or too low.

You will start with one claim. Claim `CLM-1001` opened with a reserve of
\$5,000.00. It settled at \$6,200.00. Calculate the variance and the percent
change using the formulas below.

* Variance = Settlement - Reserve

* Percent Change = Variance / Reserve x 100

## Instructions

Copy `Unsolved/Core/claim_variance.py` into your project and complete the following steps:

1. Create variables for the following:

    * `reserve`
    * `settlement`
    * `variance`
    * `percent_change`

2. Derive `variance`.

3. Derive `percent_change`.

4. Print `reserve`, `settlement`, and `percent_change` to the screen.

## Challenge

Use a [format specifier](https://peps.python.org/pep-0498/#format-specifiers)
with the f-string to print the percent change with two decimal places:
`24.00%`. Print the variance as currency with a thousands separator: `$1,200.00`.

## Expected Output

```text
5000.0 6200.0 24.0
```

Challenge (formatted):

```text
Variance: $1,200.00
Percent change: 24.00%
```

## Success Criteria

- Your script prints `reserve`, `settlement`, and `percent_change` without errors.
- `percent_change` computes to exactly `24.0` before formatting.
- The Challenge line uses a format specifier so the percent shows `24.00%` and the
  variance shows `$1,200.00`, not the raw float.

## Hint

For additional help with f-strings, visit
[Python 3's f-Strings](https://realpython.com/python-f-strings/).
