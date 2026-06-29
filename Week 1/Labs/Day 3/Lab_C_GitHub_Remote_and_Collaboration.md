# Lab C: GitHub Remote and Collaboration

**Module:** Developer foundations, Day 3  
**Format:** Pairs  
**Estimated time:** 90-120 minutes  
**Environment:** Local Linux terminal, VS Code, Chrome, GitHub

> [!WARNING]
> **AI-Free Zone.** Type each Git command yourself. The point is to understand local and remote repositories before tools automate the workflow.

## Goal

By the end of this lab, you can:

- Configure your Git identity and authenticate to GitHub with SSH.
- Create an empty GitHub repository.
- Connect a local repo to GitHub with `git remote`.
- Push local commits to GitHub.
- Pull a change made on GitHub back to your local repo.
- Clone a second copy of a repository.
- Explain `fetch`, `merge`, and `pull`.
- Create a branch, push it, open a pull request, merge it, and sync local `main`.

## Before You Start

This lab does not continue from Lab B. You will build a brand new repository from scratch so everyone starts clean. You need a GitHub account, your VM terminal, and Chrome. Work top to bottom: configure Git, create a fresh local repo, then connect it to GitHub.

## Part 0: Configure Git and Authenticate with GitHub

Do this once per machine. Your VM does not yet know who you are or how to talk to GitHub without a password prompt. SSH is the recommended approach because it lets `git push` and `git pull` work without re-entering credentials. If SSH is blocked on your network, use the HTTPS fallback at the end of this part.

### Step 1: Configure your Git identity

Use the same email as your GitHub account. On a fresh machine, set your name, email, and two helpful defaults.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

Confirm:

```bash
git config --global --list
```

### Step 2: Generate an SSH key

Use the modern `ed25519` algorithm:

```bash
ssh-keygen -t ed25519 -C "you@example.com"
```

Press Enter to accept the default path (`~/.ssh/id_ed25519`). You can add a passphrase or leave it empty.

### Step 3: Add the key to the SSH agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

The agent runs per terminal session. If a later push asks for your passphrase again or fails to authenticate, run these two lines again in the new terminal.

### Step 4: Copy your public key

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire line of output. It starts with `ssh-ed25519`. Then in Chrome:

1. Go to GitHub, then Settings, then SSH and GPG keys.
2. Click New SSH key.
3. Title it something clear, such as `techcatalyst-vm`, and paste the key.
4. Click Add SSH key.

### Step 5: Test the connection

```bash
ssh -T git@github.com
```

The first time, type `yes` to trust GitHub's fingerprint. You should then see:

```text
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```

That message means success. SSH gives you Git access, not a shell on GitHub.

Checkpoint: `git config --global --list` shows your name and email, and `ssh -T git@github.com` greets you by username. You will use SSH URLs (`git@github.com:...`) in Part 3 and Part 5.

<details>
<summary>HTTPS fallback (only if SSH is blocked)</summary>

Some networks block the SSH port. If `ssh -T git@github.com` times out, use HTTPS with a Personal Access Token instead. Keep the identity config from Step 1, use the `https://github.com/...` URLs in Part 3 and Part 5, and when Git asks for a password, paste a token, not your account password. See `GitHub Troubleshooting.md` for the token steps, and ask the instructor before continuing.

</details>

## Part 1: Create a Local Repo from Scratch

Start clean so you do not end up with a repo inside another repo. That happens when you run `git init` inside a folder that is already tracked by Git, and it causes confusing errors later. First confirm you are not already inside a repository:

```bash
cd ~/Desktop
git status
```

If you see `fatal: not a git repository`, you are in the right place. If `git status` shows branch and commit information instead, you are inside an existing repo (for example a course folder you cloned earlier). Do not continue here. Stay on the Desktop, which should not be a repo, and check again.

Create a fresh project folder and initialize it:

```bash
mkdir techcatalyst-2026-<yourname>
cd techcatalyst-2026-<yourname>
git init
```

Add a README and make two commits so the repo has history to push:

```bash
echo "# TechCatalyst DE 2026" > README.md
echo "My working repo, built by hand with the Linux terminal, VS Code, Git, and GitHub." >> README.md
git add README.md
git commit -m "Add README"

echo "Day 3: learning Git remotes and collaboration." >> README.md
git add README.md
git commit -m "Add Day 3 note"
```

Confirm:

```bash
git status
git log --oneline
```

Expected:

- You are on `main`.
- Your working tree is clean.
- You have two local commits.

## Part 2: Create an Empty GitHub Repo

