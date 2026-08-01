# Activity 6: Forecast and Anomalies

**Module:** Week 7 Day 1
**Estimated Time:** 45 minutes
**Difficulty:** Intermediate
**Format:** Individual
**Prerequisites:** Activity 5 complete (the Demand Explorer with a switchable data source)

## Objective

In this activity, you will add two new capabilities to the Demand Explorer: a Holt-Winters forecast that projects demand forward, and an anomaly detector that flags days where demand broke sharply from its recent pattern. You will also debug a rolling-window design that looks correct, boots without errors, and silently gives the wrong answer.

## Background

### Forecasting with Holt-Winters

`statsmodels` ships `ExponentialSmoothing`, an implementation of the Holt-Winters method. It decomposes a series into a level, a trend, and a seasonal component, then projects all three forward. For daily taxi demand, the seasonal component should repeat every 7 days, because ridership follows a weekly pattern (weekdays differ from weekends). That is what `seasonal_periods=7` tells the model:

```python
fit = ExponentialSmoothing(series, trend="add", seasonal="add", seasonal_periods=7).fit()
future = fit.forecast(horizon)
```

`seasonal_periods=7` is correct because daily taxi rides genuinely repeat on a 7-day cycle. That will not be true of every series you hand this model. If you switch the Demand Explorer to a live stock ticker and leave `seasonal_periods=7` in place, do not expect the seasonal component to mean much. Markets do not have a clean 7-day cycle the way commuting does, so the forecast on a ticker is mostly the trend and level, with a seasonal term that is close to noise. A forecasting method is not a universal tool. It encodes an assumption about the data, and the assumption has to match.

### Detecting anomalies with a rolling z-score

An anomaly detector here is simple: for each day, compare its value against the mean and standard deviation of a recent baseline window, and flag it if it is more than `threshold` standard deviations away.

```python
baseline = series.shift(1).rolling(28)
z = (series - baseline.mean()) / baseline.std()
flags = series[z.abs() > threshold]
```

`series.shift(1)` is what makes this a trailing window: the baseline for a given day only ever looks at days strictly before it. That matters more than it looks like it should, and the next section is about exactly why.

## Instructions

1. Copy the starter file into your work folder:

   ```bash
   cp "Week 7/Labs/Day 1/starter/activity_6_forecast_anomalies.py" student-work/week7/day1/
   ```

   Do not edit the file under `Week 7/Labs/Day 1/starter/` in place. Work only on the copy in `student-work/`.

2. Open `student-work/week7/day1/activity_6_forecast_anomalies.py` in VS Code. Read the whole file before changing anything. Everything through the smoothing chart is the finished Activity 5 app: the path resolver, `load_taxi`, `load_prices`, the source radio, the KPI tiles, and the smoothed chart are already done. Below that are two new sections, Forecast and Anomalies, each with `# TODO` blocks:
   - the `ExponentialSmoothing` fit and the `.forecast(horizon)` call
   - the trailing baseline and the z-score computation
   - the scatter trace that marks the flagged anomalies on the chart

   Each `# TODO` comment tells you exactly what to write. Replace the placeholder code with your own.

3. Run the app from the repository root:

   ```bash
   uv run streamlit run student-work/week7/day1/activity_6_forecast_anomalies.py
   ```

4. With "NYC taxi demand" selected, check the Forecast section. To confirm your `ExponentialSmoothing` call is correct independent of whatever horizon the slider happens to be on, run this from the repository root and compare against the values below:

   ```bash
   uv run python -c "
   import pandas as pd
   from pathlib import Path
   from statsmodels.tsa.holtwinters import ExponentialSmoothing
   s = pd.read_csv('Week 7/Labs/Day 1/data/nyc_taxi.csv', parse_dates=['timestamp'], index_col='timestamp')['value'].resample('D').sum()
   train = s.loc[:'2014-12-31']
   fit = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=7).fit()
   print(fit.forecast(31).head(3))
   "
   ```

   Trained on data through 2014-12-31 and forecast 31 days forward, the first three values should be:

   | date | forecast |
   |---|---|
   | 2015-01-01 | 640,527 |
   | 2015-01-02 | 769,368 |
   | 2015-01-03 | 837,933 |

   The app itself trains on the whole series and forecasts past the end of the data (into February 2015), so what you see on the page will not match this table directly. This check exists so you can confirm your Holt-Winters call is right before trusting the live chart.

5. Move on to the Anomalies section once your forecast is working. Read the next section before you touch the anomaly code: it walks you through a mistake you are meant to make first.

## The Centered-Window Trap

The starter's Anomalies section does not start with a blank TODO. It starts with a rolling baseline that already runs:

```python
baseline = series.rolling(28, center=True)
```

This is the version most people reach for first, because "average the 28 days around this point" sounds like the obvious way to describe a day's local baseline. Run the app with this line in place and threshold at the default 3.0. Note how many anomalies are flagged.

