# Claim Pipeline Banner

In this activity, you will explore loops by iterating through a string and
through a range of numbers.

## Background

The claims operations team wants a small status banner the intake system can
print when a batch of claims starts processing. The banner spells out the current
pipeline stage one letter at a time, then reports how many claims are in the
batch. You will build it with two loops: one over a string, one over a range.

## Instructions

Using `Unsolved/status_banner.py`, complete the following steps.

1. Create a variable named `stage` that holds a single pipeline stage as a string,
   for example `"INTAKE"`.

2. Use a `for` loop to loop through each letter in `stage` and print a banner line
   for each letter.

3. After the loop, print what the stage spells.

4. Use a second `for` loop over `range(1, 6)` to print one line per claim in the
   batch.

## Expected Output

```text
Give me a I!
I!
Give me a N!
N!
Give me a T!
T!
Give me a A!
A!
Give me a K!
K!
Give me a E!
E!

What does that spell?!
INTAKE! Claims are moving through INTAKE.

Processing today's batch:
  Claim 1 of 5 processed
  Claim 2 of 5 processed
  Claim 3 of 5 processed
  Claim 4 of 5 processed
  Claim 5 of 5 processed
```

## Challenge

Use `enumerate` so each batch line shows the index and a claim id from a list of
claim ids, instead of a plain counter.

## Hint

A `for` loop walks a string one character at a time. `range(1, 6)` gives you the
numbers 1 through 5.
