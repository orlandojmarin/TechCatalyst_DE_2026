---
title: "Thinking Like a Senior Data Engineer"
module: "Week 6 Day 1"
type: "concept explainer and case study companion"
audience: "Junior data engineers practicing architecture decisions for the first time"
---

# Thinking Like a Senior Data Engineer

## Data Engineering Is More Than Building Pipelines

During the first five weeks, you learned tools and techniques: Python, SQL, pandas, Polars, scheduling, batch processing, cloud services, Databricks, and Snowflake. Those skills help you build.

As engineers become more senior, they are also expected to decide:

- What should the company build?
- Which technology fits the actual need?
- What trade-offs are acceptable?
- What will be difficult to operate later?
- How should the recommendation be explained to the business?

These questions rarely have one correct answer. A strong engineer does not pretend to know everything. They ask useful questions, research unfamiliar options, make their reasoning visible, and recommend a direction.

The Boardroom Architecture Showdown is a first guided practice of that work. It is not a test of how many products you can name.

## The Senior Data Engineer Decision Loop

Use this five-step loop:

1. **Frame the need.** What result does the business need?
2. **Set principles.** What three qualities matter most?
3. **Research options.** What credible tools or patterns could satisfy the need?
4. **Compare trade-offs.** What does each choice improve, and what burden does it create?
5. **Recommend and communicate.** Which direction should the stakeholder approve, and why?

The order matters. If you choose a product first, it becomes easy to force the business problem to fit the product.

## Start With the Business

Compare these two statements:

> We want Kafka, Spark, a lakehouse, Snowflake, and a dashboard tool.

> Claims staff need updated information within five minutes, executives need reliable daily reporting, and a small engineering team must be able to support the platform.

The first statement is a shopping list. The second statement gives the team a basis for making decisions.

Before researching tools, choose three design principles. For example:

- Keep operational claims data fresh.
- Protect sensitive customer data.
- Keep the platform manageable for a small team.

When two tools look equally capable, the principles help you decide which one fits this company.

## Use the Landscape Without Getting Lost

