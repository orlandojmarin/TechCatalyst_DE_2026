# Triage Faceoff

Create a command-line program that compares your severity assessment of an
incoming claim against the system's reading, using user input and a random
choice.

## Background

When a claim comes in, an adjuster assigns it a severity: low, medium, or high.
That call decides how the claim is routed. Get it wrong and you either tie up a
senior adjuster on a small claim (over-triage) or let a risky claim sit in the
standard queue (under-triage). In this drill the system picks the claim's true
severity at random, you make your call, and the program tells you how you did.

## Instructions

Copy `Unsolved/triage_sim.py` to your project and complete the following:

* The system already picks a true severity with `random.choice` from
  `["low", "medium", "high"]`.

* Take an input of `low`, `medium`, or `high` from the adjuster.

* Compare the adjuster's call to the system's reading using the `rank` lookup and
  handle four cases:

  * Invalid input (not one of the three levels).
  * Correct triage (the calls match).
  * Under-triage (your call ranks lower than the system's).
  * Over-triage (your call ranks higher than the system's).

Run it:

```bash
uv run python triage_sim.py
```

## Challenge

Wrap the faceoff in a loop that plays five rounds and prints how many you triaged
correctly. This is the same scoring pattern a quality-assurance team uses to
audit adjuster accuracy.

## Hint

A dictionary that maps each level to a number (`{"low": 1, "medium": 2,
"high": 3}`) lets you compare severities with `<` and `>` instead of writing every
combination by hand.

## Success Criteria

- The result depends on `random.choice` and your own input, so there is no single
  fixed "Expected Output." Instead, run the program at least four times and
  confirm you can produce all four outcomes: invalid input, correct triage,
  under-triage, and over-triage.
- Invalid input (anything other than `low`, `medium`, or `high`) is handled and
  does not crash the program.
- (Challenge) Your five-round loop prints a final count of how many rounds you
  triaged correctly.
