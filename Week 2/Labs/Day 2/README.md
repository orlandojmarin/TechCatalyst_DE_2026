# Week 2 Day 2: Python Foundations for Data Engineering

Today builds Python fluency by hand on a single running scenario: you are a data
engineering intern at Charter Oak Mutual, a fictional insurer, working with claim
data. You will type, run, debug, reconcile with your table, and commit working
scripts under `student-work/week2/day2/` in the cloned course repo. Every drill
uses claims data, and the day ends with a mini-capstone that chains the whole day
into one small pipeline.

## Environment Setup

Complete `Activity_0_UV_Project_Setup.md` first. It walks you through creating
today's project. In short, from the repo root in VS Code:

```bash
mkdir -p student-work/week2/day2
cd student-work/week2/day2
uv init
uv run python --version
```

You keep all of your work under `student-work/` so that when you `git pull` new
course material it never conflicts with your files. The `.venv` lives inside
`student-work/week2/day2`, so always run UV commands from that folder.

No third-party packages are required today. Every script uses only the Python
standard library and runs the same way from inside your day project:

```bash
uv run python path/to/your_script.py
```

Commit your completed scripts under `student-work/`. Do not commit the instructor
`solutions/` folder from this repo.

## Lab Index

### Provided files

| Folder | Activity | Block |
|--------|----------|-------|
| `Activity_0_UV_Project_Setup.md` | Local UV project setup | Setup |
| `Python Drills/01-Stu_Variables/` | Claim Reserve Variance: variables, arithmetic, f-string format specifiers | Morning |
| `Python Drills/02-Stu_Conditionals/` | The Triage Conundrum: predict the output of triage logic | Morning |
| `Python Drills/03-Stu_Triage/` | Triage Faceoff: user input plus random choice, nested conditionals | Morning |
| `Python Drills/04-Stu_Loops/` | Claim Pipeline Banner: for loop over a string and a range | Afternoon |
| `Python Drills/05-Stu_Lists/` | The Claim Queue: list creation, slicing, indexing, mutation | Afternoon |
| `Python Drills/06-Stu_Dictionaries/` | Claim Reserves by Tier: dict CRUD plus tiering | Afternoon |
| `Python Drills/07-Stu_Iterate_Lists/` | Daily Claims Cash Flow: iterate and aggregate a list | Afternoon |
| `Python Drills/08-Stu_Functions/` | Loss Ratio: refactor repeated logic into a function | Afternoon |
| `Python Drills/09-Stu_Nesting/` | Claim Payment Rollup: nested dict/list traversal (**priority**) | Afternoon |
| `Python Drills/10-Stu_Classes/` | Claims as Classes: classes, methods, and class versus function | Afternoon |
| `Python Drills/11-Stu_File_IO/` | File I/O: read a text file, write a summary file | Data I/O |
| `Python Drills/12-Stu_CSV_IO/` | CSV read and write with the `csv` module | Data I/O |
| `Python Drills/13-Stu_JSON_IO/` | JSON read and write (the Day 3 API shape) | Data I/O |
| `Python Drills/14-Stu_Lambdas_Map_Filter/` | Lambdas, `map`, `filter` (the PySpark pattern) | Functional |
| `Python Drills/15-Stu_SQLite/` | SQLite: create, insert, query with `sqlite3` | Data I/O |
| `Python Drills/16-Stu_Error_Handling/` | try/except/else/finally, custom exceptions, retry (Day 3 bridge) | Core |
| `Python Drills/17-Stu_Collections/` | `defaultdict` and `Counter` for aggregation (Day 4 bridge) | Core |
| `Python Drills/18-Stu_Datetime/` | parse/format dates, `timedelta` (time-series for Day 4) | Core |
| `Activity_1_Mini_Capstone_Claims_Intake/` | Mini-capstone: clean, aggregate, and report on messy claim data | Capstone |
| `Activity_2_No_Show_Analysis/` | Analysis capstone: read a CSV, compute no-show rates, interpret the results | Homework |
| `Advanced Track/` | Optional modern-Python drills for fast finishers (comprehensions, match/case, dataclasses) | Optional |
| `Instructor_Demo/` | Notebook-based instructor demo (DE flow), plus the `.py` version | Instructor |
| `Traceback_Clinic.md` | Instructor-led clinic on reading tracebacks | Support |
| `solutions/` | Instructor solutions (drills plus mini-capstone) and legacy 2025 reference | Reference |
| `quiz/Day_2_Exit_Ticket.md` | End-of-day knowledge check | Assessment |

### Deliverables

| # | Deliverable | Format | Due |
| :--- | :--- | :--- | :--- |
| 1 | Morning drill solutions (01, 02, 03) committed under `student-work/week2/day2/` | Python files in repo | End of day |
| 2 | Afternoon drill solutions (04, 05, 06, 07, 08, 09, 10) committed. 09 is the priority | Python files in repo | End of day |
| 2b | Data I/O and tools drills (11 File, 12 CSV, 13 JSON, 14 lambdas/map/filter, 15 SQLite) | Python files in repo | End of day or homework |
| 3 | Mini-capstone `claims_pipeline.py` (at least Core and Challenge tiers) committed | Python file in repo | End of day |
| 3b | Analysis capstone (Activity 2): `no_show_analysis.py` plus `findings.md` | Python + Markdown | Homework |
| 4 | One "aha" note (a traceback you defeated or a concept that clicked) in your repo README | Markdown in repo | End of day |
| 5 | Day 2 exit ticket completed | Markdown Mash quiz | End of day |
| 6 | Optional: any `Advanced Track/` drills you reached | Python files in repo | If time |

