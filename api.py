import requests
import json
from utils import *



payload = {}
headers = {}


def get_list_countries_slugs_codes() -> list:
    url = 'https://api.covid19api.com/countries'
    response = requests.request("GET", url, headers=headers, data=payload)
    list_countries = json.loads(response.content.decode('utf-8'))
    return list_countries


def get_daily_country_data_by_status(country=str, status=str) -> list:
    url = f'https://api.covid19api.com/total/dayone/country/{country}/status/{status}'
    response = requests.request("GET", url, headers=headers, data=payload)
    list_res = json.loads(response.content.decode('utf-8'))
    return list_res


def get_countries_summary_data() -> list:
    url = 'https://api.covid19api.com/summary'
    response = requests.request("GET", url, headers=headers, data=payload)
    list_res = json.loads(response.content.decode('utf-8'))['Countries']
    return list_res
