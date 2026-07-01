#!/usr/bin/env bash
# Week 2 Day 1 solution script.
# Run from inside operations_playground with: bash summarize_hunt.sh

set -euo pipefail

ORDERS_FILE="data/orders_sample.csv"
LOG_FILE="logs/pipeline.log"
SCRIPT_FILE="scripts/run_etl.sh"

echo "Run date: $(date)"
echo

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

echo
if [[ "$missing_count" -eq 0 ]]; then
  echo "Required file check: PASS"
else
  echo "Required file check: FAIL, missing files: $missing_count"
fi

echo
echo "Order rows: $(($(wc -l < "$ORDERS_FILE") - 1))"
echo "Unique stores: $(tail -n +2 "$ORDERS_FILE" | cut -d',' -f2 | sort | uniq | wc -l)"
echo "Error lines: $(grep -ic error "$LOG_FILE")"

echo
echo "Error pattern counts:"
for pattern in "connection timeout" "schema mismatch" "auth token"; do
  count=$(grep -ic "$pattern" "$LOG_FILE")
  echo "$pattern: $count"
done

echo
echo "Top errors:"
grep -i "error" "$LOG_FILE" | sed -E 's/^[^ ]+ +(ERROR|error) +//' | sort | uniq -c | sort -rn | head -3

echo
# Part C guardrail: fail if there are fewer than 10 data rows.
row_count=$(($(wc -l < "$ORDERS_FILE") - 1))
if [[ "$row_count" -ge 10 ]]; then
  echo "Row count guardrail: PASS ($row_count rows)"
else
  echo "Row count guardrail: FAIL ($row_count rows)"
fi
