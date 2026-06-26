# Day 3: Developer Foundations Quiz
# Score 100
## Q1: You are unsure of your repository's state. Which command do you run first?
- [x] `git status`
- [ ] `git log`
- [ ] `git commit`
- [ ] `git push`
::time=25
## Q2: What does `git add hello_data.py` do?
- [ ] Saves a permanent snapshot to the repository
- [x] Moves the change into the staging area
- [ ] Uploads the file to GitHub
- [ ] Creates a branch named `hello_data.py`
::time=25
## Q3: You changed a file, ran `git add`, and now plain `git diff` shows nothing. How do you review what you are about to commit?
- [ ] `git status --remote`
- [ ] `git log --graph`
- [x] `git diff --staged`
- [ ] `git fetch`
::time=25
## Q4: Which commit message is the best choice?
- [ ] `stuff`
- [ ] `final final`
- [ ] `changes`
- [x] `Add per-state claim totals to hello_data`
::time=25
## Q5: A change flows through Git's areas in what order?
- [x] Working directory, staging area, repository
- [ ] Repository, staging area, working directory
- [ ] Staging area, working directory, repository
- [ ] Working directory, repository, staging area
::time=25
## Q6: What does `git clone <url>` do?
- [ ] Creates a new empty local repository only
- [x] Downloads an existing repository, including history, and configures `origin`
- [ ] Stages all files in the current folder
- [ ] Deletes local changes and replaces them with GitHub
::time=25
## Q7: You have a local repo with commits. How should you create the matching GitHub repo so your history pushes cleanly?
- [ ] Add every starter file GitHub offers
- [ ] Create a second unrelated history in the browser
- [x] Create it empty, with no README or .gitignore
- [ ] Clone it before adding the remote
::time=25
## Q8: Your push is rejected because the remote has commits you do not have locally. Safest next step?
- [ ] Delete the remote repository
- [ ] Run `git init` again
- [ ] Delete the `.git` folder
- [x] Run `git pull`, integrate the remote work, then push again
::time=25
## Q9: What is the difference between `git fetch` and `git pull`?
- [x] `fetch` downloads remote commits without merging; `pull` downloads and merges
- [ ] They are identical
- [ ] `fetch` uploads; `pull` downloads
- [ ] `pull` works only on the first day, `fetch` after
::time=25
## Q10: You add `.env` to `.gitignore`, but `git status` still shows `.env`. Most likely reason?
- [ ] `.gitignore` only works on GitHub, not locally
- [x] `.env` was already tracked before you added it to `.gitignore`
- [ ] You need to restart the terminal
- [ ] `.gitignore` deletes the file from disk
::time=25
## Q11: On the GitHub free tier, what protects your Codespaces core-hours?
- [ ] Nothing; they never run out
- [ ] Committing more often
- [x] Stopping a Codespace when you are not using it
- [ ] Deleting your repository
::time=25

## Q12: Which two tools, used together, give you both an isolated environment and package management?
- [ ] conda alone
- [ ] uv alone
- [x] venv plus pip
- [ ] git plus pip
::time=25
