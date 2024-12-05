"""
Main script for running the LinkedIn Company Scraper.

This script loads configuration from .env file and runs the scraper.
"""

import os

from dotenv import load_dotenv
from linkedin_scraper import LinkedInScraper, CompanySearchParams


def main() -> None:
    """Main function to run the LinkedIn scraper."""
    # Load configuration from .env
    load_dotenv()

    # Create search parameters from environment variables
    params = CompanySearchParams(
        country=os.getenv("COUNTRY", "YOUR_COUNTRY"),
        location=os.getenv("LOCATION", "YOUR_CITY"),
        min_employees=int(os.getenv("MIN_EMPLOYEES", "20")),
        max_employees=int(os.getenv("MAX_EMPLOYEES", "50")),
        output_file=os.getenv("OUTPUT_FILE", "companies_data.xlsx")
    )

    # Initialize and run scraper
    scraper = LinkedInScraper()
    scraper.fetch_company_data(params)


if __name__ == "__main__":
    main()
