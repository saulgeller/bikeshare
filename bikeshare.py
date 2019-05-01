import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ['January', 'February', 'March', 'April', 'May', 'June']
day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city_list = list(CITY_DATA.keys())
    # This block gets the user's desired city, formats it, and checks it against the city_list variable. 
    city = input('Would you like to investigate Chicago, Washington, or New York City? ').lower()
    while city not in city_list:
        print('That\'s not a valid city for this program.')
        city = input('Would you like to investigate Chicago, Washington, or New York City? ').lower()
    # This block asks if the month needs to be filtered.  If yes, it asks for the month name and checks it against the month_list variable.  
    # If no, it sets month = 'all'. 
    month_filter = input('Would you like to filter data by month? Enter yes or no: ').lower()
    while month_filter != 'yes' and month_filter != 'no':
        print('Not a valid input. Please specify yes or no')
        month_filter = input('Would you like to filter data by month? Enter yes or no: ').lower()
    if month_filter == 'yes':
        month = input('Filter by which month? This program has data for January through June: ').title()
        while month not in month_list:
            print('Not a valid month for this program.')
            month = input('Filter by which month? This program has data for January through June: ').title()
    else:
        month = 'all'
    # This block asks if the day needs to be filtered. If yes, it checks the user's input of a day name against the day_list variable.
    # If no, it sets the day variable = 'all'. 
    day_filter = input('Would you like to filter data by day? Enter yes or no: ').lower()
    while day_filter != 'yes' and day_filter != 'no':
        print('Please specify yes or no.')
        day_filter = input('Would you like to filter data by day? Enter yes or no: ').lower()
    if day_filter == 'yes':
        day = input('Filter by which day? ').title()
        while day not in day_list:
            print('Not a valid day.')
            day = input('Filter by which day? ').title()
    else:
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # This block loads the user's desired city's table into a DataFrame and uses Pandas datetime functionality to append additional columns
    # needed later for time based statistics.  It then filters the DataFrame by month and day if specified by the user. 
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        month = month_list.index(month)+1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def condisplay_message(city, month, day):
    """
    Prints a line with the user's selected filters in a string message.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    
    """
    # This block prints a string with the user's selected filters. It's not completely necessary,
    # but is useful as an easily read reminder of the filters used, located at the top of the program's output. 
    if month == 'all' and day == 'all':
        print('For all months and all days in {}:\n'.format(city.title()))
    elif month == 'all' and day != 'all':
        print('For all months and all {}s in {}:\n'.format(day, city.title()))          
    elif month != 'all' and day == 'all':
        print('For all days in the month of {} in {}:\n'.format(month, city.title()))
    else:
        print('For all {}s in the month of {} in {}:\n'.format(day, month, city.title()))

