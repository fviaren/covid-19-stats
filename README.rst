covid-19-stats
==============
Python functions to retrieve and display or export Covid-19 stats from `Coronavirus COVID19 API`_
    .. _Coronavirus COVID19 API: https://covid19api.com/

Features
--------
- **Request** different sets of data from *API*
- **Reshape data** to fit specific requirements
- Create **dataframes** with *pandas* library
- **Plot** data using *Matplotlib* library

This is a learning and **showcase project** that I developed as part of my **learning process**, with a relevant subject as of today.

Functions
-----------------
The functions are divided into **separate files** or modules for better efficiency and to follow best practices. An _interface_ functions.py file contains **3 main functions** that will use support functions from other files.

@@summary_df:@@
"""""""""""""""
    This function doesn't require any arguments, but it has an optional argument with the option to save the resulting dataframe, which is by default set to "False".

    It will:
     - request to the api a summary of all countries,
     - select data points or total and new cases of confirmed, recoveries and deaths,
     - determine the rates of recoveries and deaths based on this data,
     - create a dictionary with this data and with it
     - generate a dataframe.
     - This dataframe can be saved by passing an argument of "True".

@@compare_countries_df:@@
"""""""""""""""""""""""""
    This function returns a dataframe to compare (or see) covid stats form 1 or more countries. The dataframe is pivoted for better visibility and analysis. The dataframe may be saved as a csv file.

    The function takes 5 arguments:

     1. **countries:** mandatory, a list of country ISO2 codes as strings,

    and 4 optional arguments with default values:

     2. **daily:** a *boolean* set by default to False to define if the data wanted is by day or accumulated/total;

     3. **last_date:** a *string* date value that can be input in format *"%Y-%m-%d"* such as *"2020-11-18"* set as default to the day before the current date;

     4. **days_number:** an *integer* that determines the number of days for which data is required, set by default to 30;

     5. **save_df:** a *boolean* to tell the function if the dataframe should be saved or not, set by default to False (if True the dataframe is pivoted for better visibility and analysis and then saved).

     **Limitations:** At the moment this function makes 3 requests per country to the API, one per case status. Due to the rate limitation of 10 requests per second, for more than 3 countries the function will take longer to run with a delay of 3 seconds between a 429 error (too many requests) and the next request (after 3 countries there will be an added request of 3 seconds every 3 new countries) (see TODO section)

@@plot:@@
"""""""""
    This function creates a dataframe to compare compare (or see) covid stats form 1-3 countries, and the plots the data into 3 subplots, une per case status.<br>

    The function accepts 6 arguments:
     1. **countries:** mandatory, a list of country ISO2 codes as strings (if the list has 1 country the plot will be of kind "bar", if there are more than 1 country the plot kind will be "line");

    and 5 optional arguments with defaulta values;

     2. **daily:** a *boolean* set by default to False to define if the data wanted is by day or accumulated/total;

     3. **last_date:** a *string* date value that can be input in format *"%Y-%m-%d"* such as *"2020-11-18"* set as default to the day before the current date;

     4. **days_number:** an *integer* that determines the number of days for which data is required, set by default to 30;

     5. **save_df:** a *boolean* to tell the function if the dataframe should be saved or not, set by default to False (if True the dataframe is pivoted for better visibility and analysis and then saved);

     6. **save_img:** a *boolean* to tell the function if the plot should be saved as a png file or not (and show it instead), set by default to False.

     **Limitations:** At the moment this function makes 3 requests per country to the API, one per case status. Due to the rate limitation of 10 requests per second, for more than 3 countries the function will take longer to run with a delay of 3 seconds between a 429 error (too many requests) and the next request (after 3 countries there will be an added request of 3 seconds every 3 new countries) (see TODO section)



Usage
-----

Example 1
"""""""""
.. code-block:: python

   summary_df(True) # returns a pandas dataframe and saves it as a csv file in the current directory



Example 2
"""""""""

.. code-block:: python

    compare_countries_df(['NO', 'NZ'], daily=True, save_df=True)
    # returns a dataframe with the daily confirmed, recoverd and death cases
    # of the countries Norway and New Zealand from yesterday to 30 days backwards and saves it into the local directory as a csv file.
    # Filename: Covid-19 Stats_NO-NZ_2020-10-22_2020-11-21_1.csv

Example 3
"""""""""

.. code-block:: python

    plot(['AR', 'DE', 'BR'], daily=True, save_df=True)
    # creates a dataframe, saves it into the local directory as a csv file and shows a plot of the data in 3 line subplots
    # comparing the daily confirmed, recoverd and death cases of the countries Argentina, Germany and Brazil from yesterday to 30 days backwards.
    # Filename: Covid-19 Stats_AR-DE-BR_2020-10-22_2020-11-21_1.csv

Example 4
"""""""""

.. code-block:: python

    plot(['IN', 'MA'], daily=False, last_date='2020-10-31', days_number=50, save_df=False, save_img=True)
    # creates a dataframe and then a plot with 3 line subplots comparing the total/accumulated confirmed, recoverd and death cases per day
    # of the countries India and Morocco from October 31st 2020 to 50 days backwards, which is saved into the local directory as a png file.
    # Filename: Covid-19 Stats_IN-MA_2020-09-11_2020-10-31_1.png

Example 5
"""""""""

.. code-block:: python

    plot(['MT'], daily=True, days_number=150)
    # creates a dataframe, and then shows a plot with 3 bar subplots comparing the daily confirmed, recoverd and death cases
    # of the country Malta from yesterday to 150 days before.

TODO
----
.. |check| raw:: html

    <input checked=""  type="checkbox">

.. |uncheck| raw:: html

    <input type="checkbox">

- |uncheck| Add option to use function with multiple requests OR sorting all data
    - |check| Add delay in process for multiple requests (more countries possible)
    - |uncheck| Sort request of all data in dict comprehensible by pandas/matplotlib with primary index date, then status then country, for 1 request per country for all cases status
- |uncheck| Beautify plot
    - |uncheck| Modify xaxis ticks date format & frequency
- |uncheck| Cache data every x period of time
- |uncheck| Add directory argument to save file
