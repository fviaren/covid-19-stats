from typing import Dict, Any

import requests
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt

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




if __name__ == "__main__":
    #plot_dataframe(get_all_country_daily_data('Germany', True), 'Germany')
    #pprint(get_all_country_daily_data('Argentina'))
    #pprint(create_countries_df())
