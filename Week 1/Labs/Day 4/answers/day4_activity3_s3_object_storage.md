# Day 4 S3 Lab Worksheet: Cloud Object Storage Landing-Zone (AWS Mirror)

## Part 0: Account and Identity Preflight

**Active account:** Assigned classroom account (confirmed via account menu, top-right)
**Account ID:** 535146832369
**Signed-in role:** orlando.marin
**Region:** us-east-1

**Q1:** Which result proves that subsequent commands target the assigned account? Name where you see it in the Console (and the CLI command that shows the same thing). Why is a familiar IAM user/role name alone insufficient?

> Answer: The Account ID (visible in the account menu, top-right of the Console) proves that subsequent commands target the assigned account. The CLI equivalent is `aws sts get-caller-identity`, which returns the Account ID in its output. A familiar IAM user/role name alone is insufficient because the same name can exist across multiple AWS accounts, so it doesn't tell you which account you're actually operating in.

---

## Part 1: Create and Secure the Raw Bucket

### Access Test

**Predict:** What will happen when you open the Object URL in an incognito window? Which control or identity does your prediction depend on?

> Prediction: The Object URL will not open in an incognito window because the request won't be authenticated under my account. With Block Public Access enabled, an anonymous request has no identity that S3 can authorize, so it will be denied.

**Observe and explain:** Record the exact response or error. Compare the identity used by the console (Open) request with the identity used by the incognito request.

> Observation: Opening the Object URL in a browser where I'm not signed in returned an `AccessDenied` error. The console's Open button works because it issues a presigned request carrying my authenticated IAM identity (orlando.marin). The other browser had no AWS credentials attached to the request, so it was treated as anonymous and S3 denied it.

**Q2:** Why did the authenticated console action work while the incognito request failed?

> Answer: The console's Open button works because it builds a presigned request that carries my authenticated IAM identity, which has permission to read the object. The unauthenticated browser request had no credentials, so it was treated as an anonymous caller. With Block Public Access enabled and no public policy on the bucket, S3 denied the anonymous request with AccessDenied.

**Q3:** Did S3 create real folders? What does the console tree represent? How can you verify it?

> Answer: No, S3 didn't create real folders. Object names are flat keys (like `raw/source=classroom/year=2026/month=06/day=22/hartford.jpeg`), and the console just groups shared prefixes to display a folder-like tree. The slashes are part of the object name, not actual directory separators. You can verify this by opening an object and checking its Key or S3 URI, which shows the full flat string.

**Q4:** Why is a named-principal bucket-policy grant consistent with Block Public Access still being on?

> Answer: Block Public Access only blocks access granted to anonymous or public principals. A bucket policy that names a specific IAM principal is granting access to an authenticated identity, not the public, so it doesn't conflict with Block Public Access being on.

---

## Part 2: Build the Processed Zone

**CLI commands run:**

```bash
export AWS_ACCOUNT_ID="535146832369"
export USERNAME="orlando"
export AWS_REGION="us-east-1"
export RAW_BUCKET="techcatalyst-de-2026-orlando-raw"
export PROCESSED_BUCKET="techcatalyst-de-2026-orlando-processed"

aws s3api create-bucket \
  --bucket "$PROCESSED_BUCKET" \
  --region "$AWS_REGION"
# Output:
# {
#     "Location": "/techcatalyst-de-2026-orlando-processed",
#     "BucketArn": "arn:aws:s3:::techcatalyst-de-2026-orlando-processed"
# }

aws s3 cp \
  "s3://${RAW_BUCKET}/raw/source=classroom/year=2026/month=06/day=22/" \
  "s3://${PROCESSED_BUCKET}/staging/" \
  --recursive
# Output:
# copy: s3://techcatalyst-de-2026-orlando-raw/raw/source=classroom/year=2026/month=06/day=22/intro.docx to s3://techcatalyst-de-2026-orlando-processed/staging/intro.docx
# copy: s3://techcatalyst-de-2026-orlando-raw/raw/source=classroom/year=2026/month=06/day=22/hartford.jpeg to s3://techcatalyst-de-2026-orlando-processed/staging/hartford.jpeg

aws s3 ls "s3://${PROCESSED_BUCKET}/" --recursive --human-readable
# Output:
# 2026-06-26 14:08:42  100.5 KiB staging/hartford.jpeg
# 2026-06-26 14:08:42   13.0 KiB staging/intro.docx
```

**Q5:** The AWS CLI has no `**` glob. How do you list everything beneath a prefix instead, and what is the trade-off of recursion being a flag (`--recursive`) rather than a wildcard?

> Answer: You use `aws s3 ls s3://bucket/ --recursive` to list everything beneath a prefix. Recursion is a flag you either turn on or leave off, rather than a wildcard in the path. The trade-off is that it's simpler, but less expressive. In GCS you could use `*` for one level and `**` for all levels, giving you fine-grained control. With the AWS CLI, you can't make that distinction natively, so if you need to filter results you have to use `--exclude`/`--include` patterns instead.

**Bucket layouts:**

