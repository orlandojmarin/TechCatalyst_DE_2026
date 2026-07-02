# Week 2 Day 1 Exit Ticket
# Score 100

## Q1: Why do data engineers still use terminal commands when notebooks, cloud consoles, and AI assistants exist?
- [ ] They are always safer and faster than every graphical tool.
- [x] They inspect files, logs, and environments fast and make work repeatable.
- [ ] They remove any need for Git, code review, or documentation.
- [ ] They only add value when you work on a personal laptop.
::time=40

## Q2: A learner is on Windows Terminal with a PowerShell tab open. What should they check before copying an Ubuntu Bash command from class?
- [x] Which shell is active, since command syntax differs between them.
- [ ] Whether the terminal output shows enough syntax coloring.
- [ ] Whether the browser is currently signed in to GitHub.
- [ ] Whether the command was written earlier on the same day.
::time=40

## Q3: Which command is the best first choice for finding lines that contain the word `ERROR` inside `logs/pipeline.log`, ignoring case?
- [ ] `find logs/pipeline.log -name "ERROR"`
- [ ] `wc -l "ERROR" logs/pipeline.log`
- [ ] `sort "ERROR" logs/pipeline.log`
- [x] `grep -i "ERROR" logs/pipeline.log`
::time=40

## Q4: What does this pipeline mostly do?

```bash
tail -n +2 data/orders_sample.csv | cut -d',' -f2 | sort | uniq | wc -l
```

- [ ] Counts every row in the file, including the header row.
- [ ] Lists every file that changed in the last two days.
- [x] Counts the distinct values in the second column, minus the header.
- [ ] Prints the two largest numeric values found in the file.
::time=40

## Q5: What does this cron schedule mean?

```cron
*/15 * * * * bash /home/student/check.sh >> /home/student/check.log 2>&1
```

- [ ] Runs once a day, fifteen minutes after midnight, with no logging.
- [x] Runs every fifteen minutes, appending both output and errors to a log.
- [ ] Runs every fifteen days and overwrites the log file each run.
- [ ] Runs every weekday at fifteen hundred and clears the old log.
::time=40

## Q6: During a pull request conflict, where should the learner resolve the conflict?
- [x] On the feature branch, then stage, commit, and push the fix.
- [ ] Directly on `main`, then force push the change to origin.
- [ ] Inside the GitHub issue thread, without editing any files.
- [ ] In a separate, unrelated repository made for the fix.
::time=40

## Q7: After resolving a merge conflict, what must be removed before committing?
- [ ] Every code comment the two branches disagree about.
- [ ] The name of the feature branch used for the change.
- [ ] The final value you deliberately chose to keep.
- [x] The conflict markers `<<<<<<<`, `=======`, and `>>>>>>>`.
::time=40

## Q8: An AI assistant suggests `rm -rf ./data/raw`. What is the safest first response?
- [ ] Run it as written, since AI tools usually pick the right path.
- [ ] Add `sudo` so the delete succeeds even if it is protected.
- [x] Run `pwd` and `ls` first, and confirm what would be deleted.
- [ ] Paste it into the pull request description for a teammate.
::time=40
