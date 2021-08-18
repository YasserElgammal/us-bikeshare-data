import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # lets get input from user...
    while True:
        
        # get user input for city (chicago, new york city, washington)
        city = input("Enter city name [chicago, new york city, washington] : \n ").lower()

        if city not in CITY_DATA.keys():
            print("Unfortunately, this city not in the list, \n Please try again with [chicago, new york city, washington]")
            continue
        else:
            break

    while True:
        # get user input for month ['January', 'February', 'March', 'April', 'May', 'June', 'all']
        month = input("Please enter which month you want from [January, February, March, April, May, June] or enter all to display all Months \n ").lower()

        if month != 'all' and month not in months:
            print("Unfortunately, this month not in the list, \n Please try again with [January, February, March, April, May, June, all]")
            continue
        else:
            break
    
    while True:
        # get user input for day ['January', 'February', 'March', 'April', 'May', 'June', 'all']
        day = input("Please enter which day you want from [Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, all] \n ").lower()

        if day != 'all' and day not in days:
            print("Unfortunately, this day not in the list, \n Please try again with [Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday] or or enter all to display all months")
            continue
        else:
            break

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
    # Lets Load data
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter days
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of week'] == day.title()]

    # Extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    
    # print(city, month, day)

    return df

def show_raw_data(df):
    """Show rows of data according to user."""
    start = 0
    user_answer = input("Do you like to display the first 5 rows of the data? yes / no: \n").lower()
    # pd.set_option('display.max_columns', None) # None to display max rows

    while True:
        if user_answer == 'no':
            break
        print(df[start:start+5])
        user_answer = input("Do you like to display the first 5 rows of the data? yes / no: \n").lower()
        start += 5

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    print("Most Common Month:", month_from_number(common_month))

    # display the most common day of week
    common_day = df['Day of week'].mode()[0]
    print("Most Common Day:", common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most Common Start Hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station:", common_start_station)

    # display most commonly used end station4
    common_end_station = df['End Station'].mode()[0]
    print("Most Common End Station:", common_end_station)


    # display most frequent combination of start station and end station trip
    most_start_end = (df['Start Station'] + ' | ' + df['End Station']).mode()[0]
    print('Most frequent combination of start station and end station trip', most_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', round(total_travel_time/3600, 3) , ' Hours')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', round(mean_travel_time/3600, 3), ' Hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of gender
    if 'Gender' in df:
        print('Gender Count:', df['Gender'].value_counts())

    # Display counts of user types
    print("User Types Count:", df['User Type'].value_counts())
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        print('Earliest Birth Year:', earliest_birth_year) 
        recent_birth_year = int(df['Birth Year'].max())
        print('Most Recent Birth Year:', recent_birth_year)
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('Earliest Birth Year:', common_birth_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def month_from_number(month):
    """
    Convert number to month
    """
    month = months[month-1]
    return month.title()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
