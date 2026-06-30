# File I/O: Daily Claims

**Label: Core.** Reading and writing files is the foundation for all data work,
including the CSV drill next and the pandas work on Day 4.

In this drill you will read a text file of daily claim counts, total and count
them, compute the daily average, and write a summary file.

## Background

The intake system drops a plain text file, `Resources/daily_claims.txt`, with one
number per line: the count of claims received that day. You will read it, compute
a quick summary, and write the result to a new file.

## Instructions

Copy this drill folder (including `Resources/`) into your `student-work/week2/day2`
project, then run from the drill-folder root (the folder that contains
`Resources/`) so the relative paths resolve:

```bash
uv run python Unsolved/file_io.py
```

### Core

1. Use `pathlib.Path` to point at `Resources/daily_claims.txt`.
2. Open the file and iterate over its lines. Strip whitespace, skip blank lines,
   and convert each line to `int`.
3. Accumulate `total` and `day_count`, then compute `daily_average`
   (`round(total / day_count, 2)`).
4. Print the three values.
5. Open `claims_summary.txt` in write mode and write the three values, one per
   line.

### Stretch

6. Also track and report the busiest day (max) and quietest day (min).

## Expected Output

```text
Total claims: 1000
Days: 20
Daily average: 50.0
Wrote claims_summary.txt
```

And `claims_summary.txt` contains:

```text
Total claims: 1000
Days: 20
Daily average: 50.0
```

## Success Criteria

- The script reads the file with a `with open(...)` block.
- It writes `claims_summary.txt` with the three values.
- You can explain the difference between read mode and write mode (`"w"`).

## Hint

<details>
<summary>Reading lines gives you strings</summary>

Each line from a text file is a string, including a trailing newline. Use
`line.strip()` to clean it, then `int(line)` to do math.

</details>
