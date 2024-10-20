import pandas as pd

df_field = pd.read_csv('../data/openalex_fields.csv')
df = pd.read_csv('../data/grouped_results.csv')

# Merge the two dataframes on the 'field_id' column
df = pd.merge(df, df_field, left_on='field_id', right_on='id')
print(df.head())

# Sort by field and save the merged dataframe to a new CSV file
df = df.sort_values(by='field')

# multiply count by 1.25 for year == 2024
df.loc[df['year'] == 2024, 'count'] = df['count'] * 1.25

# Group by field and year and sum the counts
df = df.groupby(['field', 'year'])['count'].sum().reset_index()
df.to_csv('../data/grouped_results_with_fields.csv', index=False)
