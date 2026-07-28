# Juniper Shield Boardroom Presentation Template

Use this scaffold to create a short live presentation. It is a planning guide, not a written assignment. Replace the prompts with concise slide content.

## Before You Build Slides

**Team name:**  
**Research Lead:**  
**Architecture Lead:**  
**Challenger and Presenter:**  

Complete this sentence together:

> We recommend ___ because it helps Juniper Shield ___, while accepting ___ as a trade-off.

If the sentence is mostly product names, rewrite it in business language.

### AI Research Boundary

Use AI to identify candidates, suggest pros and cons, and generate research questions. Do not ask AI to select the winner, assign matrix scores, choose the architecture, or write the recommendation.

Before using an AI claim, open the original source and mark the claim:

| AI-suggested claim | Source checked | Validated, corrected, or rejected |
|---|---|---|
|  |  |  |
|  |  |  |

## Slide 1: Our Recommendation

**Slide title:** Our Recommendation for Juniper Shield

Include:

- Team name
- One-sentence recommendation
- One business result, such as faster claims decisions, reliable reporting, or manageable growth

Suggested visual:

- One strong recommendation statement
- A small icon or simple business outcome graphic

Do not begin with a list of tools.

## Slide 2: What Matters to the Business

**Slide title:** The Needs That Guided Our Design

Choose three design principles:

1. 
2. 
3. 

Possible principles include:

- Keep claims data fresh enough for operations.
- Make daily reporting reliable.
- Protect sensitive insurance data.
- Keep the platform manageable for a small engineering team.
- Allow the platform to grow without a full redesign.

Include:

- The three principles
- One important assumption
- One question you would ask the stakeholder next

## Slide 3: Main Architecture

**Slide title:** Main Architecture

Insert the exported main architecture from draw.io.

Use a left-to-right flow:

```text
Sources → Ingestion → Storage → Processing and Orchestration → Serving and Analysis
```

Also show:

- Batch and streaming paths
- Security and monitoring
- No more than eight named products or services

Prepare to explain:

1. Where the data begins.
2. How it moves.
3. Where it is stored.
4. How users receive value.
5. Why the design is manageable for this company.

**Source footer:** Add short links or source names for important product claims.

## Slide 4: Our Anchor Decision

**Slide title:** Why We Chose ___ Over ___

Compare only the two tools in your anchor decision.

| Criterion | Weight | Main score, 1 to 5 | Main weighted | Alternative score, 1 to 5 | Alternative weighted |
|---|---:|---:|---:|---:|---:|
| Technical fit | 30 |  |  |  |  |
| Ease of learning and operating | 20 |  |  |  |  |
| Documentation, training, and online answers | 15 |  |  |  |  |
| Support, community, and reputation | 15 |  |  |  |  |
| Total effort and cost | 20 |  |  |  |  |
| **Weighted total** | **100** | | | | |
| **Final score out of 100** | | | | | |

Use:

```text
Weighted points = score × weight
Final score = sum of weighted points ÷ 5
```

Below the matrix, add:

- The strongest reason for the main choice
- The strongest reason for the alternative
- The score with the most uncertainty

**Source footer:** Cite the evidence used for important scores.

## Slide 5: Credible Alternative

**Slide title:** Alternative Architecture

Insert the exported alternative architecture from draw.io.

Include:

- One sentence explaining how it differs
- Its greatest advantage
- Its greatest burden or risk
- The condition that would make it the better choice

Do not present this as a bad design. A thoughtful alternative proves that your team considered the decision rather than defending a favorite product.

## Slide 6: Decision, Risks, and Approval

**Slide title:** Our Decision

Include:

- Why the stakeholder should approve the main architecture
- Two important risks or trade-offs
- How the team would reduce those risks
- One question to validate before implementation

End with:

> Approve this direction because ___.

## Optional Slide 7: Sources

Use this only as an appendix. Do not present it unless asked.

Include at least four credible sources:

| Source | What it helped us decide |
|---|---|
| Official product or project documentation |  |
| Official product or project documentation |  |
| Community, support, or reputation evidence |  |
| Landscape or discovery source |  |

## 15-Minute Speaking Plan

The presentation must last exactly 15 minutes. Q&A happens afterward and is not included in this timing.

| Slide | Section | Time | Speaker |
|---:|---|---:|---|
| 1 | Recommendation and business result | 1 minute |  |
| 2 | Business needs and design principles | 2 minutes |  |
| 3 | Main architecture | 4 minutes |  |
| 4 | Anchor decision | 3 minutes |  |
| 5 | Alternative architecture | 2 minutes |  |
| 6 | Risks and approval request | 3 minutes |  |
| **Total** | | **15 minutes** | |

Every team member must speak. Decide who answers the first stakeholder question and who watches for a teammate who wants to add a point.

## Five-Minute Stakeholder Segment

The presentation is followed by:

| Section | Time |
|---|---:|---|
| Stakeholder questions and team answers | 3 minutes |
| Immediate stakeholder feedback | 2 minutes |
| **Total** | **5 minutes** |

## Stakeholder Question Practice

Ask each other these questions before presenting:

1. What business need made this tool necessary?
2. Why is this path streaming instead of batch?
3. What is the largest hidden effort in the open-source or managed option?
4. What would be difficult for a small engineering team to operate?
5. What condition would make the alternative the better choice?
6. What evidence supports your highest and lowest scores?
7. What is one question you still need the business to answer?

## Final Readiness Check

- [ ] We have no more than six presented slides.
- [ ] We lead with the business problem, not product names.
- [ ] Both diagrams were created in draw.io.
- [ ] Both architectures are credible.
- [ ] The matrix math is correct.
- [ ] Important claims have short citations.
- [ ] We validated important AI-suggested claims against original sources.
- [ ] Our team, not AI, assigned the scores and made the recommendation.
- [ ] Every team member speaks.
- [ ] We can explain each diagram without reading the slide.
- [ ] We have rehearsed to finish at exactly 15 minutes.
- [ ] We are ready to listen to stakeholder feedback without defending every choice.
