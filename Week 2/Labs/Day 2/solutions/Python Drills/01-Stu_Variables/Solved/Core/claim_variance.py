# Claim Reserve Variance

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

# Print the reserve
print(f"Claim CLM-1001 reserve was ${reserve}")

# Print the settlement
print(f"Claim CLM-1001 settled at ${settlement}")

# Print the percent change
print(f"Claim CLM-1001 reserve changed by {percent_change}%")
