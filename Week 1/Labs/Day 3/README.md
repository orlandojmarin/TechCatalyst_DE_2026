# Week 1 · Day 3: Lab

**Theme:** Developer foundations — Python environments, then a Git and GitHub deep dive (plus VS Code and Codespaces)
**Format:** Five guided labs in pairs (navigator and driver, swap every 20 min). Lab A is the new hands-on environments lab; Labs B and C are the Git/GitHub core; Labs D and E are the fun ones — the profile page and your live GitHub Pages site.

> **AI-Free Zone (Weeks 1 to 4).** Type every command yourself. No Copilot, no LLM-generated code, SQL, or Git commands. Read the errors; debug first.

## Lab Index

### Provided files

| File | What it is |
| :--- | :--- |
| [README.md](README.md) *(this file)* | Lab index, schedule, and deliverables |
| [Lab_A_Python_Environments.md](Lab_A_Python_Environments.md) | **Lab A (NEW):** environments & package management — conda, venv + pip, and **uv** (the focus), hands-on side-by-side |
| [Lab_B_Git_The_Solo_Cycle.md](Lab_B_Git_The_Solo_Cycle.md) | Lab B: build your course repo, the venv + pip baseline, read data, and the local Git cycle (status, add, diff, commit, log) |
| [Lab_C_GitHub_Remote_and_Collaboration.md](Lab_C_GitHub_Remote_and_Collaboration.md) | Lab C: connect to GitHub — push, pull, clone, fetch (with the 403 fix), then branch, PR, and merge |
| [Lab_D_Profile_Page.md](Lab_D_Profile_Page.md) | Lab D (Fun Lab): build your GitHub profile / personal branding page |
| [Lab_E_GitHub_Pages.md](Lab_E_GitHub_Pages.md) | Lab E (Fun Lab): publish a live GitHub Pages welcome + blog site (HTML/CSS theme provided) |
| [github-pages-template/](github-pages-template/) | Starter theme for Lab E: `index.html`, `style.css`, `posts/first-post.html` |
| [quiz/Knowledge_Check.md](quiz/Knowledge_Check.md) | Ungraded 12-question check for the wrap-up |
| [quiz/Day3_Quiz_MarkdownMash.md](quiz/Day3_Quiz_MarkdownMash.md) | The same 12 questions in Markdown Mash format for the live game |
| [quiz/Day3_Kickoff_DE_Fundamentals_Quiz.md](quiz/Day3_Kickoff_DE_Fundamentals_Quiz.md) | Optional 10-question kickoff/retrieval quiz if you want to reconnect to Day 1 data-engineering fundamentals before the developer-tools labs |
| [GitHub Troubleshooting.md](GitHub%20Troubleshooting.md) | Common auth, Codespace, and Git errors with fixes |
| [Student_Resources.md](Student_Resources.md) | VS Code, Codespaces budget, conda/venv/pip/uv, and Git references |
| [data/hartford_claims_sample.csv](data/hartford_claims_sample.csv) | 12-row sample of Hartford-style claims data for Lab B |
| [solutions/](solutions/) | Lab A, B, and C solution keys for instructor review or post-lab release |

### Suggested timing

| Time | Block |
| :--- | :--- |
| 10:15 to 11:15 | **Lab A: Python environments & package management** (about 50–60 min) |
| 1:00 to 1:45 | Lab B: Git, the solo cycle (about 45 min) |
| 1:45 to 2:45 | Lab C: GitHub — remote & collaboration (about 60 min; Section 2 is time-permitting) |
| 2:45 to 3:00 | Labs D & E (Fun Labs): your GitHub profile page and GitHub Pages site (start; finish as homework) |

*(Times are a guide. Lab A is the new centerpiece that fixes yesterday's environment confusion — protect the uv section. This cohort knows Git basics, so B runs fast; in Lab C, Parts 1–4 are the must-do core and the branch/PR section is the Week 2 on-ramp.)*

### Deliverables

| # | Deliverable | Format | From | Due |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Notes answering the Lab A reflection (the two jobs; `uv add` vs `uv sync`; when to use each tool) | Notes | Lab A | End of day |
| 2 | Pushed `techcatalyst-2026-<yourname>` repo with `hello_data.py`, `data/hartford_claims_sample.csv`, `requirements.txt`, `.gitignore` | GitHub repo | Lab B + C | End of day |
| 3 | Completed Part 5 verification checklist committed into `README.md`; at least 3 commits in `git log --oneline`, partner-verified | Markdown + Git history | Lab B | End of day |
| 4 | A clone of your repo verified to match (`journal-clone`) | Git history | Lab C | End of day |
| 5 | *(time-permitting)* About section merged into `main` via a pull request; branch deleted; Q1–Q5 noted | Notes + repo | Lab C | End of day |
| 6 | A GitHub profile page live at `github.com/<username>` (the `<username>/<username>` repo) | GitHub profile | Lab D | End of day / homework |
| 7 | A live GitHub Pages site at `https://<username>.github.io/<repo>/` with a welcome page and first post | GitHub Pages site | Lab E | End of day / homework |

---

## How the day fits together

**Lab A** is new and comes first: students run conda, venv + pip, and **uv** back-to-back on the same tiny task so the differences they were confused about yesterday become concrete — conda's careful-but-heavy solver, venv's "it's just a folder" simplicity, and uv's one-tool projects with a `pyproject.toml` and automatic lock file. It's a throwaway sandbox; the course baseline stays venv + pip.

**Lab B** is **entirely local** to the Codespace: students build their real course repo (using the venv + pip baseline), read the sample data with a hand-written script, and practice the solo Git cycle (status, add, diff, commit, log) without touching GitHub.

**Lab C** **connects local to remote**: push, pull, clone, and fetch/merge (Section 1), then branch, pull request, review, and merge (Section 2), the on-ramp to the shared-repo collaboration and merge conflicts covered in full on Week 2 Day 1.

**Lab D** (Fun Lab) turns everything into a **GitHub profile page** — a personal branding page students grow every week of the program.

**Lab E** (Fun Lab) goes one step further: students publish a real **GitHub Pages website** — a themed welcome page plus a mini-blog — from a provided HTML/CSS template. Like the profile, it's a living portfolio they feed with one short post a week, all program long. Both fun labs reinforce today's repo/commit skills with zero Codespace cost.

Use the optional kickoff quiz only if the class needs a short bridge back to Day 1 vocabulary. The main Day 3 assessment is the Git/environment knowledge check at the end.

## Troubleshooting

See `GitHub Troubleshooting.md` in this folder. The most common live issues: in Lab A, `conda activate` needs `conda init bash` + a fresh terminal, and `uv` needs `source $HOME/.local/bin/env` after install; in Lab C, the Codespaces 403 on first push (handled with Path A and Path B). Stuck more than 10 minutes? Raise a hand; debugging together is the point, but so is finishing.
