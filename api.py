import requests
import json
import re
from utils import *


payload = {}
headers = {}


def build_api_url(
    request_type=str, country_slug="", status="", date_range=[]
) -> str:
    """This function builds and returns the url needed to perform an api request, as a string. It takes 4 arguments: a mandatory "request_type" to determine the type of request to be done, that can be "summary" to get a summary of data from all countries, "slugs_codes" to get all names, ISO2 codes and slugs from all countries, and "country_by_status" to get all data from one country by a specific status on a defined date range. The last 3 arguments will be necessary for the last case, set by default to empty string, empty string and empty list, respectively."""
    if request_type == "summary":
        url = "https://api.covid19api.com/summary"
    elif request_type == "slugs_codes":
        url = "https://api.covid19api.com/countries"
    elif request_type == "country_by_status":
        url = f"https://api.covid19api.com/total/country/{country_slug}/status/{status}?from={date_range[0]}T00:00:00.000Z&to={date_range[1]}T00:00:00.000Z"
    return url


def get_api_data(url) -> list:
    """This function performs a request to the covid19api and returns a list of data based on the url provided. If too many requests are made, this function will raise an exception for error 429 as this API allows to make maximum 10 requests per second"""
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(
            f"{str(err)}\nYou most likely have input more than 3 countries, try with 3 or less less to avoid passing the limit of 10 requests per second"
        )
        raise
    list_res = json.loads(response.content.decode("utf-8"))
    return list_res
