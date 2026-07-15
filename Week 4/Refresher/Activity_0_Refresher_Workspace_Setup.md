# Activity 0: Refresher Workspace Setup

This is an AI-Free Zone activity. You may use documentation, your notes, and conversation with a partner. Do not use an AI assistant to write the work.

## Goal

Use the repository's existing Python project and keep the refresher files under `student-work/week4/day1/refresher/`. The work folder stores your notebooks and SQLite database. It does not contain another Python project or virtual environment.

## Setup

1. Start at the repository root. Confirm that `pyproject.toml` is visible.

   ```bash
   pwd
   ls pyproject.toml
   ```

2. Add the refresher dependencies to your repository-root project.

   ```bash
   uv add pandas polars pyarrow s3fs sqlalchemy ipykernel
   uv run python --version
   ```

   `uv add` records the packages in the root `pyproject.toml` and installs them into the root `.venv`. Do not run `uv init` in `student-work/`.

3. In VS Code, select `<repo-root>/.venv/bin/python` as the interpreter and Jupyter kernel.

4. Create the refresher work folder and copy the student notebooks into it.

   ```bash
   mkdir -p student-work/week4/day1/refresher
   cp "Week 4/Refresher/Activity_2_NYC_Taxi_Pandas_ETL.ipynb" student-work/week4/day1/refresher/
   cp "Week 4/Refresher/Activity_3_NYC_Taxi_Polars_ETL.ipynb" student-work/week4/day1/refresher/
   cd student-work/week4/day1/refresher
   ```

   Do not edit provided files in `Week 4/Refresher/`. Do not copy files from `solutions/`.

## Environment rules

- The shared environment is `<repo-root>/.venv`.
- The shared dependency file is `<repo-root>/pyproject.toml`.
- The only `.gitignore` is at the repository root.
- This refresher does not require an environment exception.
- If a future activity requires incompatible package versions, its instructions will explicitly offer a named root environment or a local activity environment.

## If the environment seems wrong

If you see `VIRTUAL_ENV does not match the project environment`, run `deactivate`, return to the repository root, and run:

```bash
uv sync
```

Then reselect `<repo-root>/.venv/bin/python` as the interpreter and kernel.

## Public S3 access boundary

The notebooks read one public, class-managed object with unsigned requests. The pandas notebook uses `storage_options={"anon": True}`. The Polars notebook uses `skip_signature="true"` and the object's AWS region. These settings mean that no AWS credentials are sent for this read.

Anonymous access works only because this exact object permits public reads. It does not make other S3 data public. Do not add access keys, browse buckets, change the URI, or write to S3. If the exact read fails, stop and tell the instructor.

## SQLite output

Both notebooks write small summary tables to `student-work/week4/day1/refresher/nyc_taxi_refresher.db`. The pandas activity creates the database and the first two tables. The Polars activity adds two more tables. You will open the completed database in DBeaver and verify all four tables.

## Success criteria

- The two copied notebooks are under `student-work/week4/day1/refresher/`.
- VS Code and Jupyter use `<repo-root>/.venv/bin/python`.
- No `.venv`, `pyproject.toml`, `uv.lock`, or `.gitignore` was created in the refresher or Day 1 work folder.
- The refresher dependencies are recorded in the root `pyproject.toml`.
