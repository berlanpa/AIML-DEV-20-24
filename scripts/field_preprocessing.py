import requests
import pandas as pd
from collections import defaultdict

# Base URL for OpenAlex API
base_url = "https://api.openalex.org/works"

# Parameters to query the API
per_page = 200
years_to_fetch = [2018, 2019, 2020, 2021, 2022, 2023, 2024]  # Years to iterate over


# Function to fetch grouped data by year for a given keyword
def fetch_grouped_data_by_year_and_keyword(year, keyword_id):
    url = f"{base_url}?group_by=primary_topic.field.id&per_page={per_page}&filter=publication_year:{year},keywords.id:{keyword_id}"
    print(f"Fetching data for year {year} and keyword {keyword_id}...")
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Successfully fetched data for year {year} and keyword {keyword_id}.")
        return response.json()["group_by"]
    else:
        print(f"Failed to fetch data for year {year} and keyword {keyword_id}: {response.status_code}")
        return []


# Function to group results by publication_year and primary_topic.field.id
def group_by_year_and_topic_for_keyword(years, keyword_id):
    grouped_results = []

    for year in years:
        results = fetch_grouped_data_by_year_and_keyword(year, keyword_id)
        for result in results:
            topic_id = result["key"]
            count = result["count"]
            grouped_results.append({
                "year": year,
                "field_id": topic_id,
                "count": count
            })
            print(f"Year: {year}, Topic ID: {topic_id}, Count: {count}")

    return grouped_results


# Load the keywords from CSV
keywords_csv_path = "../data/found_keywords.csv"
keywords_df = pd.read_csv(keywords_csv_path)

# Initialize an empty list to hold all grouped results across keywords
all_grouped_data = []

# Iterate through each keyword in the CSV
for index, row in keywords_df.iterrows():
    keyword_id = row['id'].split('/')[-1]  # Extract keyword ID from URL
    display_name = row['display_name']
    print(f"\nProcessing keyword: {display_name} (ID: {keyword_id})")

    # Fetch and group data for the current keyword
    grouped_data = group_by_year_and_topic_for_keyword(years_to_fetch, keyword_id)

    # Add keyword display name to each result and append to the main list
    for item in grouped_data:
        item["keyword"] = display_name
        all_grouped_data.append(item)

    print(f"Finished processing keyword: {display_name}.\n")

# Convert the final results to a pandas DataFrame
grouped_df = pd.DataFrame(all_grouped_data)

# Save the DataFrame to a CSV file
output_csv_path = "../data/grouped_results.csv"
grouped_df.to_csv(output_csv_path, index=False)

print(f"All keywords processed. Results saved to {output_csv_path}.")