---

The drills were carried over from the 2025 cohort and rewritten for 2026 around an
insurance-claims scenario. Workflow: copy the provided `Unsolved` scaffold into
your `student-work/week2/day2` project, then write the logic yourself. No AI, and
do not open the `solutions/` folder until your table has reconciled answers.

## Morning Block (about 60 min): `Python Drills/`
- `01-Stu_Variables`
- `02-Stu_Conditionals`
- `03-Stu_Triage`

## Afternoon Block (about 90 min): `Python Drills/`
- `04-Stu_Loops`
- `05-Stu_Lists`
- `06-Stu_Dictionaries`
- `07-Stu_Iterate_Lists`
- `08-Stu_Functions`
- `09-Stu_Nesting`, **priority: APIs return exactly this shape tomorrow**
- `10-Stu_Classes`

## Data I/O and Tools (Core, may extend into homework): `Python Drills/`
These are the bridge to Day 4 (pandas) and the SQL weeks. Each has a `Resources/`
folder you copy into your project.
- `11-Stu_File_IO` (read/write text)
- `12-Stu_CSV_IO` (read/write CSV with the `csv` module)
- `13-Stu_JSON_IO` (read/write JSON, the Day 3 API shape)
- `14-Stu_Lambdas_Map_Filter` (the transform pattern you reuse in PySpark)
- `15-Stu_SQLite` (create, insert, and query a real database with SQL)
- `16-Stu_Error_Handling` (robust code; the prerequisite for resilient Day 3 APIs)
- `17-Stu_Collections` (`defaultdict`/`Counter`; the group-and-count for Day 4)
- `18-Stu_Datetime` (parse and compute on dates; time-series for Day 4)

## Mini-Capstone (about 45 to 60 min): `Activity_1_Mini_Capstone_Claims_Intake/`
Chain the whole day into one pipeline: read messy claim records, clean and
validate them, aggregate by policy type, and roll up nested payments. Work the
Core, Challenge, and Stretch tiers in order. This is the bridge into Day 3.

Copy the activity's `starter/` and `data/` into your `student-work/week2/day2`
project, then write the pipeline yourself. Do not copy from `solutions/`.

## Analysis Capstone (homework): `Activity_2_No_Show_Analysis/`
A second, analysis-focused capstone on a real appointments dataset. You read a CSV,
compute no-show rates by several factors, then write `findings.md` interpreting the
results (including a famously counterintuitive result about SMS reminders). This is
the "think about the output" half of data engineering, and it pairs well with a
short share-out next session.

## Advanced Track (optional, for fast finishers): `Advanced Track/`
If you finish early, do not just float. The `Advanced Track/` adds modern Python
you will use constantly: comprehensions (A1), `match`/`case` (A2), and classes plus
dataclasses (A3), with walrus and generator stretch tiers on drills 07 and 09. See
`Advanced Track/README.md`.

## Protocol
1. Solo first for 30 to 40 minutes. Fight your own errors and write down each
   traceback you defeat.
2. Table reconcile. Compare solutions, argue about differences, converge.
3. Commit to your course repo under `student-work/week2/day2/`.
4. Done early? Push into the drill Challenge tiers, the mini-capstone Stretch, and
   the `Advanced Track/`, then float and help (teaching counts).

## Expected Run Commands

From your `student-work/week2/day2` project:

```bash
uv run python 01-Stu_Variables/Core/claim_variance.py
uv run python 02-Stu_Conditionals/conditionals.py
uv run python 03-Stu_Triage/triage_sim.py
uv run python 09-Stu_Nesting/Core/payment_rollup_core.py
```

For scripts that prompt for input (03-Triage), type the requested value in the
terminal.

## Success Criteria

- Every completed script runs with `uv run python`.
- You can explain the main data type used in each drill.
- You can read the last line of a traceback and identify the error type.
- Your `09-Stu_Nesting` rollup totals the `amount` field per claim, with no
  duplicated records.
- Your mini-capstone rejects exactly 6 rows and flags CLM-1009 and CLM-1016.
- Your repo contains an "aha" note about one bug, concept, or traceback.

## Hints

<details>
<summary>If a script says a variable is not defined</summary>

Check spelling first. Then check whether the assignment line ran before the
variable was used.

</details>

<details>
<summary>If a dictionary key crashes</summary>

Print the dictionary keys, then decide whether direct access with `record["key"]`
or safe access with `record.get("key", default)` is the better choice.

</details>

<details>
<summary>If a loop output repeats too many times</summary>

Check whether your append or print statement is inside the loop by accident.

</details>

**Deliverable:** drill solutions plus the mini-capstone committed, plus one "aha"
note in your repo README.
