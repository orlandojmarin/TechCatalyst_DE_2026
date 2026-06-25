# Day 4 Lab Worksheet: Cloud Object Storage Landing-Zone

## Part 0: Account and Project Preflight

**Active account:** Assigned classroom account (confirmed via avatar, top-right)  
**Project ID:** training-project-06  
**Billing confirmation:** Project is linked to an active billing account  
**Enabled APIs:** Cloud Storage API enabled  

**Q1:** Which signal proves your work will target the assigned project, not just that you are signed in? Why is the correct signed-in email alone insufficient?

> Answer: The project picker in the top blue bar showing "training-project-06" proves my work targets the correct project. The signed-in email alone is insufficient because one account can have access to multiple projects, so being authenticated doesn't determine which project your actions land in.

---

## Part 1: Create and Secure the Raw Bucket

### Access Test

**Predict:** What will happen when you open the Public URL in an incognito window? Which control does your prediction depend on?

> Prediction: I won't be able to view it because incognito has no signed-in identity, and the bucket has public access prevention enforced, which blocks anonymous requests. The Authenticated URL should work since it carries my identity.

**Observe and explain:** Record the AccessDenied response. Contrast the Public URL and Authenticated URL behavior.

> Observation: The Public URL returned an AccessDenied error saying "Anonymous caller does not have storage.objects.get access." This confirms that without a signed-in identity, the request is treated as anonymous and blocked by public access prevention. The Authenticated URL (on storage.cloud.google.com) works because it prompts for sign-in and attaches my identity to the request.

**Q2:** Why did opening the file inside the console (and the Authenticated URL) work, while the Public URL in incognito failed?

> Answer: The console and Authenticated URL include my signed-in identity with the request, and my account has IAM permission on the bucket. The Public URL in incognito has no identity attached, so the request is anonymous. Public access prevention blocks all anonymous access regardless of the object's contents.

**Q3:** Did Cloud Storage create real folders? What does the console tree represent?

> Answer: No, Cloud Storage didn't create real folders. Object names are flat keys (like `source=classroom/year=2026/month=06/day=22/hartford.jpeg`), and the console just groups shared prefixes to display a folder-like tree. The slashes are part of the object name, not actual directory separators.

**Q4:** Why is a bucket-level viewer grant consistent with public access prevention?

> Answer: Public access prevention blocks access granted to anonymous or public principals (like "allUsers"). Granting Storage Object Viewer to a specific named partner is an authenticated IAM grant to an identified principal, not public access. So it doesn't conflict with public access prevention.

---

## Part 2: Build the Processed Zone

**CLI commands run:**

```bash
export PROJECT_ID="training-project-06"
export USERNAME="orlando"
export RAW_BUCKET="techcatalyst-de-2026-orlando-raw"
export PROCESSED_BUCKET="techcatalyst-de-2026-orlando-processed"

gcloud storage buckets create "gs://${PROCESSED_BUCKET}" \
  --project="${PROJECT_ID}" \
  --location=us-east1 \
  --uniform-bucket-level-access \
  --public-access-prevention
# Output: Creating gs://techcatalyst-de-2026-orlando-processed/...

gcloud storage cp \
  "gs://${RAW_BUCKET}/source=classroom/year=2026/month=06/day=22/*" \
  "gs://${PROCESSED_BUCKET}/staging/"
# Output: Completed files 3/3 | 113.5kiB/113.5kiB

gcloud storage ls -l "gs://${PROCESSED_BUCKET}/**"
#          0  2026-06-24T20:22:24Z  gs://techcatalyst-de-2026-orlando-processed/staging/day=22/
#     102878  2026-06-24T20:22:24Z  gs://techcatalyst-de-2026-orlando-processed/staging/hartford.jpeg
#      13313  2026-06-24T20:22:24Z  gs://techcatalyst-de-2026-orlando-processed/staging/intro.docx
# TOTAL: 3 objects, 116191 bytes (113.47kiB)
```

**Q5:** In the CLI listing, what does `**` match that `*` may not match?

> Answer: `**` recursively matches objects across all nested prefixes (like `staging/day=22/` and `staging/hartford.jpeg`). A single `*` only matches within one path segment, so it wouldn't reach into sub-prefixes.

**Bucket layouts:**

