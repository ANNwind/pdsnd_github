import time
import pandas as pd
from datetime import timedelta

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Would you like to see data for Chicago, New York City or Washington?: ").lower()
        if not city in ['chicago', 'washington', 'new york city']:
            print("\nYou've input '{}'. Please select one of the following cities? : "
                  "Chicago, New York City or Washington.\n Check your spelling and try again :-)\n".format(city))
        elif city == 'washington':
            wash_dc = input("\nThere is no gender and birth year data available for Washington, "
                           "would you like to continue? Enter yes or no.\n")
            if wash_dc.lower() != 'no':
                break
            continue
        else:
            break

    # get user input for month (all, january, february, till june)
    while True:
        month = input("\nFor which month do you want to see data? Choose a month from january to june: ").lower()
        if not month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print("\nAre you sure you've selected a month from january to june? You've input {} "
                  "\nPlease check your spelling and try again :-)\n".format(month))
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nFor which day of the week would you like to see data?: ").lower()
        if not day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print("Are you sure you've input the day of the week correctly? You've input {}"
                  "\nPlease check your spelling and try again :-)\n".format(day))
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def raw_data_chunker(iterable, size):
    """
    Args:
        iterable: any iterable object
        size: how large the chunk of the iterable should be

    Returns: Chunked iterable and asks user if they want a new chunk
    """""
    for i in range(0, len(iterable), size):
        print(iterable[i:i + size])
        more_raw_data = input("Would you like to see more raw data? Enter yes or no.\n")
        if more_raw_data.lower() != 'yes':
            break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("Most popular month for traveling is {}".format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("Most popular day for traveling is {}".format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most popular hour for traveling is {}".format(popular_hour))

    has_passed = False
    while True:
        if not has_passed:
            more_data = input("Would you like to see raw time data? Enter yes or no.\n")
        else:
            break
        if more_data.lower() != 'no':
            has_passed = True
            raw_data_chunker(df[['Start Time', 'End Time', 'hour']], 5)
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most popular starting station is {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most popular ending station is {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Start to End Stations'] = df['Start Station'] + ' ' + '--' + ' ' + df['End Station']
    popular_start_to_end = df['Start to End Stations'].mode()[0]
    print("Most popular start to end stations are {}".format(popular_start_to_end))

    has_passed = False
    while True:
        if not has_passed:
            more_data = input("Would you like to see raw station data? Enter yes or no.\n")
        else:
            break
        if more_data.lower() != 'no':
            has_passed = True
            raw_data_chunker(df[['Start Station', 'End Station']], 5)
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = '{:0>8}'.format(str(timedelta(seconds=float(df['Trip Duration'].sum()))))
    print("The total travel time is {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = '{:0>8}'.format(str(timedelta(seconds=float(df['Trip Duration'].mean()))))
    print("The mean travel time is {}".format(mean_travel_time))

    has_passed = False
    while True:
        if not has_passed:
            more_data = input("Would you like to see raw trip duration raw data? Enter yes or no.\n")
        else:
            break
        if more_data.lower() != 'no':
            has_passed = True
            raw_data_chunker(df[['Trip Duration']], 5)
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # First, fill empty values with the most common user type
    df['User Type'] = df['User Type'].fillna(df['User Type'].mode()[0])
    user_type_counts = df['User Type'].value_counts()
    print("The distribution of user types is: \n{}\n".format(user_type_counts))

    # Display counts of gender
    if 'Gender' in df.columns:
        # Fill empty values with the most common values
        df['Gender'] = df['Gender'].fillna(df['Gender'].mode()[0])
        # get the user counts
        user_gender_count = df['Gender'].value_counts()
        print("The distribution of gender is \n{}\n".format(user_gender_count))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        # fill empty values with the mean birth year
        df['Birth Year'] = df['Birth Year'].fillna(df['Birth Year'].mean())

        oldest_user = int(df['Birth Year'].min())
        print("The oldest user was born in {}".format(oldest_user))
        youngest_user = int(df['Birth Year'].max())
        print("The youngest user was born in {}".format(youngest_user))
        common_age = int(df['Birth Year'].mode()[0])
        print("The most common birth year is {}".format(common_age))

    has_passed = False
    while True:
        if not has_passed:
            more_data = input("Would you like to see raw user statistics data? Enter yes or no.\n")
        else:
            break
        if more_data.lower() != 'no':
            has_passed = True
            raw_data_chunker(df[['User Type', 'Birth Year']], 5)
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


print('Hello! Let\'s explore some US bikeshare data!')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
