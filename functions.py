from typing import Dict, Any

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json
import re
import numpy
import getopt
import sys

from utils import *
from api import *
from data import *
from dataframes import *
from plot import *
# from pprint import pprint


# 1) Get summary of all countries by country by status (total, not by day) - with last day new cases
def get_countries_df(save_df=False) -> 'pandas.core.frame.DataFrame':
    '''This function doesn't require any arguments, but it has an optional argument with the option to save the resulting dataframe, which is by default set to "False". It will request to the api a summary of all countries, select data points or total and new cases of confirmed, recoveries and deaths, determine the rates of recoveries and deaths based on this data, create a dictionary with this data and with it generate a dataframe. This dataframe can be saved by passin an argument of "True".'''
    all_data = get_countries_summary_data()
    data = make_countries_summary(all_data)
    df = create_countries_df(data)
    if save_df:
        version_count = 1
        today = datetime.date.today()
        file_name = f'Covid-19 Summary_{today}_{str(version_count)}'
        while os.path.isfile(file_name):
            version_count += 1
            file_name = f'Covid-19 Summary_{today}_{str(version_count)}'
        save_to_csv(df, file_name)
    return df


# 2) Plot dataframe for 1-3 countries, 3 line subplots by case status, option of daily or accumulated, daterange possible with default last 30 days, option to save dataframe
def plot(countries=list, daily=bool, last_date=datetime.date.today() - datetime.timedelta(1), days_number=30, save_df=False, save_img=False) -> None:
    data = get_select_countries_daily_data(countries, daily, last_date, days_number)
    df = create_df_all_countries_daily_data(data)
    covid_plot = plot_countries_dataframe(df, countries, last_date, days_number)

    # Save df to csv file if argument save_df=True >> change for cases - save df AND img, save df, save img, save none show plot
    if (save_df, save_img) == (True, True):
        file_name = set_filename(countries, last_date, days_number)
        save_to_csv(df, file_name)
        save_plot_img(covid_plot, file_name)
    elif (save_df, save_img) == (True, False):
        file_name = set_filename(countries, last_date, days_number)
        save_to_csv(df, file_name)
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
        if opt == '-c':
            countries = arg.split(',')

    plot(countries, daily=True, save_df=True, save_img=False)

