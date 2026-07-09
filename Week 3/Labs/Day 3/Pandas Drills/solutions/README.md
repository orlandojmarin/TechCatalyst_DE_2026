# Pandas Drills Solutions

This folder contains instructor reference solutions for the Week 3 Day 3 Pandas Drills notebooks.

## Teaching Approach

These notebooks should model the simplest correct answer first. When students ask whether there is another way, treat that as a feature of pandas, not a problem. The goal is to help them learn the pattern behind the code:

1. Start with the plain solution that matches the prompt.
2. Ask what pandas object is being created or changed: Series, DataFrame, column, row filter, group, or joined table.
3. Show one alternate approach only if it reinforces the same idea.
4. Name the trade-off in plain language: readable, compact, explicit, or useful later.

Do not show every possible approach at once. For first-time learners, one main path plus one optional alternate path is usually enough.

## Ways To Slice The Pie

Use these as instructor prompts when students finish early or ask "could I also do it this way?"

| Activity | Main pattern | Simple answer to teach first | Optional alternate if there is time |
|---|---|---|---|
| Activity 2 | Filter and join | Boolean masks, `.query()`, `pd.merge()` | Ask students to write the SQL twin for the same pandas line. |
| Activity 3 | Profile and clean | `isna().sum()`, `pd.DataFrame({...})`, `dropna()` | Show `pd.concat(..., axis=1)` or `to_frame()` to combine Series. |
| Activity 4 | Select, filter, summarize | Select columns, filter rows, add one column, then `groupby()` | Compare `groupby().agg({...})` with doing one metric at a time. |
| Activity 5 | Time-series groupby | Drop unneeded columns, set a datetime index, then group | Compare grouped Series output with `as_index=False` DataFrame output. |
| Activity 6 | Find an extreme row | Filter, sort descending, then `.iloc[0]` | Show `.idxmax()` as a faster lookup after they understand sorting. |
| Activity 7 | Clean text columns | Rename, strip, title-case, convert numeric, write CSV | Show one-column cleanup first, then loop across string columns. |
| Activity 8 | Summary tables | `nunique()`, `min()`, `max()`, `value_counts()` | Build the one-row summary with a dictionary or with a list of dictionaries. |
| Activity 9 | Stack and join | `pd.concat()` for stacking, `pd.merge()` for matching | Draw the SQL idea: `UNION ALL` for concat, `JOIN` for merge. |
| Activity 10 | Duplicate checks | `duplicated()`, `drop_duplicates()`, then left join | Ask which duplicate rule is safe for claims versus lookup tables. |
| Activity 11 | Reshape | `pivot_table()`, `crosstab()`, `melt()` | Ask which output is best for humans and which is best for pandas. |
| Activity 12 | Time signals | `rolling()`, `shift()`, `pct_change()` | Change the window size and ask how the signal changes. |
| Activity 13 | Safe assignment | `.loc[row_mask, column] = value` and `.copy()` | Contrast changing the original DataFrame with creating a separate work queue. |

## Instructor Language

Useful phrasing:

- "This is the path I would teach first because it is easiest to read."
- "Pandas often has more than one correct answer. The question is which one communicates your intent."
- "If your answer creates the same DataFrame and you can explain it, it is probably valid."
- "Optimization comes later. First we want a solution we can trust and explain."

| Activity | Solution notebook |
|---|---|
| Activity 2: Pandas to SQL Bridge | `Activity_2_Pandas_to_SQL_Solutions.ipynb` |
| Activity 3: Pandas Data Cleaning | `Activity_3_Pandas_Data_Cleaning_Solutions.ipynb` |
| Activity 4: Crowdfunding Cleanup | `Activity_4_Crowdfunding_Cleanup_Solutions.ipynb` |
| Activity 5: Groupby Time Series | `Activity_5_Groupby_Time_Series_Solutions.ipynb` |
| Activity 6: Search For The Worst | `Activity_6_Search_For_The_Worst_Solutions.ipynb` |
| Activity 7: Comic Books CSV Cleanup | `Activity_7_Comic_Books_CSV_Cleanup_Solutions.ipynb` |
| Activity 8: Comic Books Summary | `Activity_8_Comic_Books_Summary_Solutions.ipynb` |
| Activity 9: Concat DataFrames | `Activity_9_Concat_Dataframes_Solutions.ipynb` |
| Activity 10: Duplicate and Key Quality Clinic | `Activity_10_Duplicate_Key_Quality_Solutions.ipynb` |
| Activity 11: Pivot, Crosstab, and Melt Review | `Activity_11_Pivot_Crosstab_Melt_Solutions.ipynb` |
| Activity 12: Rolling Windows and Time-Series Signals | `Activity_12_Rolling_Window_Signals_Solutions.ipynb` |
| Activity 13: Pandas 3 Safe Assignment | `Activity_13_Pandas3_Safe_Assignment_Solutions.ipynb` |

The solution notebooks keep the student drill notebooks unchanged.
