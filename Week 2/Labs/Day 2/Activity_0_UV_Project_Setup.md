# Activity 0: Local Python Project Setup with UV

**Module:** Week 2 Day 2, Python Foundations
**Estimated Time:** 15 minutes
**Difficulty:** Beginner
**Format:** Individual
**Prerequisites:** A VM with VS Code, the course repo already cloned, and UV installed

## Objective

In this activity, you will create a local Python project for today's drill scripts
and confirm that scripts run through UV. You will also learn exactly where your
virtual environment lives and how to point VS Code at it.

## Background

You opened VS Code at the root of the cloned course repo. Everything the
instructor ships lives in folders like `Week 2/Labs/...`. To keep your own work
separate, you will do all of your work under one folder: `student-work/`.

Why this matters:

- **No merge conflicts on pull.** The instructor only adds files outside
  `student-work/`. When you run `git pull` to get new course material, your work
  under `student-work/` is never touched, so it will not conflict.
- **A predictable environment.** UV creates the project and its `.venv` in the
  folder where you run the command. If you run it in the wrong place, your `.venv`
  lands in the wrong place and VS Code points at the wrong interpreter. You will
  run it in one known folder per day.

Today's scripts use only the Python standard library, so there are no packages to
install. We still use UV because it gives every learner the same project workflow
for the rest of the bootcamp.

## Instructions

1. Open a terminal in VS Code. Confirm you are at the repo root.

```bash
pwd
# should end with the cloned repo folder, for example .../TechCatalyst_DE_2026
```

2. Create today's project folder under `student-work/` and move into it.

```bash
mkdir -p student-work/week2/day2
cd student-work/week2/day2
```

3. Initialize a UV project **here**, inside `student-work/week2/day2`.

```bash
uv init
```

This creates `pyproject.toml` and a few starter files in this folder. The virtual
environment `.venv` is created in this same folder the first time you run a UV
command (next step).

4. Confirm Python runs through UV and see where the environment lives.

```bash
uv run python --version
ls -a
# you should now see a .venv folder in student-work/week2/day2
```

5. Point VS Code at this environment.

   - Open the Command Palette (Ctrl+Shift+P), choose **Python: Select Interpreter**,
     and pick the one at `student-work/week2/day2/.venv`.
   - If you open a notebook today, click **Select Kernel** and choose that same
     `.venv`.

6. Create a smoke-test script and run it.

```bash
touch smoke_test.py
```

Add this code to `smoke_test.py`:

```python
print("Day 2 Python setup is ready")
```

Run it from inside `student-work/week2/day2`:

```bash
uv run python smoke_test.py
```

## Expected Output

```text
Day 2 Python setup is ready
```

## Make Sure UV Uses This Project's Environment

`uv run` always targets this project's `.venv` (the one in
`student-work/week2/day2`), so you normally do not activate anything. Just prefix
commands with `uv run`.

If a `uv` command prints a warning like this:

```text
warning: `VIRTUAL_ENV=/some/other/path/venv` does not match the project
environment path `.venv` and will be ignored
```

it means a different virtual environment is active in your shell (for example one
left over from another project). Clear it, then rerun:

```bash
deactivate
uv run python smoke_test.py
```

Optional: if you would rather type plain `python` without the `uv run` prefix,
activate this project's environment first:

```bash
source .venv/bin/activate
python smoke_test.py
# run 'deactivate' when you are done for the day
```

Either way, the goal is the same: the environment that runs your code is the
`.venv` inside `student-work/week2/day2`.

## Success Criteria

- `uv init` created a project in `student-work/week2/day2`.
- A `.venv` folder exists in `student-work/week2/day2` (not at the repo root).
- `uv run python --version` prints a Python version.
- `uv run python smoke_test.py` prints the expected message.
- VS Code shows the `student-work/week2/day2/.venv` interpreter selected.
- You can explain why we keep work under `student-work/` and why the `.venv` lives
  in the day folder.

## Hints

<details>
<summary>`uv` command not found</summary>

Tell the instructor. Do not switch to plain `pip` or a different setup unless the
instructor gives that fallback.

</details>

<details>
<summary>You created the project in the wrong folder</summary>

Run `pwd` to check your current folder. If a `.venv` or `pyproject.toml` appeared
at the repo root or somewhere unexpected, delete those, move back to the repo
root, then redo step 2. Always `cd` into `student-work/week2/day2` before running
`uv` commands.

</details>

<details>
<summary>VS Code is using the wrong Python</summary>

Run **Python: Select Interpreter** again and choose the `.venv` inside
`student-work/week2/day2`. The folder you have open and the interpreter you select
must match.

</details>

<details>
<summary>Warning: VIRTUAL_ENV does not match the project environment</summary>

A different virtual environment is active in your shell. Run `deactivate`, then
rerun your `uv run` command. See "Make Sure UV Uses This Project's Environment"
above.

</details>

## Stretch Goals

- Run `uv lock` and inspect the files UV created in the day folder.
- Add a short note to your repo describing what `uv run` does and where your
  `.venv` lives.

## Instructor Notes

- The repo is cloned and VS Code is launched from the repo root. Students do all
  work under `student-work/` so that your future pushes (new items outside
  `student-work/`) never conflict with their pulled work.
- One UV project per day under `student-work/weekN/dayX/`. The `.venv` lives in the
  day folder, so students must `cd` into it before any `uv` command.
- Common mistakes: running `uv init` at the repo root, opening the wrong VS Code
  folder, selecting the wrong interpreter, and typing `python smoke_test.py`
  instead of `uv run python smoke_test.py`.
- Debrief question: why does keeping work under `student-work/` make `git pull`
  safe?
- Suggested solution approach: keep this quick. The goal is a reliable daily run
  pattern and a correctly selected interpreter, not a deep packaging lecture.
