# Activity 0: Environment and GCP Setup (Medallion ETL)

**Module:** Week 3 Day 3
**Estimated time:** 15 minutes if your environment is ready, 30 to 45 minutes if `gcloud`, permissions, or bucket setup need fixing
**Difficulty:** Beginner
**Prerequisites:** Linux terminal, VS Code, cloned repo, UV, the `gcloud` CLI, and your assigned GCP project ID

## Objective

Confirm the repo-level Python environment has the mini-project packages, authenticate to your own GCP project, and prepare copied mini-project files so pandas output can be written locally first and optionally uploaded to your GCS bucket.

## Read Order

1. Read this setup activity.
2. Copy the mini-project files into `student-work/week3/day3/`.
3. Open `Medallion_ETL_Mini_Project.ipynb`.
4. Complete the local pandas bronze-to-silver path first.
5. Attempt cloud only after local works.
6. Use `README.md` and the PR checklist before submitting.

## Background

The medallion pipeline reads raw data from a **public S3 bucket** (no AWS keys needed, the same anonymous-read pattern from Week 2 Day 3) and writes to **your own GCP project**. You each have full access to your assigned project, and the instructor cannot see your project, so you submit by pull request with a screenshot of your bucket object.

We authenticate with **Application Default Credentials (ADC)**: one `gcloud` command, no downloaded key files to manage or accidentally commit.

The required project is the local bronze-to-silver pipeline. Cloud upload is an optional stretch or evidence attempt. If cloud is blocked by authentication or permissions, document the blocker and continue with the local notebook.

You may see `cloud.cfg` in the folder. Do not put credentials in it. It is intentionally a placeholder and is not needed for this lab.

You work on copied files under `student-work/week3/day3/`, but you use the global `.venv` at the repo root. That keeps the course environment consistent while still preventing your work from colliding with instructor updates under `Week 3/Labs/...`.

## Instructions

1. From the repo root, add the mini-project packages to the global environment.

   ```bash
   uv add "pandas>=3.0" polars pyarrow boto3 google-cloud-storage
   uv run python -c "import pandas, polars, boto3; from google.cloud import storage; print('imports OK')"
   ```

   The `.venv` lives at the repo root. Run `uv add` from the repo root so UV updates
   the shared course environment instead of creating a second project somewhere else.

2. Confirm the Google Cloud CLI is installed in your Linux terminal.

   ```bash
   gcloud --version
   ```

   If that prints a version, continue to the next step. If it says `command not
   found`, install the Google Cloud CLI:

   ```bash
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates gnupg curl

   curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
     sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

   echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
     sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

   sudo apt-get update && sudo apt-get install -y google-cloud-cli

   gcloud --version
   ```

   Then refresh the VS Code terminal: type `exit`, close that terminal, and open a
   new terminal inside VS Code. Run `gcloud --version` again in the new terminal.

3. Authenticate to your GCP project with ADC (no key files).

   ```bash
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

4. Create your GCS bucket in your project (or reuse your Week 1 raw bucket).

   Use this bucket name pattern:

   ```text
   techcatalyst-de-2026-<your-username>-raw
   ```

   Console path:

   1. Open Google Cloud Console.
   2. Select your assigned project from the project picker.
   3. Go to Cloud Storage, then Buckets.
   4. Click Create.
   5. For Name, enter `techcatalyst-de-2026-<your-username>-raw`.
   6. For Location type, choose **Region**.
   7. For Region, choose **us-east1**.
   8. For Storage class, keep **Standard**.
   9. For Access control, keep **Uniform** bucket-level access.
   10. For Public access prevention, keep it enabled or enforced. This bucket should not be public.
   11. Do not enable Requester Pays.
   12. Keep the remaining protection and encryption defaults unless the instructor says otherwise.
   13. Click Create.
   14. Open the bucket you just created.
   15. Open the Permissions tab.
   16. Confirm your classroom Google account appears directly, or through a project role, with permission to create objects. `Storage Object Admin` or `Storage Admin` is enough for this lab.
   17. If your account is not listed and you have permission to grant access, click Grant access, add your classroom Google account as the principal, choose Cloud Storage, then Storage Object Admin, and click Save.
   18. If you cannot grant access, stop and ask the instructor to confirm your project IAM. Do not create a service account key.

   CLI equivalent:

   ```bash
   gcloud storage buckets create gs://techcatalyst-de-2026-your-username-raw --location=us-east1 --uniform-bucket-level-access
   ```

   If the bucket name is already taken, add your initials or a short class username
   suffix. Bucket names are global across Google Cloud, not just your project.

   Quick write check:

   ```bash
   printf "gcs write check\n" > /tmp/gcs-write-check.txt
   gcloud storage cp /tmp/gcs-write-check.txt gs://techcatalyst-de-2026-your-username-raw/_checks/gcs-write-check.txt
   gcloud storage rm gs://techcatalyst-de-2026-your-username-raw/_checks/gcs-write-check.txt
   ```

   If the copy fails with `403` or a permission message, your code will fail too.
   Fix the bucket or project permission before running Part 7.

5. Copy the mini-project files into your Week 3 Day 3 work folder, then work on the copies. Run this from the repo root.

   ```bash
   mkdir -p student-work/week3/day3/data
   cp "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/Medallion_ETL_Mini_Project.ipynb" student-work/week3/day3/
   cp "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/starter/medallion_etl.py" student-work/week3/day3/
   cp -r "Week 3/Labs/Day 3/Mini_Project_Medallion_ETL/data/raw" student-work/week3/day3/data/
   ```

   Do not edit the provided files under `Week 3/Labs/Day 3/...` in place. Copy first, then complete your copies.

6. Open the notebook copy in VS Code and select the repo-root `.venv/bin/python` as both the interpreter and the Jupyter kernel.

7. Add generated output paths to the work folder `.gitignore`.

   ```bash
   cd student-work/week3/day3
   printf "__pycache__/\ndata/bronze/\ndata/silver/\n*.parquet\n" >> .gitignore
   ```

## Success Criteria

- `imports OK` prints from the repo root.
- `gcloud --version` prints a version in your Linux terminal.
- `gcloud auth application-default login` completed and your project is set.
- Your GCS bucket exists in your project.
- The notebook, starter script, and `data/raw/` exist in `student-work/week3/day3/`.
- No key files anywhere: you used ADC, and the S3 source is public.
- VS Code/Jupyter uses the repo-root `.venv`.

## Hints

<details>
<summary>Do I need AWS credentials?</summary>

No. The S3 source bucket is public and read-only, so you read it anonymously with `boto3` (unsigned), the exact same pattern from Week 2 Day 3's Activity 2. You only authenticate to GCP, for the writes.

</details>

<details>
<summary>GCS write fails with a credentials or project error</summary>

Re-run `gcloud auth application-default login`, confirm `gcloud config get-value project` shows your project, and make sure your bucket name is globally unique.

</details>

<details>
<summary>`VIRTUAL_ENV does not match the project environment`</summary>

A leftover environment is active in your shell. Run `deactivate`, then retry with `uv run` from the folder that contains the notebook or script. UV will walk up to the repo project and use the repo-level `.venv`.

</details>
