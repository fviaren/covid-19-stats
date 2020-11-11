from typing import Dict, Any

import requests
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json

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

# new DF for list of countries and 3 status - IN PROGRESS
def get_all_countries_daily_data(countries=list, daily=bool) -> 'pd.core.frame.DataFrame':
    countries_cases_stats = {
        'Confirmed Cases': {},
        'Recovered Cases': {},
        'Deaths': {}
    }
    for country in countries:
        country_slug = get_list_countries_slugs()[country]
        countries_cases_stats['Confirmed Cases'][country] = get_daily_country_data_by_status(country_slug, 'confirmed', daily)
        countries_cases_stats['Recovered Cases'][country] = get_daily_country_data_by_status(country_slug, 'recovered',
                                                                                             daily)
        countries_cases_stats['Deaths'][country] = get_daily_country_data_by_status(country_slug, 'deaths',
                                                                                             daily)
    #countries_cases_stats = {(outerKey, innerKey): values for outerKey, innerDict in countries_cases_stats.items() for innerKey, values in innerDict.items()}

    df = pd.io.json.json_normalize(countries_cases_stats)
    #df = pd.DataFrame(countries_cases_stats)
    #df.columns = df.columns.rename('Country', level=1)
    #df.columns = df.columns.rename('Status', level=0)
    #df.index.names = ['Date']
    #df.index = df.index.strftime('%Y-%m-%d')
    df.to_csv('file_name1.csv', encoding="utf-8", index=False)
    return df

def plot_dataframe2(countries=list, daily=bool) -> None:
    df = get_all_countries_daily_data(countries, daily)

    confirmed_df = df['Confirmed Cases']
    df['Date'] = df.index
    recovered_df = df['Recovered Cases']
    deaths_df = df['Deaths']


    print(deaths_df)
    df.to_csv('file_name.csv', encoding="utf-8", index=False)

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)

    for country in confirmed_df.columns.get_level_values('Country'):
        confirmed_df.plot(kind='line', y=country, ax=ax1)


    for country in recovered_df.columns.get_level_values('Country'):
        recovered_df.plot(kind='line', y=country, ax=ax2)


    for country in deaths_df.columns.get_level_values('Country'):
        deaths_df.plot(kind='line', y=country, ax=ax3)




    plt.show()

"""
    # Second way to do it (but xticks/x-labels become overpopulated):
    
    plot_title = f'Covid-19 Daily Cases in {country}'
    plt.subplot(3, 1, 1, title=plot_title)  # (row, column, no. of plots)
    plt.bar(x, df.sort_index()['Confirmed Cases'], color='#F5B041')
    plt.ylabel('Confirmed')
    plt.xticks([], [])
    plt.grid(axis='y', linestyle='dotted')

    plt.subplot(3, 1, 2)
    plt.bar(x, df['Recovered Cases'], color='#0eb077')
    plt.ylabel('Recovered')
    plt.xticks([], [])
    plt.grid(axis='y', linestyle='dotted')

    plt.subplot(3, 1, 3)
    plt.bar(x, df['Deaths'], color='#fc2403')
    plt.ylabel('Deaths')
    plt.grid(axis='y', linestyle='dotted')

    plt.xticks(x, df.index, rotation=45, fontsize=8)
    
    plt.show()
"""

def get_all_countries_daily_data2(countries=list, daily=bool) -> 'pd.core.frame.DataFrame':
    status = ['Confirmed Cases', 'Recovered Cases', 'Deaths']

    countries_cases_stats = {}
    for country in countries:
        country_slug = get_list_countries_slugs()[country]

        confirmed = get_daily_country_data_by_status(country_slug, 'confirmed', daily)
        for date, cases in confirmed.items():
            new_date = date.strftime("%Y-%m-%d")
            countries_cases_stats[new_date]['Confirmed Cases'][country] = cases

        recovered = get_daily_country_data_by_status(country_slug, 'recovered', daily)
        for date, cases in recovered.items():
            countries_cases_stats[str(date)]['Recovered Cases'][country] = cases

        deaths = get_daily_country_data_by_status(country_slug, 'deaths', daily)
        for date, cases in deaths.items():
            countries_cases_stats[str(date)]['Confirmed Cases'][country] = cases

    df = pd.DataFrame(countries_cases_stats)
    return df


if __name__ == "__main__":
    #plot_dataframe2(['Argentina', 'Germany', 'Spain'], False)
    pprint(get_all_countries_daily_data2(['Germany', 'France', 'Argentina'], True))
    #plot_dataframe(get_all_country_daily_data('Germany', True), 'Germany')
    #pprint(get_all_country_daily_data('Argentina'))
    #pprint(create_countries_df())
