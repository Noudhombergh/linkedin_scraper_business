"""
LinkedIn Company Scraper Module

This module provides functionality to scrape company data from LinkedIn using the Coresignal API.
It includes a LinkedInScraper class that handles all the scraping operations.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass

import os
import json
import requests
import pandas as pd

from dotenv import load_dotenv


@dataclass
class CompanySearchParams:
    """Data class for company search parameters."""
    country: str
    location: str
    min_employees: int
    max_employees: int
    output_file: str


class LinkedInScraper:
    """A class to handle LinkedIn company data scraping operations.
    
    This class provides methods to search for companies and collect detailed information
    about them using the Coresignal API.
    
    Attributes:
        api_key (str): The API key for authentication with Coresignal API.
        base_url (str): The base URL for the Coresignal API.
        headers (Dict[str, str]): HTTP headers including authentication.
    """

    def __init__(self) -> None:
        """Initialize the LinkedInScraper with API configuration."""
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API key not found in .env file")

        self.base_url = "https://api.coresignal.com/cdapi/v1/professional_network/company"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _search_companies(self, params: CompanySearchParams) -> List[str]:
        """Search for company IDs based on given parameters.
        
        Args:
            params: CompanySearchParams object containing search criteria.
            
        Returns:
            List of company IDs.
            
        Raises:
            requests.exceptions.RequestException: If API request fails.
        """
        payload = json.dumps({
            "country": params.country,
            "employees_count_gte": params.min_employees,
            "employees_count_lte": params.max_employees,
            "location": params.location,
        })

        response = requests.post(
            f"{self.base_url}/search/filter",
            headers=self.headers,
            data=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    def _get_company_details(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a specific company.
        
        Args:
            company_id: The ID of the company to fetch details for.
            
        Returns:
            Dictionary containing company details if successful, None otherwise.
        """
        detail_url = f"{self.base_url}/collect/{company_id}"
        response = requests.get(detail_url, headers=self.headers, timeout=60)

        if response.status_code == 200:
            return response.json()
        print(f"Error fetching data for company ID {company_id}: {response.status_code}")
        return None

    def _process_company_data(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw company data into a structured format.
        
        Args:
            company_data: Raw company data from the API.
            
        Returns:
            Processed company information dictionary.
        """
        company_info = {
            "Company Name": company_data.get("name"),
            "Website": company_data.get("website"),
            "LinkedIn URL": company_data.get("url"),
            "Headquarters": company_data.get("headquarters_new_address"),
            "Employees Count": company_data.get("employees_count"),
            "Industry": company_data.get("industry"),
        }

        # Process featured employees
        featured_employees = company_data.get("company_featured_employees_collection", [])
        active_employees = [emp for emp in featured_employees if emp.get("deleted") == 0]

        for i, emp in enumerate(active_employees[:5], 1):
            company_info[f"Employee {i} LinkedIn"] = emp.get("url", "")

        for i in range(len(active_employees) + 1, 6):
            company_info[f"Employee {i} LinkedIn"] = ""

        # Process locations
        locations = company_data.get("company_locations_collection", [])
        active_locations = [loc for loc in locations if loc.get("deleted") == 0]
        company_info["Locations"] = ", ".join(
            [loc.get("location_address") for loc in active_locations]
        )

        return company_info

    def fetch_company_data(self, params: CompanySearchParams) -> None:
        """Main method to fetch and save company data.
        
        Args:
            params: CompanySearchParams object containing search criteria.
            
        Raises:
            ValueError: If required parameters are missing.
            requests.exceptions.RequestException: If API requests fail.
        """
        try:
            company_ids = self._search_companies(params)
            print(f"Number of companies found: {len(company_ids)}")

            company_info_list = []
            for company_id in company_ids:
                if company_data := self._get_company_details(company_id):
                    company_info = self._process_company_data(company_data)
                    company_info_list.append(company_info)
                    print(f"Data fetched for company: {company_data.get('name')}")

            # Create DataFrame and save to Excel
            df = pd.DataFrame(company_info_list)
            columns = [
                "Company Name", "Headquarters", "Employees Count",
                "Website", "Industry", "LinkedIn URL", "Locations"
            ] + [f"Employee {i} LinkedIn" for i in range(1, 6)]

            df = df[columns]
            df.to_excel(params.output_file, index=False)
            print(f"Data exported to {params.output_file}")

        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
