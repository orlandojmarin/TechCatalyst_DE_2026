#!/usr/bin/env bash
# Summarizes the operations_playground environment.
# Run from inside operations_playground with: bash summarize_hunt.sh

# Stop the script on errors.
set -euo pipefail

# File path variables for reuse.
ORDERS_FILE="data/orders_sample.csv"
LOG_FILE="logs/pipeline.log"
SCRIPT_FILE="scripts/run_etl.sh"

echo "Run date: $(date)"
echo

# Part A: Loop over ORDERS_FILE, LOG_FILE, and SCRIPT_FILE.
# For each file, print FOUND <path> when it exists.
# For each missing file, print MISSING <path> and add 1 to missing_count.
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

# Print PASS when missing_count is 0, otherwise print FAIL with the count.
echo
if [[ "$missing_count" -eq 0 ]]; then
  echo "Required file check: PASS"
else
  echo "Required file check: FAIL, missing files: $missing_count"
fi

# Part B: Print data and log metrics.
echo

# Order rows, not counting the header.
echo "Order rows: $(($(wc -l < "$ORDERS_FILE") - 1))"

# Unique stores: count of distinct store codes in column 2.
echo "Unique stores: $(tail -n +2 "$ORDERS_FILE" | cut -d',' -f2 | sort | uniq | wc -l)"

# Error lines, counting case-insensitively.
echo "Error lines: $(grep -ic "error" "$LOG_FILE")"

# Part C: Loop over error patterns and print the count of each one in the log.
echo
echo "Error pattern counts:"
for pattern in "connection timeout" "schema mismatch" "auth token"; do
  count=$(grep -ic "$pattern" "$LOG_FILE")
  echo "$pattern: $count"
done

# Top 3 error messages with their counts.
echo
echo "Top errors:"
grep -i "error" "$LOG_FILE" | cut -d' ' -f3- | sort | uniq -c | sort -rn | head -3

# Guardrail: print FAIL if orders_sample.csv has fewer than 10 data rows.
echo
row_count=$(($(wc -l < "$ORDERS_FILE") - 1))
if [[ "$row_count" -ge 10 ]]; then
  echo "Row count guardrail: PASS ($row_count rows)"
else
  echo "Row count guardrail: FAIL ($row_count rows, need at least 10)"
fi
