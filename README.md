covid-19-stats
==============
Python functions to retrieve and display or export Covid-19 stats from [Coronavirus COVID19 API](https://covid19api.com/)

Features
-----------------
- __Request__ different sets of data from _API_
- __Reshape data__ to fit specific requirements
- Create __dataframes__ with _pandas_ library
- __Plot__ data using _Matplotlib_ library

This is a learning and showcase project that I developed as part of my learning process, with a relevant subject as of today.

Functions
-----------------
The functions are divided into separate files or modules for better efficiency and to follow best practices. An _interface_ functions.py file contains 3 main functions that will use support functions from other files.

- #### summary_df:

    This function doesn't require any arguments, but it has an optional argument with the option to save the resulting dataframe, which is by default set to "False". 
    
    It will:
     - request to the api a summary of all countries, 
     - select data points or total and new cases of confirmed, recoveries and deaths, 
     - determine the rates of recoveries and deaths based on this data, 
     - create a dictionary with this data and with it 
     - generate a dataframe. 
     - This dataframe can be saved by passing an argument of "True".

- #### compare_countries_df:
    This function returns a dataframe to compare (or see) covid stats form 1-3 countries. The dataframe is pivoted for better visibility and analysis. 
    
    The function takes 5 arguments:
    
     1. _countries_ that is mandatory and takes a list of 1-3 country ISO2 codes,
    
    and 4 optional arguments with default values:
    
     2. _daily_ a _boolean_ set by default to False to define if the data wanted is by day or accumulated/total;
    
     3. _last_date_ a _datetime_ value that can be input in format "%Y-%m-%d" such as "2020-11-18" set as default to the day before the current date; 
    
     4. _days_number_ an _integer_ that determined the number of days for which data is required, set by default to 30; 
     
     5. _save_df_ a _boolean_ to tell the function if the dataframe should be saved or not, set by default to False (if True the dataframe is pivoted for better visibility and analysis and then saved).
    
     __Limitations:__ At the moment this function can only accept 1-3 countries in its _countries_ argument since the API can only receive 10 requests per seconf and each country will make 3 requests. Planned to improve soon adding more options (see TODO section)

- #### plot:
    This function creates a dataframe to compare compare (or see) covid stats form 1-3 countries, and the plots the data into 3 subplots, une per case status.<br>
    
    The function accepts 6 arguments: 
     1. _countries_ that is mandatory and takes a list of 1-3 country ISO2 codes (if the list has 1 country the plot will be of kind "bar", if there are more than 1 country the plot kind will be "line"); 
     
    and 5 optional arguments with defaulta values;
     
     2. _daily_ a _boolean_ set by default to False to define if the data wanted is by day or accumulated/total; 
     
     3. _last_date_ a _datetime_ value that can be input in format "%Y-%m-%d" such as "2020-11-18" set as default to the day before the current date; 
     
     4. _days_number_ an _integer_ that determined the number of days for which data is required, set by default to 30;
     
     5. _save_df_ a _boolean_ to tell the function if the dataframe should be saved or not, set by default to False (if True the dataframe is pivoted for better visibility and analysis and then saved). ; 
     
     6. _save_img_ a _boolean_ to tell the function if the plot should be saved as a png file or not (and show it instead), set by default to False.

     __Limitations:__ At the moment this function can only accept 1-3 countries in its _countries_ argument since the API can only receive 10 requests per seconf and each country will make 3 requests. Planned to improve soon adding more options (see TODO section)

Usage
--------
#### Example 1 
> TBD
#### Example 2 
> TBD
#### Example 3 
> TBD
#### Example 4 
> TBD

TODO
----
- [ ] Add option to use function with multiple requests OR sorting all data
    - [ ] Add delay in process for multiple requests (more countries possible)
    - [ ] Sort request of all data in dict comprehensible by pandas/matplotlib with primary index date, then status then country
- [ ] Beautify plot
    - [ ] Modify xaxis ticks date format & frequency
- [ ] Cache data every x period of time