# LinkedIn Scraper Business

This repository contains a Python script to scrape company data from the LinkedIn API using CoreSignal. The script allows you to filter companies by country, location, and employee count, and export the results to an Excel file.

## Repository Structure
```
.
├── README.md
├── app
│   └── linkedin_scraper.py
└── requirements.txt
```

## Prerequisites
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

4. Create a `.env` file in the root directory and add your API key:
   ```plaintext
   API_KEY=your_api_key_here
   ```

## Usage

1. Navigate to the `app` directory:
   ```bash
   cd app
   ```

2. Open `linkedin_scraper.py` and update the user-defined parameters at the bottom of the file:
   ```python
   COUNTRY = "Netherlands"
   LOCATION = "Venlo"
   MIN_EMPLOYEES = 20
   MAX_EMPLOYEES = 50
   OUTPUT_FILE = "company_data.xlsx"
   ```

3. Run the script:
   ```bash
   python linkedin_scraper.py
   ```

4. After the script completes, the output file (`company_data.xlsx`) will be generated in the specified location.

## Customization
You can adjust the following parameters:
- `COUNTRY`: Specify the country of the companies to fetch (e.g., `"Netherlands"`).
- `LOCATION`: Specify the city or region (e.g., `"Venlo"`).
- `MIN_EMPLOYEES`: Minimum number of employees.
- `MAX_EMPLOYEES`: Maximum number of employees.
- `OUTPUT_FILE`: Path to save the Excel output file.

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

