import pandas as pd
data = pd.read_csv('../data/level_2_concepts.csv')

# Remove duplicates based on the 'Concept' column
data_cleaned = data.drop_duplicates(subset='Concept')

# List of "far-fetched" or too broad concepts to exclude
concepts_to_exclude = [
    'The Internet', 'Cognition', 'Creativity', 'Virtual reality', 'Utopia',
    'Dystopia', 'Sentience', 'Time travel', 'Immortality', 'Posthuman',
    'Artificial life', 'Simulated reality', 'Consciousness'
]

# Filter out rows where the 'Concept' matches any of the concepts in the exclusion list
data_cleaned = data_cleaned[~data_cleaned['Concept'].isin(concepts_to_exclude)]

# Filter rows where 'Parent' is 'Machine Learning'
# data_cleaned = data_cleaned[data_cleaned['Parent'] == 'Machine Learning']



# Add ranking columns for each year from 2018 to 2024 based on publication counts
years = ['Publications 2018', 'Publications 2019', 'Publications 2020',
         'Publications 2021', 'Publications 2022', 'Publications 2023',
         'Publications 2024']

for year in years:
    # Rank the 'Concept' based on the number of publications in descending order (higher rank for more publications)
    rank_column = f"Rank {year.split()[-1]}"
    data_cleaned.loc[:, rank_column] = data_cleaned[year].rank(ascending=False)

data_cleaned = data_cleaned.sort_values(by='Rank 2024')

# Filter to keep only rows where the rank is 20 or lower for any of the years
rank_columns = [f"Rank {year.split()[-1]}" for year in years]
filtered_data = data_cleaned[(data_cleaned[rank_columns] <= 30).any(axis=1)]
print(f"Filtered data shape: {filtered_data.shape}")

# Save the cleaned and ranked data to a new CSV
output_file_path = '../data/concepts.csv'
data_cleaned.to_csv(output_file_path, index=False)
output_file_path_2 = '../data/filtered_concepts.csv'
filtered_data.to_csv(output_file_path_2, index=False)