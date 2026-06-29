# Activity 4: Git Collaboration Relay

**Module:** Week 2 Day 1, Linux CLI and Git Collaboration  
**Estimated Time:** 90 minutes  
**Difficulty:** Intermediate  
**Format:** Pairs  
**Prerequisites:** A GitHub account, the Ubuntu VM terminal, and the Git basics from Week 1 Day 3. If this is a fresh VM, complete Part 0 of Week 1 Day 3 Lab C first (Git identity and SSH). See the Setup Check below.

## Objective

In this activity, you will create, review, and resolve a real merge conflict twice. The conflict is the point of the lab.

## Setup Check Before You Start

This relay assumes Git is configured and your VM can reach GitHub without password prompts. If you have not done this on this VM yet, complete Part 0 of `Week 1/Labs/Day 3/Lab_C_GitHub_Remote_and_Collaboration.md` first: Git identity, an `ed25519` SSH key, the key added to GitHub, and `ssh -T git@github.com` greeting you by username.

Two reminders specific to today:

- Use the SSH URL (`git@github.com:...`) when you clone the relay repo, the same as in Lab C.
- Confirm `git config --global pull.rebase false` is set. This makes `git pull origin main` merge, which is what produces the conflict you will resolve. The ssh-agent runs per terminal session, so if a push stops authenticating in a new terminal, run `eval "$(ssh-agent -s)"` and `ssh-add ~/.ssh/id_ed25519` again.

## Where You Work Today, Read This First

Activities 0 to 3 had you working inside the class repository you cloned earlier (the folder open in VS Code right now). That was fine for reading files and writing notes. The Git relay must **not** happen inside that folder.

Two reasons:

- If you clone or `git init` a new repo inside the class repo, you create a confusing repo-inside-a-repo that causes errors later.
- You do not have push access to the class repo, so commits there go nowhere useful.

So before you start the relay, step out to a clean folder, exactly like Week 1 Day 3 Lab C Part 1:

```bash
cd ~/Desktop
git status
```

You should see:

```text
fatal: not a git repository (or any of the parent directories): .git
```

That `fatal` message is the result you **want** here. It confirms the Desktop is not a repo, so anything you clone into it stays separate from the class repo. If instead you see branch and commit information, you are still inside a repo. Run `pwd`, `cd ~/Desktop` again, and recheck before continuing.

You will clone your relay repo into the Desktop in Round 1. Tip: after cloning, open the relay folder as its own VS Code window with **File**, then **Open Folder**, so it is visually clear you are working in the relay repo and not the class repo. Keep a terminal open inside the relay folder for all `git` commands in this activity.

## Round 1

1. Partner A creates a new GitHub repository named `git-relay-<names>`.
2. Partner A adds Partner B as a collaborator.
3. Both partners clone the repository **into the Desktop**, not into the class repo:

   ```bash
   cd ~/Desktop
   git status   # expect: fatal: not a git repository
   git clone git@github.com:PARTNER-A-USERNAME/git-relay-<names>.git
   cd git-relay-<names>
   ```

   HTTPS fallback users clone with the `https://github.com/...` URL instead. Run every `git` command for the rest of this activity from inside this `git-relay-<names>` folder. If you are ever unsure where you are, run `pwd`.
4. Partner A creates `config.py` on `main`:

   ```python
   # pipeline configuration
   fare_threshold = 100
   max_retries = 3
   ```

5. Partner A commits and pushes to `main`.
6. Partner A creates and switches to a feature branch:

   ```bash
   git switch -c feature/raise-threshold
   ```

7. Partner A changes `fare_threshold = 250`, commits, pushes, and opens a pull request.
8. Partner B creates a branch from the current `main`:

   ```bash
   git switch main
   git pull
   git switch -c feature/lower-threshold
   ```

9. Partner B changes the same line to `fare_threshold = 50`, commits, pushes, and opens a pull request.
10. Partner B reviews Partner A's pull request, asks why `250` is the right threshold, then approves.
11. Partner A merges pull request 1 and deletes the branch.
12. Partner B resolves the conflict on their branch:

   ```bash
   git switch feature/lower-threshold
   git pull origin main
   ```

13. Partner B opens `config.py`, decides the final value, deletes every conflict marker, saves, stages, commits, and pushes.
14. Partner A reviews and merges pull request 2.

## Round 2

Swap roles. This time both partners edit `max_retries`. The final resolution must combine both intents, such as keeping one numeric value and preserving the other partner's explanatory comment.

## Expected Conflict Marker Shape

Your conflict will look similar to this:

```python
<<<<<<< HEAD
fare_threshold = 50
=======
fare_threshold = 250
>>>>>>> main
```

The final file must not contain `<<<<<<<`, `=======`, or `>>>>>>>`.

## Debrief Questions

Answer these in the Git relay repository `README.md`:

1. What did the conflict markers look like?
2. Why did pulling `main` into the branch keep `main` clean?
3. What would have prevented the conflict entirely?
4. What review comment changed how you thought about the code?

## Success Criteria

- The repository has 4 merged pull requests if your pair completed both rounds.
- The repository has at least 2 merged pull requests if your pair completed one full round.
- Every pull request has at least one review comment.
- At least 1 merge conflict was resolved.
- `main` never receives direct feature edits after the initial setup commit.
- The final `README.md` answers all 4 debrief questions.

## Hints

<details>
<summary>Hint 1: Stay on the feature branch</summary>

Resolve conflicts on the feature branch. Do not edit `main` directly to fix the conflict.

</details>

<details>
<summary>Hint 2: Search for markers</summary>

Before committing the resolution, search the file for `<<<<<<<`, `=======`, and `>>>>>>>`.

</details>

<details>
<summary>Hint 3: The final answer can be a third option</summary>

Conflict resolution is not always "choose mine" or "choose theirs." Sometimes the correct resolution combines both ideas.

</details>

<details>
<summary>Hint 4: I think I cloned inside the class repo</summary>

Run `pwd`. If the path contains the class repo (for example `.../TechCatalyst_DE_2026/...`), you are in the wrong place. Run `git rev-parse --show-toplevel` to see which repo Git thinks you are in. To recover: `cd ~/Desktop`, delete the misplaced clone if you made one (`rm -rf ~/path/to/wrong-clone` only after checking the path with `ls`), then clone again into the Desktop as shown in Round 1 step 3.

</details>

## Stretch Goals

- Add a pull request template to the repository.
- Add branch naming rules to the README.
- Add one more conflict on a README checklist and resolve it cleanly.

> Instructor notes for this activity are in `Week 2/Instructor Notes/Day 1 - Instructor Guide.md`.
