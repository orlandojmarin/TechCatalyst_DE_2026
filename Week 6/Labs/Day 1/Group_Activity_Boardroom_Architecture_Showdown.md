# Group Activity: Boardroom Architecture Showdown

## The Challenge

You are part of a three-person data architecture team advising **Juniper Shield Insurance**, a fictional regional insurer building a new data platform from scratch.

All teams receive the same assignment. Your goal is to research the technology landscape, compare two credible approaches, recommend a main architecture, and defend why it is the best fit for this company.

There is no single correct stack. A strong proposal will make clear, well-supported decisions.

## What This Activity Is Really Teaching

This is your first guided architecture consultation. You are not expected to know every tool or produce a perfect enterprise design in three and a half hours.

The tools are the setting for a larger lesson. As data engineers become more senior, their work includes more than Python and SQL. They must:

1. Ask questions before selecting technology.
2. Research unfamiliar options without getting lost in the landscape.
3. Make a decision when every option has trade-offs.
4. Connect technical choices to business needs.
5. Explain a recommendation to people who do not want a tool lecture.

Your instructor will play the business stakeholder. Speak to that stakeholder, not only to other engineers.

## Learning Goals

By the end of this activity, you will be able to:

1. Translate business needs into architecture requirements.
2. Research open-source and commercial data engineering tools.
3. Compare tools using a simple, evidence-based evaluation matrix.
4. Recognize that free software still requires engineering time and operational effort.
5. Create clear architecture diagrams with correct technology logos.
6. Recommend and defend a main design while presenting a credible alternative.

## Team Format

- Three teams of three students
- One shared assignment for every team
- Three and a half hours total
- Every student must contribute to the research, design, and presentation

Choose three roles:

| Role | Primary responsibility |
|---|---|
| Research Lead | Finds reliable evidence and records sources |
| Architecture Lead | Builds the draw.io diagrams and checks the data flow |
| Challenger and Presenter | Questions assumptions, tests the recommendation, and leads the pitch |

The roles divide responsibility, not participation. All three team members must speak during the final presentation.

## Company Brief

Juniper Shield Insurance serves customers across the United States. It is large enough to need an enterprise-grade platform, but it does not have unlimited people, time, or money.

The company currently has:

- A policy and claims database that changes throughout the day
- Billing files that arrive in scheduled batches
- Telematics events from connected vehicles
- Claim documents, adjuster notes, and call transcripts
- Business teams using SQL, dashboards, Python, and spreadsheets

The new platform must support:

- A claims operations dashboard refreshed within five minutes
- Daily executive and regulatory reporting ready each morning
- Historical analysis for pricing, risk, and fraud teams
- Access control, encryption, audit history, and enterprise identity integration such as SSO
- Reliable recovery when a pipeline or service fails
- A small data engineering team that must operate the platform
- Growth in data volume and users without a complete redesign

Assume the company is starting fresh. Do not copy an existing employer architecture.

## Your Mission

Create and defend:

1. **Main Architecture:** the approach your team recommends.
2. **Alternative Architecture:** another credible approach with a different technology or operating philosophy.

For example, your two approaches might compare:

- An open-source-leaning platform with a managed commercial platform
- ClickHouse with Snowflake
- Self-managed Apache Spark with managed Databricks
- Self-managed orchestration with managed orchestration

These are examples, not required choices. The alternative must be realistic. Do not create a weak option only to make the main architecture look better.

To keep the work achievable, choose **one anchor technology decision** for detailed scoring. The anchor decision should meaningfully distinguish the main architecture from the alternative. Give shorter justifications for the remaining components.

## Architecture Boundaries

Each architecture should show these layers:

1. Data sources
2. Ingestion
3. Storage
4. Processing and orchestration
5. Serving and analysis
6. Cross-cutting security and monitoring

Use no more than eight named products or services in each architecture. Prefer a small design that your team can explain over a diagram filled with tools.

## Required Diagram Tool

