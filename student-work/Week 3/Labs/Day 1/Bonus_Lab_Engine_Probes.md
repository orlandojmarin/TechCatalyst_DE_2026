# Bonus Lab Setup: The Engines Environment (`.venv-probes`)

**Module:** Week 3 Day 1 (optional, outside class or stretch lane)
**Estimated time:** 15 minutes setup, then 60 to 90 minutes for the notebook
**Difficulty:** Intermediate
**Format:** Individual
**Prerequisites:** Activity 0 complete, Activity 2 core path complete
**Companion notebooks:**
- `Bonus_Dask_Intro.ipynb`
- `Bonus_Modin_Intro.ipynb`
- `Bonus_FireDucks_Intro.ipynb`

## Objective

Build a separate, disposable environment for optional engine experiments, especially Modin and FireDucks. This protects the main Pandas 3 course environment from dependency changes.

## Why a Separate Environment

The shared repo-root `.venv` runs Pandas 3. Modin and FireDucks have their own dependency stacks and may pull a different Pandas version than the main course environment. Do not install them into the shared `.venv`.

If you ran `uv add modin` or `uv add fireducks` at the repo root, UV could change package versions used by the required labs. That is why this bonus uses a disposable `.venv-probes` environment.

Dask can run in the shared environment if installed there. We include it in `.venv-probes` only so the optional engine notebooks can run from one experimental kernel.

## Instructions

1. From the repo root, create a second virtual environment with a different name. The shared `.venv` is not touched.

   ```bash
   uv venv .venv-probes
   ```

2. Install the engines into it with `uv pip install --python`, which targets a specific environment instead of the project:

   ```bash
   uv pip install --python .venv-probes "modin[dask]" polars "dask[dataframe]" pyarrow ipykernel
   uv pip install --python .venv-probes fireducks
   ```

   Run the two commands separately. FireDucks is platform-sensitive. At the time of writing, PyPI provides wheels for Linux x86_64 and macOS ARM64, not Windows. If the install fails, skip the FireDucks notebook and record the OS/Python/platform reason.

   Note that we use Modin's Dask engine rather than Ray: it is a much lighter install and matches the Dask section of the notebook.

3. Look at which pandas the engines pulled in, and compare it with the shared environment:

   ```bash
   .venv-probes/bin/python -c "import pandas; print('probes env pandas:', pandas.__version__)"
   uv run python -c "import pandas; print('shared env pandas:', pandas.__version__)"
   ```

   Expected: the probes environment may show a different Pandas version than the shared environment. The important result is that the shared `.venv` still has Pandas 3.

   Windows equivalent for checking the probes environment:

   ```powershell
   .venv-probes\Scripts\python -c "import pandas; print('probes env pandas:', pandas.__version__)"
   ```

4. Copy the bonus notebooks into your work folder if you have not already:

   ```bash
   cp "Week 3/Labs/Day 1/Bonus_Dask_Intro.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Bonus_Modin_Intro.ipynb" student-work/week3/day1/
   cp "Week 3/Labs/Day 1/Bonus_FireDucks_Intro.ipynb" student-work/week3/day1/
   ```

5. Optional but recommended: download one real month of taxi data (about 55 MB) so the comparison runs on 3 million real rows instead of the synthetic fallback:

   ```bash
   cd student-work/week3/day1
   mkdir -p data
   curl -L -o data/yellow_tripdata_2024-04.parquet "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet"
   ```

6. Open your copy in VS Code, click **Select Kernel**, and choose **.venv-probes** instead of the shared `.venv`. Both appear in the picker because both live at the repo root.

7. Work through any bonus notebook you choose. These are awareness walkthroughs, not required labs. Read every markdown cell, run the code cells that match your environment, and fill the Your Turn cell yourself.

8. When you are done, remove the probe environment from the repo root:

   ```bash
   rm -rf .venv-probes
   ```

   Windows equivalent:

   ```powershell
   Remove-Item -Recurse -Force .venv-probes
   ```

## Bonus Tool Takeaways

Each bonus notebook ends with the same quick comparison table so you can keep the tools in perspective.

## Success Criteria

- The shared repo-root `.venv` still has pandas 3 after this lab. Prove it: `uv run python -c "import pandas; print(pandas.__version__)"`.
- The optional engine notebooks ran on the `.venv-probes` kernel when needed.
- Any Your Turn cells you attempted are completed by you, not copied.
- Your Day 1 README has the findings table with wall times, plus the reflection answers.
- `.venv-probes` is deleted when you are finished.

## Hints

<details>
<summary>The kernel picker does not show .venv-probes</summary>

Confirm `ipykernel` was installed into it (step 2) and that the folder is at the repo root. Reload VS Code's kernel list, or use Enter interpreter path with `.venv-probes/bin/python`.

</details>

<details>
<summary>uv pip install fireducks fails</summary>

Check your platform with `uname -m` and your Python version. If FireDucks does not provide a wheel for your OS, CPU architecture, or Python version, skip the FireDucks notebook and record the constraint in your findings table.

</details>

<details>
<summary>Modin prints engine startup messages or a short delay on first use</summary>

Normal. Modin starts its Dask engine on the first operation. The notebook asks you to include that startup cost in your findings.

</details>

<details>
<summary>The curl download is blocked or slow</summary>

Skip it. The notebook detects the missing file and builds a synthetic 1,000,000-row dataset with the same columns, and every step still works. Record which input you used.

</details>
