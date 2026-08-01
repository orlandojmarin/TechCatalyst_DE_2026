# Activity 7: Narrate With an LLM

**Module:** Week 7 Day 1
**Estimated Time:** 35 minutes
**Difficulty:** Intermediate
**Format:** Individual
**Prerequisites:** Activity 6 complete (the trailing-window anomaly detector, six flagged dates)

## Objective

In this activity, you will add a feature to the anomaly detector from Activity 6: a button that asks an LLM to draft a short analyst paragraph about the flagged dates. The model never sees the raw taxi data. It only receives a plain-text block of facts your code already computed. Your job is not to admire the paragraph. It is to fact-check it, correct it, and hand in the corrected version.

## Background

### The model narrates, it does not analyze

Week 6 taught you the OpenAI SDK: how to build a client, send messages, and read a response. Week 7 is about using that skill honestly. An LLM is very good at turning a list of numbers into readable prose, and it is not a reliable source of new numbers or new analysis. So this app draws a hard line: the code computes every fact (the date range, the mean, the six flagged dates, their values, their z-scores), and the model only writes sentences about facts it is handed as text.

```python
def build_facts(series: pd.Series, flags: pd.Series, z: pd.Series, window: int) -> str:
    lines = [
        f"Series: NYC daily taxi rides, {series.index.min().date()} to {series.index.max().date()}.",
        f"Mean daily rides: {series.mean():,.0f}. Smoothing window in use: {window} days.",
        "Anomalies detected with a trailing 28-day z-score, threshold 3:",
    ]
    for date, value in flags.items():
        lines.append(f"  {date.date()}: {value:,.0f} rides, z = {z[date]:.2f}")
    return "\n".join(lines)
```

Notice what `build_facts` takes: `series`, `flags`, and `z`, the same objects Activity 6 computed. Notice what it returns: a plain string. That string, and nothing else, is what gets sent to the model. The DataFrame never leaves this function. If a number is not printed into this string, the model has no way to know it exists, and any number the model states that is not in this string was invented.

### Why the call sits behind a button

```python
if st.button("Draft the narrative"):
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("No OPENAI_API_KEY found. Check your .env at the repository root.")
    else:
        with st.spinner("Drafting..."):
            st.write(draft_narrative(facts))
```

Remember the Streamlit rerun model from Activity 4: the whole script reruns on every interaction. If the API call sat at the top level of the script instead of behind a button, moving the smoothing slider on some other page of this app would spend an API call every single time. The button means the call only fires when you deliberately ask for it. `@st.cache_data` on `draft_narrative` adds a second layer of protection: if you press the button twice without the facts block changing, the second press returns the cached answer instead of calling the API again.

None of this makes the call expensive to worry about. A `gpt-4o-mini` call with a short prompt like this one costs a fraction of a cent. The button and the cache exist so a rerun does not spend a key by accident, not because the cost is a real concern.

### The deliverable is the correction, not the paragraph

Press the button once and read what comes back. It will look fluent and confident. That is exactly the problem. An LLM is good at prose, not at getting your five numbers right or knowing that a sixth date exists that you forgot to hand it. Model output varies between runs and between model versions, so there is no fixed transcript to compare your output against. Instead, run whatever paragraph you get against this checklist:

1. Every number in the paragraph appears in the facts block.
2. No date is mentioned that was not flagged.
3. No flagged date is omitted.
4. Superlatives are correct. If it says "the largest drop", confirm that date really has the most extreme z-score in the facts block.
5. No causal claim is made that the data does not support.

Items 3 and 4 exist because of two real failure modes observed while building this activity, with this exact prompt: a generated paragraph once called 2014-12-25 (z = -3.93) "the most significant drop" when 2015-01-27 (z = -4.75) is deeper, and a separate generated paragraph once left 2014-09-01 out entirely. Neither of these is what you should expect to see. They are examples of the two error classes the checklist is built to catch: a wrong superlative, and a silent omission. Your paragraph may show these exact errors, different errors, or no errors at all. Check against the checklist and the facts block, not against these examples.

## Instructions

1. Copy the starter file into your work folder:

   ```bash
   cp "Week 7/Labs/Day 1/starter/activity_7_narrate_with_llm.py" student-work/week7/day1/
   ```

   Do not edit the file under `Week 7/Labs/Day 1/starter/` in place. Work only on the copy in `student-work/`.

2. Confirm your `.env` at the repository root has `OPENAI_API_KEY`, the same key you used in Week 6. If it is missing, add it now. Never commit `.env`. It is already covered by the repository's root `.gitignore`.

3. Open `student-work/week7/day1/activity_7_narrate_with_llm.py` in VS Code. Read the whole file before changing anything. The path resolver, `load_taxi`, the anomaly computation, the button wiring, and the missing-key guard are already done for you. There are three `# TODO` blanks left:
   - the body of `build_facts`
   - the `messages` list inside `draft_narrative`
   - your corrected paragraph and fact-check notes, at the bottom of the file

   Each `# TODO` comment tells you exactly what to write. Replace the placeholder text with your own.

4. Run the app from the repository root:

   ```bash
   uv run streamlit run student-work/week7/day1/activity_7_narrate_with_llm.py
   ```

5. Confirm the facts block under "The facts block" shows the six flagged dates from Activity 6, each with its value and z-score, matching your `build_facts` output exactly. If any number here looks wrong, fix `build_facts` before moving on. Nothing downstream can be trusted if this block is wrong.

6. Press "Draft the narrative." Read the paragraph that comes back.

7. Run that paragraph against the five-item checklist in the Background section. For each item, note whether it held up or failed.

8. Fill in the text box at the bottom of the app with your corrected paragraph, plus the list of what the generated draft got wrong (or, if it genuinely held up on all five items, say so and explain how you checked). This text box, not the generated paragraph above it, is your deliverable for this activity.

9. Test the missing-key path. Temporarily rename your `.env` (for example `mv .env .env.bak`), restart the app, and press the button again. Confirm you see the `st.error` message, not a traceback. Restore your `.env` afterward (`mv .env.bak .env`) before moving on.

## Success Criteria

- All three `# TODO` blanks are filled in and the placeholder text is gone.
- The facts block displayed in the app matches the six flagged dates and z-scores from Activity 6 exactly.
- Pressing "Draft the narrative" produces a paragraph without a traceback.
- You ran the generated paragraph against all five checklist items and recorded the result of each.
- The text box at the bottom contains your corrected paragraph and your fact-check notes, not a copy of the generated draft.
- With `.env` temporarily renamed, pressing the button shows the `st.error` message, not a traceback, and you restored `.env` afterward.
- You can explain, in your own words, why `build_facts` passes a string and never the DataFrame or the raw series.
