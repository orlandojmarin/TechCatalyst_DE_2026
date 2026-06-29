# Activity 0: Guided Terminal First Steps

**Module:** Week 2 Day 1, Linux CLI and Git Collaboration  
**Estimated Time:** 35 minutes  
**Difficulty:** Beginner  
**Format:** Individual, then pair discussion  
**Prerequisites:** Linux terminal, VS Code, and the Day 1 lab folder

## Objective

In this activity, you will learn the first terminal habits that data engineers use when they meet a new folder: identify where you are, inspect what exists, preview files safely, count records, and search text.

## Before You Start

Read this short mental model before typing commands:

- A **terminal** is the window where you type commands.
- A **shell** is the program that interprets those commands. Today you are using a Linux shell.
- A command usually has a verb, optional flags, and a target.
- Example: `head -n 5 sales.csv` means "show the first 5 lines of this file."
- Data engineers use the terminal to ask fast first questions before opening Python, SQL, a cloud console, or a notebook.

Do not worry about memorizing commands today. Focus on the pattern:

```text
inspect -> narrow -> count -> search -> explain
```

## Setup

1. Open VS Code.
2. Open a Linux terminal.
3. Navigate to `Week 2/Labs/Day 1`.
4. Move into the provided reference folder:

   ```bash
   cd "Terminal Reference"
   ```

5. Confirm where you are:

   ```bash
   pwd
   ```

## Part 1: Inspect The Folder

Run:

```bash
ls
```

What this means:

- `ls` lists visible files and folders.
- This is the terminal version of asking, "What am I working with?"

Now run:

```bash
ls -lh
```

What this adds:

- `-l` shows a long listing.
- `-h` shows file sizes in a human-readable format.

Record one observation:

```markdown
## Folder Observation

- I see:
```

## Part 2: Preview A CSV Without Opening A Spreadsheet

Run:

```bash
head -n 5 sales.csv
```

What this means:

- `head` previews the top of a file.
- `-n 5` asks for 5 lines.
- The first line is the header, which names the columns.

Now try:

```bash
tail -n 5 sales.csv
```

What this means:

- `tail` previews the bottom of a file.
- This is useful when checking whether a file ended cleanly.

Record:

```markdown
## CSV Preview

- Columns:
- One thing I notice in the first rows:
- One thing I notice in the last rows:
```

## Part 3: Count Lines, Then Interpret The Count

Run:

```bash
wc -l sales.csv
```

What this means:

- `wc` means word count, but `-l` counts lines.
- A CSV line count usually includes the header.

Expected result:

```text
29 sales.csv
```

Interpretation:

```text
29 total lines means 28 data rows because 1 line is the header.
```

Record:

```markdown
## Row Count

- Total lines:
- Data rows:
- Why the numbers differ:
```

## Part 4: Extract One Column

Run:

```bash
cut -d',' -f1 sales.csv
```

What this means:

- `cut` extracts fields from text.
- `-d','` says the delimiter is a comma.
- `-f1` asks for the first field.

Now skip the header:

```bash
cut -d',' -f1 sales.csv | tail -n +2
```

What the pipe means:

- `|` sends output from the command on the left into the command on the right.
- This is the same idea as a small data pipeline.

Now count unique names:

```bash
cut -d',' -f1 sales.csv | tail -n +2 | sort | uniq | wc -l
```

What each stage does:

| Stage | Purpose |
| :--- | :--- |
| `cut -d',' -f1 sales.csv` | Extract the first column |
| `tail -n +2` | Remove the header row |
| `sort` | Put repeated values next to each other |
| `uniq` | Keep one copy of each repeated value |
| `wc -l` | Count the remaining lines |

Record:

```markdown
## Unique Names

- Command:
- Answer:
- Why `sort` comes before `uniq`:
```

## Part 5: Search Text With `grep`

Run:

```bash
grep -i "beauty" shakespeare.txt
```

What this means:

- `grep` searches inside files.
- `-i` ignores case, so `Beauty` and `beauty` both match.

Now count matching lines:

```bash
grep -ic "time" shakespeare.txt
```

What this means:

- `-c` counts matching lines.
- It does not count every repeated word on the same line.

Try one more:

```bash
grep -in "fortune" shakespeare.txt | head -n 5
```

What this adds:

- `-n` shows line numbers.
- `head -n 5` keeps only the first 5 matches.

Record:

```markdown
## Search Practice

- One word I searched:
- Command:
- What the result tells me:
```

## Part 6: Pair Discussion

Discuss with a partner:

1. Which command felt like data analysis?
2. Which command felt like operations or debugging?
3. Which command would you save if you had to check this folder every morning?
4. Before running a command that changes files, what should you inspect first?

## Deliverable

Create a short file named `terminal_warmup_notes.md` in `Terminal Reference` with these sections:

```markdown
# Terminal Warm-Up Notes

## Folder Observation

## CSV Preview

## Row Count

## Unique Names

## Search Practice

## Pair Discussion Takeaway
```

## Success Criteria

- You ran `pwd`, `ls`, `head`, `tail`, `wc`, `cut`, `sort`, `uniq`, and `grep`.
- You can explain what one pipe does.
- You can explain why a CSV line count includes the header.
- You created `terminal_warmup_notes.md`.
- You can name one data engineering use case for terminal commands.

## Hints

<details>
<summary>Hint 1: I am lost in folders</summary>

Run `pwd` to print your current folder. Then use `ls` to inspect what is inside it.

</details>

<details>
<summary>Hint 2: My command says file not found</summary>

Check that you are inside `Week 2/Labs/Day 1/Terminal Reference`. Then run `ls` to confirm `sales.csv` and `shakespeare.txt` are visible.

</details>

<details>
<summary>Hint 3: My unique count looks wrong</summary>

Make sure you removed the header with `tail -n +2` before counting unique values.

</details>

> Instructor notes for this activity are in `Week 2/Instructor Notes/Day 1 - Instructor Guide.md`.