def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (DataFrame) df - pre-filtered Pandas DataFrame
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # This block finds and prints the most popular month statistics if a month filter was not selected by the user. 
    if month == 'all':
        month_value_counts = df['month'].value_counts()
        pop_month = month_list[month_value_counts.keys()[0]-1]
        pop_month_count = month_value_counts.iloc[0]
        print('The most popular month was {}, with {} bikerides.'.format(pop_month, pop_month_count))
        
    
    # This block finds and prints the most popular day statistics if a day filter was not selected by the user. 
    if day == 'all':
        day_value_counts = df['day_of_week'].value_counts()
        pop_day = day_value_counts.keys()[0]
        pop_day_count = day_value_counts.iloc[0]
        print('The most popular day was {}, with {} bikerides.'.format(pop_day, pop_day_count))

    # This block finds and prints the most popular hour statistics for any and all filters selected by the user. 
    hour_value_counts = df['hour'].value_counts()
    pop_hour = hour_value_counts.keys()[0]
    pop_hour_count = hour_value_counts.iloc[0]
    print('The most popular hour was {} o\'clock with {} bikerides.'.format(pop_hour, pop_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
    (DataFrame) df - pre-filtered Pandas DataFrame
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # Adds a column to the DataFrame to help find popular start to end trip locations. 
    df['Trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')

    # This block finds and prints the name of the most popular starting place, as well as total number of trips from that station. 
    start_station_counts = df['Start Station'].value_counts()
    pop_start_station = start_station_counts.keys()[0]
    pop_start_station_count = start_station_counts.iloc[0]
    print('The most popular start station was {} with {} trips starting there.'.format(pop_start_station, pop_start_station_count))
    
    # This block finds and prints the name of the most popular ending place, as well as total number of trips that end at that station.
    end_station_counts = df['End Station'].value_counts()
    pop_end_station = end_station_counts.keys()[0]
    pop_end_station_count = end_station_counts.iloc[0]
    print('The most popular ending station was {} with {} trips ending there.'.format(pop_end_station, pop_end_station_count))

    # This block finds and prints the most popular trip, start to end, based on the new column created.
    trip_counts = df['Trip'].value_counts()
    pop_trip = trip_counts.keys()[0]
    pop_trip_count = trip_counts.iloc[0]
    print('The most popular trip was {} with {} trips.'.format(pop_trip, pop_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_time_units(trip_time_type, trip_time):
    """
    This program helps the trip_duration_stats() function decide what time units to use. The function checks if the time amount is
    less than or equal to 2 times the next biggest unit. If it is, it checks the next size unit, if it's not, it prints the time with
    the current unit. For example if its 1000 seconds, it checks if its less than or equal to 2 of the next biggest unit (minutes).
    It is not, so it checks if its less than or equal to 2 of the next biggest unit (hours). It is so it stops at minutes and prints
    the desired response.
    It also only prints to 2 decimal places, for more easily read numbers.
    
    Args:
        (str) trip_time_type - indicates the type of travel time being calculated for the printed output. Either 'total', or 'mean'
        (int) trip_time - trip time in seconds
    """
    if trip_time <= 120:
        print('The {} travel duration was {:.2f} seconds.'.format(trip_time_type, trip_time))
    elif trip_time <= 120*60:
        print('The {} travel duration was {:.2f} minutes'.format(trip_time_type, trip_time/60))
    elif trip_time <= 48*60*60:
        print('The {} travel duration was {:.2f} hours'.format(trip_time_type, trip_time/(60*60)))
    elif trip_time <= 60*24*60*60:
        print('The {} travel duration was {:.2f} days'.format(trip_time_type, trip_time/(60*60*24)))
    elif trip_time <= 48*30*24*60*60:
        print('The {} travel duration was {:.2f} months'.format(trip_time_type, trip_time/(60*60*24*30)))
    else:
        print('The {} travel duration was {:.2f} years'.format(trip_time_type, trip_time/(60*60*24*365)))

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
    (DataFrame) df - pre-filtered Pandas DataFrame
    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # This block finds the total trip duration of all trips taken for the user's selected filters. It then displays that time
    # in seconds, minutes, hours, days, months, or years, rounded to 2 decimal places. 
    total_trip_time = df['Trip Duration'].sum()
    total_trip_type = 'total'
    trip_time_units(total_trip_type, total_trip_time)
    
    # This block finds the mean trip duration for all trips taken for the user's selected filters. It then displays that time 
    # in seconds, minutes, hours, days, months, or years, rounded to 2 decimal places.  
    mean_trip_time = df['Trip Duration'].mean()
    mean_trip_type = 'mean'
    trip_time_units(mean_trip_type, mean_trip_time)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users.
    
    Args:
        (DataFrame) df - pre-filtered Pandas DataFrame
        (str) city - name of the city to analyze
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Prints a Pandas Series of all user types and their counts, as well as filling all NaNs with N/A (not available). 
    print(df['User Type'].fillna('N/A').value_counts())
    print()
    

    # Because the Washington data table doesn't have a gender column, a try/except function is used to handle any KeyErrors. 
    # If there is no KeyError exception thrown up, this block will print a Pandas series with a count of gender types (male and female)
    # as well as a column for N/A, filled with any NaN values. 
    try:
        print(df['Gender'].fillna('N/A').value_counts())
        print()
    except KeyError:
        print('{} has no gender data available.'.format(city.title()))
        print()
    

    # The Washington data table also has no birth year column, so another try/except block is used. If no KeyError comes up, this block will find and 
    # print values for the oldest birth year, most recent birth year, and the most common birth year, for the user's selected filters.
    try:
        oldest_birth_year = int(df['Birth Year'].min())
        youngest_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('The earliest user birth year is {}. The most recent user birth year is {}. The most common user birth year is {}.'.format(
            oldest_birth_year, youngest_birth_year, common_birth_year))
    except KeyError:
        print('{} has no birth year data available.'.format(city.title()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    This function gives the user the option to see 5 rows of the raw data from their filtered DataFrame
    and then see 5 more rows until they decide to stop.
    
    Args:
        (DataFrame) df - the Pandas DataFrame loaded based on the user's filters.
    """
    
    # This code gets users yes or no input on seeing 5 rows of data, then asks again and continuously shows
    # the next 5 rows until the user inputs no which stops the function.
    display_input = input('Would you like to see the raw data (5 rows)? Enter yes or no: ').lower()
    while display_input != 'yes' and display_input != 'no':
        display_input = input('Not a valid input. Please enter yes or no: ').lower()
    if display_input == 'yes':
        i=0
        while True:
            print(df.iloc[i:i+5,:])
            display_input = input('Would you like to see 5 more rows? Enter yes or no: ').lower()
            while display_input != 'yes' and display_input != 'no':
                display_input = input('Not a valid input. Please enter yes or no: ').lower()
            if display_input == 'yes':
                i += 5
            else:
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        condisplay_message(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
