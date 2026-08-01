# Week 7 Day 1 Exit Ticket: Pandas Plotting, hvPlot, Streamlit, and Anomaly Detection

1. You want a bar chart that is wider, has rotated category labels, and shows no legend. Which combination of pandas `.plot` keywords accomplishes this?
   a. `figsize`, `rot`, `legend=False`
   b. `width`, `height`, `legend=False`
   c. `rot`, `color`, `ylabel`
   d. `figsize`, `xlabel`, `grid`
   Answer: a
   Explanation: `figsize` widens the chart, `rot` rotates the tick labels, and `legend=False` hides the legend a single series does not need. Option b uses hvPlot's keyword names (`width` and `height`) instead of pandas `.plot`'s, which is exactly the swap Activity 2 introduces.

2. What does `import hvplot.pandas` actually do?
   a. Loads a sample dataset bundled with hvPlot for practice
   b. Replaces `import pandas`, since hvPlot supersedes the DataFrame class
   c. Registers a `.hvplot` accessor onto every pandas DataFrame and Series, so the data and column names never have to change
   d. Converts every `.plot()` call already written earlier in the notebook into an interactive chart automatically
   Answer: c
   Explanation: The import does not create a new object you call directly. It adds a `.hvplot` accessor that is available afterward on any DataFrame or Series, so the underlying data and code stay exactly as they were.

3. Why does this afternoon's Streamlit work use Plotly Express instead of hvPlot for charts inside the app?
   a. hvPlot cannot produce a bar chart or a scatter plot
   b. Streamlit has a dedicated `st.plotly_chart` function that renders a Plotly figure directly, while hvPlot figures need extra steps to embed
   c. Plotly is the only library that can add a dropdown widget above a chart
   d. hvPlot only runs inside Jupyter and cannot be imported from a `.py` script
   Answer: b
   Explanation: Activity 2 states this directly: `st.plotly_chart` takes a Plotly figure and renders it natively, so the course uses Plotly for anything that ends up inside a Streamlit app.

4. A charge-to-payment ratio across ten states runs from about 6.65 down to about 3.99. Activity 3 plots this as a pie chart on purpose, before switching to a bar chart. What does the pie chart demonstrate?
   a. That a pie chart is the correct choice whenever there are ten or fewer categories
   b. That a bar chart requires the values to be sorted first, while a pie chart does not
   c. That legends become unnecessary once a chart has enough slices
   d. That when the values are close together, a pie chart makes the slices look nearly identical, hiding a ranking a bar chart shows instantly
   Answer: d
   Explanation: The top ten states' ratios are close enough in size that the pie slices are visually indistinguishable, even though the underlying ranking is real and a sorted horizontal bar chart shows it clearly.

5. You are rewriting the title "Ratio by state" as a conclusion title. Which option is best, given the notebook's rule that a title must be checkable against the chart it sits on?
   a. "New Jersey bills 6.7 times more than Texas"
   b. "New Jersey hospitals bill 6.7 times what Medicare pays"
   c. "State-level billing patterns"
   d. "Charge to payment ratio, all states"
   Answer: b
   Explanation: Options c and d only label what the axes show. Option a uses the "times more than" phrasing the notebook explicitly says to avoid, because readers split on whether that means times as much or times greater than. Option b states the finding directly, in a way you can check against the chart.

6. In the Activity 4 app, you click to open a collapsed expander at the bottom of the page. What actually happens?
   a. Only the code inside the expander re-executes
   b. Nothing runs again; Streamlit just redraws the expander in place
   c. Streamlit reruns the entire script from the top, including a `st.write` line placed near the top of the file
   d. The app reruns only the lines that appear below the expander in the file
   Answer: c
   Explanation: The rerun experiment in Activity 4 makes this concrete: opening the expander changes a timestamp printed near the top of the file, which only happens if the whole script ran again from line 1.

7. What does `@st.cache_data` prevent in the Activity 4 app?
   a. Redoing the expensive read-and-resample of the whole CSV on every single rerun
   b. The CSV file from being copied into `student-work/`
   c. The metric tiles from ever changing value
   d. More than one browser tab from opening the app at once
   Answer: a
   Explanation: Without the decorator, every rerun (triggered by any interaction) re-reads and re-resamples the CSV from scratch, which is why the app visibly slows down when it is removed.

8. In Activity 5, `load_prices` has both a `try/except` around the `yfinance` download and a separate `if series.empty` check afterward. Why both?
   a. `try/except` alone is enough once `auto_adjust=True` is set
   b. Streamlit requires exactly two error handlers per widget
   c. The empty check only matters when the taxi source, not the live ticker, is selected
   d. A bad ticker or an empty date range does not always raise an exception; `yfinance` can succeed and simply return an empty DataFrame with nothing in it
   Answer: d
   Explanation: The two checks catch two different failure shapes: an outright failure (`try/except`) and a call that succeeds but returns nothing (`if series.empty`).

