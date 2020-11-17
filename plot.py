import matplotlib.pyplot as plt
import datetime
from typing import Dict, Any
# import matplotlib.dates as mdates


from utils import *


def plot_countries_dataframe(df, countries=list, last_date=datetime, days_number=int):
    # split dataframe in 3 separated by status
    df1, df2, df3 = [x for _, x in df.groupby(df['Status'])]

    if len(countries) > 1:
        plot_kind = 'line'
    else:
        plot_kind = 'bar'
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
        curr_df.unstack().plot(kind=plot_kind, ax=axes[row_position], legend=None)
        axes[row_position].set(ylabel=case_status_name[row_position])
        axes[row_position].grid(color='grey', linestyle='dotted')

        # need Matplotlib 3.2.2 for format dates to work
        #axes[row_position].xaxis.set(major_locator=mdates.AutoDateLocator(minticks=1, maxticks=5),)
        #locator = mdates.AutoDateLocator(minticks=15, maxticks=20)
        #formatter = mdates.ConciseDateFormatter(locator)
        #axes[row_position].xaxis.set_major_locator(locator)
        #axes[row_position].xaxis.set_major_formatter(formatter)

        plt.xticks(rotation=45, ha='right', fontsize=8)
        current_handles, current_labels = axes[row_position].get_legend_handles_labels()

        if len(countries) > 1:
            new_labels = list(map(split_label, current_labels))
            fig.legend(current_handles, new_labels)
        else:
            fig.legend(current_handles, ['Cases'])

        count += 1
    return plt
