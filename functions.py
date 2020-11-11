from typing import Dict, Any

import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy

from pprint import pprint


payload = {}
headers = {}

# 1) All countries data
def get_countries_summary():
    url = 'https://api.covid19api.com/summary'
    response = requests.request("GET", url, headers=headers, data=payload)
    list_res = json.loads(response.content.decode('utf-8'))['Countries']
    countries_summary = {}
    for country_data in list_res:
        if int(country_data['TotalDeaths']) > 0:
            death_rate = int(country_data['TotalDeaths']) / int(country_data['TotalConfirmed'])
        else:
            death_rate = 0
        if int(country_data['TotalRecovered']) > 0:
            recovery_rate = int(country_data['TotalRecovered']) / int(country_data['TotalConfirmed'])
        else:
            recovery_rate = 0
        countries_summary[country_data['Country']] = {
            'Total Confirmed Cases':  int(country_data['TotalConfirmed']),
            'New Confirmed Cases': int(country_data['NewConfirmed']),
            'Total Recovered': int(country_data['TotalRecovered']),
            'Total Deaths': int(country_data['TotalDeaths']),
            'New Deaths': int(country_data['NewDeaths']),
            'Death Rate': '{:.1%}'.format(death_rate),
            'Recovery Rate': '{:.0%}'.format(recovery_rate)
        }
    return countries_summary


def create_countries_df() -> 'pandas.core.frame.DataFrame':
    data = get_countries_summary()
    df = pd.DataFrame(data).transpose().sort_values(by=['Total Confirmed Cases'], ascending=False)
    df = df.reset_index().rename(columns={'index': 'Country'})
    df.index = df.index + 1
    return df


# Save dataframe to a csv and return the file name
def save_df_to_csv(df: 'pd.core.frame.DataFrame'):
    today = datetime.date.today().strftime('%d-%m-%Y')
    file_name = f'Covid-19 Countries-Stats_{today}.csv'
    df.to_csv(file_name, encoding="utf-8", index=False)
    return


# 2) Data per country daily
def format_date(date_str=str):
    # 'Date': '2020-10-25T00:00:00Z'
    new_date = datetime.datetime.strptime(date_str[:10], '%Y-%m-%d')
    #new_date = date1.strftime("%Y-%m-%d")
    return new_date


def get_list_countries_slugs() -> dict:
    url = 'https://api.covid19api.com/countries'
    response = requests.request("GET", url, headers=headers, data=payload)
    list_countries = json.loads(response.content.decode('utf-8'))
    dict_countries = {}
    for each in list_countries:
        dict_countries[each['Country']] = each['Slug']
    return dict_countries


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


def get_all_country_daily_data(country=str, daily=bool):
    country_slug = get_list_countries_slugs()[country]
    country_data = {
        'Confirmed Cases': get_daily_country_data_by_status(country_slug, 'confirmed', daily),
        'Recovered Cases': get_daily_country_data_by_status(country_slug, 'recovered', daily),
        'Deaths': get_daily_country_data_by_status(country_slug, 'deaths', daily)
    }
    df = pd.DataFrame(country_data)
    return df


def plot_dataframe(df: 'pd.core.frame.DataFrame', country=str) -> None:
    x = range(len(df.index))

    # test
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)

    fig.suptitle(f'Covid-19 Daily Cases in {country}')

    #ax1.plot_date(df.index, df['Confirmed Cases'], color="#F5B041") # (row, column, no. of plots)
    ax1.bar(df.index, df['Confirmed Cases'], color='#F5B041')
    ax1.set_ylabel('Confirmed', fontsize=12)
    ax1.grid(axis='both', linestyle='dotted')
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2.bar(df.index, df['Recovered Cases'], color='#0eb077')
    ax2.set_ylabel('Recovered', fontsize=12)
    ax2.grid(axis='both', linestyle='dotted')
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3.bar(df.index, df['Deaths'], color='#fc2403')
    ax3.set_ylabel('Deaths', fontsize=12)
    ax3.grid(axis='both', linestyle='dotted')
    plt.xticks(rotation=30, ha='right')

    plt.show()


# Added dates range with default 30 days back from yesterday - missing the differentiation between daily and accumulated/total
def get_all_countries_daily_data(countries=list, daily=bool, last_date=datetime.date.today() - datetime.timedelta(1), days_number=30) -> 'pd.core.frame.DataFrame':
    first_date = last_date - datetime.timedelta(days_number)
    status_list = ['confirmed', 'recovered', 'deaths']
    dates_list = []
    previous_date = last_date
    all_data_list =[]
    countries_slugs = get_list_countries_slugs()
    for dates in range(days_number, 0, -1):
        dates_list.append(previous_date.strftime('%Y-%m-%d'))
        previous_date = previous_date - datetime.timedelta(1)
    for status in status_list:
        for country in countries:
            country_slug = countries_slugs[country]
            url = f'https://api.covid19api.com/country/{country_slug}/status/{status}?from={first_date}T00:00:00.000Z&to={last_date}T00:00:00.000Z'
            response = requests.request("GET", url, headers=headers, data=payload)
            list_res = json.loads(response.content.decode('utf-8'))
            all_data_list += list_res
    df = pd.DataFrame(all_data_list).drop(columns=['Lon', 'Lat', 'CountryCode', 'Province', 'City', 'CityCode'])

    return df


# Reshape the dafaframe to be easier to handle for plotting - next: find the good way to create 3 subplots from each status, with multiple lines each, for each country - check also that date works in index
def plot_dataframe3(countries=list, daily=bool, last_date=datetime.date.today() - datetime.timedelta(1), days_number=30) -> None:

    # Get dataframe from other function for all countries and status
    df = get_all_countries_daily_data(countries, daily, last_date, days_number)

    # splits dataframe in 3 separated by status, get the status name to reference later, adds 2 level indexes
    df1, df2, df3 = [x for _, x in df.groupby(df['Status'])]
    cases1_status1 = df1['Status'].values[0]
    cases1_status2 = df2['Status'].values[0]
    cases1_status3 = df3['Status'].values[0]

    df1 = df1.drop(columns=['Status'])
    df2 = df2.drop(columns=['Status'])
    df3 = df3.drop(columns=['Status'])

    df1.set_index(['Date', 'Country'], inplace=True)
    df1.sort_index(inplace=True)
    df2.set_index(['Date', 'Country'], inplace=True)
    df2.sort_index(inplace=True)
    df3.set_index(['Date', 'Country'], inplace=True)
    df3.sort_index(inplace=True)

    # Plot
    df1.unstack().plot(kind='line')

    plt.show()


if __name__ == "__main__":
    plot_dataframe3(['Argentina', 'Germany', 'Spain'], True)
    #pprint(get_all_countries_daily_data(['Argentina', 'Germany', 'Spain'], True))
    #plot_dataframe(get_all_country_daily_data('Germany', True), 'Germany')
    #pprint(get_all_country_daily_data('Argentina'))
    #pprint(create_countries_df())
    #pprint(get_list_countries_slugs())
