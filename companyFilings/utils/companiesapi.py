import requests
from django.conf import settings

class CompaniesHouseAPI:
    BASE_URL = "https://api.company-information.service.gov.uk/company/"

    def __init__(self):
        self.api_key = settings.COMPANIES_HOUSE_API_KEY

    def fetch_company_profile(self, company_number):
        url = f"{self.BASE_URL}{company_number}" 
        
        response = requests.get(url, auth=(self.api_key, ''))
        
        if response.status_code == 200:
            return response.json()
        
        return {
            "company_number": company_number,
            "error": f"Not found (status {response.status_code})"
        }

    def fetch_multiple_companies(self, company_numbers):
        results = []
        for number in company_numbers:
            profile = self.fetch_company_profile(number)
            results.append(profile)  
        return results
    
    