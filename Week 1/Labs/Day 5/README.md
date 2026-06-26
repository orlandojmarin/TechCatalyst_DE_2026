# Week 1 · Day 5: Lab

**Theme:** Data architectures and pipeline design (the Week 1 deliverable)
**Format:** A reference-architecture reading warm-up (pairs), then the team design lab (teams of 3 to 4)

> **AI-Free Zone (Weeks 1 to 4).** Reason through requirements and draw architectures yourselves. No AI-generated diagrams or design write-ups.

## Lab Index

### Provided files

| File | What it is |
| :--- | :--- |
| [README.md](README.md) *(this file)* | Lab index, sequence, and deliverables |
| [Lab_A_Read_Reference_Architecture.md](Lab_A_Read_Reference_Architecture.md) | Lab A: read and annotate a real GCP/AWS reference architecture (40 min, pairs) |
| [Lab_B_Design_Your_Pipeline.md](Lab_B_Design_Your_Pipeline.md) | Lab B: design your taxi pipeline, the graded Week 1 deliverable (120 min, teams) |
| [Reference_Architecture_Examples.md](Reference_Architecture_Examples.md) | Student-facing reference diagrams and checklist for architecture grammar; read and compare the representations, do not copy them |
| [architecture_starter.drawio](architecture_starter.drawio) | Draw.io skeleton with zone containers; open at https://app.diagrams.net |
| [nyc_taxi_gcp_reference_architecture.drawio](nyc_taxi_gcp_reference_architecture.drawio) | Editable Draw.io source for the taxi pipeline reference architecture |
| [quality_pii_contract_checkpoints.drawio](quality_pii_contract_checkpoints.drawio) | Editable Draw.io source for the quality, PII, quarantine, and validation checkpoint reference |
| [pattern_choice_map.drawio](pattern_choice_map.drawio) | Editable Draw.io source for choosing batch, streaming, Lambda, Kappa, and medallion patterns |
| [images/](images/) | PNG versions of the reference diagrams used in `Reference_Architecture_Examples.md` |
| [Student_Resources.md](Student_Resources.md) | Architecture patterns, requirements framework, dataset links, Draw.io guide |
| [quiz/Day5_Data_Architectures_Pipeline_Design_Quiz.md](quiz/Day5_Data_Architectures_Pipeline_Design_Quiz.md) | Balanced Markdown Mash practice quiz for Day 5 concepts |

### Sequence

1. **Lab A (morning warm-up):** read a published reference architecture and extract its grammar. Reading one before you draw makes your own design stronger.
2. **Reference examples:** compare the example diagrams against the published architecture you read. What is reusable, what is just one possible representation, and what would your requirements change?
3. **Lab B (afternoon, graded):** translate the business need into requirements and a spec, then design and defend your team's pipeline architecture.

### Deliverables

| # | Deliverable | From | Format | Due |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Reference-architecture notes (zones, services, quality/PII/cost, medallion mapping, one idea to reuse) | Lab A | `design_notes.md` in team folder | End of day |
| 2 | `design_spec.md`: business/stakeholder/system requirements (functional + non-functional) and the data spec | Lab B Phase 1 | Markdown in repo | End of day |
| 3 | `architecture.drawio` + exported `architecture.png` (medallion zones, labeled arrows, ⚠/🔒 marks) | Lab B Phase 2 | Committed to a team repo | End of day |
| 4 | `design_narrative.md`: half-page source-to-dashboard walkthrough with the "why" of each decision | Lab B Phase 3 | Markdown in repo | End of day |
| 5 | 5-minute readout: every member presents one zone; defend against the critique protocol | Lab B Phase 4 | Verbal | End of day |

---

## How the day fits together

The morning builds the architect's vocabulary: the requirements taxonomy (business, stakeholder, system; functional vs non-functional), the data engineering lifecycle, and the architecture patterns (batch/streaming, Lambda, Kappa, Medallion, orchestration). Lab A then has you read a vetted reference architecture so you see the grammar applied. In the afternoon, Lab B is the synthesis and the graded deliverable: translate a business need into a spec, design the pipeline, and defend it. That diagram is a living document you revise in Weeks 3, 5, and 7 and present at the capstone.
