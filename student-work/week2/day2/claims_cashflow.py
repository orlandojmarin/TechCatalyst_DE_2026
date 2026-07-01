"""Student Do: Daily Claims Cash Flow.

Analyze the claims desk net cash flow (recoveries minus payouts) over a month
of 20 business days. Positive days are surplus days, negative days are deficit
days.
"""

# Initialize the metric variables
count = 0
total = 0
minimum = 0
maximum = 0

# Initialize lists to hold surplus and deficit day amounts
surplus_days = []
deficit_days = []

# List of daily net cash flow in dollars (recoveries minus payouts)
daily_net = [ -224,  352, 252, 354, -544,
              -650,   56, 123, -43,  254,
               325, -123,  47, 321,  123,
               133, -151, 613, 232, -311 ]

# Iterate over each day in the list
for day_net in daily_net:

    # TODO: sum the net cash flow and count the business days
    total += day_net
    count += 1

    # TODO: track the worst (minimum) and best (maximum) day
    if day_net < minimum:
        minimum = day_net
    if day_net > maximum:
        maximum = day_net

    # TODO: append the day to surplus_days or deficit_days
    if day_net > 0:
        surplus_days.append(day_net)
    elif day_net < 0:
        deficit_days.append(day_net)

# TODO: calculate the daily average, the counts, and the percentages
average = total / count
percent_surplus_days = len(surplus_days) / count * 100
percent_deficit_days = len(deficit_days) / count * 100

# TODO: print the summary statistics shown in the README
print("----------Summary Statistics----------")
print(f"Number of Total Days: {count}")
print(f"Number of Surplus Days: {len(surplus_days)}")
print(f"Number of Deficit Days: {len(deficit_days)}")
print(f"Percentage of Surplus Days: {percent_surplus_days:.1f}%")
print(f"Percentage of Deficit Days: {percent_deficit_days:.1f}%")
print("-" * 30)
print(f"Surplus Days: {surplus_days}")
print(f"Deficit Days: {deficit_days}")
print("-" * 30)
print(f"Net Cash Flow: {total}")
print(f"Daily Average: {average:.2f}")
print(f"Worst Deficit: {minimum}")
print(f"Best Surplus: {maximum}")