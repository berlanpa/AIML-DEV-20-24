# Here's the complete Python code that generates the plot for all fields in the dataset one by one:

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import pandas as pd

# Load the dataset
file_path = '../data/grouped_results_with_fields.csv'
data = pd.read_csv(file_path)

# List of colors to use for each field (we'll cycle through these)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Iterate through all unique fields in the dataset
for i, field in enumerate(data['field'].unique()):

    # Filter the data for the current field
    field_data = data[data['field'] == field]

    # Calculate the ratio to the 2020 value for the current field
    if 2020 in field_data['year'].values:
        count_2020 = field_data[field_data['year'] == 2020]['count'].values[0]
        field_data['ratio_to_2020'] = field_data['count'] / count_2020
    else:
        continue  # If 2020 data is missing, skip this field

    # Prepare data for spline interpolation
    years = field_data['year']
    ratios = field_data['ratio_to_2020']

    # Create a new range of years for a smoother curve
    years_smooth = np.linspace(years.min(), years.max(), 300)

    # Apply spline interpolation
    spline = make_interp_spline(years, ratios, k=3)
    ratios_smooth = spline(years_smooth)

    # Choose a color for the line and title (cycle through the list)
    color = colors[i % len(colors)]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(years_smooth, ratios_smooth, linestyle='-', color=color, linewidth=3)

    # Add the title with increased size and different color
    plt.title(field, fontsize=27, color=color, fontweight='bold', fontname='DejaVu Sans')

    # Add the dotted line at 2020 with lower opacity
    plt.axvline(x=2020, color='red', linestyle='--', linewidth=2, alpha=0.5)

    # Adjust x-ticks using a sans-serif font and larger size
    plt.xticks([2018, 2020, 2022, 2024], fontsize=14, fontweight='bold', fontname='DejaVu Sans')
    plt.yticks([])  # Remove y-axis numbers

    # Calculate the percentage increase from 2023 to 2024 for the current field
    if 2023 in field_data['year'].values and 2024 in field_data['year'].values:
        count_2023 = field_data[field_data['year'] == 2023]['count'].values[0]
        count_2024 = field_data[field_data['year'] == 2024]['count'].values[0]
        percentage_increase = ((count_2024 - count_2023) / count_2023) * 100

        # Display the percentage increase text in the top left, rounded to nearest integer
        plt.text(2018, max(ratios_smooth) * 0.85, f'{int(round(percentage_increase))}%', fontsize=60, color=color,
                 ha='left')

    # Remove gridlines and make the layout tighter for clarity in smaller displays
    plt.grid(False)
    plt.tight_layout()

    # Show each plot
    plt.show()

# General plot
# Create the combined plot with the red dashed line in 2020 and opacity adjustment
plt.figure(figsize=(12, 8))

# Iterate through all unique fields in the dataset and plot the lines
for i, field in enumerate(data['field'].unique()):

    # Filter the data for the current field
    field_data = data[data['field'] == field]

    # Prepare data for spline interpolation
    years = field_data['year']
    normalized_counts = field_data['normalized_count']

    # Create a new range of years for a smoother curve
    years_smooth = np.linspace(years.min(), years.max(), 300)

    # Apply spline interpolation
    spline = make_interp_spline(years, normalized_counts, k=3)
    normalized_counts_smooth = spline(years_smooth)

    # Choose a color for the line and title (cycle through the list)
    color = colors[i % len(colors)]

    # Plot the line for the current field
    plt.plot(years_smooth, normalized_counts_smooth, linestyle='-', color=color, linewidth=2)

