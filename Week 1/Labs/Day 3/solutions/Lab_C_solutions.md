# Lab C Solution Key: GitHub Remote and Collaboration

Share after the lab. Reward correct reasoning over exact wording.

## Section 1: Remote Sync

### Creating the Remote

- Students should create an empty GitHub repo, with no README, `.gitignore`, or license.
- The local repo already has commits, so an empty remote avoids unrelated history issues.
- `git remote -v` should show `origin` after `git remote add origin ...`.
- `git push -u origin main` publishes the local branch and sets upstream tracking.

### Web Edit and Pull

- The web edit exists only on GitHub until students run `git pull`.
- This is the central local-versus-remote lesson: GitHub and the local machine are separate repos that sync only when commanded.

### Fetch Versus Pull

- `git fetch` downloads remote commits into the remote-tracking branch, such as `origin/main`, but does not change working files.
- `git merge origin/main` integrates fetched commits.
- `git pull` is fetch plus merge.

Acceptable short answer: "fetch looks, merge integrates, pull does both."

## Common Issues

- Push rejected with "fetch first" or "behind": the remote has commits the student does not have. Correct move: `git pull`, resolve if needed, then push.
- Student edits on GitHub and expects the local folder to update automatically. Reinforce: nothing syncs without push or pull.
- Clone path confusion: students may be in `journal-clone` when they mean to be in the original repo. Always run `pwd`.
- Authentication failure: use VS Code GitHub sign-in, GitHub CLI if configured, or instructor-guided token setup.

## Section 2: Branch, PR, Merge

Reference answers:

- **Q1:** Local is the repo on your machine. Remote is the GitHub copy.
- **Q2:** `git push` sends local commits to the remote.
- **Q3:** `git pull` gets remote commits and merges them into the current local branch.
- **Q4:** A pull request diff shows exactly what changed, which makes review faster and safer than rereading the whole file.
- **Q5:** Teams use branches so work can be reviewed before changing `main`.

## Instructor Notes

- Keep this as a clean PR flow. Save merge conflicts for Week 2 Day 1.
- If students finish early, have them review a partner PR or explain fetch versus pull at the board.
