# Lab A: Read a Reference Architecture

**Module:** Data architectures and pipeline design (Day 5) · **Format:** Pairs · ⏱️ about 40 minutes (morning warm-up)

> [!WARNING]
> **AI-Free Zone (Weeks 1 to 4).** Read and reason about the architecture yourselves. No AI-generated summaries or diagrams. The skill you are building is reading an architecture like an engineer.

---

## 🎯 Goal

Before you design your own pipeline this afternoon, learn the grammar from a vetted one. By the end you can:

- read a published cloud reference architecture and identify its zones, data flow, and services;
- locate where quality checks, PII handling, and the main cost driver live;
- map any reference architecture onto the medallion model;
- name one design idea you will reuse in Lab B.

## 🧠 Why this matters

You rarely design a pipeline from a blank page. Cloud providers publish reference architectures: proven, reviewed designs for common problems. Engineers read them to learn patterns and to avoid re-deriving solved problems. Reading one well is a real skill: you are not copying it, you are extracting the reusable grammar and judging which choices fit your requirements.

---

## Part 1: Pick a reference architecture (5 min)

Choose **one** data-analytics reference architecture from either provider (give GCP and AWS equal footing; pick whichever problem is closest to a trip-records pipeline):

- **GCP Cloud Architecture Center:** https://cloud.google.com/architecture (browse the Data analytics section; for example, the data-lake or analytics-lakehouse references)
- **AWS Architecture Center:** https://aws.amazon.com/architecture/ (Analytics category; for example, a modern data lake or batch analytics reference)
- **AWS analytics lens / reference diagrams:** https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/analytics-lens.html

Record the title and URL of the one you chose.

If your pair gets stuck, open [Reference_Architecture_Examples.md](Reference_Architecture_Examples.md) only as a grammar aid. You still need to pick and read one published GCP or AWS architecture for this lab.

## Part 2: Read it like an engineer (20 min)

Annotate the diagram (sketch it, screenshot and mark it up, or describe it in notes). Answer:

| Question | Your answer |
| :--- | :--- |
| What business problem does this architecture solve? | |
| What are the zones, left to right (ingest, store, transform, serve)? | |
| Name the services in each zone | |
| Where does data quality get checked (if shown)? | |
| Where is sensitive data or access control handled (if shown)? | |
| What looks like the top cost driver? | |
| Is it batch, streaming, or both? | |

## Part 3: Map it to medallion (10 min)

- Which parts map to **bronze** (raw, as-landed), **silver** (cleaned, conformed), and **gold** (business-ready)?
- Where would a malformed file go in this design? If the reference does not show it, where would you add a quarantine path?

**Q:** Does this architecture follow medallion thinking, a different layering, or no clear layering? One sentence.

## Part 4: Steal one idea (5 min)

**Q:** Name one concrete design choice from this reference you will reuse in your Lab B taxi pipeline, and one choice you would change for the taxi use case and why.

---

## Deliverable

Add to your team folder (or `design_notes.md`): the chosen architecture's title and URL, your Part 2 table, the medallion mapping, and the two answers from Part 4. Keep it short; this is a warm-up, not a report.

## Success criteria

- [ ] Chose one GCP or AWS data-analytics reference architecture (title + URL recorded)
- [ ] Identified zones, flow, and services
- [ ] Located quality, PII, and cost (or noted where they are missing)
- [ ] Mapped it to bronze, silver, gold
- [ ] Named one idea to reuse and one to change

## 🧾 What you learned

Reading a reference architecture is the fast path to a good design: you inherit decisions that others have already validated, then adapt them to your own requirements. This afternoon you do the adapting.
