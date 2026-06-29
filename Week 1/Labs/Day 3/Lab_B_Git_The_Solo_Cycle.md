# Lab B: Local Project, Terminal, Python, and Git

**Module:** Developer foundations, Day 3  
**Format:** Pairs, driver and navigator, swap every 20 minutes  
**Estimated time:** 75-90 minutes  
**Environment:** Linux terminal plus VS Code

> [!WARNING]
> **AI-Free Zone.** Type every command yourself. Read the output before moving to the next command.

## Goal

By the end of this lab, you can:

- Create a local course project folder.
- Open it in VS Code.
- Use UV for project setup and package management.
- Read a sample claims dataset with a Python script.
- Use the Git solo cycle: `status`, `add`, `diff`, `commit`, and `log`.
- Use `.gitignore` so environments, caches, logs, and secrets do not get committed.

## Part 1: Create the Local Project

Open a Linux terminal.

```bash
mkdir -p ~/techcatalyst-work
cd ~/techcatalyst-work
mkdir techcatalyst-2026-<yourname>
cd techcatalyst-2026-<yourname>
pwd
```

Open the folder in VS Code:

```bash
code .
```

If `code .` is unavailable, open VS Code manually and choose **File**, then **Open Folder**, then select your project folder.

## Part 2: Initialize Git and UV

In the project terminal:

```bash
git init
uv init --bare
uv add pandas requests
```

Inspect what changed:

```bash
ls -a
cat pyproject.toml
test -f uv.lock && echo "uv.lock exists"
```

Expected:

```text
pyproject.toml
uv.lock
.venv
```

## Part 3: Add the Sample Dataset

Create a `data` folder:

```bash
mkdir -p data
```

Copy the sample CSV from this lab folder into your project. If you are running commands from the repository root, use:

```bash
cp "Week 1/Labs/Day 3/data/hartford_claims_sample.csv" ~/techcatalyst-work/techcatalyst-2026-<yourname>/data/
```

If you are already inside the lab folder, use:

```bash
cp data/hartford_claims_sample.csv ~/techcatalyst-work/techcatalyst-2026-<yourname>/data/
```

Verify:

```bash
ls -lh data/
head -n 5 data/hartford_claims_sample.csv
wc -l data/hartford_claims_sample.csv
```

## Part 4: Write `hello_data.py`

Create `hello_data.py` in VS Code and type:

```python
import pandas as pd
import requests

print(f"pandas {pd.__version__} ready")

df = pd.read_csv("data/hartford_claims_sample.csv")
print(f"rows: {len(df)}")
print(f"columns: {list(df.columns)}")

by_state = df.groupby("state")["amount_usd"].sum().sort_values(ascending=False)
print("Total claim amount by state:")
print(by_state)

response = requests.get("https://api.github.com", timeout=10)
print(f"GitHub API status: {response.status_code}")
```

Run it with UV:

```bash
uv run python hello_data.py
```

Expected:

```text
pandas ... ready
rows: 12
columns: [...]
Total claim amount by state:
...
GitHub API status: 200
```

If the GitHub API status is not `200`, keep going. The pandas and CSV parts are the main goal.

## Part 5: Add `.gitignore`

Create `.gitignore`:

```gitignore
.venv/
__pycache__/
.env
*.log
.DS_Store
```

Check Git status:

```bash
git status
```

`.venv/` should not appear.

## Part 6: Make Focused Commits

Configure Git identity if needed:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

First commit:

```bash
git add .gitignore pyproject.toml uv.lock
git diff --staged
git commit -m "Set up Python project with UV"
```

Second commit:

```bash
git add data/hartford_claims_sample.csv hello_data.py
git diff --staged
git commit -m "Add claims data script"
```

Third commit:

```bash
cat > README.md <<'EOF'
# TechCatalyst 2026 Working Repo

This repo contains my class work for the TechCatalyst Data Engineering 2026 bootcamp.

## Day 3 Setup

- Local Linux terminal
- VS Code
- UV Python project
- Git local history
EOF

git add README.md
git diff --staged
git commit -m "Document day 3 setup"
```

Review history:

```bash
git log --oneline
git status
```

Expected:

- At least 3 commits.
- Working tree clean.
- `.venv/` not tracked.

## Part 7: Verify With a Partner

Add this checklist to `README.md`, check each item, then commit it:

```markdown
## Verification Checklist

- [ ] `uv run python hello_data.py` runs
- [ ] `pyproject.toml` exists
- [ ] `uv.lock` exists
- [ ] `.venv/` does not appear in `git status`
- [ ] `data/hartford_claims_sample.csv` exists
- [ ] At least 3 commits appear in `git log --oneline`
- [ ] A partner verified my setup
```

Commit:

```bash
git add README.md
git commit -m "Add setup verification checklist"
git log --oneline
```

## Challenge

Choose one:

1. Add a function that prints counts by claim `status`, then commit it.
2. Add a fake `.env` file and confirm Git ignores it.
3. Use terminal commands to count the CSV rows and unique states before running Python.
4. Add a `scripts/` folder and move repeated commands into a small shell script.

## Success Criteria

- Local project exists under `~/techcatalyst-work/`.
- Project opens in VS Code.
- UV environment works.
- `hello_data.py` runs.
- Git history has at least 4 commits after the verification checklist.
- `.venv/` is ignored.

## Next

Move to `Lab_C_GitHub_Remote_and_Collaboration.md` to publish this local repo to GitHub and practice remote workflows.
