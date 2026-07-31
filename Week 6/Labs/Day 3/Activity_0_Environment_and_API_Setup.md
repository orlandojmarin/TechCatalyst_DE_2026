# Activity 0: Environment and API Key Setup

**Module:** Week 6 Day 3
**Estimated time:** 15 minutes
**Difficulty:** Beginner
**Format:** Individual
**Prerequisites:** The repo-root UV project from earlier weeks (`.venv`, `pyproject.toml`, `uv.lock` already exist)

## Objective

Add the packages today's notebooks need, store your API keys where the notebooks expect them, and copy today's starters into your own work folder before you open anything.

## Background

Most of today runs through the `openai` Python package. That is not a typo: you will point the same OpenAI client at three different backends (OpenAI, Gemini, and a local Ollama server) by changing a `base_url`. One client, three providers. Activity 1 explains why that works.

The other three are each used by one notebook: `tiktoken` and `model2vec` in Activity 2, where you look at how text becomes numbers, and `mcp` in Activity 6, where you build a small tool server of your own. Installing them all now saves interrupting the lab later.

Keys never go in a notebook cell. They live in a `.env` file at the repo root, which `.gitignore` already excludes from version control, and each notebook loads it with `python-dotenv`.

## Instructions

1. Confirm you are at the repo root and the shared environment still works.

   ```bash
   pwd
   # should end with the cloned repo folder, for example .../TechCatalyst_DE_2026
   uv sync
   ```

2. Add today's dependencies from the repo root.

   ```bash
   uv add openai python-dotenv tiktoken model2vec mcp
   ```

   `python-dotenv` may already be installed from an earlier week; `uv add` is safe to run again, it just confirms the version.

3. Create or open the `.env` file at the repo root and add your keys. If the file does not exist yet, create it.

   ```text
   OPENAI_API_KEY=your-openai-key-here
   GOOGLE_API_KEY=your-google-ai-studio-key-here
   ```

   You already created `GOOGLE_API_KEY` in Week 2 Day 3, it is the same key, reused here. Get an `OPENAI_API_KEY` from the instructor if you do not have one. Never paste a key directly into a code cell or commit `.env`.

4. Create your work folder and copy today's starter notebooks into it.

   ```bash
   mkdir -p student-work/week6/day3
   cp "Week 6/Labs/Day 3"/Activity_*.ipynb student-work/week6/day3/
   ```

   Work on the copies under `student-work/`, not on the files in `Week 6/Labs/Day 3/`. Editing the provided files directly risks a conflict the next time the instructor pushes new material.

5. Open `student-work/week6/day3/Activity_1_OpenAI_Compatible_APIs.ipynb`, select the repo-root `.venv` kernel (top right, **Select Kernel**), and run the first cell.

## Expected Output

```text
env ok
```

`student-work/week6/day3/` should now contain your own copies of all six `Activity_*` notebooks for today (Activities 1 through 6).

## Success Criteria

- `uv run python -c "import openai, dotenv, tiktoken, model2vec, mcp; print('env ok')"` prints `env ok`.
- `pyproject.toml` lists `openai`, `python-dotenv`, `tiktoken`, `model2vec`, and `mcp`.
- `.env` at the repo root has both `OPENAI_API_KEY` and `GOOGLE_API_KEY`.
- Today's notebooks are copied into `student-work/week6/day3/` and open with the `.venv` kernel selected.

## Hints

<details>
<summary>Hint 1: a cell says ModuleNotFoundError for one of today's packages</summary>

You are almost certainly on the wrong kernel, or you ran `uv add` from inside a subfolder instead of the repo root. Check `pwd` before step 2, then reselect the repo-root `.venv` kernel in the notebook.

</details>

<details>
<summary>Hint 2: the notebook cannot find my key</summary>

`load_dotenv()` only finds `.env` if it is at the repo root and you are running the kernel from inside this project. Confirm the file is named exactly `.env` (not `.env.txt`) and sits next to `pyproject.toml`.

</details>
