# Activity 0: UV Project and Notebook Setup

**Module:** Week 2 Day 3
**Estimated time:** 25 minutes
**Difficulty:** Beginner
**Format:** Individual, with neighbor check
**Prerequisites:** A VM with VS Code, the course repo already cloned, Git, and UV installed

## Objective

In this activity, you will create the one Python environment used for the rest
of Week 2, run the first notebook cell in VS Code (a first-time setup you only
do once), and copy today's starter files into your own work folder so you never
edit the provided course files directly.

## Background

You opened VS Code at the root of the cloned course repo. Everything the
instructor ships lives in folders like `Week 2/Labs/Day 3/`. You will do all of
your own writing under `student-work/`.

**One environment, created at the repo root.** You will run `uv init` in the
repo root (the folder VS Code already has open), which creates the project and,
on the first `uv add`, a `.venv` there. Because the environment lives in the
folder VS Code has open, VS Code **auto-detects** it and offers it as your
interpreter and notebook kernel, so you do not have to hunt for a path. You set
this up once today and reuse the exact same environment tomorrow (Day 4).

Keep two ideas separate:

- **The environment** (`pyproject.toml`, `uv.lock`, `.venv/`) lives at the repo
  root. It is generated and gitignored, so `git pull` never touches it.
- **Your work** (the notebooks and scripts you fill in, plus any `data/` you
  create) lives under `student-work/week2/`. The instructor only ships files
  outside `student-work/`, so a `git pull` of new course material never
  conflicts with what you wrote. This is also why you copy the provided
  notebooks into your folder instead of editing them in place.

Why one shared environment instead of a new one per day:

- **Auto-detection, no path typing.** A `.venv` at the open folder shows up in
  the kernel picker automatically. A `.venv` buried in a subfolder often does
  not, which is why we put it at the root.
- **Less repeated setup.** One `uv init`, and tomorrow you only `uv add` the
  couple of new packages Day 4 introduces.
- **`uv run` and the kernel use the same packages.** Whether you run a script
  with `uv run` or a notebook cell with the selected kernel, you are using the
  one environment you built here.

## Instructions

1. Open a terminal in VS Code and confirm you are at the repo root.

   ```bash
   pwd
   # should end with the cloned repo folder, for example .../TechCatalyst_DE_2026
   ```

2. Initialize a UV project **here, at the repo root**.

   ```bash
   uv init
   ```

   This adds `pyproject.toml`, `main.py`, and `.python-version`. It does **not**
   overwrite the repo's existing `README.md` or `.gitignore`. The `.venv` folder
   is created on the next command.

3. Add today's packages, including `ipykernel`.

   ```bash
   uv add requests httpx python-dotenv boto3 google-genai pandas polars ipykernel
   ```

   `ipykernel` is the one that makes notebooks work: without it, VS Code cannot
   use this environment as a Jupyter kernel. This command also creates `.venv/`
   at the repo root.

4. Confirm the environment works and see where it lives.

   ```bash
   uv run python -c "import requests, pandas, polars; print('env ok')"
   ls -a
   # you should see .venv, pyproject.toml, and uv.lock at the repo root
   ```

5. Create your work folder and copy today's starter files into it. Work on the
   copies, never on the provided originals.

   ```bash
   mkdir -p student-work/week2/data
   cp "Week 2/Labs/Day 3"/Activity_*.ipynb student-work/week2/
   cp "Week 2/Labs/Day 3/Bonus_Lab_Weather_API_Explorer.ipynb" student-work/week2/
   cp "Week 2/Labs/Day 3/starter/weather_explorer_starter.py" student-work/week2/weather_explorer.py
   ```

   Do not edit the provided notebooks under `Week 2/Labs/Day 3/` directly. You
   copy them into your project and work on the copies so a later `git pull`
   cannot conflict. This is the same copy-then-complete pattern as the Day 2
   drills.

