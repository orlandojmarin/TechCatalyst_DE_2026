#!/usr/bin/env bash
# Week 2 Day 1 starter script
# Run from inside operations_playground with: bash summarize_hunt.sh

# Stop the script on errors.
set -euo pipefail

# File path variables
ORDERS_FILE="data/orders_sample.csv"
LOG_FILE="logs/pipeline.log"
SCRIPT_FILE="scripts/run_etl.sh"

echo "Run date: $(date)"
echo

echo "Checking required files:"
missing_count=0

# TODO Part A: Loop over ORDERS_FILE, LOG_FILE, and SCRIPT_FILE.
# For each file, print FOUND <path> when it exists.
# For each missing file, print MISSING <path> and add 1 to missing_count.
for file in "$ORDERS_FILE" "$LOG_FILE" "$SCRIPT_FILE"; do
  if [[ -f "$file" ]]; then
    echo "FOUND $file"
  else
    echo "MISSING $file"
    missing_count=$((missing_count + 1))
  fi
done

# Print PASS when missing_count is 0, otherwise print FAIL with the count.
# TODO (Part A): Use an if condition to print PASS when missing_count is 0.
# Otherwise print FAIL and include the missing count.
echo
if [[ "$missing_count" -eq 0 ]]; then
  echo "Required file check: PASS"
else
  echo "Required file check: FAIL, missing files: $missing_count"
fi

echo
# Part B: Print data and log metrics.
# TODO (Part B): Print "Order rows: <count>" with the header excluded
# Order rows, not counting the header.
echo "Order rows: $(($(wc -l < "$ORDERS_FILE") - 1))"

# TODO (Part B): Print "Unique stores: <count>" of distinct store codes from column 2
# Unique stores: count of distinct store codes in column 2.
echo "Unique stores: $(tail -n +2 "$ORDERS_FILE" | cut -d',' -f2 | sort | uniq | wc -l)"

# TODO (Part B): Print "Error lines: <count>" counted case insensitively with grep -ic.
# Error lines, counting case-insensitively.
echo "Error lines: $(grep -ic "error" "$LOG_FILE")"

echo
echo "Error pattern counts:"
# TODO (Part C): Loop over these patterns and count each one in LOG_FILE:
# connection timeout
# schema mismatch
# auth token
# Part C: Loop over error patterns and print the count of each one in the log.
for pattern in "connection timeout" "schema mismatch" "auth token"; do
  count=$(grep -ic "$pattern" "$LOG_FILE")
  echo "$pattern: $count"
done

echo
echo "Top errors:"
# TODO (Part C): Print the 3 most common error messages and their counts.
# Top 3 error messages with their counts.
grep -i "error" "$LOG_FILE" | cut -d' ' -f3- | sort | uniq -c | sort -rn | head -3

# Guardrail: print FAIL if orders_sample.csv has fewer than 10 data rows.
echo
row_count=$(($(wc -l < "$ORDERS_FILE") - 1))
if [[ "$row_count" -ge 10 ]]; then
  echo "Row count guardrail: PASS ($row_count rows)"
else
  echo "Row count guardrail: FAIL ($row_count rows, need at least 10)"
fi