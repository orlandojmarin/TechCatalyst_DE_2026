# Activity 3: Bash Automation And Cron Reading

**Module:** Week 2 Day 1, Linux CLI and Git Collaboration  
**Estimated Time:** 45 minutes  
**Difficulty:** Intermediate  
**Format:** Pairs  
**Prerequisites:** Activity 1 or Activity 2

## Objective

In this activity, you will turn repeated terminal checks into a reusable Bash script, then read cron schedules that could run a script later.

## How This Activity Is Structured

This activity has three practice tiers so you are never staring at a blank file, and never handed the whole answer either.

| Part | Mode | What you do |
| :--- | :--- | :--- |
| Part A | Guided build | We write the first block of the script together. You type it, run it, and see the output. |
| Part B | On your own | You add the data and log metrics. Try it first. The answers are revealed after you attempt them. |
| Part C | Challenge | You add error-pattern counts, top errors, and a safety guardrail. Your instructor shows the answers after class. |
| Part D | Read cron | One schedule is explained for you, then you explain the rest. |
| Part E | Reflect | You explain the script in your own words. |

Do not open the instructor solution script. Use earlier activities, the hints at the bottom, and your notes.

## Why This Matters

Typing a command once is exploration. Saving a checked sequence in a script is operations work.

A data engineer might use a script to confirm required input files exist, count rows before loading data, scan logs for common errors, print a simple pass or fail result, and produce output that can be saved in a runbook or scheduled job.

Cron is one way to schedule commands on Linux systems. Today you will read cron expressions and explain logging behavior. You do not need to install, start, or edit the cron service.

## Setup

From `Week 2/Labs/Day 1`, move into the provided operations folder:

```bash
cd "Terminal Reference/operations_playground"
pwd
ls
```

Copy the starter script:

```bash
cp ../../starter/summarize_hunt_starter.sh summarize_hunt.sh
```

Open `summarize_hunt.sh` in VS Code. Read the top of the file:

```bash
sed -n '1,20p' summarize_hunt.sh
```

The starter already defines three path variables and sets a counter. You will fill in the `TODO` blocks below them.

| Script idea | What it means |
| :--- | :--- |
| `ORDERS_FILE="..."` | A variable that stores a path so you do not retype it |
| `LOG_FILE="..."` | Another reusable path |
| `SCRIPT_FILE="..."` | Path to the ETL script you check for |
| `missing_count=0` | A counter for missing files, starts at zero |
| `set -euo pipefail` | Safety setting: stop the script on most errors instead of continuing blindly |

## Part A: Guided Build, The File-Check Block

Goal: loop over the three files and print `FOUND` or `MISSING` for each, then print a single `PASS` or `FAIL` line. A real ingestion job checks its inputs exist before doing any work. You are writing that guard.

**Step 1.** Replace the first `TODO` (the file loop) with this code. Type it, do not paste blindly, so you read each line:

```bash
for file in "$ORDERS_FILE" "$LOG_FILE" "$SCRIPT_FILE"; do
  if [[ -f "$file" ]]; then
    echo "FOUND $file"
  else
    echo "MISSING $file"
    missing_count=$((missing_count + 1))
  fi
done
```

What each line does:

| Line | Purpose |
| :--- | :--- |
| `for file in ...; do` | Repeat the same check for each path, one at a time |
| `if [[ -f "$file" ]]` | `-f` is true when the file exists and is a regular file |
| `echo "FOUND $file"` | Readable message when the file is there |
| `missing_count=$((missing_count + 1))` | Arithmetic: add one to the counter when a file is missing |
| `done` | End of the loop |

**Step 2.** Replace the second `TODO` (the pass or fail line) with this:

```bash
if [[ "$missing_count" -eq 0 ]]; then
  echo "Required file check: PASS"
else
  echo "Required file check: FAIL, missing files: $missing_count"
fi
```

`-eq 0` means "equals zero." If nothing was missing, the check passes.

**Step 3.** Run the script:

```bash
bash summarize_hunt.sh
```

You should see (the metrics below `PASS` are still blank for now):

```text
Run date: ...

Checking required files:
FOUND data/orders_sample.csv
FOUND logs/pipeline.log
FOUND scripts/run_etl.sh

Required file check: PASS
```

This is why it matters: you just turned five separate `ls` checks into one reviewable, rerunnable guard. If a file is ever missing, the script tells you in one line instead of failing silently halfway through a load.

**Checkpoint:** do not continue until your script prints `Required file check: PASS`.

## Part B: On Your Own, Add Data And Log Metrics

