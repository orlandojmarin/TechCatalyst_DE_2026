# Lab B: Solution Key (instructor) : Git, the Solo Cycle

Share after the lab. These are reference answers, not the only acceptable ones; reward correct reasoning.

## Challenge

### 1. Count open versus closed claims

A clean function added to `hello_data.py`:

```python
def claim_status_counts(df):
    counts = df["status"].value_counts()
    print("Claims by status:")
    print(counts)
    return counts
```

Call it after the per-state aggregation: `claim_status_counts(df)`. Expected for the provided 12-row sample: 6 open, 6 closed. The graded behavior is that the student reviewed the staged diff (`git diff --staged`) before committing and used a clear, imperative message such as `Add open vs closed claim count`.

### 2. The secret.env reasoning

- With `.gitignore` containing `.env` (and the student naming the file `secret.env`, note the pattern must match): if the pattern is just `.env`, then `secret.env` is **not** matched. This is a good teaching catch. A pattern of `*.env` or `secret.env` would match. Confirm whether the student's pattern actually covers the file by checking `git status`.
- The key reasoning: **`.gitignore` only affects untracked files.** If the file had been committed last week, adding it to `.gitignore` today would **not** remove it from history or from tracking. The file stays tracked, and the secret remains in every past commit. The correct response is to **rotate the secret** (and, separately, untrack it with `git rm --cached` and optionally scrub history, which is an advanced topic). Ignoring is not securing.

### 3. Full hash of the first commit

```bash
git log               # scroll to the oldest commit; the 40-char hash is on its "commit" line
# or:
git rev-list --max-parents=0 HEAD
```

## Common issues to watch

- Student forgets to activate the venv (no `(.venv)` in prompt) and installs into the global interpreter. Teach the prompt-check reflex.
- `.venv/` appears in `git status`: the `.gitignore` was added after staging `.`; have them check the pattern and re-run `git status`.
- `data/hartford_claims_sample.csv` path errors: the script must be run from the repo root so the relative path resolves.
- Windows learners on personal laptops: activation is `.venv\Scripts\activate`; this course uses the Linux (Ubuntu VM) path, so use `source .venv/bin/activate` for the venv comparison tasks.

> The environment-management depth (conda / venv / uv comparison) moved to **Lab A**; its solution key is `Lab_A_solutions.md`. Lab B is now Git-focused.
