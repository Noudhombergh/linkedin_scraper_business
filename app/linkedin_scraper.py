import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API key not found in .env file")

# Define API endpoints and headers
BASE_URL = "https://api.coresignal.com/cdapi/v1/professional_network/company"
SEARCH_URL = f"{BASE_URL}/search/filter"
COLLECT_URL = f"{BASE_URL}/collect"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}


def fetch_company_data(country, location, min_employees, max_employees, output_file):
    # Define the payload
    payload = json.dumps(
        {
            "country": country,
            "employees_count_gte": min_employees,
            "employees_count_lte": max_employees,
            "location": location,
        }
    )

    # Search for company IDs
    response = requests.post(SEARCH_URL, headers=HEADERS, data=payload)

    if response.status_code != 200:
        print(f"Error fetching company IDs: {response.status_code}")
        print(response.text)
        return

    company_ids = response.json()
    print(f"Number of companies found: {len(company_ids)}")

    company_info_list = []

    # Fetch details for each company
    for company_id in company_ids:
        detail_url = f"{COLLECT_URL}/{company_id}"
        detail_response = requests.get(detail_url, headers=HEADERS)

        if detail_response.status_code == 200:
            company_data = detail_response.json()
            company_info = {
                "Company Name": company_data.get("name"),
                "Website": company_data.get("website"),
                "LinkedIn URL": company_data.get("url"),
                "Headquarters": company_data.get("headquarters_new_address"),
                "Employees Count": company_data.get("employees_count"),
                "Industry": company_data.get("industry"),
            }

            # Add featured employees
            featured_employees = company_data.get(
                "company_featured_employees_collection", []
            )
            active_employees = [
                emp for emp in featured_employees if emp.get("deleted") == 0
            ]

            for i, emp in enumerate(active_employees[:5], 1):
                emp_url = emp.get("url", "Unknown URL")
                company_info[f"Employee {i} LinkedIn"] = emp_url

            for i in range(len(active_employees) + 1, 6):
                company_info[f"Employee {i} LinkedIn"] = ""

            # Add location information
            locations = company_data.get("company_locations_collection", [])
            active_locations = [loc for loc in locations if loc.get("deleted") == 0]
            company_info["Locations"] = ", ".join(
                [loc.get("location_address") for loc in active_locations]
            )

            company_info_list.append(company_info)
            print(f"Data fetched for company: {company_data.get('name')}")
        else:
            print(
                f"Error fetching data for company ID {company_id}: {detail_response.status_code}"
            )

    # Create a DataFrame and save to an Excel file
    df = pd.DataFrame(company_info_list)
    columns = [
        "Company Name",
        "Headquarters",
        "Employees Count",
        "Website",
        "Industry",
        "LinkedIn URL",
        "Locations",
    ] + [f"Employee {i} LinkedIn" for i in range(1, 6)]
    df = df[columns]
    df.to_excel(output_file, index=False)
    print(f"Data exported to {output_file}")


# User-defined parameters
if __name__ == "__main__":
    COUNTRY = "YOUR_COUNTRY"
    LOCATION = "YOUR_CITY"
    MIN_EMPLOYEES = 20
    MAX_EMPLOYEES = 50
    OUTPUT_FILE = "path/to/your/file.xlsx"

    fetch_company_data(COUNTRY, LOCATION, MIN_EMPLOYEES, MAX_EMPLOYEES, OUTPUT_FILE)
