# GitHub and Local Setup Troubleshooting

Use this guide for the Linux terminal + VS Code environment (Ubuntu VM or local Linux). It assumes Git, UV, and GitHub.

## Start Here

Run these commands before guessing:

```bash
pwd
git status
git remote -v
git branch
python3 --version
uv --version
```

## I Am in the Wrong Folder

Symptom:

```text
fatal: not a git repository
```

Fix:

```bash
cd ~/techcatalyst-work/techcatalyst-2026-<yourname>
pwd
git status
```

## Git Does Not Know Who I Am

Symptom:

```text
Author identity unknown
```

Fix:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the email connected to your GitHub account if possible.

## `uv` Is Not Found

Symptom:

```text
uv: command not found
```

Fix:

1. Ask the instructor whether UV was installed on the class machine image.
2. If the class setup includes UV but the shell cannot see it, open a new terminal.
3. If UV must be installed live, use the official UV docs or instructor-provided command.

## `uv run python hello_data.py` Cannot Find the CSV

Symptom:

```text
FileNotFoundError: data/hartford_claims_sample.csv
```

Fix:

```bash
pwd
ls
ls data
```

You should be in the project root, and `data/hartford_claims_sample.csv` should exist.

## `.venv/` Appears in Git Status

Symptom:

```text
.venv/
```

Fix:

1. Add `.venv/` to `.gitignore`.
2. If `.venv/` is only untracked, it will disappear from `git status`.
3. If you already staged it, unstage it:

```bash
git restore --staged .venv
git status
```

## I Created the GitHub Repo With a README

Problem: Your local repo and GitHub repo both have separate first commits.

Preferred fix for class: create a new empty GitHub repo without README, `.gitignore`, or license.

If the instructor wants to keep the repo, you may need:

```bash
git pull origin main --allow-unrelated-histories
```

Only use this with instructor guidance because it can create conflicts.

## Push Is Rejected

Symptom:

```text
rejected
fetch first
```

Fix:

```bash
git pull
git status
git push
```

If there are conflicts, stop and ask the instructor.

## Authentication Fails

Symptoms:

```text
Authentication failed
Permission denied
```

Fix options:

- Sign in to GitHub in VS Code.
- Use GitHub CLI if installed and configured by class setup.
- Use a Personal Access Token only if the instructor directs you.

Do not paste tokens into shared screens or commit them.

## Find Conflict Markers

After a conflicted pull or merge:

```bash
git status
```

Open the listed files and search for:

```text
<<<<<<<
=======
>>>>>>>
```

Resolve the file, then:

```bash
git add <resolved-file>
git commit
```

## Safe Investigation Commands

```bash
git status
git diff
git diff --staged
git log --oneline --decorate --graph --all -10
git remote -v
```

When in doubt, read before writing.
