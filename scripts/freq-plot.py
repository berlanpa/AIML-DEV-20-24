import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

# Load the data
file_path = '../data/filtered_keywords.csv'  # Replace with your actual file path
df_latest = pd.read_csv(file_path)

# Prepare the data for plotting
df_latest_melted = df_latest.melt(id_vars='keyword_id', var_name='Year', value_name='Popularity')

# Create the plot
plt.figure(figsize=(10, 6))

# Interpolation and plotting
for keyword in df_latest['keyword_id'].unique():
    data = df_latest_melted[df_latest_melted['keyword_id'] == keyword]

    # Convert 'Year' to numerical format and sort the data
    years = pd.to_numeric(data['Year'])
    popularity = data['Popularity']

    # Spline interpolation for smooth lines
    X_smooth = np.linspace(years.min(), years.max(), 300)
    spline = make_interp_spline(years, popularity, k=3)  # Cubic spline
    Y_smooth = spline(X_smooth)

    # Plot smoothed line
    plt.plot(X_smooth, Y_smooth, label=keyword)

    # Get the current line color for labeling
    line_color = plt.gca().lines[-1].get_color()

    # Label the curve with a little spacing to the right
    plt.text(X_smooth[-1] + 0.1, Y_smooth[-1], keyword, fontsize=10, color=line_color, verticalalignment='center')

# Add dotted vertical lines with reduced opacity
plt.axvline(x=2020, color='red', linestyle=':', linewidth=1.5, alpha=0.6)
plt.axvline(x=2024, color='red', linestyle=':', linewidth=1.5, alpha=0.6)
plt.axvline(x=2022, color='yellow', linestyle=':', linewidth=1.5, alpha=0.6)

# Customize the plot
plt.xlabel('Year', fontsize=14)
plt.ylabel('Publications per year by N-Gram', fontsize=14)
plt.xticks(rotation=45)
plt.grid(False)  # Remove gridlines
plt.xlim([X_smooth.min(), X_smooth.max() + 1])  # Extend x-axis for better label spacing
plt.legend().remove()  # Remove the legend box

# Display the plot
plt.tight_layout()
plt.show()
