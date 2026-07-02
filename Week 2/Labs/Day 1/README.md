# Week 2 Day 1 Lab: Linux CLI and Git Collaboration

**Theme:** Developer foundations by hand  
**Format:** Multiple short activities with reset points  
**Primary tools:** Linux terminal, VS Code, Chrome, Git, GitHub  
**Estimated lab time:** Full day with demos, breaks, troubleshooting, and debriefs

## Learning Objectives

By the end of this lab day, you will be able to:

- Navigate, inspect, search, and transform files from a Linux terminal.
- Compare common terminal options on Windows, macOS, Linux, and browser-based cloud shells.
- Combine small commands with pipes and redirection.
- Explain when to use `grep`, `find`, `cut`, `sort`, `uniq`, `wc`, `head`, and `tail`.
- Use terminal commands for quick EDA, data analysis, log triage, and data engineering operations.
- Turn repeated checks into a small Bash script and read basic cron schedules.
- Create a feature branch, push it, open a pull request, review a teammate's code, and merge.
- Resolve a merge conflict on the feature branch without damaging `main`.

## Lab Index

### Provided Files

| File | Purpose |
| :--- | :--- |
| `README.md` | This pacing map and activity index |
| `Reading_Terminal_for_Data_Engineers.md` | Learner explainer on terminal history, modern relevance, local terminals, cloud shells, and safety habits |
| `Activity_0_Terminal_Warm_Up.md` | Guided terminal first steps using `sales.csv` and `shakespeare.txt` |
| `Activity_1_Mini_EDA_Sprint.md` | Guided terminal EDA on provided retail operations files |
| `Activity_2_CLI_Scavenger_Hunt.md` | CLI investigation challenge with command explanations |
| `Activity_3_Bash_Automation.md` | Bash automation in three tiers: Part A guided build, Part B on-your-own metrics, Part C challenge, plus cron-reading practice |
| `Instructor_Demo.md` | Instructor-led command script with examples, pause points, expected observations, reset notes, and troubleshooting |
| `Activity_4_Git_Collaboration_Relay.md` | Branch, pull request, review, merge, and conflict practice |
| `Group_Activity_Terminal_Operations_Decision_Brief.md` | Non-technical team decision brief about choosing the right terminal and automation surface, framed as a Week 1 synthesis (IAM, version control, object storage, architecture) |
| `Activity_5_Debrief_and_Stretch.md` | Fast-finisher extensions and reflection |
| `starter/summarize_hunt_starter.sh` | Starter Bash script for Activity 3 |
| `starter/cron_schedule_practice.txt` | Cron expression practice for Activity 3 |
| `solutions/Instructor_Answer_Key.md` | Single instructor answer key for the day: Activity 2 hunt, Activity 3 Parts B to D, and cron, with teaching explanations. Instructor-only. |
| `solutions/Activity_3_summarize_hunt_solution.sh` | Runnable instructor solution script for Activity 3. Instructor-only. |
| `solutions/Activity_2_cli_hunt_answer_key.md` | Detailed per-activity backup key for Activity 2 (folded into the consolidated key) |
| `solutions/Activity_3_cron_answer_key.md` | Detailed per-activity backup key for cron practice (folded into the consolidated key) |
| `Student_Resources.md` | Shell, cron, VS Code, Git, and GitHub references |
| `Terminal Reference/terminal.md` | Extra terminal walkthrough rewritten for Linux terminal and VS Code |
| `Terminal Reference/sales.csv` | Existing CSV for Activity 0 command warm-up |
| `Terminal Reference/shakespeare.txt` | Existing text file for Activity 0 `grep` practice |
| `Terminal Reference/operations_playground/` | Provided operations folder for Activities 1 to 3, including data, logs, notes, and scripts |
| `quiz/Day_1_Exit_Ticket.md` | Markdown Mash exit ticket |

Activities 1 to 3 use provided files in `Terminal Reference/operations_playground/`. Students do not generate the analysis data. Shell scripting is taught in Activity 3 by writing checks, loops, and conditions over those provided files.

### Deliverables

| # | Deliverable | Format | Source |
| :--- | :--- | :--- | :--- |
| 1 | `terminal_warmup_notes.md` with guided command observations | Markdown | Activity 0 |
| 2 | `eda_notes.md` with file, store, amount, log, and follow-up question observations | Markdown | Activity 1 |
| 3 | `cli_hunt.md` with 12 commands, answers, and explanations | Markdown | Activity 2 |
| 4 | `summarize_hunt.sh` that prints reusable file, row, store, and log checks | Bash script | Activity 3 |
| 5 | `automation_notes.md` with script and cron explanations | Markdown | Activity 3 |
| 6 | Cron schedule annotations for schedules 2 to 4 (schedule 1 is the worked model) | Text or Markdown | Activity 3 |
| 7 | Terminal operations decision brief | Short memo and 2-minute presentation | Group activity |
| 8 | Git relay repository with merged pull requests and resolved conflicts | GitHub repository | Activity 4 |
| 9 | Debrief answers in the Git relay repository `README.md` | Markdown | Activity 4 |
| 10 | Exit ticket submitted from `quiz/Day_1_Exit_Ticket.md` | Markdown Mash quiz | End of day |

## AI-Free Zone

Use documentation, `man`, `tldr`, explainshell, and teammate discussion. Do not use AI code assistants for command generation, Git steps, or conflict resolution during this lab.

## Terminal Options Across Operating Systems

