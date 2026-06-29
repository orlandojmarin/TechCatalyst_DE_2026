# Lab A: Python Environments With UV

**Module:** Developer foundations, Day 3  
**Format:** Pairs, driver and navigator, swap every 20 minutes  
**Estimated time:** 60-75 minutes  
**Environment:** Linux terminal plus VS Code

> [!WARNING]
> **AI-Free Zone.** Type the commands yourself. The goal is to understand what the environment tool is doing, not just to finish quickly.

## Goal

By the end of this lab, you can:

- Explain the two jobs of Python tooling: isolate the environment and manage packages.
- Create a local Python project with `uv init`.
- Add packages with `uv add`.
- Run code inside the project with `uv run`.
- Rebuild the environment with `uv sync`.
- Compare UV to venv plus pip at a high level.

## Why This Matters

Every data engineering project has dependencies. If your teammate cannot recreate your environment, the project is fragile. UV gives us a modern project workflow with `pyproject.toml`, `.python-version`, `.venv`, and `uv.lock`.

## Part 0: Check Your Machine

Open VS Code and use the integrated terminal, or use a regular Linux terminal.

Run:

```bash
pwd
python3 --version
git --version
uv --version
```

If `uv --version` fails, tell the instructor. If UV is installed by class setup, continue. If it is not installed, the instructor can install it or provide the install command from the official UV docs.

Expected:

```text
Python 3.11 or higher
git version ...
uv ...
```

## Part 1: The Two Jobs

Every Python environment tool does one or both jobs:

| Job | Meaning | Why it matters |
| :--- | :--- | :--- |
| Isolate environment | Give this project its own Python packages | One project does not break another |
| Manage packages | Install, remove, and record dependencies | Teammates can rebuild the project |

Comparison:

| Tool | Isolates | Manages packages | Notes |
| :--- | :--- | :--- | :--- |
| `venv` | Yes | No | Built into Python |
| `pip` | No | Yes | Installs packages into the active environment |
| `uv` | Yes | Yes | Project workflow with lock file |
| `conda` | Yes | Yes | Useful for scientific stacks and non-Python binaries, optional today |

Say this to your partner before moving on:

> venv isolates, pip installs, UV does both for a project.

## Part 2: Create a UV Project

Create a sandbox project outside any existing repo:

```bash
mkdir -p ~/env-lab
cd ~/env-lab
uv init claims-uv
cd claims-uv
ls -a
```

Inspect what UV created:

```bash
cat pyproject.toml
cat .python-version
cat main.py
```

Expected files:

```text
.python-version
README.md
main.py
pyproject.toml
```

## Part 3: Add Packages

Add packages for a tiny data task:

```bash
uv add pandas requests
```

Inspect the project again:

```bash
cat pyproject.toml
ls -a
cat uv.lock | head -40
```

Notice:

- `pyproject.toml` lists the direct dependencies you asked for.
- `uv.lock` records the full resolved dependency set.
- `.venv/` is created for the project environment.

## Part 4: Run Python Without Activating

Run a quick check:

```bash
uv run python -c "import pandas as pd; import requests; print('pandas', pd.__version__); print('requests ready')"
```

Expected:

```text
pandas ...
requests ready
```

## Part 5: Write a Tiny Script

Replace `main.py` with:

```python
import pandas as pd

data = [
    {"state": "CT", "amount_usd": 1250},
    {"state": "NY", "amount_usd": 900},
    {"state": "CT", "amount_usd": 700},
]

df = pd.DataFrame(data)
totals = df.groupby("state")["amount_usd"].sum().sort_values(ascending=False)

print("Claim totals by state:")
print(totals)
```

Run it:

```bash
uv run python main.py
```

Expected:

```text
Claim totals by state:
state
CT    1950
NY     900
Name: amount_usd, dtype: int64
```

## Part 6: Rebuild From the Lock

Pretend you just cloned the project and do not have an environment:

```bash
rm -rf .venv
uv sync
uv run python main.py
```

Expected: the script still runs.

Key distinction:

- `uv add pandas` changes the project dependency list and updates the lock.
- `uv sync` rebuilds the environment from the existing lock.

## Part 7: Compare With venv Plus pip

Create a small venv comparison:

```bash
cd ~/env-lab
python3 -m venv claims-venv
source claims-venv/bin/activate
pip install pandas requests
pip freeze > requirements.txt
python -c "import pandas as pd; print(pd.__version__)"
deactivate
rm -rf claims-venv
```

Discussion:

- Where did venv store the environment?
- What file recorded dependencies?
- Which workflow had a lock file?
- Which workflow would you rather hand to a teammate?

## Reflection

Write answers in your notes:

1. What are the two jobs of Python environment tooling?
2. What does `uv add` do?
3. What does `uv sync` do?
4. Why do we commit `pyproject.toml` and `uv.lock` but not `.venv/`?
5. When might a team still use venv plus pip?

## Cleanup

```bash
cd ~
rm -rf ~/env-lab
```

## Success Criteria

- `uv --version` works.
- `uv init claims-uv` created a project.
- `uv add pandas requests` updated `pyproject.toml` and created `uv.lock`.
- `uv run python main.py` runs successfully.
- `uv sync` rebuilds the environment after deleting `.venv`.
- You can explain `uv add` versus `uv sync`.
