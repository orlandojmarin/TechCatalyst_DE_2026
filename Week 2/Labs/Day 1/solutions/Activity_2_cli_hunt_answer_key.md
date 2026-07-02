# CLI Investigation Answer Key

The exact human-readable file sizes can differ slightly by platform, but the ordering should remain stable. Question 1 counts only the four provided starter folders so generated notes do not change the expected answer.

## Expected Answers

| # | Expected answer |
| :--- | :--- |
| 1 | `7` files |
| 2 | `./data`, about `12K` on macOS, size may differ on Linux |
| 3 | `16` lines, `15` data rows |
| 4 | `./notes/.secret_flag`, containing `you found me! flag: TC2026-SHELL` |
| 5 | `10` case-insensitive error lines |
| 6 | `2026-06-28T06:20:00` |
| 7 | Largest first: `clickstream_2026-06.jsonl`, `orders_sample.csv`, `returns_2026-06.csv` |
| 8 | `scripts/run_etl.sh` |
| 9 | `5` unique store codes |
| 10 | Lines that mention `connection timeout to source api` or `schema mismatch in column amount` |
| 11 | `work/pipeline_working.log` ends with the learner's completion line, while `logs/pipeline.log` still ends with `2026-06-28T06:20:00 INFO  daily summary written` |
| 12 | `4 connection timeout to source api`, `3 schema mismatch in column amount`, `2 auth token expired` |

## Representative Commands

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
