"""Activity 2 starter: Appointment No-Show Analysis.

Read the no-show data with the csv module, compute no-show rates by several
factors, and print them. Then write your interpretation in findings.md.

Run from the activity folder (the folder that contains data/):
    uv run python starter/no_show_analysis.py
"""
import csv
from pathlib import Path

DATA = Path("data/no_shows.csv")


def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def is_no_show(row):
    # The No-show column is "Y" when the patient did not show up.
    return row["No-show"].strip().lower() in ("yes", "y")


def is_yes(value):
    return value.strip().lower() in ("yes", "y")


def rate(rows):
    """Return (appointments, no_shows, percent) for a list of rows."""
    # TODO: count the rows and the no-shows, return the count, the no-show count,
    # and the no-show percentage rounded to 1 decimal. Guard against an empty list.
    pass


def main():
    rows = load_rows(DATA)
    print(f"Total appointments: {len(rows)}")

    # CORE
    # TODO: print the overall no-show rate.
    # TODO: print the no-show rate for SMS received vs no SMS.
    # TODO: print the no-show rate for scholarship vs no scholarship.
    # TODO: print the no-show rate by age group (18-34, 35-54, 55+).

    # CHALLENGE
    # TODO: print the no-show rate for patients with hypertension and with diabetes.
    # TODO: find the neighborhoods with the highest no-show rate among those with
    # at least 50 appointments, and print the top 3.


if __name__ == "__main__":
    main()