You will use Ubuntu today. The bigger idea transfers across systems:

| Environment | Common terminal option | What to remember |
| :--- | :--- | :--- |
| Windows | Windows Terminal with PowerShell, Command Prompt, or Ubuntu through Windows Subsystem for Linux | The shell language can differ by profile, so check which shell you are in before copying commands |
| macOS | Terminal or iTerm2 with `zsh` by default | Many Unix commands are familiar, but some flags differ from GNU/Linux |
| Linux and Ubuntu | GNOME Terminal, VS Code integrated terminal, or another shell emulator using Bash or Zsh | This is the closest match to many servers, containers, and cloud shells |
| Cloud platforms | Browser-based shells such as AWS CloudShell, Google Cloud Shell, and Azure Cloud Shell | Useful for cloud tasks because credentials and CLIs are often preconfigured, but storage, quotas, and permissions vary |

## Why the Terminal Still Matters in 2026

The terminal is not old-fashioned. It is the control surface for modern data engineering.

In 2026, data engineers use more managed tools, cloud consoles, notebooks, and AI assistants than ever. The terminal still matters because it gives you:

- **Speed:** answer simple questions without opening a notebook or waiting for a dashboard.
- **Repeatability:** turn a working command into a script, a scheduled job, or a CI/CD step.
- **Auditability:** commands can be saved, reviewed, committed, and rerun.
- **Remote control:** cloud servers, containers, runners, and production systems often have no GUI.
- **AI judgment:** AI may suggest a command, but you need enough shell fluency to check whether it is safe, correct, and appropriate.
- **Debugging power:** when something breaks, logs, files, permissions, paths, and environment variables usually tell the story first.

Today is not about memorizing every command. It is about learning how data engineers think at the terminal: inspect, narrow, transform, verify, and automate.

## Where Data Engineers Use the Terminal

| Area | What data engineers do | Example terminal moves |
| :--- | :--- | :--- |
| File triage | Check what arrived, how big it is, and whether it looks complete | `ls -lh`, `du -sh`, `find`, `wc -l` |
| Data EDA | Preview CSVs, count rows, inspect columns, find bad values | `head`, `tail`, `cut`, `sort`, `uniq`, `awk` |
| Log analysis | Find errors, count failure types, watch jobs in real time | `grep`, `tail -f`, `sort`, `uniq -c` |
| Automation | Turn repeated command sequences into scripts | Bash variables, loops, redirects, executable scripts |
| Scheduling | Describe when jobs should run | cron syntax, later Airflow and Cloud Composer schedules |
| Cloud work | Move data, inspect storage, run jobs, deploy services | Cloud CLIs, shell scripts, environment variables |
| Git collaboration | Branch, commit, review, merge, and recover from conflicts | `git switch`, `git status`, `git pull`, `git push` |
| Production debugging | Confirm what happened before changing code | logs, paths, configs, recent file changes |

## Teach, Then Practice Flow

Use `Instructor_Demo.md` before each activity block. Students should first see commands modeled with expected observations, then complete the matching activity.

| Teach first | Then students do | Focus |
| :--- | :--- | :--- |
| `Instructor_Demo.md` Demos 1 to 4 | Activity 0 | Terminal identity, navigation, previewing, line counts, pipes, and `grep` |
| `Instructor_Demo.md` Demos 5 to 7 | Activity 1 | File profiling, CSV EDA, `awk`, and log triage |
| `Instructor_Demo.md` Demo 8 plus selected prior commands | Activity 2 | Independent investigation, regex search, safe working copies, and command explanations |
| `Instructor_Demo.md` Demos 9 to 10 | Activity 3 | Bash scripting and cron reading |
| `Instructor_Demo.md` Demo 11 | Activity 4 | Git branch, review, merge, and conflict refresher |

## Full-Day Activity Flow

| Block | Time | File | What you practice |
| :--- | :--- | :--- | :--- |
| Instructor demo | 75-95 min total | `Instructor_Demo.md` | Short live examples before each student activity |
| Activity 0 | 35 min | `Activity_0_Terminal_Warm_Up.md` | Guided terminal first steps with `sales.csv` and `shakespeare.txt` |
| Activity 1 | 50 min | `Activity_1_Mini_EDA_Sprint.md` | Guided EDA sprint on provided operations files |
| Activity 2 | 60 min | `Activity_2_CLI_Scavenger_Hunt.md` | CLI investigation challenge and command explanations |
| Activity 3 | 45 min | `Activity_3_Bash_Automation.md` | Bash variables, loops, conditions, and cron reading |
| Group activity | 35 min | `Group_Activity_Terminal_Operations_Decision_Brief.md` | Decide and defend terminal, automation, and safety choices |
| Activity 4 | 90 min | `Activity_4_Git_Collaboration_Relay.md` | GitHub collaboration relay and conflict resolution |
| Activity 5 | 45-60 min | `Activity_5_Debrief_and_Stretch.md` | Share patterns, finish deliverables, complete extensions |

Use each activity as a natural classroom checkpoint. Finish one, debrief it, take a break or reset, then move to the next file.

## Suggested Instructor Rhythm

1. Use the matching section of `Instructor_Demo.md` to model the concept.
2. Ask students to predict one output before running the next command.
3. Start the matching activity file.
4. Stop at the success criteria.
5. Ask one pair to explain one command or Git decision.
6. Reset the room before opening the next activity.

Fast students can move into Activity 5 stretch work. Students who need more practice should complete Activities 0 to 4 first.
