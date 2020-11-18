from typing import Dict, Any

import datetime
import matplotlib.pyplot as plt
import getopt
import sys

from utils import *
from api import *
from data import *
from dataframes import *
from plot import *

# from pprint import pprint

# url = build_api_url(request_type='summary', country_slug, status, date_range)

# 1) Get summary of all countries by country by status (total, not by day) - with last day new cases
def summary_df(save_df=False) -> "pandas.core.frame.DataFrame":
    """This function doesn't require any arguments, but it has an optional argument with the option to save the resulting dataframe, which is by default set to "False". It will request to the api a summary of all countries, select data points or total and new cases of confirmed, recoveries and deaths, determine the rates of recoveries and deaths based on this data, create a dictionary with this data and with it generate a dataframe. This dataframe can be saved by passing an argument of "True"."""
    url = build_api_url(request_type="summary")
    all_data = get_api_data(url)["Countries"]
    data = make_countries_summary(all_data)
    df = create_countries_df(data)
    if save_df:
        version_count = 1
        today = datetime.date.today()
        file_name = f"Covid-19 Summary_{today}_{str(version_count)}"
        while os.path.isfile(file_name):
            version_count += 1
            file_name = f"Covid-19 Summary_{today}_{str(version_count)}"
        save_to_csv(df, file_name)
    return df


# 2) Create dataframe for 1-3 countries with daily data for a specific date range
def compare_countries_df(
    countries=list,
    daily=bool,
    last_date=datetime.date.today() - datetime.timedelta(1),
    days_number=30,
    save_df=False,
) -> "pandas.core.frame.DataFrame":
    """This function returns a dataframe to compare (or see) covid stats form 1-3 countries. The dataframe is pivoted for better visibility and analysis. The function takes 5 arguments: "countries" that is mandatory and takes a list of 1-3 country ISO2 codes; and 4 optional arguments with defaulta values. "daily" a boolean set by default to False to define if the data wanted is by day or accumulated/total; "last_date" a datetime value that can be input in format "%Y-%m-%d" such as "2020-11-18" set as default to the day before the current date; "days_number" an integer that determined the number of days for which data is required, set by default to 30; and "save_df" a boolean to tell the function if dataframe should be saved or not, set by default to False."""
    data = get_select_countries_daily_data(
        countries, daily, last_date, days_number
    )
    df = create_df_all_countries_daily_data(data)
    pivoted = pivot_df(df, ["Status", "Country"])
    if save_df:
        file_name = set_filename(countries, last_date, days_number)
        save_to_csv(pivoted, file_name)
    return pivoted


# 3) Plot dataframe for 1-3 countries, 3 line subplots by case status, option of daily or accumulated, daterange possible with default last 30 days, option to save dataframe
def plot(
    countries=list,
    daily=bool,
    last_date=datetime.date.today() - datetime.timedelta(1),
    days_number=30,
    save_df=False,
    save_img=False,
) -> None:
    """This function creates a dataframe to compare compare (or see) covid stats form 1-3 countries, and the plots the data into 3 subplots, une per case status. The function takes 6 arguments: "countries" that is mandatory and takes a list of 1-3 country ISO2 codes (if the list has 1 country the plot will be of kind "bar", if there are more than 1 coutnry the plot kind will be "line"); and 5 optional arguments with defaulta values. "daily" a boolean set by default to False to define if the data wanted is by day or accumulated/total; "last_date" a datetime value that can be input in format "%Y-%m-%d" such as "2020-11-18" set as default to the day before the current date; "days_number" an integer that determined the number of days for which data is required, set by default to 30; "save_df" a boolean to tell the function if the dataframe should be saved or not, set by default to False (if True the dataframe is pivoted for better visibility and analysis and then saved). ; "save_img" a boolean to tell the function if the plot should be saved as a png file or not (and show it instead), set by default to False."""
    data = get_select_countries_daily_data(
        countries, daily, last_date, days_number
    )
    df = create_df_all_countries_daily_data(data)
    covid_plot = plot_countries_dataframe(
        df, countries, last_date, days_number
    )

    # Save df to csv file if argument save_df=True
    if (save_df, save_img) == (True, True):
        pivoted = pivot_df(df, ["Status", "Country"])
        file_name = set_filename(countries, last_date, days_number)
        save_to_csv(pivoted, file_name)
        save_plot_img(covid_plot, file_name)
    elif (save_df, save_img) == (True, False):
        pivoted = pivot_df(df, ["Status", "Country"])
        file_name = set_filename(countries, last_date, days_number)
        save_to_csv(pivoted, file_name)
        covid_plot.show()
    elif (save_df, save_img) == (False, True):
        file_name = set_filename(countries, last_date, days_number)
        save_plot_img(covid_plot, file_name)
    else:
        covid_plot.show()


if __name__ == "__main__":
    countries = []

    opts, args = getopt.getopt(sys.argv[1:], "c:")
    for opt, arg in opts:
        if opt == "-c":
            countries = arg.split(",")

    # plot(countries, daily=True, save_df=True, save_img=False)
    print(
        compare_countries_df(
            countries, days_number=50, daily=True, save_df=True
        )
    )
