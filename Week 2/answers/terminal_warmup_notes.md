# Terminal Warm-Up Notes

## Folder Observation

- I see 5 items: an `images` folder, an `operations_playground` folder, `sales.csv` (392 bytes), `shakespeare.txt` (93K), and `terminal.md` (8.5K). The shakespeare file is by far the largest.

## CSV Preview

- Columns: Name, Count, Revenue
- One thing I notice in the first rows: the data starts with Andrew having 9 count and 58 revenue, and values vary quite a bit across people.
- One thing I notice in the last rows: names repeat (Madison, Phil, Sally appear again), so the same person can have multiple rows. Also the last line has no trailing newline.

## Row Count

- Total lines: 29
- Data rows: 28
- Why the numbers differ: the first line is the header row (Name, Count, Revenue), so actual data rows = total lines minus 1.

## Unique Names

- Command: `cut -d',' -f1 sales.csv | tail -n +2 | sort | uniq | wc -l`
- Answer: 16 unique names
- Why `sort` comes before `uniq`: `uniq` only removes adjacent duplicates. Without sorting first, repeated names that aren't next to each other would each be counted separately.

## Search Practice

- One word I searched: "fortune"
- Command: `grep -in "fortune" shakespeare.txt | head -n 5`
- What the result tells me: "fortune" appears in multiple sonnets, and the `-n` flag shows the exact line numbers (204, 367, 425, 472, 549) so I could jump directly to those locations.

## Pair Discussion Takeaway

1. The `cut | sort | uniq | wc -l` pipeline felt like data analysis. It's essentially a `GROUP BY` and count in SQL, just done with pipes.
2. `grep` on logs or large text files felt like operations/debugging. You're searching for specific patterns to triage an issue.
3. If I had to check this folder every morning, I'd save the `wc -l` command to confirm expected row counts haven't changed (a quick data quality check).
4. Before running a command that changes files, you should inspect with `ls`, `cat`, or `head` first to confirm you're targeting the right file and understand its current state.
