# Week 1 · Day 3: Student Resources

> **AI-Free Zone, Weeks 1 to 4:** Type every command yourself. Use these docs to understand commands, not to skip thinking.

## Core Documentation

| Resource | Why it helps |
| :--- | :--- |
| [VS Code terminal basics](https://code.visualstudio.com/docs/terminal/basics) | Use the integrated terminal from VS Code |
| [VS Code Python docs](https://code.visualstudio.com/docs/python/python-tutorial) | Python editing and interpreter basics |
| [UV documentation](https://docs.astral.sh/uv/) | Modern Python project setup with `uv init`, `uv add`, `uv sync`, and `uv run` |
| [Python venv docs](https://docs.python.org/3/library/venv.html) | Official reference for Python virtual environments |
| [pip user guide](https://pip.pypa.io/en/stable/user_guide/) | Package installation and requirements files |
| [Git reference](https://git-scm.com/docs) | Official command reference |
| [Git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf) | One-page Git reference |
| [GitHub cloning docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) | How clone works |
| [GitHub pull request docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) | Official PR workflow |
| [.gitignore templates](https://github.com/github/gitignore) | Patterns for files that should not be committed |

## Quick Terminal Checks

```bash
pwd
ls -la
python3 --version
uv --version
git --version
code --version
```

If `code --version` fails, open VS Code manually and use its integrated terminal.

## Python Environment Mental Model

| Tool | Isolates environment | Manages packages | Class use |
| :--- | :--- | :--- | :--- |
| `venv` | Yes | No | Comparison path |
| `pip` | No | Yes | Comparison path |
| `uv` | Yes | Yes | Main local project workflow |

Key commands:

```bash
uv init project-name
cd project-name
uv add pandas requests
uv run python main.py
uv sync
```

Remember:

- `uv add <package>` changes the project dependencies.
- `uv sync` rebuilds the local environment from the lock file.
- Commit `pyproject.toml` and `uv.lock`.
- Do not commit `.venv/`.

## Git Mental Model

| Area | What it means |
| :--- | :--- |
| Working directory | Files you are editing |
| Staging area | Changes selected for the next commit |
| Local repository | Commits saved on your machine |
| Remote repository | GitHub copy |

Useful commands:

```bash
git status
git add <file>
git diff
git diff --staged
git commit -m "Message"
git log --oneline
git remote -v
git push
git pull
git clone <url>
git fetch
git merge origin/main
```

## Troubleshooting First Moves

When stuck, run:

```bash
pwd
git status
git remote -v
python3 --version
uv --version
```

Then read the error out loud. Most Day 3 issues are one of these:

- Wrong folder.
- Git identity not configured.
- Missing GitHub authentication.
- `.venv/` accidentally staged.
- Running Python outside the UV project.
- Local repo and GitHub repo are out of sync.

## Lab Deliverable Checklist

| Done | Deliverable |
| :--- | :--- |
| [ ] | UV project works with `uv run python hello_data.py` |
| [ ] | `pyproject.toml` and `uv.lock` exist |
| [ ] | `.venv/` is ignored |
| [ ] | `hello_data.py` reads the sample CSV |
| [ ] | At least 4 commits appear in `git log --oneline` |
| [ ] | GitHub repo is connected as `origin` |
| [ ] | Web edit was pulled locally |
| [ ] | `journal-clone` was created and verified |
| [ ] | Pull request was opened and merged |
| [ ] | Local `main` was updated after the PR merge |
