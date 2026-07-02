# Instructor Demo: Linux Terminal For Data Engineers

**Module:** Week 2 Day 1, Linux CLI and Git Collaboration  
**Audience:** Beginning data engineering learners  
**Estimated Time:** 75 to 95 minutes across the day  
**Environment:** Linux terminal in VS Code  
**Required files:** `Week 2/Labs/Day 1/Terminal Reference/`

## Demo Purpose

Use this file before the student activities. The goal is to model how a data engineer thinks at the terminal before students try the commands themselves.

Teaching sequence:

1. Explain terminal options and why Ubuntu is the classroom target today.
2. Demo safe navigation and file inspection.
3. Demo quick CSV analysis with commands and pipes.
4. Demo text search and log triage.
5. Demo safe file changes using a copy.
6. Demo how repeated checks become a Bash script.
7. Demo cron schedule reading.
8. Connect the workflow back to Git collaboration.

## Instructor Setup

Open VS Code at the repository root, then open a terminal.

Run:

```bash
cd "Week 2/Labs/Day 1"
pwd
ls
```

Expected observation: you see the full day folder. That includes the activity files `Activity_0_Terminal_Warm_Up.md` through `Activity_5_Debrief_and_Stretch.md`, the `Group_Activity_Terminal_Operations_Decision_Brief.md`, this `Instructor_Demo.md`, `Reading_Terminal_for_Data_Engineers.md`, `README.md`, `Student_Resources.md`, and the `Terminal Reference`, `starter`, `solutions`, and `quiz` folders.

PAUSE: Ask students what the terminal gives us that a file browser does not. Listen for speed, repeatability, logs, remote systems, and automation.

## Demo 1: Terminal Options And Shell Awareness

Use this as a short speaking script before typing many commands.

```text
A terminal is the window. A shell is the command interpreter.
Windows Terminal can run PowerShell, Command Prompt, or Ubuntu through Windows Subsystem for Linux.
macOS Terminal usually runs Zsh.
Linux terminals often run Bash or Zsh.
Cloud shells run in the browser near cloud resources, often with cloud CLIs and credentials already configured.
Today we use Ubuntu-style Linux commands because they transfer well to servers, containers, cloud shells, and automation jobs.
```

Run:

```bash
echo "$SHELL"
pwd
```

Expected observation:

- Students see the active shell path.
- Students see the current working directory.

PAUSE: Ask, "Before copying a command from a tutorial, what should you check?" Expected answers: shell, current folder, target path, whether the command writes or deletes.

## Demo 2: Safe Navigation And File Inspection

Move into the reference folder:

```bash
cd "Terminal Reference"
pwd
ls
ls -lh
```

Explain:

- `pwd` answers "Where am I?"
- `ls` answers "What exists here?"
- `ls -lh` adds sizes and details.

Preview the CSV:

```bash
head -n 5 sales.csv
tail -n 5 sales.csv
wc -l sales.csv
```

Expected observation:

```text
29 sales.csv
```

Teaching point:

```text
29 total lines means 28 data rows because one line is the header.
```

PAUSE: Ask students why the header matters when counting records.

## Demo 3: Build A Pipeline One Stage At A Time

Run each command separately. Do not paste the final pipeline first.

```bash
cut -d',' -f1 sales.csv
```

Explain:

- `cut` extracts a field.
- `-d','` means comma-delimited.
- `-f1` means first field.

Now remove the header:

```bash
cut -d',' -f1 sales.csv | tail -n +2
```

Now sort:

```bash
cut -d',' -f1 sales.csv | tail -n +2 | sort
```

Now remove duplicates:

```bash
cut -d',' -f1 sales.csv | tail -n +2 | sort | uniq
```

Now count:

```bash
cut -d',' -f1 sales.csv | tail -n +2 | sort | uniq | wc -l
```

Expected observation:

- Students see that each command transforms the stream.
- Students see why `sort` comes before `uniq`.

PAUSE: Ask, "Which part of this pipeline is like an extract step? Which part is like a transform step?"

## Demo 4: Search Text With `grep`

Run:

```bash
grep -i "beauty" shakespeare.txt
grep -ic "time" shakespeare.txt
grep -in "fortune" shakespeare.txt | head -n 5
```

Explain:

- `grep` searches inside files.
- `-i` ignores case.
- `-c` counts matching lines.
- `-n` shows line numbers.
- `head` keeps the output readable.