Use [draw.io](https://app.diagrams.net/) for both diagrams.

Create one editable `.drawio` file with two pages:

- Page 1: Main Architecture
- Page 2: Alternative Architecture

Export each page as PNG or PDF so it can be placed in the presentation slides.

Diagram standards:

- Use official or current product logos.
- Arrange the flow from left to right.
- Label arrows with what moves, such as events, files, SQL queries, or dashboard data.
- Show batch and streaming paths clearly.
- Use a legend if colors or line styles have meaning.
- Include a small security and monitoring area rather than repeating every control.
- Add a short text description so the architecture can still be understood without relying only on color or logos.

In draw.io, select **More Shapes**, then enable the relevant cloud and networking libraries. If a built-in icon is outdated or missing, import the current SVG from the vendor's official architecture icon page.

## Research Rules

Use AI as a research assistant, not as the decision-maker.

AI can help you:

- Discover possible tools and useful search terms.
- Suggest potential advantages and disadvantages for each option.
- Generate questions that your team should investigate.
- Summarize documentation that you provide.

AI cannot do the team's judgment work. Do not ask it to:

- Select the winning technology.
- Assign your matrix scores.
- Choose your main architecture.
- Make the final recommendation.
- Replace your review of the original sources.

AI output is a research lead, not evidence. Open the cited sources, confirm that they support the claim, check important conditions such as product edition or deployment model, and correct or reject anything that is inaccurate.

### Example AI Research Prompt

Replace the brackets before using this prompt:

```text
Act as a research assistant, not a decision-maker.

We are advising Juniper Shield Insurance, a regional insurer with a small
data engineering team. The company needs a five-minute claims dashboard,
reliable daily reporting, historical analytics, security, SSO, and room
to grow.

Help us research [Tool A] and [Tool B] for [the anchor decision].

For each tool:
1. Suggest potential advantages for this specific company.
2. Suggest potential disadvantages, hidden effort, and operating risks.
3. Identify important unknowns that our team must investigate.
4. Suggest official documentation or primary sources for each major claim.
5. List questions that would help us compare technical fit, learning and
   operations, documentation and training, support and reputation, and
   total effort and cost.

Do not recommend a winner, assign scores, select an architecture, or make
the final decision. Clearly label uncertain claims. We will open every
source and independently validate the claims before using them.
```

After using AI, make a quick research check:

| AI-suggested claim | Original source opened | Validated, corrected, or rejected | How it affects our decision |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

Use at least four credible sources, including:

- At least two official product or project documentation pages
- At least one source that provides evidence about community, support, reputation, or maturity
- At least one source that helps you discover unfamiliar tools

Useful discovery starting points:

- [2025 MAD Landscape](https://mad.firstmark.com/)
- [Apache Software Foundation Projects](https://www.apache.org/index.html#projects-list)
- [GitHub Data Engineering Topic](https://github.com/topics/data-engineering)

Discovery is not proof. A tool appearing on a landscape, in an Apache project list, or in a popular GitHub repository does not prove that it fits Juniper Shield. Verify important claims in official documentation.

## Tool Landscape Scavenger Hunt

Before selecting your architecture, find:

- One open-source candidate
- One commercial or managed candidate
- One tool that nobody on your team knew before today

Record what problem each tool solves and one reason it may or may not fit Juniper Shield. Your new discovery does not have to appear in the final architecture.

## Simple Tool Evaluation Matrix

Score the two candidates in your anchor decision from 1 to 5.

| Criterion | Weight | What to consider |
|---|---:|---|
| Technical fit | 30 | Required connectors, batch or streaming support, scale, security, SSO, and integrations |
| Ease of learning and operating | 20 | Learning curve, setup, upgrades, monitoring, and daily administration |
| Documentation, training, and online answers | 15 | Documentation quality, tutorials, training, examples, and ability to find reliable answers |
| Support, community, and reputation | 15 | Vendor support, community health, project maturity, adoption, and reputation |
| Total effort and cost | 20 | Licensing or cloud charges plus engineering time for setup, maintenance, patching, and support |
| **Total** | **100** | |

Use this scale:

| Score | Meaning |
|---:|---|
| 1 | Poor fit or high burden |
| 2 | Significant concerns |
| 3 | Acceptable with trade-offs |
| 4 | Strong fit |
| 5 | Excellent fit or low burden |

For **Total effort and cost**, a score of 5 means the lowest overall burden for this company. Do not calculate a three-year financial forecast. Explain the important visible and hidden costs.

### Full Scoring Example

This fictional example compares two operating scenarios, not named products:

- **Managed Service Scenario:** the company uses a vendor-managed service.
- **Self-Managed Open-Source Scenario:** the company operates an open-source tool itself.

The labels describe who operates the technology. They are not product or vendor names, and the example is not a recommendation.

| Criterion | Weight | Managed Service score | Managed Service weighted | Self-Managed Open Source score | Self-Managed Open Source weighted |
|---|---:|---:|---:|---:|---:|
| Technical fit | 30 | 5 | 150 | 4 | 120 |
| Ease of learning and operating | 20 | 4 | 80 | 3 | 60 |
| Documentation, training, and online answers | 15 | 4 | 60 | 4 | 60 |
| Support, community, and reputation | 15 | 4 | 60 | 5 | 75 |
| Total effort and cost | 20 | 3 | 60 | 4 | 80 |
| **Weighted total** | **100** | | **410** | | **395** |
| **Final score out of 100** | | | **82** | | **79** |

Calculation:

```text
Weighted points = criterion score × criterion weight
Final score = sum of weighted points ÷ 5

Managed Service = (5×30 + 4×20 + 4×15 + 4×15 + 3×20) ÷ 5
                = 410 ÷ 5
                = 82

Self-Managed Open Source = (4×30 + 3×20 + 4×15 + 5×15 + 4×20) ÷ 5
                         = 395 ÷ 5
                         = 79
```

The numbers do not make the decision for you. A close result means the trade-offs and company context matter. Every score must have a short reason and supporting evidence.

## 3.5-Hour Activity Arc

| Step | Minutes | Team output |
|---:|---:|---|
| 1. Form the team and choose roles | 5 | Named roles |
| 2. Read the brief and choose three design principles | 15 | Three prioritized principles |
| 3. Complete the landscape scavenger hunt | 15 | Three researched candidates |
| 4. Research the main and alternative anchor technologies | 35 | Evidence notes and source links |
| 5. Complete the evaluation matrix | 20 | Scored comparison with reasons |
| 6. Build both architecture pages in draw.io | 40 | Main and alternative diagrams |
| 7. Build and rehearse the presentation | 20 | Six concise slides and shared speaking plan |
| 8. Present, answer questions, and receive feedback | 60 | Fifteen-minute presentation, three-minute Q&A, and two-minute feedback per team |
| **Total** | **210** | |

## Live Presentation Only

There is no written proposal, file submission, or activity grade. Your work ends in a live boardroom presentation. Your instructor will ask questions as the Juniper Shield stakeholder and give feedback immediately after each team presents.

Create no more than six slides:

| Slide | Purpose | What to show |
|---:|---|---|
| 1 | Recommendation | Team name, one-sentence recommendation, and the business result it supports |
| 2 | Business needs | Three design principles and the most important company constraints |
| 3 | Main architecture | Main draw.io diagram, data flow, and why it fits |
| 4 | Anchor decision | Completed evaluation matrix, evidence, and the biggest trade-off |
| 5 | Alternative architecture | Alternative draw.io diagram and the condition that would make it the better choice |
| 6 | Decision and risks | Why the stakeholder should approve the main design, two risks, and one next question |

Add short source citations in slide footers. You may include one optional source appendix slide, but do not present it unless the stakeholder asks.

Use any shared slide tool available to your team. Create both architecture diagrams in draw.io, then place the exported diagrams into the slides. If you download working files, keep them under `student-work/week6/day1/`. Nothing needs to be submitted.

Use the [student presentation template](./starter/Insurance_Architecture_Presentation_Template.md) to plan the slides.

## The 15-Minute Boardroom Presentation

Every team member must speak.

The presentation itself must last exactly 15 minutes. It does not include Q&A or feedback. Rehearse so that your team does not finish early or run over. The stakeholder will stop the presentation at 15 minutes.

Use this structure:

| Slide | Focus | Time |
|---:|---|---:|
| 1 | Recommendation and business result | 1 minute |
| 2 | Business needs and design principles | 2 minutes |
| 3 | Main architecture and data flow | 4 minutes |
| 4 | Anchor decision and evidence | 3 minutes |
| 5 | Alternative architecture and switch condition | 2 minutes |
| 6 | Trade-offs, risks, and approval request | 3 minutes |
| **Total presentation** | | **15 minutes** |

After the presentation, the stakeholder has:

- Three minutes for questions and answers
- Two minutes for immediate feedback

Each team therefore receives one 20-minute boardroom slot. Expect questions such as:

- What evidence supports your lowest or highest score?
- Where is the largest hidden cost?
- What happens if data volume grows ten times?
- What would be hardest for a small team to operate?
- What condition would make you switch to the alternative?

## Live Feedback Lens

This activity is for practice, not points. Live feedback will focus on:

- **Strategy:** Did the team identify what matters to the business before choosing tools?
- **Research:** Did the team support important claims with credible evidence?
- **Decision quality:** Are the main and alternative both credible, and are the trade-offs honest?
- **Architecture:** Can the stakeholder follow the flow and understand why each major component exists?
- **Communication:** Did the team explain business impact in plain language and respond thoughtfully to questions?

## Success Checklist

- [ ] We selected three design principles before choosing tools.
- [ ] We found an open-source candidate, a commercial or managed candidate, and one unfamiliar tool.
- [ ] We selected one anchor decision for detailed comparison.
- [ ] Our five criterion weights total 100.
- [ ] We showed the calculation and explained every score.
- [ ] Our main and alternative architectures are both credible.
- [ ] Each diagram uses no more than eight named products or services.
- [ ] Both pages were created in draw.io with current logos and labeled flows.
- [ ] We included security, monitoring, batch, and streaming concerns.
- [ ] Our slides include at least four credible sources in short footers or an appendix.
- [ ] Every team member has a speaking part.
- [ ] Our presentation explains business value, not only product features.
- [ ] We have rehearsed the presentation to finish at exactly 15 minutes.