Now you complete the next three `TODO` sections yourself. Each one reuses a pipeline you already built in Activity 1 or Activity 2. Try each one, run the script, and confirm your numbers match.

Complete these three metrics:

1. **Order rows**, not counting the header.
2. **Unique stores**, the count of distinct store codes in column 2.
3. **Error lines**, counting case-insensitively.

When this section is correct, running the script prints:

```text
Order rows: 15
Unique stores: 5
Error lines: 10
```

Attempt all three before asking for help. Your instructor will reveal the exact commands and explain them after you try. The answers live in the instructor answer key, not in your handout.

## Part C: Challenge, Patterns, Top Errors, And A Guardrail

This is the after-class challenge tier. Attempt as much as you can. Your instructor will show the answers and explanations after class.

Complete these:

1. **Error pattern counts.** Loop over these three patterns and print the count of each one in the log:
   - `connection timeout`
   - `schema mismatch`
   - `auth token`
2. **Top 3 error messages.** Print the three most common error messages with their counts. Reuse the `sed` pipeline from Activity 1 Part 5.
3. **Guardrail.** Make the script also print `FAIL` if `data/orders_sample.csv` has fewer than 10 data rows, otherwise `PASS`.

When the challenge is correct, the script prints:

```text
Error pattern counts:
connection timeout: 4
schema mismatch: 3
auth token: 2

Top errors:
   4 connection timeout to source api
   3 schema mismatch in column amount
   2 auth token expired
```

## Part D: Read Cron Schedules

Cron describes when a command should run. The format is:

```text
minute hour day-of-month month day-of-week command
```

One schedule is done for you as a model. Open the practice file:

```bash
sed -n '1,40p' ../../starter/cron_schedule_practice.txt
```

**Worked example (schedule 1):**

```cron
0 6 * * * bash /home/student/check_orders.sh >> /home/student/check_orders.log 2>&1
```

- Plain English: run the order check every day at 6:00 AM.
- Output file: standard output is appended to `/home/student/check_orders.log`.
- `2>&1`: send error output to the same place as standard output, so the log captures both.
- Logging note: the job uses an absolute path and appends to a log, which makes scheduled runs easy to inspect later.

**Now you do schedules 2, 3, and 4.** For each one write:

- Plain-English meaning.
- What file receives standard output.
- What `2>&1` does.
- One risk or logging note.

Answers are revealed after you attempt them.

## Part E: Explain The Script

Create `automation_notes.md` with:

```markdown
# Automation Notes

## What The Script Checks

## Why Variables Help

## Why A Loop Helps

## Why The Script Prints PASS Or FAIL

## One Thing I Would Add Before Scheduling
```

## Success Criteria

- `summarize_hunt.sh` runs from inside `operations_playground` and prints `Required file check: PASS` (Part A).
- The script prints correct order rows, unique stores, and error lines (Part B).
- You attempted the error pattern counts, top errors, and guardrail (Part C).
- The script uses at least 2 variables, one `for` loop, and one `if` condition.
- The output is readable by another person.
- `automation_notes.md` explains the script in your own words.
- You explained cron schedules 2, 3, and 4 in plain English (Part D).
- You can explain why scheduled jobs should write logs.

## Hints

<details>
<summary>Hint 1: Part B, order rows</summary>

If `wc -l` counts the header, subtract one data row with arithmetic expansion:

```bash
echo "$(($(wc -l < "$ORDERS_FILE") - 1))"
```

</details>

<details>
<summary>Hint 2: Part B, unique stores and error lines</summary>

Unique stores reuses your Activity 1 store pipeline: `tail -n +2`, then `cut -d',' -f2`, then `sort`, then `uniq`, then `wc -l`.

Error lines use `grep -ic error "$LOG_FILE"`. The `-c` counts matching lines and `-i` ignores case.

</details>

<details>
<summary>Hint 3: Part C, looping over patterns</summary>

A loop can count several search patterns with the same logic:

```bash
for pattern in "connection timeout" "schema mismatch" "auth token"; do
  count=$(grep -ic "$pattern" "$LOG_FILE")
  echo "$pattern: $count"
done
```

</details>

<details>
<summary>Hint 4: Cron logging</summary>

`>> file.log` appends standard output. `2>&1` sends errors to the same place as standard output, so one log captures both.

</details>

## Stretch Goals

- Modify `summarize_hunt.sh` so it also writes results to `hunt_summary.txt`.
- Add a short comment above each major section of the script.
- Draft a cron line that would run your script every weekday at 7:30 AM and append output to `hunt_summary.log`.

> Instructor notes for this activity are in `Week 2/Instructor Notes/Day 1 - Instructor Guide.md`.
