# Lab C: GitHub Remote and Collaboration

**Module:** Developer foundations, Day 3  
**Format:** Pairs  
**Estimated time:** 90-120 minutes  
**Environment:** Local Linux terminal, VS Code, Chrome, GitHub

> [!WARNING]
> **AI-Free Zone.** Type each Git command yourself. The point is to understand local and remote repositories before tools automate the workflow.

## Goal

By the end of this lab, you can:

- Create an empty GitHub repository.
- Connect a local repo to GitHub with `git remote`.
- Push local commits to GitHub.
- Pull a change made on GitHub back to your local repo.
- Clone a second copy of a repository.
- Explain `fetch`, `merge`, and `pull`.
- Create a branch, push it, open a pull request, merge it, and sync local `main`.

## Before You Start

You should have completed Lab B and have a local repo at:

```text
~/techcatalyst-work/techcatalyst-2026-<yourname>
```

Go there:

```bash
cd ~/techcatalyst-work/techcatalyst-2026-<yourname>
git status
git log --oneline
```

Expected:

- You are on `main`.
- Your working tree is clean.
- You have several local commits.

## Part 1: Create an Empty GitHub Repo

In Chrome:

1. Go to GitHub.
2. Click **+**, then **New repository**.
3. Repository name: `techcatalyst-2026-<yourname>`.
4. Choose public or private based on instructor guidance.
5. Do **not** add a README, `.gitignore`, or license. Your local repo already has files and commits.
6. Click **Create repository**.

Copy the repository URL.

## Part 2: Connect Local to Remote

In your local terminal:

```bash
git remote -v
git remote add origin https://github.com/YOUR-USERNAME/techcatalyst-2026-<yourname>.git
git remote -v
git branch -M main
git push -u origin main
```

Refresh GitHub. Your files should appear.

If authentication fails, use `GitHub Troubleshooting.md` and ask the instructor before trying random commands.

## Part 3: Pull a Web Edit

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

## Part 4: Clone a Second Copy

Move out of the original repo and clone:

```bash
cd ~/techcatalyst-work
git clone https://github.com/YOUR-USERNAME/techcatalyst-2026-<yourname>.git journal-clone
cd journal-clone
git log --oneline
git remote -v
```

Checkpoint: `journal-clone` has the same history.

## Part 5: Fetch Versus Pull

In `journal-clone`, make and push a change:

```bash
echo "from the clone" > clone-note.md
git add clone-note.md
git commit -m "Add clone note"
git push
```

Return to the original repo:

```bash
cd ~/techcatalyst-work/techcatalyst-2026-<yourname>
git fetch
git status
git log --oneline origin/main
git merge origin/main
```

Explain to your partner:

- `fetch` downloads remote commits without changing your files.
- `merge origin/main` integrates fetched commits.
- `pull` is fetch plus merge.

## Part 6: Branch and Pull Request

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

- GitHub repo exists and contains your Lab B files.
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
