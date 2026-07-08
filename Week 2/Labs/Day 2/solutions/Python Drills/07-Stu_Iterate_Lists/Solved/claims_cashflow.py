"""Student Do: Daily Claims Cash Flow.

Analyze the claims desk net cash flow (recoveries minus payouts) over a month
of 20 business days. Positive days are surplus days, negative days are deficit
days.
"""

# Initialize the metric variables
count = 0
total = 0
average = 0
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

    # Cumulatively sum the net cash flow and count business days
    total += day_net
    count += 1

    # Logic to determine the worst (minimum) and best (maximum) day
    if minimum == 0:
        minimum = day_net
    elif day_net < minimum:
        minimum = day_net
    elif day_net > maximum:
        maximum = day_net

    # Logic to separate surplus days from deficit days
    if day_net > 0:
        surplus_days.append(day_net)
    elif day_net <= 0:
        deficit_days.append(day_net)

# Calculate the daily average
average = round(total / count, 2)

# Count metrics
surplus_count = len(surplus_days)
deficit_count = len(deficit_days)

# Percentage metrics
percent_surplus = surplus_count / count * 100
percent_deficit = deficit_count / count * 100

# Print out the summary statistics
print("---------Summary Statistics----------")
print(f"Number of Total Days: {count}")
print(f"Number of Surplus Days: {surplus_count}")
print(f"Number of Deficit Days: {deficit_count}")
print(f"Percentage of Surplus Days: {percent_surplus}%")
print(f"Percentage of Deficit Days: {percent_deficit}%")
print("-------------------------------------")
print(f"Surplus Days: {surplus_days}")
print(f"Deficit Days: {deficit_days}")
print("-------------------------------------")
print(f"Net Cash Flow: {total}")
print(f"Daily Average: {average}")
print(f"Worst Deficit: {minimum}")
print(f"Best Surplus: {maximum}")
