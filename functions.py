from typing import Dict, Any

import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json
import os.path
import re
import numpy
from pprint import pprint


payload = {}
headers = {}


# Get summary of all countries by country by status (total, not by day) - with last day new cases, updated daily
# Add rates for status based on New/Total cases
def get_countries_summary() -> dict:
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


# Create dataframe with data from summary of all countries
def create_countries_df(save_df=False) -> 'pandas.core.frame.DataFrame':
    data = get_countries_summary()
    df = pd.DataFrame(data).transpose().sort_values(by=['Total Confirmed Cases'], ascending=False)
    df = df.reset_index().rename(columns={'index': 'Country'})
    df.index = df.index + 1
    return df


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


# Create dataframe with 1 country daily data by case status by date
def get_all_country_daily_data(country=str, daily=bool):
    country_slug = get_list_countries_slugs_codes()[country][0]
    country_data = {
        'Confirmed Cases': get_daily_country_data_by_status(country_slug, 'confirmed', daily),
        'Recovered Cases': get_daily_country_data_by_status(country_slug, 'recovered', daily),
        'Deaths': get_daily_country_data_by_status(country_slug, 'deaths', daily)
    }
    df = pd.DataFrame(country_data)
    return df


# Plot dataframe into bar graph (1 country, by status from day 1)
def plot__country_dataframe(df: 'pd.core.frame.DataFrame', country=str) -> None:

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


# Get all data for dates range, multiple requests, will work in an alternative - good for 3 countries max (err 429, max 10 requests) option to save dataframe
def get_all_countries_daily_data(countries=list, daily=bool, last_date=datetime.date.today() - datetime.timedelta(1), days_number=30, save_df=False) -> 'pd.core.frame.DataFrame':
    # the date of the day before the requested start date, to be able to get daily numbers later
    first_date = last_date - datetime.timedelta(days_number + 1)
    status_list = ['confirmed', 'recovered', 'deaths']
    all_data_list =[]
    countries_slugs = get_list_countries_slugs_codes()
    for status in status_list:
        for country in countries:
            country_slug = countries_slugs[country][0]
            url = f'https://api.covid19api.com/total/country/{country_slug}/status/{status}?from={first_date}T00:00:00.000Z&to={last_date}T00:00:00.000Z'
            response = requests.request("GET", url, headers=headers, data=payload)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(f'{str(err)}\nYou most likely have input more than 3 countries, try with 3 or less less to avoid passing the limit of 10 requests per second')
                raise
            list_res = json.loads(response.content.decode('utf-8'))
           # New test
            if daily:
                cases_until_yesterday = 0
                for each in list_res:
                    cases_until_today = int(each['Cases'])
                    cases_today = cases_until_today - cases_until_yesterday
                    each['Cases'] = cases_today
                    cases_until_yesterday = cases_until_today
            # Delete the first row, a day before the start date requested
            list_res.pop(0)
            all_data_list += list_res
    df = pd.DataFrame(all_data_list).drop(columns=['Lon', 'Lat', 'CountryCode', 'Province', 'City', 'CityCode'])
    # Save df to csv file if argument save_df=True
    if save_df:
        countries_abbr_list = []
        for country in countries:
            countries_abbr_list.append(countries_slugs[country][1])
        countries_str = '-'.join(countries_abbr_list)
        start_date = last_date - datetime.timedelta(days_number)
        date_range_str = f'{start_date}_{last_date}'
        # avoid saving over existing file
        version_count = 1
        file_name = f'Covid-19 Stats_{countries_str}_{date_range_str}_{str(version_count)}.csv'
        while os.path.isfile(file_name):
            version_count += 1
            file_name = f'Covid-19 Stats_{countries_str}_{date_range_str}_{str(version_count)}.csv'
        save_to_csv(df, file_name)
    return df


# Plot dataframe for 1-3 countries, 3 line subplots by case status, option of daily or accumulated, daterange possible with default last 30 days, option to save dataframe
def plot_dataframe3(countries=list, daily=bool, last_date=datetime.date.today() - datetime.timedelta(1), days_number=30, save_df=False) -> None:
    # Get dataframe from other function for all countries and status
    df = get_all_countries_daily_data(countries, daily, last_date, days_number, save_df)

    # split dataframe in 3 separated by status
    df1, df2, df3 = [x for _, x in df.groupby(df['Status'])]

    nrow = 3
    ncol = 1
    case_status_name = []
    df_list = [df1, df2, df3]
    plot_title = f'Covid-19 cases in {", ".join(countries)}: {last_date - datetime.timedelta(days_number)} to {last_date} '

    fig, axes = plt.subplots(nrow, ncol, sharex=True, gridspec_kw={'hspace': 0})
    fig.suptitle(plot_title)
    count = 0
    for row_position in range(nrow):
        curr_df = df_list[count]
        # Determine status name for labels
        case_status_name.append(curr_df['Status'].values[0])
        # Remove column status
        curr_df.drop('Status', axis=1, inplace=True)
        # Set 2 level index
        curr_df.set_index(['Date', 'Country'], inplace=True)
        # Plot 3 cases status in 3 rows
        curr_df.unstack().plot(kind='line', ax=axes[row_position], legend=None)
        axes[row_position].set(ylabel=case_status_name[row_position])
        axes[row_position].grid(color='grey', linestyle='dotted')
        current_handles, current_labels = axes[row_position].get_legend_handles_labels()
        if len(countries) > 1:
            new_labels = list(map(split_label, current_labels))
            fig.legend(current_handles, new_labels)
        else:
            fig.legend(current_handles, ['Cases'])

        count += 1

    plt.show()


def split_label(label=str):
    new_label = re.sub('[()]', '', label).split(", ")[1]
    return new_label


# Save dataframe to a csv
def save_to_csv(df=pd.core.frame.DataFrame, file_name=str):
    df.to_csv(file_name, encoding="utf-8", index=False)
    return


if __name__ == "__main__":
    #print(split_label('(Cases, Argentina)'))
    plot_dataframe3(['United States of America'], daily=True, save_df=True)
    #pprint(get_all_countries_daily_data(['Argentina', 'Germany', 'Spain'], False))
    #plot_dataframe(get_all_country_daily_data('Germany', True), 'Germany')
    #pprint(get_all_country_daily_data('Argentina'))
    #pprint(create_countries_df())
    #pprint(get_list_countries_slugs_codes())
    #pprint(get_data_indiv_date_country_status('germany', '2020-10-17T00:00:00Z','confirmed'))
