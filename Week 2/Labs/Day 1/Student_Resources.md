# Week 2 Day 1 Student Resources

## AI-Free Zone Reminder

Use these references to understand commands and official workflows. Do not use AI assistants to generate your commands, Git steps, scripts, conflict resolutions, or written answers for this lab.

## Core Documentation

| Resource | Date checked | Why it helps |
| :--- | :--- | :--- |
| [VS Code Integrated Terminal](https://code.visualstudio.com/docs/terminal/basics) | 2026-06-29 | Shows the terminal surface we will use inside VS Code |
| [Linux man pages](https://man7.org/linux/man-pages/) | 2026-06-29 | Authoritative reference for Linux commands and flags |
| [Windows Terminal documentation](https://learn.microsoft.com/en-us/windows/terminal/) | 2026-06-29 | Explains Windows terminal profiles such as PowerShell, Command Prompt, and Linux shells |
| [Apple Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac) | 2026-06-29 | Official macOS terminal reference |
| [AWS CloudShell User Guide](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html) | 2026-06-29 | Shows how a browser-based cloud shell supports cloud CLI work |
| [Google Cloud Shell documentation](https://cloud.google.com/shell/docs) | 2026-06-29 | Shows the browser-based shell model for Google Cloud |
| [Git switch documentation](https://git-scm.com/docs/git-switch) | 2026-06-29 | Official reference for creating and switching branches |
| [GitHub command-line merge conflict guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line) | 2026-06-29 | Official workflow for resolving pull request conflicts from the command line |

## Terminal Options

| Environment | Typical terminal | What to check before copying a command |
| :--- | :--- | :--- |
| Windows | Windows Terminal with PowerShell, Command Prompt, or Ubuntu through Windows Subsystem for Linux | Confirm the active shell profile because Bash and PowerShell syntax differ |
| macOS | Terminal or iTerm2, usually with Zsh | Confirm whether a command uses GNU/Linux flags that macOS tools may not support |
| Linux and Ubuntu | GNOME Terminal, VS Code integrated terminal, Bash, or Zsh | Confirm your current folder and the target files before running write or delete commands |
| Cloud shell | AWS CloudShell, Google Cloud Shell, Azure Cloud Shell | Confirm cloud project, account, region, storage persistence, and permissions |

## Quick Command Reference

```bash
# Where am I?
pwd

# List files with sizes
ls -lh

# Count files recursively, not directories
find . -type f | wc -l

# Show the largest direct child of the current directory
du -sh * | sort -rh | head -1

# Count lines in a file
wc -l data/orders_sample.csv

# Find hidden files
find . -name ".*" -type f

# Count pattern matches, case-insensitive
grep -ic "error" logs/pipeline.log

# Show the last line of a file
tail -1 logs/pipeline.log

# List data files by size
ls -lhS data/*

# Files modified in the last 24 hours
find . -mtime -1 -type f

# Count unique values in column 2 of a CSV, skipping the header
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort | uniq | wc -l

# Top 3 common error messages, counted
grep -i "error" logs/pipeline.log | sed -E 's/^[^ ]+ +(ERROR|error) +//' | sort | uniq -c | sort -rn | head -3
```

## `grep` and Pattern Search

Use `grep` to search inside files. Use `find` to search for file paths.

```bash
grep "ERROR" logs/pipeline.log
grep -i "error" logs/pipeline.log
grep -n "schema" logs/pipeline.log
grep -E "timeout|schema" logs/pipeline.log
grep -oi "error" logs/pipeline.log | wc -l
```

Useful flags:

| Flag | Meaning |
| :--- | :--- |
| `-i` | Ignore case |
| `-n` | Show line numbers |
| `-c` | Count matching lines |
| `-o` | Print only the matched text |
| `-E` | Use extended regular expressions |
| `-v` | Invert the match |

## Cron

Cron expression format:

```text
minute hour day-of-month month day-of-week command
```

Examples:

```cron
0 6 * * *      run every day at 6:00 AM
*/15 * * * *   run every 15 minutes
0 0 * * 1      run every Monday at midnight
0 8 1 * *      run at 8:00 AM on the first day of every month
```

Classroom note: many short-lived classroom terminals do not run a cron daemon. Today, focus on reading and writing cron expressions. Production scheduling returns in orchestration lessons.

Cron safety habits:

- Use absolute paths in scheduled commands.
- Append output to a log file with `>>`.
- Capture errors with `2>&1`.
- Keep scheduled scripts small, readable, and committed to Git.

## Git and GitHub

```bash
git status
git switch main
git pull
git switch -c feature/my-change
git add config.py
git commit -m "Update pipeline config"
git push -u origin feature/my-change
```

Conflict marker anatomy:

```python
<<<<<<< HEAD
fare_threshold = 50
=======
fare_threshold = 250
>>>>>>> main
```

Rule: read both sides, decide the final code, delete all marker lines, save, stage, commit, and push.

Working location for the Git relay: run the relay in a separate folder, not inside the class repo you cloned. Step out first and confirm you are not in a repo before cloning:

```bash
cd ~/Desktop
git status   # expect: fatal: not a git repository
```

That `fatal` message is the result you want. Clone your relay repo here, then run every relay `git` command from inside the cloned folder. Full steps are in Activity 4.

## Lab Deliverable Checklist

| Done | Deliverable |
| :--- | :--- |
| [ ] | `terminal_warmup_notes.md` includes guided command observations |
| [ ] | `eda_notes.md` includes file, store, amount, log, and follow-up question observations |
| [ ] | `cli_hunt.md` includes all 12 commands, answers, and explanations |
| [ ] | `summarize_hunt.sh` runs from inside `operations_playground` |
| [ ] | `automation_notes.md` explains variables, loops, pass or fail checks, and cron logging |
| [ ] | Cron schedule practice includes plain-English translations and logging notes |
| [ ] | Group decision brief includes recommendation, risks, assumptions, trade-off table, and at least two Week 1 lenses (IAM, version control, object storage, or architecture) |
| [ ] | Git relay repository has at least 2 merged pull requests |
| [ ] | Every pull request has a review comment |
| [ ] | At least 1 merge conflict is resolved on a feature branch |
| [ ] | Repository `README.md` includes all debrief answers |
| [ ] | Day 1 exit ticket is complete |
