"""
Define a reusable function to calculate the loss ratio for a book of business.

Loss ratio = incurred losses / earned premium * 100
A lower loss ratio is better for the insurer.
"""

# Create a global, empty list named loss_ratios
loss_ratio_list = []

# TODO: Define calculate_loss_ratio(incurred_losses, earned_premium, round_to=2)
# that returns the loss ratio as a percentage rounded to round_to places.
def calculate_loss_ratio(incurred_losses, earned_premium, round_to = 2):
    loss_ratio = incurred_losses / earned_premium * 100
    loss_ratio_rounded = round(loss_ratio, round_to)
    return loss_ratio_rounded

# Challenge
# Define calculate_loss_ratio_list(...) that appends to loss_ratios instead of
# returning, then call it for all three years and print the list
def calculate_loss_ratio_list(incurred_losses, earned_premium, round_to = 2):
    loss_ratio = incurred_losses / earned_premium * 100
    loss_ratio_rounded = round(loss_ratio, round_to)
    loss_ratio_list.append(loss_ratio_rounded)
    return loss_ratio_rounded

# 2024 results: incurred_losses = 2900, earned_premium = 4500
# Call the function and capture year_2024
year_2024 = calculate_loss_ratio_list(2900, 4500)

# 2025 results: incurred_losses = 3600, earned_premium = 4800
# Call the function and capture year_2025
year_2025 = calculate_loss_ratio_list(3600, 4800)

# 2026 results: incurred_losses = 4200, earned_premium = 5000
# Call the function and capture year_2026
year_2026 = calculate_loss_ratio_list(4200, 5000)

# Print each year's loss ratio as a percentage
print(f"Loss Ratio for 2024: {year_2024}%")
print(f"Loss Ratio for 2025: {year_2025}%")
print(f"Loss Ratio for 2026: {year_2026}%")

# Identify the worst (highest) loss ratio of the three years
print(f"Worst loss ratio: {max(loss_ratio_list)}%")
print(f"Loss ratios: {loss_ratio_list}")



