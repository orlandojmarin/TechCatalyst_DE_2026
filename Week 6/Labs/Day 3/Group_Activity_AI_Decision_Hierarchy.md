# Group Activity: The AI Decision Hierarchy

**Time:** 45 minutes
**Format:** Small groups (3-4)
**Concepts practiced:** Problem framing, AI-vs-no-AI judgment, capability taxonomy (rules, classical ML, managed AI service, LLM, LLM with tools), data readiness assessment, build vs. buy vs. experiment vs. kill reasoning
**Senior-thinking muscle:** Resisting the pull toward the most exciting technology before confirming the problem needs it at all, and stopping the moment a gate fails instead of forcing the idea through to a build decision anyway

## Why this exists

You have now spent two days building things. Day 2 was classical ML on tabular data. Today was LLM APIs, function calling, agents, and MCP. Both were fun, and that is the trap.

The most expensive mistakes in this field are not bad code. They are a team spending a quarter building a model for a problem that a `WHERE amount > 10000` clause already solved, or wiring an LLM into a workflow that needed a lookup table. The skill that separates a data engineer from someone who follows tutorials is knowing when **not** to reach for the thing you just learned.

## Scenario

Leadership at Hartford Mutual Insurance is reviewing five "AI initiatives" pitched by different departments this quarter. Before any budget is approved, your team has been asked to run one of them through a decision framework and report back with a recommendation, and the reasoning behind it.

## The Five Gates

Work through these **in order**. If an initiative fails a gate, stop there, record why, and skip the remaining gates. Do not skip ahead just because a later gate looks more interesting.

1. **Is this actually an AI problem?** If a fixed rule, a lookup table, or a SQL query already solves it, that is the answer. Stop here.
2. **Can you frame it?** Is there a specific input, a specific output, and a concrete way to know whether the output was right? A problem nobody can define a success metric for cannot be built, no matter how much data or budget you throw at it.
3. **Which class of solution does it need?** Pick exactly one from the table below.
4. **Do you have the data that specific class needs?** Not "do we have data," but "do we have the data *this class of solution* requires." A managed vision API needs images. A classical model needs labeled history. An agent needs a real system to call.
5. **Build, Buy/Partner, Experiment, or Kill?** Only reachable if the initiative survived Gates 1 to 4. Justify with one concrete fact from the scenario card, not a general impression.

### Gate 3: the classes

| Class | What it is | What it needs |
|---|---|---|
| **Deterministic automation** | A rule, a threshold, a SQL query. No learning involved. | A clearly stated rule |
| **Classical ML** | A model trained on your structured/tabular history (Day 2) | Labeled historical rows |
| **AI as a service** | A pre-trained, narrow model behind one API call (vision, speech, entity extraction) | Inputs in the format that service expects |
| **LLM, prompt only** | Open-ended language work: summarize, classify, rewrite, extract (Activities 1 and 4) | A good prompt, and tolerance for occasional wrong answers |
| **LLM with tools** | A model in a loop calling your systems to act or fetch live facts (Activities 3 and 5) | Real functions or APIs worth calling, and a way to check the result |

If a team's answer is "an LLM grounded in our own documents," that is **RAG**, and it is tomorrow's topic. Name it, note that it is a distinct sixth class, and move on.

## Your Task

1. Your team is assigned **one** initiative card below.
2. Walk it through the five gates in order. Record your team's answer and one-sentence reasoning at each gate you reach.
3. If it survives all five gates, make the Gate 5 call and defend it in 2-3 sentences.
4. Prepare a 3-minute verbal readout for the room: which gate you stopped at (or didn't), and your recommendation.

## Constraints

- Stop at the first gate your initiative fails. "But AI would still be cool here" is not a reason to continue.
- Gate 3's classes are mutually exclusive for this exercise. Pick the single best fit and be ready to explain why you rejected the others, especially the one directly above and below it in the table.
- Your Gate 5 answer needs one concrete piece of evidence pulled from the scenario card, not a vibe.
- **The no-code question.** Somebody in the room will suggest wiring your initiative together in a no-code automation tool (n8n, Zapier, Power Automate) with an LLM node in the middle. Have an answer ready for whether that is a reasonable way to ship your initiative, a reasonable way to *prototype* it, or neither, and say why. "It would work" and "it would be the right call" are different claims.

## Initiative Cards

### Card A: Large Claim Auto-Flagging

Hartford Mutual's claims system already stores every claim's dollar amount as a clean, structured field. A department head wants "an AI system that flags claims over $10,000 for manager review," concerned that the current process misses some.

### Card B: Intake Photo Data Extraction

Adjusters currently retype the license plate and VIN from intake photos into the claim record by hand, a slow, error-prone step. Thousands of intake photos exist from past claims, but none of them are labeled with the correct plate or VIN text; that information only lives in the claim record itself, entered separately by a human.

### Card C: Policyholder Churn Prediction

Retention wants to know which policyholders are likely to cancel in the next 90 days so an agent can reach out first. Hartford Mutual has full billing and policy history for every customer going back years, but has never systematically recorded *why* someone actually left. Cancellations are just a status flag with no reason code attached.

### Card D: Plain-English Policy Q&A

Customer support wants policyholders to be able to ask questions in plain English ("am I covered if my basement floods?") and get an instant, accurate answer instead of waiting on hold. Hartford Mutual has a full library of policy documents and FAQ content, currently maintained as PDFs and Word documents scattered across three different internal SharePoint sites.

### Card E: The Adjuster Assistant

Claims operations wants an internal assistant adjusters can ask things like "what is the net payout on claim CLM_4471 after the deductible, and has this policyholder filed before?" Today an adjuster answers that by opening three systems and doing the arithmetic in their head. All three systems have stable, documented internal APIs, and every one of those APIs is read-only.

## Deliverable

A filled worksheet (the gates you reached, your team's answer and reasoning at each, and your final Gate 5 call if you reached it) and a 3-minute verbal defense to the class. Be ready for the room to push back with a counter-scenario. If your Gate 3 pick was "LLM with tools," someone will ask why not a plain prompt, or why not a report, and you should have an answer ready.

## Optional Follow-Up

Your instructor may point you to `ai_opportunity_scorer.html` in the Day 4 lab folder, a more detailed weighted scoring tool covering the same Build/Buy/Experiment/Kill decision across six business dimensions. Score your assigned initiative in the tool and compare its output to your team's own Gate 5 call. Where do they agree, and where does the tool's more detailed scoring change the picture?
