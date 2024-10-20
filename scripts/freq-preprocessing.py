import requests
import pandas as pd
import time


# Function to query OpenAlex API for each keyword
def fetch_works_per_year_by_keyword(keyword_id):
    api_url = f"https://api.openalex.org/works?group_by=publication_year&per_page=200&filter=keywords.id:keywords/{keyword_id}"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        results = data.get('group_by', [])
        return results
    else:
        print(f"Error fetching data for {keyword_id}: {response.status_code}")
        return []


# Function to get works per year for all keywords
def fetch_data_for_keywords(keyword_ids):
    all_data = []

    for keyword_id in keyword_ids:
        print(f"Fetching data for keyword: {keyword_id}")
        data = fetch_works_per_year_by_keyword(keyword_id)

        # Add keyword ID to each entry
        for entry in data:
            entry['keyword_id'] = keyword_id

        all_data.extend(data)
        time.sleep(1)  # To avoid hitting API rate limits

    return all_data


# Read the CSV file that contains the found keywords
found_keywords_df = pd.read_csv('../data/found_keywords.csv')

# Process the keyword IDs by extracting from the 'id' column
found_keywords_df['keyword_id'] = found_keywords_df['id'].apply(lambda x: x.split('/')[-1].lower().replace(' ', '-'))

# Extract the keyword IDs from the dataframe
keyword_ids = found_keywords_df['keyword_id'].tolist()

# Fetch works per year data for all keywords
all_keyword_data = fetch_data_for_keywords(keyword_ids)

df = pd.DataFrame(all_keyword_data)
print(df)

df = df.drop_duplicates(subset=['keyword_id', 'key'])

# Years we are interested in
years_of_interest = ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

# Pivot the data to have 'keyword_id' as distinct rows and 'key' as columns
df_pivot = df.pivot(index='keyword_id', columns='key', values='count')

# Reset the index to ensure 'keyword_id' is a column
df_pivot.reset_index(inplace=True)

# Only keep the years of interest
df_pivot = df_pivot[['keyword_id'] + years_of_interest]

# sort by 2024 count
df_pivot = df_pivot.sort_values(by='2024', ascending=False)

# filter out row with 'keyword_id' == 'anticipation'
df_pivot = df_pivot[df_pivot['keyword_id'] != 'anticipation']

# only keep first 10 rows
df_pivot = df_pivot.head(10)

# multiply '2024' column by 1.25
df_pivot['2024'] = df_pivot['2024'] * 1.25

# Preview the reshaped DataFrame
print(df_pivot)

# Optionally, save the reshaped data to a CSV
df_pivot.to_csv('../data/filtered_keywords.csv', index=False)