In Chrome:

1. Go to [github.com](https://github.com) and sign in to your own personal GitHub account. Confirm your username in the top right corner before continuing. Do not use a shared, classroom, or someone else's account, and make sure it is the same account whose email you set in Part 0.
2. Click **+**, then **New repository**.
3. Repository name: `techcatalyst-2026-<yourname>`.
4. Choose public or private based on instructor guidance.
5. Do **not** add a README, `.gitignore`, or license. Your local repo already has files and commits.
6. Click **Create repository**.

On the next page, click the green **Code** button and copy the **SSH** URL (it starts with `git@github.com:`). Use the HTTPS URL only if you used the HTTPS fallback in Part 0.

## Part 3: Connect Local to Remote

In your local terminal:

```bash
git remote -v
git remote add origin git@github.com:YOUR-USERNAME/techcatalyst-2026-<yourname>.git
git remote -v
git branch -M main
git push -u origin main
```

HTTPS fallback users: use the `https://github.com/YOUR-USERNAME/...` URL instead.

Refresh GitHub. Your files should appear.

If authentication fails, recheck Part 0 (especially `ssh -T git@github.com`), then use `GitHub Troubleshooting.md`, and ask the instructor before trying random commands.

## Part 4: Pull a Web Edit

On GitHub:

1. Open `README.md`.
2. Click the pencil edit button.
3. Add this line at the bottom:

   ```markdown
   Remote edit: changed directly on GitHub.
   ```

4. Commit the change to `main`.

In your terminal, prove local is behind:

```bash
git log --oneline
tail -n 5 README.md
```

Pull:

```bash
git pull
git log --oneline
tail -n 5 README.md
```

Checkpoint: the web edit is now local.

## Part 5: Clone a Second Copy

Move out of the original repo and clone:

```bash
cd ~/Desktop
git clone git@github.com:YOUR-USERNAME/techcatalyst-2026-<yourname>.git techcatalyst-clone
cd techcatalyst-clone
git log --oneline
git remote -v
```

HTTPS fallback users: clone with the `https://github.com/YOUR-USERNAME/...` URL instead.

Checkpoint: `techcatalyst-clone` has the same history.

## Part 6: Fetch Versus Pull

In `techcatalyst-clone`, make and push a change:

```bash
echo "from the clone" > clone-note.md
git add clone-note.md
git commit -m "Add clone note"
git push
```

Return to the original repo:

```bash
cd ~/Desktop/techcatalyst-2026-<yourname>
git fetch
git status
git log --oneline origin/main
git merge origin/main
```

Explain to your partner:

- `fetch` downloads remote commits without changing your files.
- `merge origin/main` integrates fetched commits.
- `pull` is fetch plus merge.

## Part 7: Branch and Pull Request

Start from local `main`:

```bash
git switch main
git pull
git status
git switch -c add-about-section
```

Edit `README.md` and add:

```markdown
## About this repo

My TechCatalyst DE 2026 working repo. Built by hand with Linux terminal, VS Code, UV, Git, and GitHub.
```

Commit and push the branch:

```bash
git add README.md
git diff --staged
git commit -m "Add About section to README"
git push -u origin add-about-section
```

On GitHub:

1. Open the pull request prompt.
2. Confirm the PR merges `add-about-section` into `main`.
3. Add a title and short description.
4. Open the **Files changed** tab.
5. Review the diff.
6. Merge the pull request.

Back in terminal:

```bash
git switch main
git pull
cat README.md
git branch -d add-about-section
git branch
```

Checkpoint:

- The About section appears on local `main`.
- The feature branch is deleted locally.

## Partner Review

If time allows:

1. Swap repo URLs.
2. Open a partner pull request before it is merged.
3. Leave one useful review comment.
4. Do not approve unless you actually reviewed the diff.

## Questions

Write short answers:

1. What is the difference between local and remote?
2. What does `git push` do?
3. What does `git pull` do?
4. Why review the diff before merging a pull request?
5. Why do teams use branches instead of pushing directly to `main`?

## Success Criteria

- Git identity is set and `ssh -T git@github.com` authenticates you (or HTTPS works if you used the fallback).
- GitHub repo exists and contains your README and commits.
- Local repo has `origin` configured.
- You pulled a web edit.
- You cloned a second copy.
- You can explain fetch, merge, and pull.
- You opened and merged a pull request.
- Local `main` is up to date after the PR merge.

## Next

Choose an optional portfolio lab:

- `Lab_D_Profile_Page.md`
- `Lab_E_GitHub_Pages.md`
