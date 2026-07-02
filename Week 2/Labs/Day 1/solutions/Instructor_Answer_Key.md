# Day 1 Instructor Answer Key

Instructor-only. Do not distribute to students. This is the single answer key for every on-your-own and challenge task across Week 2 Day 1, with the answer plus a short teaching explanation you can read aloud. The detailed per-task files (`Activity_2_cli_hunt_answer_key.md`, `Activity_3_cron_answer_key.md`) remain in this folder as backups; everything is gathered here.

Reveal timing:
- Reveal Activity 3 Part B after pairs attempt all three metrics.
- Reveal Activity 3 Part C and the cron answers after class.
- Reveal Activity 2 answers after teams submit their `cli_hunt.md`.

Platform note: on the student Ubuntu VMs (GNU coreutils), `... | sort | uniq | wc -l` prints a clean `5`. If you demo on macOS (BSD `wc`), the same pipeline pads the number with spaces. That is cosmetic only and does not affect correctness.

---

## Activity 2: CLI Investigation Challenge

Expected answers and the reasoning to require from each team.

| # | Expected answer | Why it works |
| :--- | :--- | :--- |
| 1 | `7` files | `find data logs notes scripts -type f` lists all regular files under the four provided folders, including the hidden `.secret_flag`; `wc -l` counts them. We count only the four starter folders so generated notes do not change the answer. |
| 2 | `./data`, about `12K` on macOS, may differ on Linux | `du -sh *` reports folder sizes; `sort -rh \| head -1` keeps the largest human-readable size. |
| 3 | `16` lines, `15` data rows | `wc -l` counts every line including the header; subtract one for the header to get data rows. |
| 4 | `./notes/.secret_flag`, containing `you found me! flag: TC2026-SHELL` | `find . -name ".*" -type f` finds hidden files; `cat` reveals contents. Hidden files start with a dot and do not show in plain `ls`. |
| 5 | `10` case-insensitive error lines | `grep -ic "error"` counts matching lines. `-i` matters because the log mixes `ERROR` and `error`. |
| 6 | `2026-06-28T06:20:00` | `tail -1` gives the last line; `cut -d' ' -f1` keeps the first space-delimited field, the timestamp. |
| 7 | Largest first: `clickstream_2026-06.jsonl`, `orders_sample.csv`, `returns_2026-06.csv` | `ls -lhS data/*` sorts by size, largest first. |
| 8 | `scripts/run_etl.sh` | `find scripts -name "*.sh" -type f` locates shell scripts under `scripts/`. |
| 9 | `5` unique store codes | `tail -n +2` drops the header, `cut -d',' -f2` extracts the store column, `sort \| uniq` collapses duplicates, `wc -l` counts. |
| 10 | Lines mentioning `connection timeout to source api` or `schema mismatch in column amount` | `grep -Ein "timeout\|schema"` uses extended regex to match either word; `-i` ignores case, `-n` adds line numbers. |
| 11 | `work/pipeline_working.log` ends with the learner's completion line; `logs/pipeline.log` still ends with `2026-06-28T06:20:00 INFO  daily summary written` | Copy first, then append to the copy. The original evidence file must not change. |
| 12 | `4 connection timeout to source api`, `3 schema mismatch in column amount`, `2 auth token expired` | Reduce each error line to the message text, then `sort \| uniq -c \| sort -rn \| head -3`. |

Representative commands:

```bash
find data logs notes scripts -type f | wc -l
du -sh * | sort -rh | head -1
wc -l data/orders_sample.csv
find . -name ".*" -type f
cat notes/.secret_flag
grep -ic "error" logs/pipeline.log
tail -1 logs/pipeline.log | cut -d' ' -f1
ls -lhS data/*
find scripts -name "*.sh" -type f
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort | uniq | wc -l
grep -Ein "timeout|schema" logs/pipeline.log
mkdir -p work
cp logs/pipeline.log work/pipeline_working.log
echo "hunt completed by <your name>" >> work/pipeline_working.log
tail -1 logs/pipeline.log
tail -1 work/pipeline_working.log
grep -i "error" logs/pipeline.log | sed -E 's/^[^ ]+ +(ERROR|error) +//' | sort | uniq -c | sort -rn | head -3
```

---

## Activity 3 Part B: Data And Log Metrics

The three TODO lines students write on their own, with what to emphasize.

**1. Order rows (exclude header):**

