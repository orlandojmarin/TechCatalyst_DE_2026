# Data Quality Incident Report

**Team:**
**Date:**

Fill this in as you go, not on Thursday from memory.

---

## Summary

| Metric | Count |
| :--- | :--- |
| Rows in source files | |
| Rows loaded to bronze | |
| Rows surviving to silver | |
| Rows dropped | |
| Percentage dropped | |

If rows in source and rows in bronze do not match, explain the gap before anything else. A load that silently dropped records is a more serious problem than dirty data, because you did not choose it.

---

## Defects found

Copy this block per defect. Aim for at least five, including at least one not named in `Data_Catalog.md`.

### Defect 1: [name it precisely]

**What it is**

**How we found it**

**Scale**

| | Count | Percent of total |
| :--- | :--- | :--- |
| Records affected | | |

**Which metrics it would distort, and in which direction**

**Our decision:** drop / correct / quarantine / keep with caveat

**Why, and what we gave up**

---

## Defects we found but did not address

Being explicit about what you left alone, and why, is a strength. It shows you made a decision rather than missing it.

| Defect | Scale | Why we left it | How it limits our conclusions |
| :--- | :--- | :--- | :--- |
| | | | |

---

## The cash tip question

Every team hits this, so answer it explicitly.

`tip_amount` is recorded for credit card transactions but not for cash, so cash tips appear as zero.

**Does any of our analysis involve tips?** yes / no

**If yes, how did we handle it?**

**If we present a tipping chart, what does the slide say about this?**

---

## What we would do with more time

The data quality work you would prioritize next, and why.

---

## Effect on our conclusions

The most important section. For each headline finding you present, state how the data quality issues could affect it.

| Our finding | Could a data quality issue explain it? | Why we are confident, or how confident we are |
| :--- | :--- | :--- |
| | | |

A finding you cannot defend here should not be a headline on Demo Day.
