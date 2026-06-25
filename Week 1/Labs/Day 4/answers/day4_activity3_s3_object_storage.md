# Day 4 S3 Lab Worksheet: Cloud Object Storage Landing-Zone (AWS Mirror)

## Part 0: Account and Identity Preflight

**Active account:** Assigned classroom account (confirmed via account menu, top-right)
**Account ID:**
**Signed-in role:**
**Region:** us-east-1

**Q1:** Which result proves that subsequent commands target the assigned account? Name where you see it in the Console (and the CLI command that shows the same thing). Why is a familiar IAM user/role name alone insufficient?

> Answer:

---

## Part 1: Create and Secure the Raw Bucket

### Access Test

**Predict:** What will happen when you open the Object URL in an incognito window? Which control or identity does your prediction depend on?

> Prediction:

**Observe and explain:** Record the exact response or error. Compare the identity used by the console (Open) request with the identity used by the incognito request.

> Observation:

**Q2:** Why did the authenticated console action work while the incognito request failed?

> Answer:

**Q3:** Did S3 create real folders? What does the console tree represent? How can you verify it?

> Answer:

**Q4:** Why is a named-principal bucket-policy grant consistent with Block Public Access still being on?

> Answer:

---

## Part 2: Build the Processed Zone

**CLI commands run:**

```bash
export AWS_ACCOUNT_ID=""
export USERNAME="orlando"
export AWS_REGION="us-east-1"
export RAW_BUCKET="techcatalyst-de-2026-orlando-raw"
export PROCESSED_BUCKET="techcatalyst-de-2026-orlando-processed"

aws s3api create-bucket \
  --bucket "$PROCESSED_BUCKET" \
  --region "$AWS_REGION"
# Output:

aws s3 cp \
  "s3://${RAW_BUCKET}/raw/source=classroom/year=2026/month=06/day=22/" \
  "s3://${PROCESSED_BUCKET}/staging/" \
  --recursive
# Output:

aws s3 ls "s3://${PROCESSED_BUCKET}/" --recursive --human-readable
# Output:
```

**Q5:** The AWS CLI has no `**` glob. How do you list everything beneath a prefix instead, and what is the trade-off of recursion being a flag (`--recursive`) rather than a wildcard?

> Answer:

**Bucket layouts:**

Raw bucket (`techcatalyst-de-2026-orlando-raw`):
-
-
-

Processed bucket (`techcatalyst-de-2026-orlando-processed`):
-
-
-

---

## Part 3: Lifecycle and Recovery Controls

### A. Lifecycle Rules

**Predict:** Will a "Standard-IA after 30 days" rule move today's objects immediately? What object property will the rule evaluate?

> Prediction:

**Observe and explain:** What is coffee.jpg's current storage class after saving the rule? Why?

> Observation:

**Q6:** Regulatory raw data must be retained for seven years. Why is a 365-day expiration rule unsafe, and which control prevents early deletion rather than merely scheduling deletion?

> Answer:

**Lifecycle rules:**

| Rule | Action | Condition |
| :--- | :--- | :--- |
| 1 | Transition to Standard-IA | Age > 30 days |
| 2 | Expire (delete) object | Age > 365 days |

### B. Versioning and Overwrite

**Bucket Versioning (before enabling):** Disabled (now enabled)

**Predict:** When coffee.jpg is overwritten, will the original version disappear or be kept? What will the new latest version contain?

> Prediction:

**Observe and explain:** Record the versions you see. Identify which Version ID is current (IsLatest) and explain how this differs from a bucket with versioning disabled.

> Observation:

### C. Restore Original Version

**Predict:** Will restoring the old version erase the newer version, or create another latest version?

> Prediction:

**Observe and explain:** Confirm the newest Version ID is current and the intervening version is still listed.

> Observation:

**Q7:** How do unique, append-only object keys reduce the value of versioning on a high-volume raw zone, and why can deletions or operational mistakes still create billable recovery data? Name one bounded recovery control.

> Answer:

---

## Part 4: Document and Compare to GCS

### Checklist

- [ ] Preflight evidence recorded
- [ ] Commands run or observed
- [ ] Q1 through Q7 answered
- [ ] All four Predict/Observe responses completed
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

> Answer:
