from db import get_counter_data, single_habit_cut_list, get_periodicity, get_countername_list
import pandas as pd
from datetime import timedelta

def calculate_count(db, counter):
    """
    Calculate the count of the counter.

    :param db: an initialized sqlite3 database connection
    :param counter: name of the counter present in the db
    :return: length of the counter increment events
    """
    data = get_counter_data(db, counter)
    return len(data)

def calculate_streak(db, name):
    periodicity = get_periodicity(db, name)
    date_list = single_habit_cut_list(db, name) # Convert the list of dates to datetime.date objects
    df = pd.DataFrame({'date': date_list}) # Create a DataFrame with the date objects

    if periodicity == "Daily":  # For Daily periodicity
        df["diff"] = df["date"].diff()  # Calculate the difference between consecutive dates
        streaks = (df["diff"] != timedelta(days=1)).cumsum()  # Identify streaks by grouping consecutive dates with the same difference (timedelta)
        streak_counts = df.groupby(streaks)["date"].agg(["count", "min", "max"])  # Group the DataFrame by streaks and count the number of consecutive dates in each streak

    else:
        df["date"] = pd.to_datetime(df["date"])  # Convert 'date' column to pandas datetime
        df["week_number"] = df["date"].dt.isocalendar().week  # Extract week number and add it to a new column 'week_number'
        df["streaks"] = (df["week_number"].diff() > 1).cumsum() # Identify streaks by grouping consecutive weeks number
        streaks = df["streaks"].fillna(0).astype(int) # Fill any streaks at the beginning with 0
        streak_counts = df.groupby(streaks)["date"].agg(["count", "min", "max"])  # Group the DataFrame by streaks and count the number of consecutive dates in each streak

    index_of_longest_streak = streak_counts["count"].idxmax()  # Find the index of the row with the maximum count (longest streak)
    longest_streak = streak_counts.loc[index_of_longest_streak]  # Get the first line (longest streak) using the index
    streak_list = [longest_streak["count"], str(longest_streak["min"].strftime("%Y-%m-%d")),str(longest_streak["max"].strftime("%Y-%m-%d"))]
    return streak_list

def calculate_longest_streak(db):
    longest_streak = [0]
    for name in get_countername_list(db): # Loops each habit
        try:
            if calculate_streak(db, name)[0] > longest_streak[0]: # Replaces longest_streak if the habit has a bigger streak than the habit before
                longest_streak = calculate_streak(db, name)
                longest_streak.append(name) # Adds the name of the habit to the list
            else:
                continue
        except:
            pass

    return longest_streak








