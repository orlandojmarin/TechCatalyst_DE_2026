# Activity 0: Environment and API Key Setup

**Module:** Week 6 Day 4
**Estimated time:** 15 minutes
**Difficulty:** Beginner
**Format:** Individual
**Prerequisites:** The repo-root UV project (`.venv`, `pyproject.toml`, `uv.lock`), and yesterday's `openai` / `python-dotenv` setup from [Week 6 Day 3](../Day%203/Activity_0_Environment_and_API_Setup.md)

## Objective

Add today's new packages, collect the credentials four different services need, and copy today's starters into your own work folder before you open anything.

## Background

Today crosses more services and libraries than any other day this week: two managed AI APIs on two clouds, an embeddings API, two keyword-search libraries, a vector database, two RAG frameworks, and an experiment tracker. That means more entries in `.env` and a longer install, not more complexity, every credential still loads the same way you already know from Day 3.

## Instructions

1. Confirm the shared environment still works from the repo root.

   ```bash
   pwd
   uv sync
   ```

2. Add today's new packages. `boto3` and `scikit-learn` are already in the project from earlier weeks; `openai` and `python-dotenv` from yesterday.

   ```bash
   uv add requests pillow chromadb pypdf rank-bm25 llama-index llama-index-retrievers-bm25 langchain-community langchain-text-splitters langchain-openai langchain-chroma
   ```

   `chromadb`, `llama-index`, and the `langchain-*` packages pull in a fair number of dependencies, this may take several minutes the first time. You will see a `DeprecationWarning` when Activity 4 imports from `langchain_community`, that is expected, not a sign anything is broken, and Activity 4 explains why.

   One package is deliberately **not** in that list: `llama-index-readers-file`, which is what LlamaIndex normally uses to read PDFs. It requires `pandas` below version 3, and this repository is pinned to pandas 3, so `uv add` will refuse to install it. This is the same class of conflict as the MLflow one in the next step, and it is worth noticing that it happens twice in one day. Activity 4 works around it by reusing the `pypdf` extraction you wrote in Activity 3, which is better for learning anyway. If you install it regardless, `SimpleDirectoryReader` will not error, it will silently read your PDFs as raw binary and answer questions from nonsense.

3. Create a second, separate environment just for MLflow.

   MLflow cannot live in the main project. Every MLflow release requires `pandas` below version 3, and this repository is pinned to pandas 3, which the rest of the course depends on. Worse, `uv add mlflow` does not fail when you try: it quietly installs a four-year-old MLflow that then crashes the moment you import it. So Activities 5 and 6 get their own environment.

   Run both commands from the repository root:

   ```bash
   uv venv .venv-mlflow --python 3.13
   uv pip install --python .venv-mlflow/bin/python mlflow openai python-dotenv scikit-learn ipykernel
   ```

   This creates a second environment beside your main `.venv`. It does not touch, replace, or interfere with it. Activities 1 through 4 keep using the root `.venv` exactly as before, and only Activities 5 and 6 use this one.

   This is a genuine dependency conflict, not a quirk of this course. You will meet these constantly as a data engineer, and there are only ever three answers: downgrade the whole project to satisfy one package, isolate that package, or drop it. Isolating is the right call here because one library should not dictate the pandas version for six weeks of other work.

4. Add today's credentials to the repo-root `.env`. You already have `OPENAI_API_KEY` and `GOOGLE_API_KEY` from Day 3, both are reused today, so only these four are new:

   ```text
   AWS_ACCESS_KEY_ID=your-classroom-access-key
   AWS_SECRET_ACCESS_KEY=your-classroom-secret-key
   AWS_DEFAULT_REGION=us-east-1
   GCP_API_KEY=your-gcp-api-key
   ```

   - `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`: get these from the instructor. `boto3` reads them from the environment automatically, no `aws configure` needed. Same classroom AWS account as Week 1.
   - `GCP_API_KEY` is **not** the same key as `GOOGLE_API_KEY`. `GOOGLE_API_KEY` is an AI Studio key for Gemini. `GCP_API_KEY` is a Google Cloud API key, scoped to the **Cloud Vision API** and **Cloud Natural Language API**, created in the GCP Console under **APIs & Services -> Credentials**. The instructor will either hand these out or walk through creating one live; either way, both target APIs must be enabled on the project before the key works.

