# Group Activity: Terminal Operations Decision Brief

**Time:** 35 minutes  
**Format:** Triads  
**Concepts practiced:** terminal environment choice, automation risk, cloud shell trade-offs, operational communication, Week 1 synthesis (IAM, version control, object storage, architecture)  
**Senior-thinking muscle:** advising a team before implementation

## Why This Activity

You just wrote a real check: `summarize_hunt.sh`. It counts rows, scans a log for errors, and prints a pass or fail result. You also read cron schedules that could run it on a timer. A data engineer is not only the person who writes that script. They are the person who decides where it should run, how it gets scheduled, and how a team can trust it. That decision is the job this activity practices.

This is also a checkpoint that pulls Week 1 forward. A good answer here is not just about the terminal. It uses the cloud and permissions thinking from Week 1 Day 2, the version control and code review habits from Week 1 Day 3, the object storage and lifecycle ideas from Week 1 Day 4, and the pipeline architecture your team drew on Week 1 Day 5. The strongest briefs connect today's small script to the bigger picture you have been building all along.

By the end you will be able to defend a run-location choice using evidence, not opinion, place it inside your team's architecture, and explain it to a non-technical stakeholder.

## Scenario

A small analytics team wants to move your daily check off one analyst laptop into a more reliable workflow. The script is the one you wrote today: it counts order rows, scans `pipeline.log` for errors, and writes a summary. The stakeholder wants the fastest path that is still safe, explainable, and easy to recover if something fails.

There are three possible places to run it:

1. The **Ubuntu terminal** on a class machine.
2. A **browser-based cloud shell** in the managed cloud account.
3. A **future orchestrator** such as Airflow or Cloud Composer, once the team has learned it.

## Ops Reality Card

Use these facts as evidence. Do not invent around them.

- The class Ubuntu VM is wiped when the cohort ends. Nothing saved only on it survives.
- The cloud shell already has cloud credentials and CLIs configured. It also has a session timeout and limited home storage.
- Your script currently writes output to the terminal. It does not yet write a saved log or summary file.
- A scheduled run would use a cron line you can already read, for example:
  ```cron
  0 6 * * * bash /home/student/summarize_hunt.sh >> /home/student/summarize_hunt.log 2>&1
  ```
- The orchestrator is powerful but the team has not learned it yet. Standing it up now would take days the team does not have this week.

## Your Task

1. List 3 assumptions or questions you must confirm before choosing a run location. Tie at least one to a fact on the Ops Reality Card.
2. Fill in the trade-off table with short, evidence-based notes.
3. Recommend one run location for **today** and one **future** migration path.
4. State exactly where logs or summary output should go, and one safety check to run before the command.
5. Use the Week 1 lenses below to pressure-test your recommendation, and place this check inside your team's Week 1 architecture diagram.
6. Prepare a 2-minute briefing for the stakeholder.

## Connect To Week 1

Your recommendation is stronger when it speaks the language your team already built last week. Use each lens at least once in the brief.

| Week 1 idea | Day | Question to answer here |
| :--- | :--- | :--- |
| IAM, permissions, billing | Day 2 | Who is allowed to run this, and where do the credentials live? Is the cloud shell safer than copying secrets onto a laptop? |
| Git, version control, code review | Day 3 | How is the script itself stored, versioned, and peer reviewed, so a teammate can trust and change it? |
| Object storage and lifecycle | Day 4 | Where should the summary output and logs persist so they survive after the run, instead of only printing to a terminal that disappears? |
| Pipeline architecture | Day 5 | Where does this check sit in your team architecture diagram? What does it depend on, and what depends on it? |

You do not need to redraw the diagram. One or two sentences placing the check in it is enough.

## Trade-Off Table

Rate each cell High, Medium, or Low, then add a few words of justification from the Ops Reality Card.

| Criterion | Ubuntu terminal | Cloud shell | Future orchestrator |
| :--- | :--- | :--- | :--- |
| Setup effort today |  |  |  |
| Credential and permission risk |  |  |  |
| Logging and auditability |  |  |  |
| Repeatability and scheduling |  |  |  |
| Survives after the cohort ends |  |  |  |
| Fit for today's learners |  |  |  |

For the orchestrator column, do not pretend to know the tool. Instead answer one question: **what would have to become true for this to be the right move?** That is the real senior skill, knowing when not to overbuild.

## Constraints

- The class is in the AI-Free Zone. You may use documentation, but no AI assistant may write the recommendation for you.
- The solution must be explainable to a non-technical stakeholder.
- The recommendation must include one safety check before running a command, such as `pwd` and `ls`.
- The recommendation must say where logs or summary output should go, since the script does not save them yet.

## Deliverable

A short decision brief with:

- Recommended run location for today, with one sentence of evidence.
- Future migration path, and the trigger that would justify it.
- 3 assumptions or questions.
- Completed trade-off table.
- 2 risks and their mitigations.
- One or two sentences placing the check in your Week 1 architecture, and at least two of the Week 1 lenses applied (IAM, version control, object storage, or architecture).
- 5-minute presentation (use your slides).

## What A Strong Brief Looks Like

**Strong:** "Run it on the cloud shell today. Credentials are already configured, so we avoid copying secrets onto a laptop, and it survives the cohort wipe. Before running, we check `pwd` and `ls` so we do not run it in the wrong folder. We append output to `summarize_hunt.log` with `>> ... 2>&1` so both results and errors are saved. We move to an orchestrator only when this job grows dependencies on other jobs, which it does not have yet."

**Weak:** "Use cloud because cloud is better." No evidence, no log location, no recovery plan, no reason against the other two options.

## Presenting

Be ready to deliver your 2-minute brief to the room as if the stakeholder were present. Every member of the triad should be able to answer a follow-up question about the recommendation.

> Facilitation notes, probes, and the strong-versus-weak answer guide for this activity live in the instructor guide (`Week 2/Instructor Notes/Day 1 - Instructor Guide.md`), not in this handout.
