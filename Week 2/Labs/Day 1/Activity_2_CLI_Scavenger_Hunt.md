# Activity 2: CLI Investigation Challenge

**Module:** Week 2 Day 1, Linux CLI and Git Collaboration  
**Estimated Time:** 60 minutes  
**Difficulty:** Intermediate  
**Format:** Teams of 2 to 3  
**Prerequisites:** Activity 1 or the provided `operations_playground/` folder

## Objective

In this activity, you will answer realistic file, CSV, text-search, and log questions using terminal commands and command pipelines.

## How This Activity Works

Activity 0 showed commands one at a time. Activity 1 guided you through a data profile. This activity gives you more independence, but it is still structured.

For each investigation question, record:

- The question number.
- The exact command or command pipeline you ran.
- The answer printed by the command.
- One short sentence explaining why the command works.

## Setup

From `Week 2/Labs/Day 1`, run:

```bash
cd "Terminal Reference/operations_playground"
pwd
ls
```

Create your answer file:

```bash
touch cli_hunt.md
```

Start it with:

```markdown
# CLI Investigation Answers
```

## Command Bank

Use this bank when you are stuck. You will not need every command for every question.

| Need | Useful commands |
| :--- | :--- |
| Confirm location | `pwd`, `ls`, `ls -lh` |
| Find files | `find . -type f`, `find . -name "*.csv"` |
| Preview files | `head`, `tail`, `less` |
| Count lines | `wc -l` |
| Search contents | `grep`, `grep -i`, `grep -n`, `grep -E` |
| Extract CSV columns | `cut -d',' -f2` |
| Filter CSV rows | `awk -F',' 'condition {print}'` |
| Count groups | `sort`, `uniq -c`, `wc -l` |
| Work with files safely | `mkdir -p`, `cp`, `mv`, `ls` |
| Save output | `>`, `>>` |

Safety rule: before a command creates, moves, overwrites, or appends to a file, run `pwd` and `ls` so you know where the change will happen.

## Investigation Questions

### 1. Count Provided Files

How many provided files, not directories, are under `data/`, `logs/`, `notes/`, and `scripts/`?

Starter:

```bash
find data logs notes scripts -type f
```

Then add a command to count the lines.

### 2. Find The Largest Direct Folder Or File

What is the largest file or directory directly under the current folder, and how large is it in human-readable format?

Starter:

```bash
du -sh *
```

Then sort the sizes and keep the largest result.

### 3. Count Orders

How many lines does `data/orders_sample.csv` have? How many data rows is that?

Explain why those two numbers differ.

### 4. Find Hidden Files

There is a hidden file somewhere. What is its name, and what does it contain?

Starter:

```bash
find . -name ".*" -type f
```

### 5. Count Log Errors

How many lines contain the word `ERROR`, ignoring case, in `logs/pipeline.log`?

Explain why ignoring case matters for this file.

### 6. Find The Last Log Timestamp

What is the timestamp of the last line of `logs/pipeline.log`?

Starter:

```bash
tail -1 logs/pipeline.log
```

Then extract only the first field.

### 7. Sort Data Files By Size

List every file under `data/`, sorted by size, largest first.

### 8. Find Shell Scripts

Which shell scripts exist under `scripts/`?

### 9. Count Unique Store Codes

How many unique store codes are in column 2 of `data/orders_sample.csv`?

Required tools: `tail`, `cut`, `sort`, `uniq`, and `wc`.

### 10. Search With A Regex Pattern

Which log lines mention either `timeout` or `schema`?

Required tool: `grep -E`.

### 11. Make A Safe Working Copy

Create a `work/` folder. Copy `logs/pipeline.log` into it as `pipeline_working.log`.

Then append this line to the copied file, not the original:

```text
hunt completed by <your name>
```

Prove the original log did not change by showing the last line of both files.

### 12. Top Error Messages

Write a single piped command that prints the 3 most common error messages in the log with their counts.

Use the original file:

```text
logs/pipeline.log
```

## Expected Answer Format

Use this structure for every answer:

````markdown
## 1. Count Provided Files

Command:
```bash
find data logs notes scripts -type f | wc -l
```

Answer:
```text
7
```

Why it works:
`find data logs notes scripts -type f` lists provided files under the four starter folders, and `wc -l` counts those lines.
````

## Success Criteria

- `cli_hunt.md` contains all 12 numbered answers.
- Every answer includes the command, result, and explanation.
- At least 5 answers use a pipe.
- At least 1 answer uses `grep -E`.
- At least 1 answer uses `awk`, `cut`, or both.
- Your team can explain one command pipeline out loud.

## Hints

<details>
<summary>Hint 1: Counting and searching files</summary>

Use `find` when the question is about locating files. Add `-type f` when directories should not be counted.

</details>

<details>
<summary>Hint 2: CSV column work</summary>

Use `tail -n +2` when you need to skip the header row before counting data values.

</details>

<details>
<summary>Hint 3: Common error messages</summary>

First reduce log lines to the message text, then sort, count with `uniq -c`, sort again, and keep the top 3.

</details>

<details>
<summary>Hint 4: Safe file changes</summary>

Question 11 changes a copied log in `work/`. Do not append to the original file.

</details>

## Stretch Goals

- Add a thirteenth question for another team.
- Solve one question two different ways.
- Use `awk` to count orders where `amount` is greater than 50.
- Add a `cli_hunt_review.md` file with feedback on another team's explanations.

> Instructor notes for this activity are in `Week 2/Instructor Notes/Day 1 - Instructor Guide.md`.
