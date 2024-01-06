import requests
from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
import os
import json
from urllib.parse import urlparse
import textrazor
from .models import Company, Page
from dotenv import load_dotenv

load_dotenv()

textrazor.api_key = os.environ.get("TEXTRAZOR_KEY")

class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username=os.environ.get("DATAFORSEO_USER"), 
              password=os.environ.get("DATAFORSEO_PASSWORD")):
        self.username = username
        self.password = password

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
                ).decode("ascii")
            headers = {'Authorization' : 'Basic %s' %  base64_bytes, 'Content-Encoding' : 'gzip'}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)


def update_company_fields_from_json():
    for company in Company.objects.filter(traffic_us__isnull=True, domain_data_json__isnull=False):
        company.traffic_us = company.domain_data_json["tasks"][0]["result"][0]["items"][0]["metrics"]["organic"]["etv"]
        company.save()

    for company in Company.objects.filter(pages_in_serps__isnull=True, domain_data_json__isnull=False):
        company.pages_in_serps = company.domain_pages_data_json["tasks"][0]["result"][0]["total_count"]
        company.save()



def get_seo_domain_data():
    print('getting seo data for domains..')
    companies = Company.objects.filter(domain_data_json__isnull=True, is_published=True)

    client = RestClient()

    for company in companies:
        print('getting domain data for', company.name)
        # simple way to set a task
        domain = urlparse(company.domain).netloc
        post_data = dict()
        post_data[len(post_data)] = dict(
            target=domain,
            location_name="United States",
            language_name="English",
            exclude_top_domains=True,
            limit=20,
        )
        # POST /v3/dataforseo_labs/google/competitors_domain/live
        response = client.post("/v3/dataforseo_labs/google/competitors_domain/live", post_data)
        # you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
        if response["status_code"] == 20000:
            try:
                company.domain_data_json = response
                company.traffic_us = company.domain_data_json["tasks"][0]["result"][0]["items"][0]["metrics"]["organic"]["etv"]
                company.save()
            except ValueError as e:
                            print(e)
        else:
            print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

        print('finding domain pages')

    companies = Company.objects.filter(domain_pages_data_json__isnull=True)

    for company in companies:
        domain = urlparse(company.domain).netloc
        post_data = dict()
        post_data[len(post_data)] = dict(
            target=domain,
            location_name="United States",
            language_name="English",
            limit=1000,
            order_by=["metrics.organic.etv,desc"]
        )
        # POST /v3/dataforseo_labs/google/relevant_pages/live
        response = client.post("/v3/dataforseo_labs/google/relevant_pages/live", post_data)
        # you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
        if response["status_code"] == 20000:
            # print(response)
            try:
                company.domain_pages_data_json = response
                company.pages_in_serps = company.domain_pages_data_json["tasks"][0]["result"][0]["total_count"]
                company.save()
            except ValueError as e:
                print(e) 
        else:
            print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))


def get_competitors():
    for company in Company.objects.filter(domain_data_json__isnull=False, is_published=True):
        competitors = company.domain_data_json['tasks'][0]['result'][0]['items'][1:]
        for comp in competitors:
            domain = 'https://'+comp["domain"]
            existing_comp = Company.objects.filter(domain=domain).first()
            if not existing_comp:
                Company.objects.create(
                    name=comp["domain"],
                    domain=domain,
                    niche=company.niche
                )


def get_entity_for_root_domain(company):
    if textrazor.api_key == None:
         print('textrazor api key not set')
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    page, created = Page.objects.get_or_create(company=company, url=company.domain)
    if not page.textrazor_json:
        if company and company.domain:
            print("Company: ", company)  # Check if your Company object exists
            print("Domain: ", company.domain)  # Check if Company's Domain attribute indeed contains valid/enough data
            print('getting entities for root of |', company.domain)
            response = client.analyze_url(str(company.domain))
            page.textrazor_json = response.json
            page.save()


def get_entities_for_companies():
    for company in Company.objects.filter(is_published=True):
         get_entity_for_root_domain(company)