5. Copy today's starter notebooks and shared assets into your own work folder.

   ```bash
   mkdir -p student-work/week6/day4
   cp "Week 6/Labs/Day 4"/Activity_*.ipynb student-work/week6/day4/
   cp "Week 6/Labs/Day 4/claims_feedback_sample.csv" student-work/week6/day4/
   cp "Week 6/Labs/Day 4/social_posts_sample.csv" student-work/week6/day4/
   cp -r "Week 6/Labs/Day 4/images" student-work/week6/day4/images
   cp -r "Week 6/Labs/Day 4/pdfs" student-work/week6/day4/pdfs
   ```

   Work on the copies under `student-work/`, never on the files in `Week 6/Labs/Day 4/`. `images/` (31 real vehicle photos for Activity 1) and `pdfs/` (9 research papers for Activities 3 and 4) are shared assets your notebooks load by relative path, they need to sit next to your copied notebooks, not in a separate folder.

   Do **not** copy `solutions/`. Activities 1, 2, 3, and 4 all hand you `TODO` cells to write yourself. The solutions folder is there to check your work against after you have attempted a section, not to copy from.

6. Open `student-work/week6/day4/Activity_1_Vision_AI_AWS_vs_GCP.ipynb`, select the repo-root `.venv` kernel, and run the first cell.

   When you reach Activities 5 and 6, switch that notebook's kernel to `.venv-mlflow` instead. In VS Code that is **Select Kernel** in the top right, then **Python Environments**, then `.venv-mlflow`. Selecting the wrong one is the single most common way to get stuck today.

## Expected Output

```text
env ok
```

`student-work/week6/day4/` should contain your own copies of today's `Activity_*` notebooks.

## Success Criteria

- This one-liner prints `env ok` (a `DeprecationWarning` about `langchain-community` above it is expected):

  ```bash
  uv run python -c "import boto3, requests, PIL, chromadb, sklearn, pypdf, rank_bm25, tiktoken, llama_index.core, langchain_community, langchain_chroma; from llama_index.retrievers.bm25 import BM25Retriever; print('env ok')"
  ```
- `.venv-mlflow/bin/python -c "import mlflow; print(mlflow.__version__)"` prints a version starting with `3.`, not an ImportError.
- `.env` at the repo root has `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, and `GCP_API_KEY`, alongside yesterday's `OPENAI_API_KEY` and `GOOGLE_API_KEY`.
- Today's notebooks, `images/`, `pdfs/`, `claims_feedback_sample.csv`, and `social_posts_sample.csv` are all copied into `student-work/week6/day4/`, and a notebook opens with the `.venv` kernel.

## Hints

<details>
<summary>Hint 1: boto3 says "Unable to locate credentials"</summary>

Confirm `.env` has `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` spelled exactly like that (boto3 reads these exact names from the environment) and that `load_dotenv()` ran before you created any `boto3` client.

</details>

<details>
<summary>Hint 2: GCP call returns a 403 or "API not enabled"</summary>

`GCP_API_KEY` must be a Google Cloud Console API key with the Cloud Vision API and Cloud Natural Language API enabled on the project it belongs to, an AI Studio key (`GOOGLE_API_KEY`) will not work here. Ask the instructor to confirm both APIs are enabled.

</details>

<details>
<summary>Hint 3: chromadb is slow to install or import</summary>

This is normal the first time, it is a larger package than most you have installed this course. If `uv add chromadb` fails outright, confirm you are on the repo-root project (`pwd`, then `uv sync`) and not a leftover environment from another week.

</details>

<details>
<summary>Hint 4: Activity 5 or 6 says ModuleNotFoundError: No module named 'mlflow'</summary>

That notebook is running on the root `.venv`, which deliberately does not have MLflow. Switch the kernel to `.venv-mlflow`. The reverse also happens: if Activity 1 through 4 suddenly cannot find `chromadb`, `rank_bm25`, `llama_index`, or `langchain_chroma`, you left the kernel on `.venv-mlflow` and need to switch back.

</details>

<details>
<summary>Hint 6: Activity 3 or 4 says ModuleNotFoundError for rank_bm25, llama_index, or tiktoken</summary>

These are new today. Re-run the `uv add` in step 2 from the repository root, then re-run the `env ok` check in Success Criteria. Note the import name does not always match the install name: you install `rank-bm25` and import `rank_bm25`, and you install `llama-index-retrievers-bm25` but import `llama_index.retrievers.bm25`.

</details>

<details>
<summary>Hint 7: LlamaIndex returns gibberish, or answers that cite nothing in the papers</summary>

You most likely installed `llama-index-readers-file` and used `SimpleDirectoryReader`. Do not. As step 2 explains, that package conflicts with this project's pandas version, and without it `SimpleDirectoryReader` does not raise an error, it reads each PDF as raw binary and builds an index over thousands of chunks of meaningless characters. Activity 4 deliberately builds `Document` objects from your own `pypdf` `extract_text` function instead. If you see node text full of things like `endobj` and `/GoTo`, this is what happened.

</details>

<details>
<summary>Hint 5: a notebook says it cannot find images/ or pdfs/</summary>

Those folders need to sit next to the notebook you are running, inside `student-work/week6/day4/`, not one level up. Re-run the `cp -r` commands in step 5 if you skipped them or copied the notebooks before the folders existed.

</details>
