# Activity 7: Comic Books CSV Cleanup

**Module:** Week 3 Day 3, Pandas Review  
**Estimated Time:** 35 minutes  
**Difficulty:** Intermediate  
**Format:** Individual or pair  
**Prerequisites:** Repo-root `.venv` selected as the VS Code interpreter and Jupyter kernel. Do not run `uv init` inside this activity folder.

## Objective

In this activity, you will reduce a large CSV to an analysis-ready table and write the cleaned result back to disk.

## Concepts Covered

| Concept | Where it appears |
|---|---|
| Large CSV loading | `read_csv` on a wide file |
| Column pruning | select useful columns |
| Renaming | `rename(columns=...)` |
| String cleanup | `str.strip`, `str.title` |
| File output | `to_csv(index=False)` |

## Background

This is a practical file-cleaning drill. It reinforces column pruning, renaming, text cleanup, numeric coercion, and CSV output.

## Setup

From the repo root, copy this whole activity folder into your day workspace:

```bash
mkdir -p student-work/week3/day3
cp -R "Week 3/Labs/Day 3/Activity_7_Comic_Books_CSV_Cleanup" student-work/week3/day3/
```

Open the copied notebook from `student-work/week3/day3/Activity_7_Comic_Books_CSV_Cleanup/`. Use the repo-root `.venv` as the kernel. If VS Code shows a `VIRTUAL_ENV does not match` warning, run `deactivate` in the terminal and keep using `uv run` from the repo root.

Weeks 1 to 4 are still an AI-Free Zone. Write the pandas code yourself, ask a partner, or ask the instructor.

## Instructions

1. Copy the activity folder into `student-work/week3/day3/`.
2. Open `comic_books_csv_cleanup.ipynb` from your copied folder.
3. Inspect the raw file and keep only useful columns.
4. Rename columns and clean text fields.
5. Convert publication year to numeric and write `Output/books_clean.csv`.

## Starter Code

Use `comic_books_csv_cleanup.ipynb` in this folder. The notebook has imports, data paths, and TODO cells.

## Expected Output

```text
`Output/books_clean.csv` exists and can be read back into pandas.
```

## Success Criteria

- The cleaned DataFrame has only the requested columns.
- Column names are clearer than the raw source names.
- `Publication Year` is numeric and non-missing in the cleaned output.

## Hints

<details>
<summary>Hint 1</summary>

Use `df.rename(columns={...})` for column names.

</details>

<details>
<summary>Hint 2</summary>

Use `Path("Output").mkdir(exist_ok=True)` before writing the CSV.

</details>

## Stretch Goals

- Add a duplicate ISBN check.
- Create a small table of the top 10 publishers by book count.

## Instructor Notes

- Common mistakes: forgetting `index=False` in `to_csv`, or converting publication year before renaming the column.
- Debrief question: why is writing a clean file different from just displaying a clean DataFrame?
