# Activity 1: Guided Mini EDA Sprint

**Module:** Week 2 Day 1, Linux CLI and Git Collaboration  
**Estimated Time:** 50 minutes  
**Difficulty:** Beginner to intermediate  
**Format:** Pairs  
**Prerequisites:** Activity 0 or equivalent terminal basics

## Objective

In this activity, you will use terminal commands to profile a small retail operations folder before opening Python or a notebook.

## Why This Matters

Data engineers often receive a folder before they receive a clear explanation. The first job is to inspect reality:

- What files exist?
- How large are they?
- What columns and rows are present?
- What do the logs say?
- What question should we investigate next?

This is exploratory data analysis, but at terminal speed.

## Setup

From `Week 2/Labs/Day 1`, run:

```bash
cd "Terminal Reference/operations_playground"
pwd
ls
```

You should see:

```text
data
logs
notes
scripts
```

Create your notes file:

```bash
touch eda_notes.md
```

## Part 1: Map The Folder

Run:

```bash
find . -maxdepth 2 -type f
```

What this means:

- `find` searches for paths.
- `.` means start from the current folder.
- `-maxdepth 2` keeps the search near the top of the folder.
- `-type f` lists files, not directories.

Now list folder sizes:

```bash
du -sh *
```

Record in `eda_notes.md`:

```markdown
## File Profile

- Files I found:
- Largest direct folder:
- One file I want to inspect:
```

## Part 2: Inspect The Orders CSV

Run:

```bash
head -n 5 data/orders_sample.csv
tail -n 5 data/orders_sample.csv
wc -l data/orders_sample.csv
```

What to notice:

- `head` shows the header and first rows.
- `tail` checks the end of the file.
- `wc -l` counts total lines, including the header.

Expected count:

```text
16 data/orders_sample.csv
```

That means:

```text
15 data rows
```

Record:

```markdown
## Orders Profile

- Total lines:
- Data rows:
- Columns:
- One row-level observation:
```

## Part 3: Analyze One Column With A Pipeline

Run the pipeline one stage at a time:

```bash
tail -n +2 data/orders_sample.csv
```

```bash
tail -n +2 data/orders_sample.csv | cut -d',' -f2
```

```bash
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort
```

```bash
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort | uniq -c
```

Now count unique stores:

```bash
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort | uniq | wc -l
```

Record:

```markdown
## Store Profile

- Unique store count:
- Store codes observed:
- Most common store count pattern:
```

## Part 4: Use `awk` For A Simple Business Question

Run:

```bash
awk -F',' 'NR > 1 && $3 >= 100 {print}' data/orders_sample.csv
```

What this means:

- `awk` filters structured text.
- `-F','` says fields are separated by commas.
- `NR > 1` skips the header.
- `$3 >= 100` keeps rows where the third column is at least 100.

Now count those rows:

```bash
awk -F',' 'NR > 1 && $3 >= 100 {print}' data/orders_sample.csv | wc -l
```

Record:

```markdown
## Amount Check

- Orders at or above 100:
- Why this might matter to an analyst:
```

## Part 5: Triage The Log

Preview the log:

```bash
head -n 5 logs/pipeline.log
tail -n 5 logs/pipeline.log
```

Search for errors:

```bash
grep -i "error" logs/pipeline.log
```

Count error lines:

```bash
grep -ic "error" logs/pipeline.log
```

Group the most common error messages:

```bash
grep -i "error" logs/pipeline.log | sed -E 's/^[^ ]+ +(ERROR|error) +//' | sort | uniq -c | sort -rn | head -3
```

What this pipeline does:

| Stage | Purpose |
| :--- | :--- |
| `grep -i "error"` | Keep log lines with errors |
| `sed -E 's/^[^ ]+ +(ERROR\|error) +//'` | Remove timestamp and level |
| `sort` | Put matching messages together |
| `uniq -c` | Count repeated messages |
| `sort -rn` | Sort counts from high to low |
| `head -3` | Keep the top 3 |

Record:

```markdown
## Log Profile

- Error line count:
- Most common error:
- Last log timestamp:
- Did the job appear to finish? Evidence:
```

## Part 6: Ask Better Follow-Up Questions

Add this final section:

```markdown
## Questions I Would Ask Next

- Data question:
- Operations question:
- Question for the business stakeholder:
```

Examples:

- Data question: Why are some regions represented more than others?
- Operations question: Why did the source API time out four times?
- Business question: Which stores or regions need priority review?

## Deliverable

Submit `eda_notes.md` with these sections:

```markdown
# Mini EDA Notes

## File Profile

## Orders Profile

## Store Profile

## Amount Check

## Log Profile

## Questions I Would Ask Next
```

## Success Criteria

- `eda_notes.md` exists inside `operations_playground`.
- Your pair used at least 4 command pipelines.
- Your notes include row counts, unique store counts, and log error counts.
- Your notes include one data question, one operations question, and one business question.
- Your pair can explain one pipeline stage by stage.

## Hints

<details>
<summary>Hint 1: Difference between `find` and `grep`</summary>

Use `find` when searching for file paths. Use `grep` when searching inside file contents.

</details>

<details>
<summary>Hint 2: Why skip the header?</summary>

The header is metadata, not a data row. Use `tail -n +2` when counting or grouping CSV data values.

</details>

<details>
<summary>Hint 3: Why sort before `uniq`?</summary>

`uniq` only combines repeated lines when they are next to each other. Sorting first puts matching values together.

</details>

## Stretch Goals

- Count how many orders appear per region.
- Show the top 2 order amounts with `sort`.
- Add one command that would help an operations team decide whether to rerun the pipeline.

> Instructor notes for this activity are in `Week 2/Instructor Notes/Day 1 - Instructor Guide.md`.
