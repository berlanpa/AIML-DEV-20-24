import requests
import csv

# OpenAlex API base URL for concept search
base_url = "https://api.openalex.org/concepts"

# OpenAlex concept IDs for Machine Learning and Artificial Intelligence
concepts = {
    "Machine Learning": "https://openalex.org/C119857082",
    "Artificial Intelligence": "https://openalex.org/C154945302"
}

# Years to collect publication counts for
years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]


# Function to get level 2 related concepts for a given concept ID
def get_related_concepts(concept_id):
    # Extract the concept identifier from the URL
    concept_identifier = concept_id.split('/')[-1]

    # Query OpenAlex API for related concepts
    print(f"Fetching related concepts for Concept ID: {concept_id}...")
    response = requests.get(f"https://api.openalex.org/concepts/{concept_identifier}")

    if response.status_code == 200:
        data = response.json()
        related_concepts = data.get("related_concepts", [])

        # Filter for level 2 concepts (direct sub-concepts)
        level_2_concepts = [concept for concept in related_concepts if concept['level'] == 2]

        print(f"Found {len(level_2_concepts)} level 2 concepts for Concept ID {concept_id}.")
        return level_2_concepts
    else:
        print(f"Error: {response.status_code} for Concept ID {concept_id}")
        return []


# Function to get the publication count for a concept for a given year
def get_publication_count(concept_id, year):
    concept_identifier = concept_id.split('/')[-1]
    # Query OpenAlex API for concept works and filter by year
    print(f"Fetching publication count for Concept ID: {concept_id} for year {year}...")
    response = requests.get(
        f"https://api.openalex.org/works?filter=concepts.id:{concept_identifier},publication_year:{year}")

    if response.status_code == 200:
        data = response.json()
        return data.get('meta', {}).get('count', 0)  # Return the number of publications
    else:
        print(f"Error fetching publication count for Concept ID {concept_id} in year {year}: {response.status_code}")
        return 0


# Prepare a list to hold the data for the CSV
csv_data = []

# Fetch and process level 2 concepts for Machine Learning and Artificial Intelligence
for concept_name, concept_id in concepts.items():
    print(f"\nProcessing {concept_name}...")
    level_2_concepts = get_related_concepts(concept_id)

    # Append the level 2 concepts along with their parent concept to the CSV data
    for concept in level_2_concepts:
        concept_info = {
            'Concept': concept['display_name'],
            'Concept ID': concept['id'],
            'Parent': concept_name
        }

        # Fetch publication counts for each year
        for year in years:
            publication_count = get_publication_count(concept['id'], year)
            concept_info[f'Publications {year}'] = publication_count

        csv_data.append(concept_info)

# Write the data to a CSV file
csv_filename = '../data/level_2_concepts.csv'
with open(csv_filename, mode='w', newline='') as file:
    fieldnames = ['Concept', 'Concept ID', 'Parent'] + [f'Publications {year}' for year in years]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv_data:
        writer.writerow(row)

print(f"\nCSV file '{csv_filename}' with Level 2 concepts and publication counts has been created.")
