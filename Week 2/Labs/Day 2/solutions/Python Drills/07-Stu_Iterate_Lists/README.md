# Daily Claims Cash Flow

In this activity, you will use a list to track the claims desk net cash flow for
each business day of the month, then iterate over the list to calculate the best
and worst days and split the month into surplus and deficit days.

## Background

Each business day the claims desk records its net cash flow: recoveries (money in,
such as subrogation) minus payouts (money out). Some days the desk runs a surplus,
some days a deficit. The operations lead wants a quick monthly readout: how many
surplus days, how many deficit days, the best and worst days, and the average. You
will build it with a for loop over a list.

## Instructions

Using `Unsolved/claims_cashflow.py`, complete the following:

* Create a for loop over the `daily_net` list and cumulatively sum the `total` net
  cash flow and the `count` of business days.

* Use conditionals to track the `maximum` (best day) and `minimum` (worst day)
  values.

* Create lists `surplus_days` and `deficit_days` and group each day's value into
  the matching list.

* Determine and print:

  * Number of total business days
  * Net cash flow for the month
  * Daily average
  * Worst deficit
  * Best surplus
  * Number and percentage of surplus days
  * Number and percentage of deficit days
  * The surplus days list and the deficit days list

## Hints

Use these formulas:

* Number of total days = length of `daily_net`
* Surplus day = value greater than 0
* Deficit day = value less than or equal to 0
* Net cash flow = sum of `daily_net`
* Daily average = net cash flow divided by number of days
* Worst deficit = smallest number in `deficit_days`
* Best surplus = largest number in `surplus_days`
* Percentage of surplus days = surplus days divided by total days, times 100

Your results should look similar to the following:

```text
---------Summary Statistics----------
Number of Total Days: 20
Number of Surplus Days: 13
Number of Deficit Days: 7
Percentage of Surplus Days: 65.0%
Percentage of Deficit Days: 35.0%
-------------------------------------
Surplus Days: [352, 252, 354, 56, 123, 254, 325, 47, 321, 123, 133, 613, 232]
Deficit Days: [-224, -544, -650, -43, -123, -151, -311]
-------------------------------------
Net Cash Flow: 1139
Daily Average: 56.95
Worst Deficit: -650
Best Surplus: 613
```
