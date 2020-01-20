import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please input city name (chicago, new york city, washington): ").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("INVALID! Please enter the name one of three cities (chicago, new york city, washington): ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Please input full month name (january-june), OR input (all) for all the months: ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input("INVALID! Please input full month name (january-june), OR input (all) for all the months: ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please input full week day name (monday-sunday), OR input (all) for all the days in the week: ").lower()
    while day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
         day = input("INVALID! Please input full week day name (monday-sunday), OR input (all) for all the days in the week: ").lower()

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
    filename = city.replace(" ", "_").lower() + ".csv"
    df = pd.read_csv(filename)

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    mc_month = str(months[df['month'].mode().values[0] - 1])
    print("The most common month is: {}".format(mc_month).title())

    # TO DO: display the most common day of week
    mc_day = str(df['day_of_week'].mode().values[0])
    print("The most common day of week is: {}".format(mc_day).title())

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    mc_time = str(df['start_hour'].mode().values[0])
    print("The most common start hour is: {}".format(mc_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mc_start_station = df['Start Station'].mode().values[0]
    print("The most common start station is: {}".format(mc_start_station))

    # TO DO: display most commonly used end station
    mc_end_station = df['End Station'].mode().values[0]
    print("The most common end station is: {}".format(mc_end_station))
    
    # TO DO: display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station']+ " " + df['End Station']
    mc_trip = df['trip'].mode().values[0]
    print("The most common start and end station combo is: {}".format(mc_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Trip Dutation'] = df['End Time'] - df['Start Time']
    total =  str(df['Trip Dutation'].sum())
    print("The total travel time is: {}".format(total))

    # TO DO: display mean travel time
    mean = str(df['Trip Dutation'].mean())
    print("The mean travel time is: {}".format(mean))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    c_type = df['User Type'].value_counts()
    print("The counts of user types:")
    print(c_type)

    # TO DO: Display counts of gender
    if 'Gender' not in df:
        print("No Gender data for the specified city")
    else:
        c_gender = df['Gender'].value_counts()
        print("The counts of user gender:")
        print(c_gender)
    
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print("No Birth Year data for the specified city")
    else:
        ealiest = str(int(df['Birth Year'].min()))
        recent = str(int(df['Birth Year'].max()))
        common = str(int(df['Birth Year'].mode().values[0]))       
        print("The earliest birth year is: {}".format(ealiest))
        print("The most recent birth year is: {}".format(recent))
        print("The most common birth year is: {}".format(common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    """
    Display raw data of the specified CSV file
    The default number of records is 5, but the user may change it
    """
    start = 0
    row_req = input("The default number of records is 5, do you want to change it (Y/N)?: ").lower()
    if row_req == 'y':
        row = int(input("Enter the number of records (integer): "))
    else:
        row = 5
    
    end = row

    while end <= df.shape[0] - 1:

        print(df.iloc[start:end,:])
        start += row 
        end += row

        exit_display = input("Do you want to exit (Y/N)?: ").lower()
        if exit_display == 'y':
            break

def main():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        user = input("Would you like to see the time statistics (Y/N)? ").lower()
        if(user == 'y'):
            time_stats(df)
        else:
            print('-'*40)
            
        user = input("Would you like to see the stations statistics (Y/N)? ").lower()
        if(user == 'y'):
            station_stats(df)
        else:
            print('-'*40)
            
        user = input("Would you like to see the trips statistics (Y/N)? ").lower()
        if(user == 'y'):
            trip_duration_stats(df)
        else:
            print('-'*40)
        
        user = input("Would you like to see the users statistics (Y/N)? ").lower()
        if(user == 'y'):
            user_stats(df)
        else:
            print('-'*40)
            
        user = input("Would you like to see the raw data (Y/N)? ").lower()
        if(user == 'y'):
            display_raw(df)
        else:
            print('-'*40)

        restart = input('\nWould you like to restart (Y/N)? ').lower()
        if restart.lower() != 'y':
            break
        else:
            print('Restarted!\n')


if __name__ == "__main__":
	main()
