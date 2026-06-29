#!/usr/bin/env bash
# This script summarizes the operations_playground environment by checking
# that required files exist, printing key data and log metrics, and
# reporting the most common error patterns found in the pipeline log.
# Run from inside operations_playground with: bash summarize_hunt.sh

# Stop the script immediately if any command fails, if an undefined variable
# is used, or if any command in a pipeline fails.
set -euo pipefail

# Store file paths in variables so they can be reused without retyping,
# and changed in one place if the paths ever move.
ORDERS_FILE="data/orders_sample.csv"
LOG_FILE="logs/pipeline.log"
SCRIPT_FILE="scripts/run_etl.sh"

# Print the current date so the output is timestamped.
echo "Run date: $(date)"
echo

# Part A: Loop over each required file and check whether it exists.
# Print FOUND or MISSING for each one, and keep a count of missing files.
echo "Checking required files:"
missing_count=0

for file in "$ORDERS_FILE" "$LOG_FILE" "$SCRIPT_FILE"; do
  if [[ -f "$file" ]]; then
    echo "FOUND $file"
  else
    echo "MISSING $file"
    missing_count=$((missing_count + 1))
  fi
done

# Print a single PASS/FAIL summary based on whether any files were missing.
echo
if [[ "$missing_count" -eq 0 ]]; then
  echo "Required file check: PASS"
else
  echo "Required file check: FAIL, missing files: $missing_count"
fi

# Part B: Print data and log metrics.
# Count order rows by subtracting 1 from the total line count (removes the header).
echo
echo "Order rows: $(($(wc -l < "$ORDERS_FILE") - 1))"

# Count unique store codes by skipping the header, extracting column 2,
# sorting, removing duplicates, and counting the remaining lines.
echo "Unique stores: $(tail -n +2 "$ORDERS_FILE" | cut -d',' -f2 | sort | uniq | wc -l)"

# Count how many lines in the log contain "error" (case-insensitive).
echo "Error lines: $(grep -ic "error" "$LOG_FILE")"

# Part C: Loop over known error patterns and print how many times each appears.
echo
echo "Error pattern counts:"
for pattern in "connection timeout" "schema mismatch" "auth token"; do
  count=$(grep -ic "$pattern" "$LOG_FILE")
  echo "$pattern: $count"
done

# Print the 3 most common error messages by stripping the timestamp and
# log level, then sorting, counting duplicates, and keeping the top 3.
echo
echo "Top errors:"
grep -i "error" "$LOG_FILE" | cut -d' ' -f3- | sort | uniq -c | sort -rn | head -3

# Guardrail: fail if the orders file has fewer than 10 data rows,
# which would indicate incomplete or missing data.
echo
row_count=$(($(wc -l < "$ORDERS_FILE") - 1))
if [[ "$row_count" -ge 10 ]]; then
  echo "Row count guardrail: PASS ($row_count rows)"
else
  echo "Row count guardrail: FAIL ($row_count rows, need at least 10)"
fi
