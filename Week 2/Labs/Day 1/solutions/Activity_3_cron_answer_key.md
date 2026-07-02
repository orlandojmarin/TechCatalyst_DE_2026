# Cron Schedule Answer Key

## 1. Daily Check

```cron
0 6 * * * bash /home/student/check_orders.sh >> /home/student/check_orders.log 2>&1
```

Plain English: run the order check every day at 6:00 AM.

Risk or logging note: the script uses an absolute path and appends both standard output and errors to a log file, which makes scheduled runs easier to inspect.

## 2. API Polling

```cron
*/15 * * * * python /home/student/poll_api.py >> /home/student/poll_api.log 2>&1
```

Plain English: run the API polling script every 15 minutes.

Risk or logging note: frequent jobs can create large logs or hit API limits, so the team should monitor log size and API response failures.

## 3. Monthly Archive

```cron
30 2 1 * * bash /home/student/monthly_archive.sh >> /home/student/monthly_archive.log 2>&1
```

Plain English: run the monthly archive script at 2:30 AM on the first day of every month.

Risk or logging note: archive jobs can move or overwrite data, so the script should log source paths, destination paths, and row or file counts.

## 4. Weekly Report

```cron
0 8 * * 1 bash /home/student/weekly_report.sh >> /home/student/weekly_report.log 2>&1
```

Plain English: run the weekly report every Monday at 8:00 AM.

Risk or logging note: the log should make it clear whether the report ran, where the output was written, and whether any upstream file was missing.