The data technology landscape is enormous. The [2025 MAD Landscape](https://mad.firstmark.com/) shows many categories and vendors. The [Apache Software Foundation project list](https://www.apache.org/index.html#projects-list) and the [GitHub data-engineering topic](https://github.com/topics/data-engineering) reveal a wide range of open-source projects.

Use these resources to discover possibilities. Do not treat discovery as proof.

A tool is not automatically right because:

- it appears on a popular landscape;
- it is an Apache project;
- it has many GitHub stars;
- a cloud vendor promotes it;
- an AI assistant recommends it;
- you used it in a previous lab.

After discovering a candidate, verify the important claims in official documentation. Check what problem it solves, required connectors, deployment model, security features, support options, and operating responsibilities.

## Free Software Still Has a Cost

Open-source software may not charge a license fee. That does not make it free to adopt or operate.

The company may still pay for:

- cloud compute and storage;
- setup and configuration;
- upgrades and security patches;
- monitoring and incident response;
- connector development;
- employee training;
- specialists who understand the platform;
- support contracts;
- time spent finding and fixing answers.

A managed commercial service may cost more on the invoice but require less engineering effort. An open-source tool may offer more control and portability but require more ownership.

Neither approach is automatically better. Ask which burden fits the company.

## Compare One Anchor Decision

In a three-hour activity, you cannot investigate every component deeply. Select one **anchor decision** that meaningfully separates the two architectures.

Examples include:

- Snowflake compared with ClickHouse
- Managed Databricks compared with self-managed Apache Spark
- Managed orchestration compared with self-managed orchestration

Your main architecture is the direction you recommend. Your alternative is another credible direction. The alternative should not be a weak design created to make the favorite win.

The purpose of two designs is to expose the trade-off:

- convenience versus control;
- managed support versus operational ownership;
- integrated platform versus flexible components;
- fast adoption versus portability.

## Use a Simple Evaluation Matrix

Score the two anchor technologies from 1 to 5 using five criteria:

| Criterion | Weight | Question |
|---|---:|---|
| Technical fit | 30 | Does it provide the connectors, processing, scale, security, SSO, and integrations we need? |
| Ease of learning and operating | 20 | Can this team learn, deploy, monitor, upgrade, and troubleshoot it? |
| Documentation, training, and online answers | 15 | Can engineers find reliable help and learning material? |
| Support, community, and reputation | 15 | Is there a healthy support path and evidence of maturity? |
| Total effort and cost | 20 | What will the company pay in money, time, and operational effort? |

For each row:

```text
Weighted points = score × weight
Final score out of 100 = sum of weighted points ÷ 5
```

Suppose a managed service scenario receives scores of 5, 4, 4, 4, and 3:

```text
(5×30 + 4×20 + 4×15 + 4×15 + 3×20) ÷ 5
= (150 + 80 + 60 + 60 + 60) ÷ 5
= 410 ÷ 5
= 82
```

The result is 82 out of 100.

The calculation does not make the decision for you. It makes your judgment visible. A score without a reason is only a guess. A close result means the trade-offs and company context matter even more.

Useful explanations sound like this:

> We scored ease of operation as 4 because the service handles upgrades and scaling, but the team must still learn its security and cost controls.

Weak explanations sound like this:

> We gave it a 5 because it is the best.

## Draw an Architecture People Can Understand

An architecture diagram is a communication tool, not a collection of logos.

Build both diagrams in [draw.io](https://app.diagrams.net/). Use a simple left-to-right flow:

```text
Sources → Ingestion → Storage → Processing and Orchestration → Serving and Analysis
```

Show security and monitoring as cross-cutting concerns. Label arrows so the stakeholder can tell whether data moves as events, files, scheduled batches, SQL queries, or dashboard results.

Keep each architecture to no more than eight named products or services. If you cannot explain why a box exists, remove it.

Use current official icons from sources such as:

- [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)
- [Google Cloud Icon Library](https://cloud.google.com/icons)
- The official brand or architecture page for the selected product

Logos help people recognize products. Labels and arrows explain the architecture.

## Communicate to the Stakeholder

A business stakeholder usually does not want a six-minute product tour. They want to understand:

- What problem will this solve?
- Why should we choose this direction?
- What will it require from the company?
- What risk are we accepting?
- When would the alternative be better?

Connect technical choices to consequences.

Instead of:

> We selected a distributed columnar database.

Try:

> We selected this platform because it can support the claims dashboard as usage grows, while keeping the query experience familiar to the SQL team.

Instead of:

> The open-source option has more operational complexity.

Try:

> The open-source option gives us more control, but our small team would own upgrades, patching, monitoring, and incident response.

A strong recommendation is direct:

> We recommend the managed option because Juniper Shield needs reliable delivery with a small platform team. We accept the license cost in exchange for lower setup and maintenance effort. The open-source alternative becomes more attractive if the company builds a larger platform operations team or needs greater control over deployment.

## Research Like an Advisor

For every important claim:

1. Write the question you are trying to answer.
2. Find the official documentation.
3. Check whether the feature requires a particular edition, cloud, connector, or support plan.
4. Record the source link.
5. Explain how the fact changes the decision.

Use AI to expand your research, not to make the decision. It can suggest candidates, search terms, questions, and possible advantages or disadvantages. It can also summarize documentation that you provide.

The team must still:

- open and read the original sources;
- validate or reject each important AI claim;
- decide the matrix scores;
- choose the architecture;
- make the recommendation;
- explain the reasoning to the stakeholder.

Do not accept a citation only because the link looks official. Confirm that the page exists, supports the claim, applies to the relevant product edition or deployment model, and is current enough for the decision.

A useful AI research request ends with:

> Do not recommend a winner, assign scores, or select the architecture. Give us potential pros, cons, unknowns, and primary sources to investigate. Clearly label uncertain claims. Our team will validate the claims and make the decision.

Do not copy a vendor reference architecture and change the title. Vendor diagrams show what a platform can do. Your team must decide what this company should do.

## Common First-Time Mistakes

### The Logo Parade

The diagram contains every popular tool.

**Better move:** Use the fewest components that meet the important needs.

### Product First

The team picks a favorite tool and searches only for reasons to support it.

**Better move:** Choose business principles first, then compare credible candidates.

### Streaming Everything

The team makes every path real time because one dashboard needs fresh data.

**Better move:** Use streaming where delay affects the business. Keep daily reporting and file movement in simpler batch paths.

### Free Means No Cost

The team ignores setup, upgrades, monitoring, training, and support.

**Better move:** Include people and operating effort in the comparison.

### Feature Language

The presentation lists technical specifications but never explains the business result.

**Better move:** Finish every major technology statement with “so the business can...”

### A Fake Alternative

The second design is obviously weaker.

**Better move:** Explain the situation in which the alternative would become the better decision.

## Key Takeaways

- Senior data engineers frame, research, decide, and communicate.
- Start with business needs and design principles.
- Use landscapes and GitHub for discovery, then verify claims in official documentation.
- Open source can reduce license cost while increasing ownership and engineering effort.
- Compare one anchor decision deeply enough to explain the trade-off.
- Use the matrix to make judgment visible, not to replace judgment.
- Draw the smallest architecture that clearly meets the need.
- Speak in business outcomes, not only technical features.
- A credible alternative strengthens the recommendation.

## Additional Reading

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html): Questions and principles for reviewing cloud architecture decisions.
- [Google Cloud Well-Architected Framework](https://cloud.google.com/architecture/framework): Guidance for connecting architecture choices to operations, security, reliability, cost, and sustainability.
- [Apache Software Foundation Projects](https://www.apache.org/index.html#projects-list): A discovery list of Apache open-source projects.
- [GitHub Data Engineering Topic](https://github.com/topics/data-engineering): A discovery view of public data-engineering repositories.
- [2025 MAD Landscape](https://mad.firstmark.com/): A map of the machine learning, AI, and data technology landscape.
- [draw.io AWS and Google Cloud Shape Libraries](https://www.drawio.com/blog/gcp-aws-shapes-network-diagrams): Instructions for enabling cloud icon libraries in draw.io. Confirm icons against current official vendor assets.

## Currentness Check

| Topic | Source checked | Date checked | How it is used |
|---|---|---|---|
| Architecture principles | AWS and Google Cloud Well-Architected frameworks | 2026-07-27 | Connect technical decisions to business and operating qualities |
| Open-source discovery | Apache Software Foundation project list and GitHub data-engineering topic | 2026-07-27 | Discover candidates, then verify fit separately |
| Technology landscape | 2025 MAD Landscape | 2026-07-27 | Demonstrate the size of the market without treating inclusion as endorsement |
| Diagram assets | AWS, Google Cloud, and draw.io icon guidance | 2026-07-27 | Use draw.io with current, labeled product icons |
