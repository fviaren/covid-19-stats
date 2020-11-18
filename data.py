import datetime
import requests
import re

from utils import *
from api import *


def make_countries_summary(data=list) -> dict:
    countries_summary = {}
    for country_data in data:
        if int(country_data["TotalDeaths"]) > 0:
            death_rate = int(country_data["TotalDeaths"]) / int(
                country_data["TotalConfirmed"]
            )
        else:
            death_rate = 0
        if int(country_data["TotalRecovered"]) > 0:
            recovery_rate = int(country_data["TotalRecovered"]) / int(
                country_data["TotalConfirmed"]
            )
        else:
            recovery_rate = 0
        countries_summary[country_data["Country"]] = {
            "Total Confirmed Cases": int(country_data["TotalConfirmed"]),
            "New Confirmed Cases": int(country_data["NewConfirmed"]),
            "Total Recovered": int(country_data["TotalRecovered"]),
            "Total Deaths": int(country_data["TotalDeaths"]),
            "New Deaths": int(country_data["NewDeaths"]),
            "Death Rate": "{:.1%}".format(death_rate),
            "Recovery Rate": "{:.0%}".format(recovery_rate),
        }
    return countries_summary


def list_countries_slugs_codes() -> dict:
    url = build_api_url(request_type="slugs_codes")
    list_countries = get_api_data(url)
    dict_countries = {}
    for each in list_countries:
        dict_countries[each["ISO2"]] = [each["Slug"], each["Country"]]
    return dict_countries


# Get all data for dates range, multiple requests, will work in an alternative - good for 3 countries max (err 429, max 10 requests) option to save dataframe
def get_select_countries_daily_data(
    countries=list,
    daily=bool,
    last_date=datetime.date.today() - datetime.timedelta(1),
    days_number=30,
) -> list:
    # the date of the day before the requested start date, to be able to get daily numbers later
    first_date = last_date - datetime.timedelta(days_number + 1)
    status_list = ["confirmed", "recovered", "deaths"]
    all_data_list = []
    countries_slugs = list_countries_slugs_codes()
    for status in status_list:
        for country in countries:
            country_slug = countries_slugs[country][0]
            url = build_api_url(
                request_type="country_by_status",
                country_slug=country_slug,
                status=status,
                date_range=[first_date, last_date],
            )
            list_res = get_api_data(url)
            if daily:
                cases_until_yesterday = 0
                for each in list_res:
                    cases_until_today = int(each["Cases"])
                    cases_today = cases_until_today - cases_until_yesterday
                    each["Cases"] = cases_today
                    cases_until_yesterday = cases_until_today
            # Delete the first row, a day before the start date requested
            list_res.pop(0)
            all_data_list += list_res
    return all_data_list
