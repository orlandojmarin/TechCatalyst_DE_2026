"""
Define a reusable function to calculate the loss ratio for a book of business.

Loss ratio = incurred losses / earned premium * 100
A lower loss ratio is better for the insurer.
"""

# Define a function that calculates the loss ratio as a percentage.
# round_to has a default value, so callers can omit it.
def calculate_loss_ratio(incurred_losses, earned_premium, round_to=2):
    loss_ratio = incurred_losses / earned_premium * 100
    return round(loss_ratio, round_to)


# 2024 results
incurred_losses = 2900
earned_premium = 4500
year_2024 = calculate_loss_ratio(incurred_losses, earned_premium)

# 2025 results
incurred_losses = 3600
earned_premium = 4800
year_2025 = calculate_loss_ratio(incurred_losses, earned_premium)

# 2026 results
incurred_losses = 4200
earned_premium = 5000
year_2026 = calculate_loss_ratio(incurred_losses, earned_premium)

print(f"Loss Ratio for 2024: {year_2024}%")
print(f"Loss Ratio for 2025: {year_2025}%")
print(f"Loss Ratio for 2026: {year_2026}%")

# The highest loss ratio is the worst year for the insurer
worst = max(year_2024, year_2025, year_2026)
print(f"Worst loss ratio: {worst}%")


# Challenge

# Create a global, empty list
loss_ratios = []


# Define a function that appends to the global list instead of returning
def calculate_loss_ratio_list(incurred_losses, earned_premium, round_to=2):
    loss_ratio = incurred_losses / earned_premium * 100
    loss_ratios.append(round(loss_ratio, round_to))


calculate_loss_ratio_list(2900, 4500)
calculate_loss_ratio_list(3600, 4800)
calculate_loss_ratio_list(4200, 5000)

print("Loss ratios:", loss_ratios)
