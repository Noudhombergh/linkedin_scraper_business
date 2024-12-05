# LinkedIn Scraper Business

This repository contains a Python script to scrape company data from the LinkedIn API using CoreSignal. The script allows you to filter companies by country, location, and employee count, and export the results to an Excel file.

## Repository Structure
```
.
├── README.md
├── main.py
├── linkedin_scraper/
│   └── scraper.py
├── output/
└── requirements.txt
```

## Prerequisites
Before using this repository, you must sign up at [CoreSignal](https://coresignal.com) and obtain an API key. CoreSignal offers a free trial period, allowing you to test the API without cost.

1. Python 3.8 or higher
2. An API key for CoreSignal
3. Required Python libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Noudhombergh/linkedin_scraper_business.git
   cd linkedin_scraper_business
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate   # For Windows
   ```

3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following configuration:
   ```plaintext
   API_KEY=your_api_key_here
   COUNTRY=YOUR_COUNTRY
   LOCATION=YOUR_CITY
   MIN_EMPLOYEES=20
   MAX_EMPLOYEES=50
   OUTPUT_FILE=companies_data.xlsx
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. The output Excel file will be generated in the specified location (default: `companies_data.xlsx`).

## Configuration
You can configure the following parameters in the `.env` file:
- `API_KEY`: Your CoreSignal API key
- `COUNTRY`: Specify the country of the companies to fetch (e.g., `"Netherlands"`).
- `LOCATION`: Specify the city or region (e.g., `"Amsterdam"`).
- `MIN_EMPLOYEES`: Minimum number of employees (default: 20).
- `MAX_EMPLOYEES`: Maximum number of employees (default: 50).
- `OUTPUT_FILE`: Path to save the Excel output file (default: `companies_data.xlsx`).

## Customization
You can adjust the parameters in the `.env` file to customize the script's behavior.

## Example Output
The exported Excel file contains the following columns:
- **Company Name**
- **Headquarters**
- **Employees Count**
- **Website**
- **Industry**
- **LinkedIn URL**
- **Locations**
- **Employee 1-5 LinkedIn**

## Notes
- Ensure that your `.env` file is not included in version control by using the provided `.gitignore`.
- API response errors will be printed in the console for debugging.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Support
For issues or questions, please create a GitHub issue in this repository.