PAUSE: Ask, "What is the difference between searching file names and searching inside files?" Expected answer: `find` searches paths, `grep` searches contents.

## Demo 5: Move From Reference Files To Operations Data

Run:

```bash
cd operations_playground
pwd
find . -maxdepth 2 -type f
du -sh *
```

Expected observation:

- Students see data, logs, notes, and scripts.
- `data/` is likely the largest direct folder.

Preview orders:

```bash
head -n 5 data/orders_sample.csv
tail -n 5 data/orders_sample.csv
wc -l data/orders_sample.csv
```

Expected observation:

```text
16 data/orders_sample.csv
```

Teaching point:

```text
16 total lines means 15 order records.
```

Count stores:

```bash
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort | uniq -c
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort | uniq | wc -l
```

Expected observation:

```text
5
```

PAUSE: Ask students what question a business stakeholder might ask after seeing store counts.

## Demo 6: Use `awk` For A Simple Filter

Run:

```bash
awk -F',' 'NR > 1 && $3 >= 100 {print}' data/orders_sample.csv
```

Then count:

```bash
awk -F',' 'NR > 1 && $3 >= 100 {print}' data/orders_sample.csv | wc -l
```

Explain:

- `awk` is useful when you need field-aware filtering.
- `NR > 1` skips the header.
- `$3 >= 100` checks the third column.

PAUSE: Ask, "When would you stop using terminal commands and move to Python or SQL?" Good answers include larger files, complex joins, statistical work, charting, and reusable business logic.

## Demo 7: Log Triage

Preview the log:

```bash
head -n 5 logs/pipeline.log
tail -n 5 logs/pipeline.log
```

Search errors:

```bash
grep -i "error" logs/pipeline.log
grep -ic "error" logs/pipeline.log
```

Expected observation:

```text
10
```

Search two patterns:

```bash
grep -Ein "timeout|schema" logs/pipeline.log
```

Group common errors:

```bash
grep -i "error" logs/pipeline.log | sed -E 's/^[^ ]+ +(ERROR|error) +//' | sort | uniq -c | sort -rn | head -3
```

Expected observation:

```text
4 connection timeout to source api
3 schema mismatch in column amount
2 auth token expired
```

PAUSE: Ask, "Does the final log line mean there was no problem?" Expected answer: no. A job can finish after retries or partial failures, so logs need interpretation.

## Demo 8: Safe File Changes With A Working Copy

Explain:

```text
Reading commands are safer than writing commands. When learning, make a copy before appending, moving, or renaming.
```

Run:

```bash
mkdir -p work
cp logs/pipeline.log work/pipeline_working.log
tail -1 logs/pipeline.log
tail -1 work/pipeline_working.log
```

Append only to the copy:

```bash
echo "demo completed by instructor" >> work/pipeline_working.log
tail -1 logs/pipeline.log
tail -1 work/pipeline_working.log
```

Expected observation:

- The original log still ends with `daily summary written`.
- The working copy ends with the new demo line.

PAUSE: Ask students why Activity 2 appends to a copy instead of the original evidence file.

## Demo 9: Turn Repeated Checks Into A Script (Activity 3 Part A only)

Activity 3 is now three tiers: Part A is a guided build, Part B is on their own, and Part C is a challenge. In this demo you model **only Part A** so students still have Part B and Part C to do themselves. Do not project the full solution or the Part B and C answers.

Return to the operations folder if needed:

```bash
pwd
```

Copy the starter and read the top:

```bash
cp ../../starter/summarize_hunt_starter.sh summarize_hunt_demo.sh
sed -n '1,30p' summarize_hunt_demo.sh
```

Point out the three path variables, the `missing_count=0` counter, and the `TODO (Part A)`, `TODO (Part B)`, and `TODO (Part C)` markers.

Model Part A live. Type the file-check loop and the pass or fail check into the demo script, the same code students will type:

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

```bash
if [[ "$missing_count" -eq 0 ]]; then
  echo "Required file check: PASS"
else
  echo "Required file check: FAIL, missing files: $missing_count"
fi
```

Run after completing Part A only:

```bash
bash summarize_hunt_demo.sh
```

Expected observation (Part A only, the metrics below are still blank):

```text
Checking required files:
FOUND data/orders_sample.csv
FOUND logs/pipeline.log
FOUND scripts/run_etl.sh

Required file check: PASS
```

