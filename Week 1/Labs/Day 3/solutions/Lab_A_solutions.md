# Lab A: Solution Key (instructor) : Python Environments & Package Management

Share after the lab. Reward correct reasoning over exact wording.

## Part 4 reflection answers

1. **The two jobs:** *isolate the environment* (give this project its own Python + packages, walled off) and *manage packages* (install/upgrade/remove and **record** them). `venv` isolates only; `pip` manages packages only; **conda and uv do both**. A student who can state this has resolved the core confusion.
2. **A venv is "just a folder":** `python -m venv claims-venv` creates a directory containing a copy/link of Python and a `site-packages`. Activating just puts that folder's `bin/` first on `PATH`. **Strength:** trivially simple : delete the folder and the env is gone, nothing left in a central registry. **Limit:** it only isolates; you still need pip to install, `pip freeze` to record, and it has no real lock file.
3. **`uv.lock` vs `pip freeze`/requirements.txt:** the lock file is produced and maintained automatically by uv's resolver and records the **full dependency graph** : every direct *and* transitive package pinned to an exact version **with hashes**. A `requirements.txt` from `pip freeze` captures versions too, but it's a flat snapshot you maintain by hand, with no hashes and no separation of "what I asked for" vs "what got pulled in."
4. **When to choose each:** conda -> you need non-Python/scientific binaries (GDAL, CUDA, R) in the same env; venv + pip -> the universal baseline, always available, what the ecosystem assumes (our course default); uv -> modern projects wanting speed + reproducibility by default.

## `uv add` vs `uv sync` (the key distinction)

- **`uv add <pkg>`** *changes* the project: edits `pyproject.toml` and re-locks `uv.lock` ("I want this new thing"). Also creates/updates `.venv`.
- **`uv sync`** *reproduces* the project: makes the installed `.venv` exactly match the existing `uv.lock`, installing/removing as needed ("make this machine match the agreed set"). This is what a teammate or CI runs after cloning. No new dependencies.

## Challenge answers

1. **`uv python install 3.12` + fresh `uv init`:** `.python-version` pins the interpreter; uv will fetch/use 3.12 for that project. The point: uv manages **Python versions**, not just packages : a project can pin its interpreter so every machine runs the same one.
2. **A transitive dep in `uv.lock` but not `pyproject.toml`:** e.g. `numpy`, `python-dateutil`, `pytz` (pandas dependencies). It's in the lock because pandas requires it (the resolver records the whole graph), but not in `pyproject.toml` because *you* didn't ask for it directly. This is exactly the "direct vs transitive" distinction a flat `requirements.txt` blurs.
3. **`environment.yml` vs `pyproject.toml`:** `environment.yml` lists conda channels + packages (and can include pip deps); `pyproject.toml` is the standardized Python project file with direct deps under `[project]`. Most students prefer handing over a `pyproject.toml` + `uv.lock` (or a `requirements.txt`) for a pure-Python project because it's standard and reproducible without conda; reach for `environment.yml` when non-Python binaries are in play. Accept either with sound reasoning.

## Common issues to watch

- **conda:** `conda activate` fails ("shell not initialized") because they skipped `conda init bash` + reopening the terminal. Have them run it and open a fresh terminal. Watch for students installing into `(base)` instead of `(claims-conda)` : check the prompt.
- **venv:** forgetting to `source .venv/bin/activate` (no `(claims-venv)` in prompt) and installing globally. Teach the prompt-check reflex. `which python` is the quick diagnostic.
- **uv:** `uv: command not found` after install : they skipped `source $HOME/.local/bin/env` (or didn't open a new terminal). uv lands in `~/.local/bin`.
- **General:** students working in their course repo instead of `~/env-lab`. Stop them : this lab is a throwaway sandbox; remind them to `rm -rf ~/env-lab` at the end and that the course repo (Lab B) stays venv + pip.
- **Timing:** if running long, conda (Part 1) is the safe place to go faster (it's the "awareness" tool); protect the full uv section (Part 3) : that's the focus.
