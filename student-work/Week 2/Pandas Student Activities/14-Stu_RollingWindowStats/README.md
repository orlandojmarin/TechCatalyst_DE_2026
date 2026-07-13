# Smoothing Out the Noise

Daily counts are noisy: a single busy Monday can make it look like claims are spiking when they are not. Rolling and expanding windows are how you smooth that out. This is also a preview: in Week 4 Day 2 you will write the same kind of question in SQL using window functions (`LAG`, `LEAD`, running totals). Today you do it in pandas first.

## Instructions

Using the [starter file](Unsolved/rolling_window_stats.ipynb) and `Resources/daily_claims_volume.csv`, complete the following steps:

1. Read `daily_claims_volume.csv` into a DataFrame. Convert `date` to a datetime and set it as the index.

2. Plot `claims_filed` as a line chart. Note how noisy the daily counts look.

3. Calculate a 7-day rolling mean of `claims_filed` using `.rolling(window=7).mean()`. Store it in a new column called `claims_7day_avg`.

4. Plot `claims_filed` and `claims_7day_avg` on the same chart. The rolling average line should look much smoother than the raw daily counts.

5. Calculate a 7-day rolling **sum** of `premium_collected` using `.rolling(window=7).sum()`. Store it in a new column called `premium_7day_total`.

6. Calculate a running (expanding) total of `premium_collected` for the whole period using `.expanding().sum()`. Store it in a new column called `premium_running_total`. This is the running-total pattern you will see again as `SUM(...) OVER (ORDER BY ...)` in SQL.

7. Answer in a markdown cell: why are the first 6 rows of `claims_7day_avg` and `premium_7day_total` `NaN`? What would you have to do differently if you needed a value for every single row starting from day 1?

## Challenge

Add a 3-day rolling mean (`.rolling(window=3).mean()`) alongside your 7-day rolling mean and plot both on the same chart as `claims_filed`. Which window size reacts faster to a real change in the data, and which one is smoother? What would you tell a claims manager who wants "early warning" of a spike versus one who wants "the general trend"?

## Hint

* `.rolling()` needs a fixed-size window and produces `NaN` until enough rows exist to fill that window. `.expanding()` never produces `NaN` after the first row, because it always includes everything seen so far.
* Consult the [pandas window functions documentation](https://pandas.pydata.org/docs/user_guide/window.html) if you get stuck.

## References

Synthetic daily insurance claims volume dataset created for this activity.
