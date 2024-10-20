import requests
import csv

# Base URL for OpenAlex API
base_url = "https://api.openalex.org/"


def get_domains():
    url = base_url + "domains"
    response = requests.get(url)
    return response.json()


def extract_fields_from_domains():
    # Open a CSV file to write the data
    with open('../data/openalex_fields.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['id', 'field', 'parent domain'])

        # Fetch all domains
        domains = get_domains()

        # Iterate through each domain and extract fields
        for domain in domains['results']:
            domain_name = domain['display_name']

            # Get fields for the domain
            fields = domain['fields']

            # Iterate through each field in the fields object and write to CSV
            for field in fields:
                field_id = field['id']
                field_name = field['display_name']
                # Write row to the CSV file
                writer.writerow([field_id, field_name, domain_name])

    print("Data saved to openalex_fields.csv")


extract_fields_from_domains()