Now look at what a centered 28-day window actually requires: 14 days of data on each side of the point being evaluated. The taxi series ends on 2015-01-31. For every day in the last two weeks of the series, roughly 2015-01-19 through 2015-01-31, there is no "after" half of the window available, so the baseline is `NaN`. A `NaN` comparison never exceeds a threshold, so those days can never be flagged, no matter how extreme they are.

That silently hides Winter Storm Juno, the single largest anomaly in this dataset, from a detector that ran without raising a single error. It also flags nothing at all elsewhere in the series: with the centered window, no day anywhere clears a z-score of 3.0.

Two lessons follow directly from this, and they generalize past this one lab:

- **A centered window leaks information from the future.** Averaging days on both sides of a point means the baseline for "today" depends on data that has not happened yet. A live monitoring system does not have tomorrow's numbers. If your anomaly detector needs them to compute a baseline, it cannot run in production the way you tested it.
- **Silent `NaN` at the edges hides exactly the data you care about most.** The most recent days are usually the ones a monitoring system exists to watch. An edge effect that quietly disables detection right where the data ends is the worst possible place for a design flaw to hide, because nothing crashes and nothing warns you.

Fix it with the trailing window from the Background section:

```python
baseline = series.shift(1).rolling(28)
```

Every day's baseline now looks only backward, so there is no future leakage and no window that runs off the end of the data. Rerun the app. Winter Storm Juno now shows up as the two deepest anomalies in the series.

Verify your fix independent of the app:

```bash
uv run python -c "
import pandas as pd
from pathlib import Path
s = pd.read_csv('Week 7/Labs/Day 1/data/nyc_taxi.csv', parse_dates=['timestamp'], index_col='timestamp')['value'].resample('D').sum()
b = s.shift(1).rolling(28)
z = (s - b.mean()) / b.std()
f = z[z.abs() > 3].dropna()
print(len(f))
print(f.round(2).to_string())
"
```

At the default threshold of 3.0, this should give you exactly six rows:

| date | value | z |
|---|---|---|
| 2014-09-01 | 556,314 | -3.07 |
| 2014-09-06 | 881,714 | +3.25 |
| 2014-11-01 | 986,568 | +3.26 |
| 2014-12-25 | 379,302 | -3.93 |
| 2015-01-26 | 375,311 | -4.20 |
| 2015-01-27 | 232,058 | -4.75 |

If your count differs from six, the fix is not correct yet. Check that you are computing the baseline with `.shift(1)` before `.rolling(28)`, not the other way around.

## Interpretation

Six flagged days is not the deliverable. The deliverable is a short written note, one line per date, naming what each flagged day was and why demand broke from its baseline. Do the research yourself first, then check your answers against the ones below.

- **2014-09-01, Labor Day.** A federal holiday with most offices closed pulls the weekday commute out of the demand pattern.
- **2014-09-06, no clear single cause.** This is a positive spike, and there is no well-known citywide event on this date that explains it. That is the honest answer. An anomaly you cannot explain is a finding to report, not a failure to hide. Write that down instead of inventing a story to fill the gap.
- **2014-11-01, the Saturday of Halloween weekend, the day before the NYC Marathon.** Both a major nightlife weekend and race-related street activity land here.
- **2014-12-25, Christmas.** The city empties out and ridership collapses, the same shape as Labor Day but deeper.
- **2015-01-26 and 2015-01-27, Winter Storm Juno.** The city ordered vehicles off the streets during the storm. Rides fell from 694,262 on January 25 to 375,311 on January 26 to 232,058 on January 27, the lowest point in the dataset, before recovering to 621,483 on January 28 once the travel ban lifted.

One date that does **not** appear on this list, even though most students expect it: **Thanksgiving, 2014-11-27.** It comes close (its z-score is roughly -2.93) but does not clear the default threshold of 3.0. Lower the threshold slider from 3.0 to 2.5 and watch it appear. That is the point of having a threshold slider at all: the line between "normal variation" and "anomaly" is a choice you make, not a fact the data hands you, and moving that choice changes what gets reported.

## Success Criteria

- All three `# TODO` blanks are filled in and the placeholder values (`series.tail(horizon)` for the forecast, the zero-filled `z` and empty `flags` for anomalies) are gone.
- The app runs with `uv run streamlit run student-work/week7/day1/activity_6_forecast_anomalies.py` and shows a Forecast section and an Anomalies section below the Activity 5 chart.
- Your standalone Holt-Winters check (Step 4) matches the three forecast values in the table above.
- You ran the anomaly detector with the centered window first, and can explain in your own words why it misses the January 2015 blizzard.
- Your standalone anomaly check, using `series.shift(1).rolling(28)`, matches all six rows in the table above.
- You wrote a one-line interpretation for each of the six flagged days, including an honest "no clear cause" for 2014-09-06 instead of a guess.
- You lowered the anomaly threshold and confirmed Thanksgiving (2014-11-27) appears once the threshold drops below its z-score.