6. **First time only: open a notebook and pick the kernel.** The very first time
   you open a notebook in a fresh VS Code, there are a few one-time clicks.

   1. In VS Code's Explorer, open one of your copies, for example
      `student-work/week2/Activity_1_HTTP_and_REST_Fundamentals.ipynb`.
   2. At the **top-right** of the notebook, click **Select Kernel**.
   3. If VS Code prompts you to install the recommended **Python** and
      **Jupyter** extensions (from Microsoft), click **Install**. Wait for the
      install to finish (watch the bottom status bar); VS Code may reload once.
   4. Click **Select Kernel** again, choose **Python Environments...**, and pick
      the environment at the repo root, shown as **.venv (Python 3.x.x)**.
      Because the project is in the folder VS Code has open, it appears near the
      top automatically. You should **not** need to type a path.
   5. Run the first cell (Shift+Enter). If it runs with no `ModuleNotFoundError`,
      your kernel is correct. You will reuse this same kernel for every notebook
      today and tomorrow.

   **Fallback**, only if `.venv` is not in the list: choose **Select Another
   Kernel... -> Python Environments... -> Enter interpreter path**, and paste:

   ```text
   .venv/bin/python
   ```

7. Running a script (the independent build `weather_explorer.py`). Scripts use
   the same environment. Move into your work folder first, so anything a script
   writes (like `data/`) lands there, then use `uv run`, which walks up to find
   the repo-root project automatically:

   ```bash
   cd student-work/week2
   uv run python weather_explorer.py "Hartford,US" 41.7658 -72.6734
   ```

   `uv run` finds the repo-root `.venv` even from this subfolder, so you do not
   have to activate anything.

## Expected Output

```text
env ok
```

At the repo root you should now have (generated, gitignored): `.venv/`,
`pyproject.toml`, `uv.lock`. Your work folder `student-work/week2/` should
include:

```text
data/
Activity_1_HTTP_and_REST_Fundamentals.ipynb    (your copy)
Activity_2_Async_SDKs_and_the_AI_Era.ipynb      (your copy)
Activity_3_DataFrame_Fundamentals.ipynb         (your copy)
Bonus_Lab_Weather_API_Explorer.ipynb            (optional copy)
weather_explorer.py                              (your copy of the starter)
```

## Make Sure UV Uses This Environment

`uv run` always targets the repo-root `.venv`, so you normally do not activate
anything. If a `uv` command prints a warning like:

```text
warning: `VIRTUAL_ENV=/some/other/path/venv` does not match the project
environment path `.venv` and will be ignored
```

a different virtual environment is active in your shell (often a leftover from
Day 2's separate project). Clear it and rerun:

```bash
deactivate
uv run python -c "import requests; print(requests.__version__)"
```

Optional, if you prefer plain `python` without the `uv run` prefix:

```bash
source .venv/bin/activate
# run 'deactivate' when you are done
```

## Success Criteria

- `uv run python -c "import requests, pandas, polars; print('env ok')"` prints
  `env ok`.
- `.venv/`, `pyproject.toml`, and `uv.lock` exist at the repo root.
- `pyproject.toml` lists `requests`, `httpx`, `python-dotenv`, `boto3`,
  `google-genai`, `pandas`, `polars`, and `ipykernel`.
- A notebook opened from `student-work/week2/` runs its first cell with the
  `.venv` kernel selected (no `ModuleNotFoundError`).
- Your starter notebooks and `weather_explorer.py` are copies under
  `student-work/week2/`.

## Hints

<details>
<summary>Hint 1: uv is not found</summary>

If `uv` is not found, stop and tell the instructor. Do not switch to global
`pip` unless the instructor explicitly tells the room to do that.

</details>

<details>
<summary>Hint 2: the kernel picker does not show .venv</summary>

Confirm you ran `uv add ... ipykernel` (step 3) and that `.venv` is at the repo
root (`ls -a`). Then reopen the notebook and click **Select Kernel** again. If
it still does not appear, use the fallback in step 6: **Enter interpreter path**
and paste `.venv/bin/python`.

</details>

<details>
<summary>Hint 3: a cell says ModuleNotFoundError</summary>

You almost certainly have the wrong kernel selected. Click **Select Kernel** at
the top-right and choose the repo-root `.venv`. If a package is genuinely
missing, add it from the repo root with `uv add <package>`.

</details>
