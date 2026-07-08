# Claim Reserve Variance (Challenge)

# Formulas
# Variance = Settlement - Reserve
# Percent Change = Variance / Reserve x 100

# Create a float variable for the reserve
reserve = 5000.00

# Create a float variable for the settlement
settlement = 6200.00

# Calculate the variance (settlement minus reserve)
variance = settlement - reserve

# Calculate the percent change
percent_change = (variance / reserve) * 100

# Print the reserve as currency
print(f"Claim CLM-1001 reserve was ${reserve:,.2f}")

# Print the settlement as currency
print(f"Claim CLM-1001 settled at ${settlement:,.2f}")

# Print the variance as currency with a thousands separator
print(f"Claim CLM-1001 variance was ${variance:,.2f}")

# Print the percent change with two decimal places and a percent sign
print(f"Claim CLM-1001 reserve changed by {percent_change:.2f}%")
