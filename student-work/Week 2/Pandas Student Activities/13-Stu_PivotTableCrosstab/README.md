# Claims by Region and Type

You have already used `groupby` to summarize data. `pivot_table` and `crosstab` answer a specific, common version of that question: "break this down by two categories at once, and lay it out as a grid." In this activity you will summarize a batch of insurance claims the way a claims manager would ask for it.

## Instructions

Using the [starter file](Unsolved/claims_pivot.ipynb) and `Resources/insurance_claims.csv`, complete the following steps:

1. Read `insurance_claims.csv` into a DataFrame.

2. Use `pd.pivot_table` to build a grid of **total `claim_amount`**, with `region` as the rows and `claim_type` as the columns. Use `aggfunc="sum"`.

3. Rebuild the same pivot table, but this time use `aggfunc="mean"` instead of `"sum"`. Compare the two: which region/type combination has a high total but a low average, or vice versa? What does that tell you about claim volume versus claim size?

4. Use `pd.crosstab` to count how many claims fall into each combination of `region` and `status` (Open, Closed, Denied).

5. Add `margins=True` to your crosstab from step 4 to get row and column totals. Confirm the grand total matches the number of rows in the original DataFrame.

## Challenge

Use `pivot_table` with a list of two aggregation functions, `aggfunc=["sum", "count"]`, on `claim_amount`, broken down by `region` and `claim_type`. This gets you total dollars and claim counts in a single table. Which region/type combination should the claims team look at first: the one with the most claims, or the one with the highest total dollars?

## Hint

* `pivot_table` and `groupby().unstack()` can produce the same result. `pivot_table` is usually more readable when you are laying out two categorical columns as a grid.
* `crosstab` is built for counts specifically; you do not need to pass a value column or an aggfunc unless you want something other than a count.
* Consult the [pivot_table documentation](https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html) and [crosstab documentation](https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html) if you get stuck.

## References

Synthetic insurance claims dataset created for this activity.
