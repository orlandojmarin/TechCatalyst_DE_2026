# Day 3 - Lab A: Python Environments With UV

## Part 7 Discussion

- **Where did venv store the environment?** In the `claims-venv/` directory (wherever you ran `python3 -m venv claims-venv`).
- **What file recorded dependencies?** `requirements.txt`, generated manually with `pip freeze`.
- **Which workflow had a lock file?** The UV workflow (`uv.lock`), which records the full resolved dependency set automatically.
- **Which workflow would you rather hand to a teammate?** UV. It handles both isolation and package management in one tool, and the lock file ensures everyone gets the exact same versions without extra steps.

## Reflection

1. **What are the two jobs of Python environment tooling?** Isolate the environment (so one project's packages don't interfere with another) and manage packages (install, remove, and record dependencies so others can rebuild the project).

2. **What does `uv add` do?** Adds a package to the project's dependency list in `pyproject.toml` and updates `uv.lock` with the full resolved dependency tree.

3. **What does `uv sync` do?** Rebuilds the `.venv` environment from the existing `uv.lock` file without changing any dependency declarations.

4. **Why do we commit `pyproject.toml` and `uv.lock` but not `.venv/`?** `pyproject.toml` and `uv.lock` are small text files that describe what to install. `.venv/` contains the actual installed binaries, which are large, platform-specific, and can be recreated at any time with `uv sync`.

5. **When might a team still use venv plus pip?** When the project is simple with few dependencies, when working in an environment where UV isn't available, or when the team is already established on a venv/pip workflow and the overhead of switching isn't justified.