Then say: "Part B, the order rows, unique stores, and error lines, is yours to complete. Part C, the error patterns, top errors, and guardrail, is the challenge. I am not going to show those answers now."

Instructor-only reference, do not project to the room: the full completed script is `solutions/Activity_3_summarize_hunt_solution.sh` and the per-task answers with explanations are in `solutions/Instructor_Answer_Key.md`. Reveal Part B after pairs attempt it. Reveal Part C after class.

If running the demo script from `operations_playground` fails, check:

```bash
pwd
ls data logs scripts
```

PAUSE: Ask, "What changed when commands became a script?" Expected answers: reusable, reviewable, easier to schedule, easier to debug, easier to hand to another engineer.

## Demo 10: Read Cron Schedules

Open the practice file:

```bash
sed -n '1,160p' ../../starter/cron_schedule_practice.txt
```

Explain cron format:

```text
minute hour day-of-month month day-of-week command
```

Read these examples aloud:

```cron
0 6 * * * bash /home/student/check_orders.sh >> /home/student/check_orders.log 2>&1
*/15 * * * * python /home/student/poll_api.py >> /home/student/poll_api.log 2>&1
30 2 1 * * bash /home/student/monthly_archive.sh >> /home/student/monthly_archive.log 2>&1
0 8 * * 1 bash /home/student/weekly_report.sh >> /home/student/weekly_report.log 2>&1
```

Teaching points:

- `*` means every value for that field.
- `*/15` in the minute field means every 15 minutes.
- `>>` appends output to a log.
- `2>&1` sends errors to the same log stream.
- Today students read cron. They do not need to start or edit the cron service.

PAUSE: Ask, "Which schedule fits a daily batch check? Which fits API polling?"

## Demo 11: Git Refresher Bridge

Use this script as a verbal bridge before Activity 4:

```text
The terminal is also how we collaborate safely.
The same habits apply: inspect first, make a focused change, check status, then commit.
Conflicts are not failures. They are places where Git needs human judgment.
```

Run in any Git repository:

```bash
git status
git branch
```

If you are in the course repo, do not make demo commits here. Use a disposable repository for the live conflict demo described in the instructor guide.

Make the working location explicit before Activity 4. This is the single biggest source of confusion today, because Activities 0 to 3 leave students inside the class repo clone. Model the step-out check on screen:

```bash
cd ~/Desktop
git status
```

Expected observation:

```text
fatal: not a git repository (or any of the parent directories): .git
```

Tell students plainly: that `fatal` message is the result you want here. It confirms the Desktop is not a repo, so the relay repo they clone next stays separate from the class repo. They run all relay `git` commands from the cloned relay folder, not from the class repo or `operations_playground`. Do a quick room-wide check that everyone sees this before the relay begins.

Key Git commands to review:

```bash
git switch main
git pull
git switch -c feature/my-change
git status
git add config.py
git commit -m "Update pipeline config"
git push -u origin feature/my-change
```

PAUSE: Ask, "Why do we resolve conflicts on the feature branch instead of making emergency edits on main?"

## Reset Notes

The demos may create these files inside `Terminal Reference/operations_playground`:

```text
work/pipeline_working.log
summarize_hunt_demo.sh
```

Before class, you can leave them in place as instructor artifacts or remove them manually after confirming you are in the correct folder.

Safety check before any cleanup:

```bash
pwd
ls
```

## Troubleshooting

| Symptom | Likely cause | Fast fix |
| :--- | :--- | :--- |
| `cd "Terminal Reference"` fails | You are not in `Week 2/Labs/Day 1` | Run `pwd`, then navigate back to the Day 1 folder |
| `sales.csv` is not found | You are in the wrong folder | Run `ls` and confirm you are inside `Terminal Reference` |
| `data/orders_sample.csv` is not found | You are not inside `operations_playground` | Run `cd "Terminal Reference/operations_playground"` from Day 1 |
| Store counts look wrong | The header row was counted | Add `tail -n +2` before `cut` |
| `uniq` does not combine duplicates | Values were not sorted first | Add `sort` before `uniq` |
| The script cannot find files | The script is being run from the wrong folder | Run it from inside `operations_playground` |

## Instructor Closing Message

Use this close before students start independent work:

```text
Today is not about memorizing flags. It is about learning a professional loop: inspect, narrow, count, search, explain, automate, and collaborate. If a command changes files, slow down and inspect first. If a command answers a question, write down both the command and the reasoning.
```