```bash
echo "Order rows: $(($(wc -l < "$ORDERS_FILE") - 1))"
```

Teaching point: `wc -l < file` counts lines without printing the filename, so the number is clean for arithmetic. We subtract one for the header. Accept the equivalent `tail -n +2 "$ORDERS_FILE" | wc -l`.

**2. Unique stores:**

```bash
echo "Unique stores: $(tail -n +2 "$ORDERS_FILE" | cut -d',' -f2 | sort | uniq | wc -l)"
```

Teaching point: this is the same pipeline they built in Activity 1. `sort` must come before `uniq` because `uniq` only collapses adjacent duplicates.

**3. Error lines, case-insensitive:**

```bash
echo "Error lines: $(grep -ic error "$LOG_FILE")"
```

Teaching point: `-c` counts matching lines, not total word matches. `-i` is required because the log has both `ERROR` and `error`.

Expected output for Part B:

```text
Order rows: 15
Unique stores: 5
Error lines: 10
```

---

## Activity 3 Part C: Patterns, Top Errors, And Guardrail

**1. Error pattern counts (loop):**

```bash
echo "Error pattern counts:"
for pattern in "connection timeout" "schema mismatch" "auth token"; do
  count=$(grep -ic "$pattern" "$LOG_FILE")
  echo "$pattern: $count"
done
```

Teaching point: one loop replaces three near-identical `grep` lines. This is the same reuse idea as Part A, applied to search patterns instead of file paths.

**2. Top 3 error messages:**

```bash
echo "Top errors:"
grep -i "error" "$LOG_FILE" | sed -E 's/^[^ ]+ +(ERROR|error) +//' | sort | uniq -c | sort -rn | head -3
```

Teaching point: `sed` strips the timestamp and level so identical messages group together. `uniq -c` counts, `sort -rn` ranks high to low, `head -3` keeps the top three. This is the same pipeline from Activity 1 Part 5.

**3. Guardrail (fail if fewer than 10 data rows):**

```bash
row_count=$(($(wc -l < "$ORDERS_FILE") - 1))
if [[ "$row_count" -ge 10 ]]; then
  echo "Row count guardrail: PASS ($row_count rows)"
else
  echo "Row count guardrail: FAIL ($row_count rows)"
fi
```

Teaching point: a guardrail turns a silent assumption ("the file is big enough") into a visible, testable check. Connect this to data quality checks they will see in later weeks.

Expected output for Part C:

```text
Error pattern counts:
connection timeout: 4
schema mismatch: 3
auth token: 2

Top errors:
   4 connection timeout to source api
   3 schema mismatch in column amount
   2 auth token expired
```

The complete runnable reference is `solutions/Activity_3_summarize_hunt_solution.sh`, which now includes Parts A, B, and C (the guardrail is wired in at the end).

---

## Activity 3 Part D: Cron Schedules

Schedule 1 is the worked example in the handout. Answers for 2, 3, and 4:

**2. API polling**

```cron
*/15 * * * * python /home/student/poll_api.py >> /home/student/poll_api.log 2>&1
```

- Plain English: run the API polling script every 15 minutes.
- Output file: `/home/student/poll_api.log`.
- `2>&1`: errors go to the same log as standard output.
- Risk: frequent jobs create large logs and can hit API rate limits, so monitor log size and response failures.

**3. Monthly archive**

```cron
30 2 1 * * bash /home/student/monthly_archive.sh >> /home/student/monthly_archive.log 2>&1
```

- Plain English: run the archive script at 2:30 AM on the first day of every month.
- Output file: `/home/student/monthly_archive.log`.
- `2>&1`: errors go to the same log as standard output.
- Risk: archive jobs move or overwrite data, so the script should log source paths, destination paths, and row or file counts.

**4. Weekly report**

```cron
0 8 * * 1 bash /home/student/weekly_report.sh >> /home/student/weekly_report.log 2>&1
```

- Plain English: run the weekly report every Monday at 8:00 AM. In cron, day-of-week `1` is Monday.
- Output file: `/home/student/weekly_report.log`.
- `2>&1`: errors go to the same log as standard output.
- Risk: the log should make it clear whether the report ran, where output went, and whether any upstream file was missing.

Common student mistakes to watch for:
- Reading `*/15` as "15 minutes after the hour" instead of "every 15 minutes."
- Reading the day-of-week field as 0-based or naming the wrong day.
- Forgetting that `>>` appends while `>` overwrites; a scheduled job using `>` loses history every run.
