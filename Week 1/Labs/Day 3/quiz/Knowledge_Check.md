# Day 3 Knowledge Check

**Format:** 12-question ungraded check · **Use:** final 10 to 15 minutes, or as a self-check · **Scoring:** 1 point each

> **Running it live?** Use `Day3_Quiz_MarkdownMash.md` (same 12 questions in Markdown Mash format, with per-question timers and answer positions rebalanced for the game). This file is the explained answer key for review and self-study.

Scope is the Day 3 solo workflow (environments and Git through the remote). Branching, merge conflicts, and pull requests are covered in Week 2 Day 1; they are not on this check.

---

### Q1. Which command do you run first when you are unsure of your repository's state?

- A. `git log`
- B. `git status`
- C. `git commit`
- D. `git push`

**Answer:** B. `git status` shows the branch, staged and unstaged changes, untracked files, and useful next steps.

### Q2. What does `git add hello_data.py` do?

- A. Saves a permanent snapshot to the repository
- B. Uploads the file to GitHub
- C. Moves the change into the staging area
- D. Creates a branch named `hello_data.py`

**Answer:** C. `git add` stages a change; the permanent snapshot happens at `git commit`.

### Q3. You changed a file, ran `git add`, and now plain `git diff` shows nothing. How do you review what you are about to commit?

- A. `git diff --staged`
- B. `git status --remote`
- C. `git log --graph`
- D. `git fetch`

**Answer:** A. `git diff` shows unstaged changes; `git diff --staged` shows what is staged and about to be committed.

### Q4. Which commit message is the best choice?

- A. `stuff`
- B. `final final`
- C. `changes`
- D. `Add per-state claim totals to hello_data`

**Answer:** D. Good messages are specific, imperative, and readable in history.

### Q5. A change flows through Git's areas in what order?

- A. Repository, staging area, working directory
- B. Staging area, working directory, repository
- C. Working directory, staging area, repository
- D. Working directory, repository, staging area

**Answer:** C. Edit in the working directory, stage with `git add`, save with `git commit`.

### Q6. What does `git clone <url>` do?

- A. Creates a new empty local repository only
- B. Downloads an existing repository, including history, and configures `origin`
- C. Stages all files in the current folder
- D. Deletes local changes and replaces them with GitHub

**Answer:** B. Clone copies the full history and wires up the remote automatically.

### Q7. You already have a local repo with commits. How should you create the matching GitHub repo so your history pushes cleanly?

- A. Create it empty, with no README or .gitignore
- B. Add every starter file GitHub offers
- C. Create a second unrelated history in the browser
- D. Clone it before adding the remote

**Answer:** A. An empty remote lets your existing local history push without an unrelated history getting in the way.

### Q8. Your push is rejected because the remote has commits you do not have locally. Safest next step?

- A. Delete the remote repository
- B. Run `git pull`, integrate the remote work, then push again
- C. Run `git init` again
- D. Delete the `.git` folder

**Answer:** B. Git is protecting commits you do not have. Pull first, then push.

### Q9. What is the difference between `git fetch` and `git pull`?

- A. They are identical
- B. `fetch` downloads remote commits without merging; `pull` downloads and merges
- C. `fetch` uploads; `pull` downloads
- D. `pull` works only on the first day, `fetch` after

**Answer:** B. Pull is fetch plus a merge into your current branch.

### Q10. You add `.env` to `.gitignore`, but `git status` still shows `.env`. Most likely reason?

- A. `.gitignore` only works on GitHub, not locally
- B. `.env` was already tracked before you added it to `.gitignore`
- C. You need to restart the terminal
- D. `.gitignore` deletes the file from disk

**Answer:** B. `.gitignore` only affects untracked files. An already-committed secret stays in history; rotate it.

### Q11. What habit protects your local project from environment and secret mistakes?

- A. Committing `.venv/` so GitHub stores the environment
- B. Adding `.venv/`, `.env`, caches, and logs to `.gitignore`
- C. Running `git init` again whenever something breaks
- D. Keeping all work in the Downloads folder

**Answer:** B. Local project folders can accidentally include environments, secrets, caches, and logs. `.gitignore` keeps those out of commits when they are still untracked.

### Q12. Which two tools, used together, give you both an isolated environment and package management?

- A. conda alone
- B. uv alone
- C. venv plus pip
- D. git plus pip

**Answer:** C. venv isolates the environment; pip manages packages. conda and uv each do both jobs in a single tool.

---

## Bias check

- Correct answer distribution: A=1, B=5, C=4, D=1. (Acceptable for a short formative check; rebalance if reused for grading.)
- Longest-answer pattern: mixed; the correct option is not consistently longest.
- Alignment: every question maps to a Day 3 objective (environments, the solo Git cycle, local versus remote, budget). No branching, PR, or conflict questions (those are Week 2 Day 1).
