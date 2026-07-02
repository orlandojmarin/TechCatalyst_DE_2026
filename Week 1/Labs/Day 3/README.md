# Week 1 · Day 3 · Lab

**Theme:** Developer foundations: Linux terminal, VS Code, Python environments with UV, Git, and GitHub
**Format:** Guided labs in pairs (driver/navigator) with built-in breaks for pacing
**Environment:** Linux terminal, VS Code, Chrome, GitHub. UV is the primary Python tool.

> [!WARNING]
> **AI-Free Zone (Weeks 1 to 4).** Type every command yourself. No Copilot, no LLM-generated code, SQL, or Git commands. Read the errors; debug first.

## Lab Index

### Provided files

| File | What it is |
| :--- | :--- |
| [README.md](README.md) *(this file)* | Lab index, schedule, and deliverables |
| [Lab_A_Python_Environments.md](Lab_A_Python_Environments.md) | **Lab A:** Python environments and package management (focus on `uv`: init, add, sync, run), with venv + pip comparison |
| [Lab_B_Git_The_Solo_Cycle.md](Lab_B_Git_The_Solo_Cycle.md) | **Lab B:** Create local course repo, add sample data, write a Python script, practice the Git solo cycle (status, add, diff, commit, log) |
| [Lab_C_GitHub_Remote_and_Collaboration.md](Lab_C_GitHub_Remote_and_Collaboration.md) | **Lab C:** Connect local work to GitHub (remote, push, pull, clone, fetch), then branch, PR, review, merge |
| [Lab_D_Profile_Page.md](Lab_D_Profile_Page.md) | **Lab D (optional/fun):** Build your GitHub profile README page |
| [Lab_E_GitHub_Pages.md](Lab_E_GitHub_Pages.md) | **Lab E (optional/fun):** Publish a live GitHub Pages site from the provided template |
| [github-pages-template/](github-pages-template/) | Starter HTML/CSS theme for Lab E |
| [data/hartford_claims_sample.csv](data/hartford_claims_sample.csv) | Sample claims data for Lab B |
| [GitHub Troubleshooting.md](GitHub%20Troubleshooting.md) | Common terminal, Git, GitHub, and path errors with fixes |
| [Student_Resources.md](Student_Resources.md) | VS Code terminal, UV, venv, Git, and GitHub references |
| [solutions/](solutions/) | Instructor solution keys for Labs A, B, C |
| [quiz/](quiz/) | Knowledge checks (Markdown Mash + plain) and optional kickoff quiz |

### Suggested timing

| Time | Block |
| :--- | :--- |
| 10:15 to 11:15 | Lab A: Python environments with UV (60-75 min) |
|  | Break and reset (10-15 min) |
|  | Lab B: Local repo, terminal, script, and Git solo cycle (75-90 min) |
|  | Lunch or longer break |
|  | Lab C Section 1: GitHub remote (push, pull, clone, fetch) (60-75 min) |
|  | Break and troubleshooting (10-15 min) |
|  | Lab C Section 2: Branch, PR, review, merge (45-60 min) |
|  | Optional Labs D/E, quiz, debrief (as time allows) |

Times are a guide. Protect Lab A (UV focus). Labs B and C Section 1 are the core must-dos. Use Labs D and E for fast finishers or homework.

### Deliverables

| # | Deliverable | Source | Format |
| :--- | :--- | :--- | :--- |
| 1 | Notes answering the Lab A reflection questions (two jobs, uv add vs sync, when to use tools) | Lab A | Notes |
| 2 | Local `techcatalyst-2026-<yourname>` project with `pyproject.toml`, script, data, `.gitignore`, and Git history | Lab B | Local folder |
| 3 | GitHub repo connected and pushed from the local project | Lab C | GitHub repo |
| 4 | Verified clone (`journal-clone`) matching the original | Lab C | Local folder |
| 5 | About section added via PR and merged to main | Lab C | GitHub PR + local sync |
| 6 | *(optional)* GitHub profile page or live Pages site | Lab D or E | GitHub |

## How the day fits together

**Lab A** removes environment confusion from Day 2. Students run a small project with `uv`, then compare the workflow to venv + pip.

**Lab B** stays completely local: create the course repo, use the terminal to explore, run Python against the sample data, and build the habit of constant `git status` / `git diff` / commit.

**Lab C** connects the local work to GitHub: first the solo remote loop (push / pull / clone / fetch), then the collaboration loop (branch / PR / merge). This is the foundation for Week 2 team work.

**Labs D and E** are low-stakes portfolio builders. They reinforce the Git flow and give students something public to show.

## Environment notes

- Use the Linux terminal inside VS Code or a standalone terminal.
- Run commands from the project folder you create (`~/techcatalyst-work/techcatalyst-2026-<yourname>`).
- UV must be available (`uv --version`). The classroom Linux setup provides it.
- GitHub authentication is required for Lab C (HTTPS or SSH as configured in class).
- Everything runs in the local Linux terminal for this day.

## Troubleshooting

See [GitHub Troubleshooting.md](GitHub%20Troubleshooting.md). Most issues are:
- Running commands from the wrong directory
- Missing `git config` identity
- GitHub auth not set up for push
- Forgetting to `cd` into the project before `uv` or `git` commands

Raise a hand early if stuck more than a few minutes. Debugging is part of the lab.
