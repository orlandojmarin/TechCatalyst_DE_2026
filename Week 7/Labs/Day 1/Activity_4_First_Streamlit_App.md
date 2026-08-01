# Activity 4: Your First Streamlit App

**Module:** Week 7 Day 1
**Estimated Time:** 30 minutes
**Difficulty:** Beginner
**Format:** Individual
**Prerequisites:** Activity 0 complete (packages installed, `student-work/week7/day1/data/` populated)

## Objective

In this activity, you will complete a small Streamlit app that turns the NYC taxi CSV into a title, two metric tiles, a line chart, and a table, and you will observe how Streamlit reruns your script.

## Background

Every notebook you have used so far runs cell by cell, and you choose when a cell executes. A Streamlit app is different: it is a single Python script that Streamlit reads from top to bottom and turns into a web page. There are no callbacks to register and no event handlers to write. You just write plain Python, and functions like `st.title(...)` or `st.line_chart(...)` draw something on the page in the order they appear.

The one idea that trips up every beginner: Streamlit does not run your script once and then wait. It reruns the entire file from line 1 every time you interact with the page, for example clicking a button or opening an expander. If your script reads a CSV file at the top level, that read happens again on every single interaction, unless you tell Streamlit to cache it.

That is what `@st.cache_data` is for. It remembers the result of a function for a given set of arguments, so a rerun reuses the cached result instead of redoing the work. You will feel the difference directly in Step 4 below.

## Instructions

1. Copy the starter file into your work folder, if you have not already copied it as part of Activity 0:

   ```bash
   cp "Week 7/Labs/Day 1/starter/activity_4_first_app.py" student-work/week7/day1/
   ```

   Do not edit the file under `Week 7/Labs/Day 1/starter/` in place. Work only on the copy in `student-work/`.

2. Open `student-work/week7/day1/activity_4_first_app.py` in VS Code. Read the whole file before changing anything. The imports, `st.set_page_config`, the `@st.cache_data` decorator, and the path resolver block near the top are already done for you. There are three `# TODO` comments left to fill in:
   - the body of `load_taxi`
   - the two `st.metric` calls
   - the `st.line_chart` call

   Each `# TODO` comment tells you exactly what to write and what the result should look like. Replace the placeholder code with your own.

3. Run the app from the repository root:

   ```bash
   uv run streamlit run student-work/week7/day1/activity_4_first_app.py
   ```

   Streamlit opens the app at `http://localhost:8501` in your browser. Leave the terminal running: that process is your live server. To stop the app, go back to the terminal and press `Ctrl+C`.

4. Check your work against the expected output:

   ```text
   NYC taxi demand
   215 days, 2014-07-01 to 2015-01-31
   ```

   Two metric tiles ("Busiest day" and "Quietest day"), a line chart with a visible dip in late January 2015, and a collapsed "See the raw daily numbers" section that expands into a table.

## Experiment: Watch the Rerun Model

This is the part that makes the rerun model click instead of staying an abstract sentence in a reading. Do all four steps in order.

1. Near the top of your file, right after `daily = load_taxi(str(DATA))`, add:

   ```python
   st.write("script ran at", pd.Timestamp.now())
   ```

2. Save the file. Streamlit shows a "Rerun" prompt in the browser, or reruns automatically if you have that setting on. Look at the timestamp.

3. Click to open the "See the raw daily numbers" expander at the bottom of the page. Watch the timestamp at the top. It changes, even though all you did was open an expander. That is the whole idea: any interaction on the page reruns your entire script from the top, including the line that prints that timestamp.

4. Now comment out or delete the `@st.cache_data` line above `load_taxi`, save, and interact with the app again (open and close the expander a few times). Notice the app feels slower to respond. Without the cache, every rerun re-reads and re-resamples the whole CSV from scratch. With the cache, that expensive work only happens once, and reruns reuse the cached Series. Put `@st.cache_data` back before moving on.

## Success Criteria

- All three `# TODO` blanks are filled in and the placeholder return statement in `load_taxi` is gone.
- The app runs with `uv run streamlit run student-work/week7/day1/activity_4_first_app.py` and shows the exact line `215 days, 2014-07-01 to 2015-01-31`.
- Both metric tiles show a value and a date on hover.
- The line chart renders and the raw numbers table expands.
- You completed the rerun experiment: you saw the timestamp change on interaction, and you saw the app slow down without `@st.cache_data`, then restored the decorator.
