# Terminal Reference: Linux CLI for Data Engineers

**Use case:** Extra practice before or after the Day 1 guided terminal activities  
**Primary tools:** Linux terminal and VS Code integrated terminal  
**Reference source date:** 2026-06-28

This reference adapts the 2025 terminal walkthrough for the 2026 classroom. Use it from a Linux terminal. If you are in VS Code, open the integrated terminal with ``Ctrl+` ``.

## Why Terminal in 2026?

The terminal is still central to data engineering because many real systems are operated through text commands:

- Cloud storage and compute services expose command-line interfaces.
- Containers, CI/CD runners, and servers often have no graphical interface.
- Logs, config files, credentials, and environment variables are easiest to inspect from a shell.
- Repeated command sequences can become scripts, scheduled jobs, or automated checks.
- AI can suggest commands, but you still need to know what those commands do before running them.

Think of the terminal as a control room. You can inspect data, move files, check jobs, debug failures, and turn repeatable work into automation.

## Terminal Options You May Encounter

| Environment | Common terminal | Practical note |
| :--- | :--- | :--- |
| Windows | Windows Terminal with PowerShell, Command Prompt, or Ubuntu through Windows Subsystem for Linux | Check the active profile before copying commands because PowerShell and Bash syntax differ |
| macOS | Terminal or iTerm2, usually with Zsh | Many commands look familiar, but some flags differ from GNU/Linux |
| Linux and Ubuntu | GNOME Terminal, VS Code integrated terminal, Bash, or Zsh | Best match for many servers, containers, and cloud shell environments |
| Cloud | AWS CloudShell, Google Cloud Shell, Azure Cloud Shell | Good for cloud tasks when credentials and CLIs are preconfigured, but project, region, storage, and permissions still matter |

The professional habit is simple: identify the terminal, identify the shell, then run commands with intention.

## Data Engineer Terminal Use-Case Map

| Use case | Why it matters | Common commands |
| :--- | :--- | :--- |
| Inspect a new data drop | Before writing Python, confirm what arrived | `ls -lh`, `du -sh`, `find`, `head` |
| Estimate data shape | Quickly count files, rows, columns, and unique values | `wc -l`, `cut`, `sort`, `uniq`, `awk` |
| Debug a failed pipeline | Find the first useful clue in logs | `grep`, `tail`, `less`, `sort`, `uniq -c` |
| Build repeatable checks | Save manual commands as scripts | Bash scripts, variables, redirection |
| Prepare automation | Convert "I did this once" into "run this every time" | `bash`, `chmod`, cron syntax |
| Collaborate safely | Keep changes reviewable and recoverable | `git status`, `git switch`, `git pull`, `git push` |

## Terminal for EDA and Data Analysis

Terminal EDA is not a replacement for pandas, SQL, or notebooks. It is the fast first pass before you choose a heavier tool.

Use terminal EDA when you need to answer questions like:

- Did the file arrive?
- Is the file empty?
- How many records are there?
- What columns exist?
- Are there obvious errors or missing values?
- Which values appear most often?
- Is the log failure repeated or isolated?

Example pattern:

```bash
head -n 5 data/orders_sample.csv
wc -l data/orders_sample.csv
cut -d',' -f2 data/orders_sample.csv | tail -n +2 | sort | uniq -c
grep -i "error" logs/pipeline.log | sort | uniq -c | sort -rn
```

## Terminal for Data Engineering Operations

Data engineering work often begins when something moved, failed, changed, or needs to run again. The terminal helps you answer operational questions quickly:

| Operational question | Command pattern |
| :--- | :--- |
| What changed recently? | `find . -mtime -1 -type f` |
| Which file is largest? | `du -sh * | sort -rh | head` |
| Is the job still writing logs? | `tail -f logs/pipeline.log` |
| What failed most often? | `grep -i error logs/pipeline.log | sort | uniq -c | sort -rn` |
| Can I rerun this check tomorrow? | Save commands in a `.sh` file |

## 1. Navigate Your Workspace

Core commands:

- `pwd`: print the current working directory.
- `mkdir`: create a directory.
- `cd`: change directories.
- `ls`: list directory contents.

```bash
mkdir tech
cd tech
pwd
cd ..
pwd
```

Useful variants:

```bash
ls
ls -a
ls -lh
ls -R
```

## 2. Inspect Files

```bash
head -n 5 sales.csv
tail -n 5 sales.csv
less shakespeare.txt
```

Press `q` to quit `less`.

Use `cat` only for small files you can comfortably read on one screen. For larger files, prefer `head`, `tail`, or `less`.

## 3. Write Small Notes, Not Datasets

```bash
echo "first run" > run_history.log
echo "second run" >> run_history.log
cat run_history.log
```

Use `>` when you want to overwrite a small text file. Use `>>` when you want to append. Do not hand-build analysis datasets with `echo` or `cat`; use provided files, scripts, downloads, APIs, or real data exports.

## 4. Find Files and Read File Contents

Use `find` when you are looking for files.

```bash
find . -type f
find . -type f -name "*.txt"
find . -type f -name "sh*"
```

Use `less`, `head`, and `tail` when you want to inspect file contents.

```bash
head -n 5 sales.csv
tail -n 5 sales.csv
less shakespeare.txt
```

Press `q` to quit `less`.

## 5. Count Lines, Words, and Bytes

`wc` means word count, but it can count lines and bytes too.

```bash
wc sales.csv
wc -l sales.csv
wc -w shakespeare.txt
```

Data engineers often use `wc -l` to check whether a file has the expected number of records.

## 6. Extract Columns From CSV Files

Use the provided `sales.csv` file.

```bash
cut -d',' -f1 sales.csv
cut -d',' -f1-2 sales.csv
cut -d',' -f1,3 sales.csv
```

The `-d` flag sets the delimiter. The `-f` flag chooses fields.

## 7. Compose Commands With Pipes

A pipe sends the output of one command into the next command.

```bash
cut -d',' -f1 sales.csv
cut -d',' -f1 sales.csv | tail -n +2
cut -d',' -f1 sales.csv | tail -n +2 | sort
cut -d',' -f1 sales.csv | tail -n +2 | sort | uniq
cut -d',' -f1 sales.csv | tail -n +2 | sort | uniq | wc -l
```

This is the same mental model as a data pipeline: each stage transforms the stream before handing it to the next stage.

## 8. Search Inside Files With `grep`

Use the provided `shakespeare.txt` file for text search practice.

Search examples:

```bash
grep "beauty" shakespeare.txt
grep -i "beauty" shakespeare.txt
grep -ic "time" shakespeare.txt
```

Use `grep` for text inside files. Use `find` for file paths.

## 9. Filter Structured Text With `awk`

`awk` can filter rows based on field values.

```bash
awk -F',' 'NR > 1' sales.csv
awk -F',' 'NR > 1 && $3 > 300' sales.csv
awk -F',' 'NR > 1 && $3 > 300' sales.csv | wc -l
```

In these examples, `-F','` says the file is comma-delimited, `NR > 1` skips the header row, and `$3` means the third column.

## 10. Copy, Move, Rename, and Delete

```bash
mkdir backup archive
cp sales.csv backup/
cp sales.csv backup/sales_backup.csv
mv backup/sales.csv archive/
mv archive/sales.csv archive/sales_archived.csv
```

Deletion has no easy undo:

```bash
rm sample.txt
```

Safety habits:

- Run `pwd` before deleting.
- Use `ls` to inspect the target before deleting.
- Prefer deleting one known file at a time while learning.
- Do not run `rm -r` unless you can explain exactly what it will remove.

## 11. Practice Pipeline

Find the top 2 sales rows by revenue and save them:

```bash
awk -F',' 'NR > 1' sales.csv | sort -t',' -k3 -nr | head -n 2 > top_revenue.csv
cat top_revenue.csv
```

Expected output:

```text
Lina,5,700
Mina,3,450
```

## 12. Tiny Bash Script for Repeatable Checks

When you run the same checks repeatedly, put them in a script.

Create a file named `summarize_sales.sh` in VS Code, then add this content:

```bash
echo "Run date: $(date)"
echo "CSV lines:"
wc -l sales.csv
echo "Unique names:"
cut -d',' -f1 sales.csv | tail -n +2 | sort | uniq | wc -l
echo "Top revenue rows:"
awk -F',' 'NR > 1' sales.csv | sort -t',' -k3 -nr | head -n 2
```

Run it:

```bash
bash summarize_sales.sh
```

Why this matters: a script is easier to review, rerun, schedule, and debug than a set of commands remembered from chat or terminal history.

## Quick Self-Check

Try these without looking at the commands above:

1. Count how many lines are in `sales.csv`.
2. Print only the `name` column, without the header.
3. Count unique names.
4. Find all lines in `shakespeare.txt` that contain `beauty`, regardless of case.
5. Save the top revenue row to `best_sale.csv`.
6. Write a 4-line Bash script that prints the date, row count, unique names, and top revenue row.