9. Why does a centered 28-day window (`series.rolling(28, center=True)`) fail to flag the January 2015 blizzard, the most extreme swing in the whole series?
   a. The default threshold of 3.0 was set too high specifically for winter months
   b. A centered window needs 14 days of data on each side of the point being evaluated; near the end of the series there is no "after" half, so the baseline is `NaN`, and a `NaN` comparison never clears the threshold
   c. The blizzard dates were dropped from `nyc_taxi.csv` during loading
   d. Centered windows only work when the series has fewer than 28 rows
   Answer: b
   Explanation: The series ends 2015-01-31, so every day in roughly the last two weeks has no future half for the window to average, producing a `NaN` baseline that can never be flagged. With this window, no day anywhere in the series clears a z-score of 3.0.

10. What does `.shift(1)` accomplish in `baseline = series.shift(1).rolling(28)`?
    a. It shifts the flagged threshold down by one standard deviation
    b. It converts the window from trailing back to centered
    c. It makes each day's baseline look only at days strictly before it, so no future data leaks into the comparison
    d. It drops the first 28 rows of the series before any computation
    Answer: c
    Explanation: The trailing window fixes exactly the problem in question 9: a day's baseline never depends on data that has not happened yet, which is also what a live monitoring system would require.

11. At the default threshold of 3.0, using the trailing window (`series.shift(1).rolling(28)`), which statement is correct?
    a. Exactly six dates are flagged, and Thanksgiving's z-score of about -2.93 does not clear the threshold
    b. Thanksgiving (2014-11-27) is flagged along with the six blizzard-adjacent dates
    c. No dates are flagged until the threshold is lowered to 2.5
    d. Christmas (2014-12-25, z = -3.93) is the single most extreme flagged date
    Answer: a
    Explanation: The six flagged dates are 2014-09-01, 2014-09-06, 2014-11-01, 2014-12-25, 2015-01-26, and 2015-01-27. Thanksgiving's z-score is near the threshold but does not clear 3.0. Option d is incorrect for a separate reason: 2015-01-27 (z = -4.75) is deeper than Christmas.

12. In Activity 7, `build_facts` returns a plain string built from `series`, `flags`, and `z`, and that string, not the DataFrame, is what gets sent to the model. Why?
    a. The OpenAI API rejects DataFrame objects at the network layer
    b. Sending a string instead of a DataFrame is what allows `@st.cache_data` to work at all
    c. The model needs the raw series so it can compute its own z-scores as a check
    d. An LLM is good at turning listed facts into prose, not at generating new numbers or analysis; a number that was never printed into that string has no way to reach the model except by invention
    Answer: d
    Explanation: The app keeps a strict separation between computation (done in code, before the call) and narration (done by the model, from a fixed text block). Anything the model states that is not in that string was invented.

13. Why does gating the LLM call behind the "Draft the narrative" button matter, given the Streamlit rerun model?
    a. Buttons are the only Streamlit widget that supports `st.spinner`
    b. Without the button, the whole script, including the API call, would rerun on every interaction anywhere on the page, not only when the user actually wants a narrative
    c. `st.error` cannot be called unless it sits inside a button block
    d. The button converts the API call from asynchronous to synchronous
    Answer: b
    Explanation: Every interaction reruns the entire script from the top (the same rule from Activity 4). If the API call sat at the top level instead of behind a button, moving the smoothing slider elsewhere in the app would trigger an API call every time.

14. While building Activity 7, one generated paragraph called 2014-12-25 (z = -3.93) "the most significant drop" when 2015-01-27 (z = -4.75) is deeper. Which fact-check item catches this?
    a. Every number in the paragraph appears in the facts block
    b. No flagged date is omitted
    c. Superlatives are correct: if it says "the largest drop," that date must really have the most extreme z-score in the facts block
    d. No causal claim is made that the data does not support
    Answer: c
    Explanation: This is one of two failure modes observed while building this activity, alongside a separate draft that silently omitted 2014-09-01 entirely. Both numbers, -3.93 and -4.75, are correct and present in the facts block; the error is which date the paragraph called the largest.

## Reflection

Answer in a few sentences each. There is no single correct answer for these three.

1. What is one thing from today that clicked for you (a moment where something finally made sense)?

2. What is one thing that is still unclear, that you would want explained again?

3. Of every chart you built today, which one would you put in front of a business audience, and why?
