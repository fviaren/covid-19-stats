import datetime
import pandas as pd
import re
import matplotlib.pyplot as plt
import os.path

from data import *

# 2) Data per country daily from day 0
def format_date_str(date_str=str) -> datetime:
    new_date = datetime.datetime.strptime(date_str[:10], "%Y-%m-%d").date()
    return new_date


def split_label(label=str):
    new_label = re.sub("[()]", "", label).split(", ")[1]
    return new_label


# Save dataframe to a csv
def save_to_csv(df=pd.core.frame.DataFrame, file_name=str):
    df.to_csv(f"{file_name}.csv", encoding="utf-8")
    return


def save_plot_img(plot, file_name):
    plot.savefig(f"{file_name}.png")
    return


def set_filename(countries=list, last_date=datetime, days_number=int) -> str:
    countries_str = "-".join(countries)
    start_date = last_date - datetime.timedelta(days_number)
    date_range_str = f"{start_date}_{last_date}"
    # avoid saving over existing file
    version_count = 1
    file_name = (
        f"Covid-19 Stats_{countries_str}_{date_range_str}_{str(version_count)}"
    )
    while os.path.isfile(f"{file_name}.csv") or os.path.isfile(
        f"{file_name}.png"
    ):
        version_count += 1
        file_name = f"Covid-19 Stats_{countries_str}_{date_range_str}_{str(version_count)}"
    return file_name
