# CLI Investigation Answers

## 1. Count Provided Files

Command:
```bash
find data logs notes scripts -type f | wc -l
```

Answer:
```text
7
```

Why it works:
`find data logs notes scripts -type f` lists only files (not directories) under the four specified folders, and `wc -l` counts those lines.

## 2. Find The Largest Direct Folder Or File

Command:
```bash
du -sh * | sort -hr | head -1
```

Answer:
```text
16K	notes
```

Why it works:
`du -sh *` shows the size of each top-level item in human-readable format, `sort -hr` sorts them largest first (human-readable, reverse), and `head -1` keeps only the top result.

## 3. Count Orders

Command:
```bash
wc -l data/orders_sample.csv
```

Answer:
```text
16 total lines, 15 data rows
```

Why it works:
`wc -l` counts all lines including the header row. Since the first line contains column names (not data), the number of actual data rows is 16 - 1 = 15.

## 4. Find Hidden Files

Command:
```bash
find . -name ".*" -type f
cat notes/.secret_flag
```

Answer:
```text
./notes/.secret_flag
Contents: you found me! flag: TC2026-SHELL
```

Why it works:
`find . -name ".*" -type f` matches files whose names start with a dot (hidden files in Linux), and `cat` prints the file contents.

## 5. Count Log Errors

Command:
```bash
grep -ic "error" logs/pipeline.log
```

Answer:
```text
10
```

Why it works:
`grep -i` matches "error" regardless of case (ERROR, error, Error), and `-c` counts matching lines. Ignoring case matters because this log file uses both "ERROR" and "error" on different lines.

## 6. Find The Last Log Timestamp

Command:
```bash
tail -1 logs/pipeline.log | cut -d' ' -f1
```

Answer:
```text
2026-06-28T06:20:00
```

Why it works:
`tail -1` gets the last line of the file, and `cut -d' ' -f1` extracts the first space-delimited field, which is the timestamp.

## 7. Sort Data Files By Size

Command:
```bash
ls -lhS data/
```

Answer:
```text
464  clickstream_2026-06.jsonl
387  orders_sample.csv
171  returns_2026-06.csv
```

Why it works:
`ls -lhS` lists files in human-readable format sorted by size (largest first), showing every file under `data/`.

## 8. Find Shell Scripts

Command:
```bash
find scripts -name "*.sh" -type f
```

Answer:
```text
scripts/run_etl.sh
```

Why it works:
`find` searches the `scripts/` folder for files ending in `.sh`, which is the standard shell script extension.

## 9. Count Unique Store Codes

Command:
```bash
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort | uniq | wc -l
```

Answer:
```text
5
```

Why it works:
`tail -n +2` skips the header row, `cut -d',' -f2` extracts column 2 (store codes), `sort` groups identical values together, `uniq` removes consecutive duplicates, and `wc -l` counts the unique values.

## 10. Search With A Regex Pattern

Command:
```bash
grep -E "timeout|schema" logs/pipeline.log
```

Answer:
```text
2026-06-28T06:00:22 ERROR connection timeout to source api
2026-06-28T06:01:24 ERROR connection timeout to source api
2026-06-28T06:02:12 ERROR schema mismatch in column amount
2026-06-28T06:04:18 ERROR schema mismatch in column amount
2026-06-28T06:10:44 ERROR connection timeout to source api
2026-06-28T06:15:31 ERROR schema mismatch in column amount
2026-06-28T06:18:45 ERROR connection timeout to source api
```

Why it works:
`grep -E` enables extended regex, and `timeout|schema` matches lines containing either word, finding 7 lines total (4 timeouts and 3 schema mismatches).

## 11. Make A Safe Working Copy

Command:
```bash
mkdir -p work
cp logs/pipeline.log work/pipeline_working.log
echo "hunt completed by Orlando" >> work/pipeline_working.log
tail -1 logs/pipeline.log
tail -1 work/pipeline_working.log
```

Answer:
```text
Original last line:  2026-06-28T06:20:00 INFO  daily summary written
Copy last line:      hunt completed by Orlando
```

Why it works:
`mkdir -p` creates the folder safely (no error if it already exists), `cp` copies the file, `>>` appends only to the copy, and `tail -1` on both files proves the original is unchanged while the copy has the new line.

## 12. Top Error Messages

Command:
```bash
grep -i "error" logs/pipeline.log | cut -d' ' -f3- | sort | uniq -c | sort -rn | head -3
```

Answer:
```text
      4 connection timeout to source api
      3 schema mismatch in column amount
      2 auth token expired
```

Why it works:
`grep -i "error"` gets all error lines, `cut -d' ' -f3-` strips the timestamp and log level to isolate the message text, `sort | uniq -c` counts duplicates, `sort -rn` puts highest counts first, and `head -3` keeps the top 3.
