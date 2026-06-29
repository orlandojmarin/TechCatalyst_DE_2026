#!/usr/bin/env bash
# Week 2 Day 1 starter script.
# Run from inside operations_playground with: bash summarize_hunt.sh

set -euo pipefail

ORDERS_FILE="data/orders_sample.csv"
LOG_FILE="logs/pipeline.log"
SCRIPT_FILE="scripts/run_etl.sh"

echo "Run date: $(date)"
echo

echo "Checking required files:"
missing_count=0

# TODO (Part A): Loop over ORDERS_FILE, LOG_FILE, and SCRIPT_FILE.
# For each file, print FOUND <path> when it exists.
# For each missing file, print MISSING <path> and add 1 to missing_count.

echo
# TODO (Part A): Use an if condition to print PASS when missing_count is 0.
# Otherwise print FAIL and include the missing_count.

echo
# TODO (Part B): Print "Order rows: <count>" with the header excluded.

# TODO (Part B): Print "Unique stores: <count>" of distinct store codes from column 2.

# TODO (Part B): Print "Error lines: <count>" counted case-insensitively with grep -ic.

echo
echo "Error pattern counts:"
# TODO (Part C): Loop over these patterns and count each one in LOG_FILE:
# connection timeout
# schema mismatch
# auth token

echo
echo "Top errors:"
# TODO (Part C): Print the 3 most common error messages and their counts.