Raw bucket (`techcatalyst-de-2026-orlando-raw`):
- coffee.jpg
- raw/source=classroom/year=2026/month=06/day=22/hartford.jpeg
- raw/source=classroom/year=2026/month=06/day=22/intro.docx

Processed bucket (`techcatalyst-de-2026-orlando-processed`):
- staging/hartford.jpeg
- staging/intro.docx

---

## Part 3: Lifecycle and Recovery Controls

### A. Lifecycle Rules

**Predict:** Will a "Standard-IA after 30 days" rule move today's objects immediately? What object property will the rule evaluate?

> Prediction: No, it won't move today's objects immediately. The rule evaluates the object's age based on its creation date, so objects uploaded today haven't been around for 30 days yet and won't be transitioned until they reach that age.

**Observe and explain:** What is coffee.jpg's current storage class after saving the rule? Why?

> Observation: coffee.jpg's storage class is still Standard. It hasn't reached the 30-day age threshold yet, so the rule hasn't moved it.

**Q6:** Regulatory raw data must be retained for seven years. Why is a 365-day expiration rule unsafe, and which control prevents early deletion rather than merely scheduling deletion?

> Answer: A 365-day expiration rule would delete data after one year, which violates the seven-year retention requirement. A lifecycle rule only automates when things get deleted, it doesn't actually prevent anyone or anything from deleting objects early. The control that enforces minimum retention is Object Lock (Governance or Compliance mode), which blocks deletion until the retention period expires. Object Lock can only be enabled at bucket creation.

**Lifecycle rules:**

| Rule | Action | Condition |
| :--- | :--- | :--- |
| 1 | Transition to Standard-IA | Age > 30 days |
| 2 | Expire (delete) object | Age > 365 days |

### B. Versioning and Overwrite

**Bucket Versioning (before enabling):** Disabled (now enabled)

**Predict:** When coffee.jpg is overwritten, will the original version disappear or be kept? What will the new latest version contain?

> Prediction: The original version will be kept because versioning is enabled. The new latest version will contain whatever file I upload as the replacement.

**Observe and explain:** Record the versions you see. Identify which Version ID is current (IsLatest) and explain how this differs from a bucket with versioning disabled.

> Observation: There are two versions of coffee.jpg. The new upload has a real Version ID and is marked as the current (latest) version. The original has a "null" Version ID because it was uploaded before versioning was enabled. With versioning disabled, the overwrite would have destroyed the original entirely. With versioning on, both versions are retained.

### C. Restore Original Version

**Predict:** Will restoring the old version erase the newer version, or create another latest version?

> Prediction: Restoring the old version will create a new latest version rather than erasing the newer version. Everything stays in the history.

**Observe and explain:** Confirm the newest Version ID is current and the intervening version is still listed.

> Observation: There are now three versions of coffee.jpg. The newest Version ID (the re-uploaded original) is marked as current. The intervening version (the replacement I uploaded earlier) is still listed as a noncurrent version. Nothing was erased, the full history is preserved.

**Q7:** How do unique, append-only object keys reduce the value of versioning on a high-volume raw zone, and why can deletions or operational mistakes still create billable recovery data? Name one bounded recovery control.

> Answer: If every ingested object has a unique key and nothing ever overwrites an existing object, versioning doesn't add much on the happy path since there's nothing to version. But deletions, accidental overwrites, or reruns that reuse a key can still create noncurrent versions and delete markers that stick around and cost money. One bounded recovery control is a lifecycle rule on noncurrent versions (`NoncurrentVersionExpiration`), which automatically cleans up old versions after a set number of days so they don't pile up indefinitely.

---

## Part 4: Document and Compare to GCS

### Checklist

- [x] Preflight evidence recorded
- [x] Commands run or observed
- [x] Q1 through Q7 answered
- [x] All four Predict/Observe responses completed
- [ ] Lifecycle JSON or screenshot included
- [ ] Both bucket screenshots included

### GCS to S3 Comparison

| Concept | Google Cloud (main lab) | AWS (this lab) |
| :--- | :--- | :--- |
| Object storage service | Cloud Storage | Amazon S3 |
| URI scheme | `gs://bucket/key` | `s3://bucket/key` |
| Block anonymous access | Public access prevention | Block Public Access |
| Disable per-object ACLs | Uniform bucket-level access | ACLs disabled (Bucket owner enforced) |
| Recursive list | `gcloud storage ls gs://b/**` | `aws s3 ls s3://b/ --recursive` |
| Tiering/expiry | Lifecycle rules | Lifecycle rules |
| Recover overwrites/deletes | Soft delete + versioning | Versioning (+ delete markers) |
| Lock minimum retention | Retention policy + Bucket Lock | Object Lock (Governance/Compliance) |

**Q (multicloud point):** In one sentence, name one concept that transfers directly from GCS to S3 and one implementation detail that changes.

> Answer: Lifecycle rules transfer directly (both GCS and S3 use age-based rules to transition or expire objects), but the way you list objects recursively changes: GCS uses a `**` wildcard in the path while AWS uses a `--recursive` flag on the command.
