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

    # TODO: sum the net cash flow and count the business days


    # TODO: track the worst (minimum) and best (maximum) day


    # TODO: append the day to surplus_days or deficit_days
    pass

# TODO: calculate the daily average, the counts, and the percentages


# TODO: print the summary statistics shown in the README
