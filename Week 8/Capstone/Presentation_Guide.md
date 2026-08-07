# Presentation Guide

**20 minutes, plus 5 minutes of questions. Three people. Everyone speaks. Everyone takes at least one question.**

Your audience is mixed. Some listeners write pipelines for a living. Some will only ever see the dashboard. You have to land with both in the same 20 minutes, which is the hardest and most valuable communication skill in this profession.

---

## Structure

Roughly this, adapted to your project. Times are guides, not rules.

| Section | Time | What it does |
| :--- | :--- | :--- |
| Problem and question | 2 to 3 min | What you set out to answer and why anyone should care |
| Data and approach | 3 to 4 min | What you were given, what shape it was in, and your architecture |
| Data quality | 2 to 3 min | What was wrong with the data and what you did about it |
| Findings | 5 to 6 min | Your year-over-year result and supporting analysis, with the dashboard |
| Technical deep dive | 3 to 4 min | Design decisions, trade-offs, cost reasoning |
| Future state | 1 to 2 min | What you would build next and what it would take |
| Recommendation | 1 min | What the client should do |

Findings is the largest block. If your technical deep dive runs longer than your findings, you have built a tool demonstration rather than a consulting engagement.

---

## Open with the finding, not the agenda

The strongest openings in past cohorts stated the headline result in the first 30 seconds and spent the rest of the talk earning it.

The weakest opened with "Hi, we are team 2, here is our agenda, first we will discuss our architecture."

Your audience decides in the first minute whether this is worth their attention. Spend it on something real.

---

## Serving both audiences

A technique that works: state the business fact, then immediately support it with the technical detail, in the same breath.

> "Trips to the airport zones grew 12 percent year over year, and we are confident in that number because we reconciled it against the source files and confirmed it is not an artifact of the zone lookup change."

The business listener hears the first half. The engineer hears the second. Nobody is bored and nobody is lost.

What does not work is splitting the talk into a business half and a technical half. You lose one audience for ten minutes each time.

---

## The data quality section

Do not skip this and do not apologize for it. Being able to say "here is what was wrong with the data, here is how much of it, here is what we did, and here is how that limits our conclusions" is exactly what marks an engineer who can be trusted.

Cover: what you found, how much was affected, what you decided, and what it means for the findings you just presented.

If the cash tip trap touches any of your charts, say so explicitly. An unacknowledged one is the fastest way to lose credibility with anyone in the room who knows the dataset.

---

## Your visuals

- Every chart has a labeled axis and a title that states the point, not the mechanics. "Airport trips grew 12 percent" beats "Trips by zone by year."
- Do not show raw table dumps. If a number matters, put it on a slide by itself.
- The architecture diagram gets its own slide and enough time to actually read it.
- Screenshot your dashboard as a fallback. Live demos fail, networks drop, and Snowflake sessions expire.
- Do not read your slides aloud. The audience is faster at reading than you are at speaking.

---

## Splitting the talk

Three people, 20 minutes. Do not split into three rigid seven minute blocks with awkward handoffs.

What works better: assign sections by who did the work and who tells that part best. Practice the handoffs specifically, they are where teams look unrehearsed. One person should own the opening and the closing so the talk has a frame.

Everyone must speak for a meaningful stretch. A member who says one sentence has not presented.

---

## Questions

Expect them to be hard. That is a sign the audience is engaged.

- **"How do you know that number is right?"** Have the answer ready. It is the most likely question and the most important one.
- **"What would you do differently?"** Have a real answer, not a modest deflection.
- **"Why did you choose X over Y?"** This is why the decision log exists.
- **"What is the cost of running this?"** Your cost rationale covers it.

If you do not know: say so, say how you would find out, and move on. That is a complete and professional answer. Bluffing is obvious to everyone in the room and it costs you more than the admission would have.

If a question is for a specific teammate, let them answer. Talking over each other reads as a team that did not work together.

---

## Rehearse

Out loud. With slides. Timed. Once before you deliver on Friday, and at least twice more in the days before Demo Day.

Reading through the deck silently is not rehearsal, and it will not reveal that your findings section runs eleven minutes.

Time the whole thing. Going long is the most common failure and it usually eats the recommendation, which is the part your audience most wanted.

---

## What a strong presentation looks like

The audience leaves able to state your finding in one sentence, believing it, understanding roughly how you built the thing that produced it, and knowing what you think should happen next.

That is the bar. Not "they were impressed by the technology."