Raw bucket (`techcatalyst-de-2026-orlando-raw`):
- coffee.jpg (root)
- source=classroom/year=2026/month=06/day=22/hartford.jpeg
- source=classroom/year=2026/month=06/day=22/intro.docx

Processed bucket (`techcatalyst-de-2026-orlando-processed`):
- staging/day=22/ (0 bytes, prefix marker)
- staging/hartford.jpeg (102878 bytes)
- staging/intro.docx (13313 bytes)

---

## Part 3: Lifecycle and Recovery Controls

### A. Lifecycle Rules

**Predict:** Will saving a "Nearline after 30 days" rule move today's objects immediately? What object property will the rule evaluate?

> Prediction: No, it won't move today's objects immediately. The rule evaluates the object's age (days since creation), and since today's objects are 0 days old, they won't meet the 30-day condition until next month.

**Observe and explain:** What is coffee.jpg's current storage class after saving the rule? Why?

> Observation: coffee.jpg still shows "Standard" storage class. The rule hasn't moved it because the object is less than 30 days old, so it doesn't meet the age condition yet.

**Q6:** Regulatory raw data must be retained for seven years. Why is a 365-day lifecycle deletion rule unsafe, and which control prevents early deletion?

> Answer: A 365-day deletion rule would automatically delete data after one year, violating the seven-year requirement. Lifecycle rules only schedule actions but don't prevent deletion. A retention policy is the control that prevents early deletion by blocking any delete before the required age. Bucket Lock can make that retention policy irreversible for compliance.

**Lifecycle rules:**

| Rule | Action | Condition |
| :--- | :--- | :--- |
| 1 | Set storage class to Nearline | Age > 30 days |
| 2 | Delete object | Age > 365 days |

### B. Versioning and Overwrite

**Soft delete policy (before enabling versioning):** Retention period 7 days, effective date 24 June 2026  
**Object versioning (before enabling):** Off (now enabled)  

**Predict:** When coffee.jpg is overwritten, will the original version disappear or be kept?

> Prediction: The original won't disappear because versioning is turned on. It should be kept as a noncurrent version while the new upload becomes the live version.

**Observe and explain:** Record the versions you see. Identify live vs. noncurrent.

> Observation: I can see two versions of coffee.jpg in the version history. The live version is the dog image I just uploaded, and the original coffee image is listed as noncurrent (shown as "one non-current"). Without versioning, the overwrite would have destroyed the original entirely.

### C. Restore Original Generation

**Predict:** Will restoring an old generation erase the newer generation, or create another live generation?

> Prediction: It will create another live generation rather than erasing the dog version. The dog version should become noncurrent instead of being deleted.

**Observe and explain:** What became live and does the intervening generation remain available?

> Observation: After restoring, the original coffee image is now the live version again. The dog image is still available as a noncurrent generation. Restoring copies the old generation as a new live generation rather than deleting any history, so all versions remain accessible.

**Q7:** How do unique append-only object names reduce the value of versioning on a high-volume raw zone, and why can deletions or operational mistakes still create billable recovery data? Name one bounded recovery control.

> Answer: If every ingested file gets a unique name (like a timestamp or ID in the path), then normal ingestion never overwrites an existing object, so versioning doesn't add much protection for the normal write path. However, accidental deletions, reruns that reuse a name, or cleanup scripts can still create noncurrent or soft-deleted versions that remain billable. A bounded soft-delete window (e.g., 7 days) provides short-term recovery without accumulating unlimited noncurrent data.

---

## Part 4: Document and Check Your Work

### Checklist

- [ ] Preflight evidence recorded
- [ ] Commands run or observed
- [ ] Q1 through Q7 answered
- [ ] All four Predict/Observe responses completed
- [ ] Lifecycle JSON or screenshot included
- [ ] Both bucket screenshots included

### Optional: GCS to S3 Comparison

| Concept | Google Cloud | AWS |
| :--- | :--- | :--- |
| Object storage service | Cloud Storage | Amazon S3 |
| URI | `gs://bucket/key` | `s3://bucket/key` |
| Default secure posture | Public access prevention + uniform bucket IAM | Block Public Access + bucket/IAM policies |
| CLI example | `gcloud storage ls gs://bucket/**` | `aws s3 ls s3://bucket/ --recursive` |

**Optional S3 reflection:**

> Answer:
