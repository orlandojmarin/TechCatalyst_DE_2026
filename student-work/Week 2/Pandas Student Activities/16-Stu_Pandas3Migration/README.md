# What Changed in Pandas 3.0

Your `pyproject.toml` pins `pandas>=3.0`. Pandas 3.0 (released January 2026) changed a few defaults that tutorials, Stack Overflow answers, and older course material written before 2026 will get wrong. This activity does not build anything; it makes you observe the new defaults directly so you recognize them later.

## Instructions

Using the [starter file](Unsolved/pandas3_migration.ipynb), complete the following steps. Each one builds a tiny DataFrame from scratch, so there is no dataset to load.

1. Build a small DataFrame with a text column and a numeric column, for example `pd.DataFrame({"claim_type": ["Auto", "Home", "Auto"], "amount": [500, 1200, 300]})`. Check `df.dtypes`. In pandas 3.0, `claim_type` infers to a dedicated `str` dtype, not the old `object` dtype you may see in older tutorials. Write a markdown cell explaining what you observed.

2. Try a **chained assignment**: something like `df[df["claim_type"] == "Auto"]["amount"] = 0`. Run it. Pandas 3.0 raises a `ChainedAssignmentError` warning that names the exact fix, and the message tells you the assignment did not take effect. Check `df` afterward and confirm it is unchanged. Copy-on-Write means every subset now behaves like an independent copy, so chained assignment can never update the original.

3. Now do the same update the correct way, using `df.loc[df["claim_type"] == "Auto", "amount"] = 0`. Confirm this time that `df` did change.

4. Create a small date column from strings, for example `pd.to_datetime(["2025-03-01 10:15:00", "2025-03-02 08:00:00"])`. Check the dtype with `.dtype`. In pandas 3.0 the default resolution for string-parsed datetimes is microseconds (`datetime64[us]`), not nanoseconds (`datetime64[ns]`) like older pandas versions. This matters if you ever cast a datetime column to an integer.

## Challenge

Look up one more pandas 3.0 change that was not covered here (the [pandas 3.0 release notes](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html) are the authoritative source). Write two or three sentences in a markdown cell explaining what changed and why it matters for someone still writing code from a 2023-era tutorial.

## Hint

* None of these are things you did "wrong." They are default-behavior changes between pandas versions. The skill here is learning to notice when a version boundary might explain surprising behavior, instead of assuming your code is broken.
* If you get an unexpected `SettingWithCopyWarning` in older pandas material you find online, that warning was removed in pandas 3.0. It does not mean copy-on-write problems disappeared, it means pandas now always behaves safely instead of warning you.

## References

Pandas 3.0.0 release notes, `https://pandas.pydata.org/docs/whatsnew/v3.0.0.html`. No external dataset; all data is created inline in the notebook.
