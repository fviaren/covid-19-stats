import datetime
import pandas as pd
import requests
import json
import re

payload = {}
headers = {}

# 2) Data per country daily from day 0
def format_date(date_str=str) -> datetime:
    new_date = datetime.datetime.strptime(date_str[:10], '%Y-%m-%d')
    return new_date


def get_list_countries_slugs_codes() -> dict:
    url = 'https://api.covid19api.com/countries'
    response = requests.request("GET", url, headers=headers, data=payload)
    list_countries = json.loads(response.content.decode('utf-8'))
    dict_countries = {}
    for each in list_countries:
        dict_countries[each['Country']] = [each['Slug'], each['ISO2']]
    return dict_countries


# Get country data of 1 country from day 1, by status, return a dict, option for daily or accumulated/total
def get_daily_country_data_by_status(country=str, status=str, daily=bool) -> dict:
    url = f'https://api.covid19api.com/total/dayone/country/{country}/status/{status}'
    response = requests.request("GET", url, headers=headers, data=payload)

    list_res = json.loads(response.content.decode('utf-8'))

    dict_cases_by_date = {}
    cases_until_yesterday = 0
    for each in list_res:
        if type(each) is dict:
            date = format_date(each['Date'])
            cases_until_today = int(each['Cases'])
            cases = cases_until_today
            if daily:
                cases = cases - cases_until_yesterday
                cases_until_yesterday = cases_until_today
            dict_cases_by_date[date] = cases
    return dict_cases_by_date


def split_label(label=str):
    new_label = re.sub('[()]', '', label).split(", ")[1]
    return new_label


# Save dataframe to a csv
def save_to_csv(df=pd.core.frame.DataFrame, file_name=str):
    df.to_csv(file_name, encoding="utf-8", index=False)
    return
