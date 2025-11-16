from django.views import View
from django.shortcuts import render
import csv
from django.http import HttpResponse
from companyFilings.utils.companiesapi import CompaniesHouseAPI
from companyFilings.utils.numbervalidators import parse_company_numbers

# Create your views here.

class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')

class CompaniesInfoView(View):
    def get(self, request):
        return render(request, 'companiesInfo.html')
    
    def post(self, request):
        action = request.POST.get('action')
        raw_text = request.POST.get('company_numbers', '')
        

        if action == 'generate':
            return render(request, 'companiesInfo.html')
        elif action == 'download':
            return self.download_company_info(raw_text)
    
    def download_company_info(self,raw_text):
        
        valid_numbers, errors = parse_company_numbers(raw_text)
        api = CompaniesHouseAPI()
        company_data = api.fetch_multiple_companies(valid_numbers)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="company_info.csv"'

        writer = csv.writer(response)
        writer.writerow(['Company Number', 
                         'Company Name', 
                         'Status',
                         'Status Detail', 
                         'Confirmation Due', 
                         'Last Account Made Up To',
                         'Next Account Due'])
        
        for company in company_data:
            if 'error' in company:
                writer.writerow([company.get('company_number', 'N/A'), company['error']])
            else:
                writer.writerow([
                    company.get('company_number', 'N/A'),
                    company.get('company_name', 'N/A'),
                    company.get('company_status', 'N/A'),
                    company.get('company_status_detail', 'N/A'),
                    company.get('confirmation_statement', {}).get('next_due', 'N/A'),
                    company.get('accounts', {}).get('last_accounts', {}).get('made_up_to', 'N/A'),
                    company.get('accounts', {}).get('next_accounts', {}).get('due_on', 'N/A')
                ])
        
        for error in errors:
            writer.writerow([error])


        return response