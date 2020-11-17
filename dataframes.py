import pandas as pd


# Create dataframe with data from summary of all countries
def create_countries_df(data=dict) -> 'pandas.core.frame.DataFrame':
    df = pd.DataFrame(data).transpose().sort_values(by=['Total Confirmed Cases'], ascending=False)
    df = df.reset_index().rename(columns={'index': 'Country'})
    df.index = df.index + 1
    return df


# Get all data for dates range, multiple requests, will work in an alternative - good for 3 countries max (err 429, max 10 requests) option to save dataframe
def create_df_all_countries_daily_data(data) -> 'pd.core.frame.DataFrame':
    df = pd.DataFrame(data).drop(columns=['Lon', 'Lat', 'CountryCode', 'Province', 'City', 'CityCode'])

    return df
