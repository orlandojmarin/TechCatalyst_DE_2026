# The Triage Conundrum

In this activity, you will read Python scripts that implement conditional
statements using comparison and logical operators, and predict what each one
prints before you run it.

## Background

Claim triage is decision logic: route this claim to the standard queue, escalate
that one, send another to the Special Investigations Unit. A teammate has written
a Python script full of triage conditionals and wants to quiz you. Work through
the decisions in your head first, then run the file to check yourself.

## Instructions

1. Open `Unsolved/conditionals.py`. Look through each example and figure out what
   the output would be for each conditional statement.

2. Do not run the code yet. First see if you can follow the thought process and
   predict the output.

3. Once you have predicted every answer, run the file and compare.

```bash
uv run python conditionals.py
```

## Challenge

For any branch you predicted wrong, write one sentence explaining which operator
or comparison you misread. Reading conditionals correctly is how you debug routing
logic in a real pipeline.

## Success Criteria

- You wrote down a prediction for every branch before running the file (this is a
  predict-then-verify drill, so there is no separate "Expected Output" to check
  against; the file's own printed output is the answer key).
- After running it, every prediction matches the actual output, or you can name
  exactly which comparison or operator you misread.
- You can explain, in your own words, the difference between `==` and `=`, and
  between `and`/`or` short-circuiting.
