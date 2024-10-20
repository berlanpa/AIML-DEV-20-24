import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import matplotlib.cm as cm

# Load the data
file_path = '../data/filtered_concepts.csv'  # Adjust the file path as necessary
data = pd.read_csv(file_path)

# Extract the relevant columns for ranking
concepts = data['Concept']
years = ['Rank 2018', 'Rank 2019', 'Rank 2020', 'Rank 2021', 'Rank 2022', 'Rank 2023', 'Rank 2024']
rank_data = data[years]

# Calculate the rank difference between 2018 and 2024
rank_diff = rank_data['Rank 2024'] - rank_data['Rank 2018']

# Define color boundaries: Reclassify the differences into 5 groups with balanced boundaries
bins_adjusted = np.percentile(rank_diff, [0, 20, 40, 60, 80, 100])  # Use percentiles for more even grouping
colors = cm.get_cmap('rainbow', 5)  # Use a bright color map with 5 distinct colors
color_indices_adjusted = np.digitize(rank_diff, bins_adjusted) - 1  # Recalculate color index based on adjusted bins
assigned_colors_adjusted = [colors(i) for i in color_indices_adjusted]  # Map to bright colors

# Plot with adjusted color boundaries and curvy lines
plt.figure(figsize=(10, 12))

# Interpolate each concept's rank evolution and plot with slightly thicker lines
for i, concept in enumerate(concepts):
    x_vals = np.arange(len(years))  # Convert years into numeric x-values
    y_vals = rank_data.iloc[i].values  # Get the rank data

    # Create a spline to make the line curvy
    x_smooth = np.linspace(x_vals.min(), x_vals.max(), 300)  # Smooth x-values
    spline = make_interp_spline(x_vals, y_vals, k=3)  # k=3 for cubic spline
    y_smooth = spline(x_smooth)  # Get smooth y-values

    line_color = assigned_colors_adjusted[i]
    plt.plot(x_smooth, y_smooth, label=concept, color=line_color, linewidth=1.5)  # Slightly thicker curvy lines

    # Add larger points at the specific years
    plt.plot(x_vals, y_vals, 'o', markerfacecolor='white', markeredgewidth=2, color=line_color,
             markersize=6)  # Points only at year markers

    # Left side label
    plt.text(-0.5, rank_data.iloc[i, 0], concept, va='center', ha='right', fontsize=9, color=line_color)
    # Right side label
    plt.text(len(years) - 0.5, rank_data.iloc[i, -1], concept, va='center', ha='left', fontsize=9, color=line_color)

# Customizing the plot
plt.xlabel('Publication Year')
plt.xticks(ticks=range(len(years)), labels=[year.split(' ')[1] for year in years], rotation=45)
plt.gca().invert_yaxis()  # Lower rank is better, so invert the y-axis
plt.gca().yaxis.set_visible(False)  # Remove y-axis numbering and labels

# Remove the y-axis and x-axis borders (spines)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)

# Set y-axis limit to stop at rank 30
plt.ylim(30, 1)

# Show the plot
plt.tight_layout()

# Display the final plot
plt.show()
