import sqlite3
import questionary
from db import get_db, get_countername_list, get_counternameper_list, delete_habit
from counter import Counter
from analyse import calculate_count, calculate_streak, calculate_longest_streak

def cli():
    db = get_db()

    while True:
        if questionary.confirm("Are you ready to start?").ask() == True:
            break

    stop = False
    while not stop:
        choice = questionary.select("What do you want to do?", choices=["Create", "Increment", "Analyse", "Delete Habit","Exit"]).ask()

        if choice == "Create":

            try: # In case of creating a habit that already exists
                name = questionary.text("What is the name of your counter?").ask().lower()
                desc = questionary.text("What is the description of your counter?").ask().lower()
                per = questionary.select("What is the periodicity of you habit?", choices=["Daily", "Weekly"]).ask()
                counter = Counter(name, desc, per)
                counter.store(db)
            except sqlite3.IntegrityError: # Handling error when user creates a habit that already exists
                print("This habit already exists")

        elif choice == "Increment":

            try:  # In case of trying to increment on habit with an empty db
                name = questionary.select("What counter do you want to increment?", choices=get_countername_list(db)).ask()
                counter = Counter(name, "no description", "no periodicity")
                counter.increment()
                counter.add_event(db)
            except ValueError: # Handling error when user tries to increment on a habit with an empty db
                print("There isn't any habit created yet to increment")

        elif choice == "Analyse":

            name = questionary.select("Do you want to analyze by habit, periodicity or check the longest streak?", choices=["Habit", "Periodicity", "Longest Streak"]).ask()
            if name == "Longest Streak": # In case of selecting longest streak

                try: # In case the db is empty or there is no streak yet
                    longest_streak_name = calculate_longest_streak(db)[3]
                    longest_streak_counter = calculate_longest_streak(db)[0]
                    print(f"The longest streak from all the habits is: \"{longest_streak_name}\" - {longest_streak_counter} streaks")
                except (IndexError): # Handling error when the db is empty or or there is no streak yet
                    print("The db is empty or or there is no streak yet")

            else:  # In case of selecting habit or periodicity

                if name == "Habit": # In case of selecting directly from a habit

                    try:  # In case of trying to analyze on habit with an empty db or the habit has been incremented 0 times
                        name = questionary.select("What habit do you want to analyze?", choices=get_countername_list(db)).ask()
                        count = calculate_count(db, name)
                        streak = calculate_streak(db, name)[0]
                        start_date = calculate_streak(db, name)[1]
                        end_date = calculate_streak(db, name)[2]
                        print(f"{name} has been incremented {count} times")
                        print(f"The longest streak for the habit \"{name}\" is {streak}, starting at {start_date} and ending at {end_date}")
                    except (ValueError, UnboundLocalError):  # Handling error when user tries to analyze on a habit with an empty db or the habit has been incremented 0 times
                        print("There isn't any habit created yet to analyze or this habit has been incremented 0 times")

                elif name == "Periodicity": # in case of selecting from the periodicity of a habit the habit has been incremented 0 times
                    name = questionary.select("Which periodicity do you want to analyze from?", choices=["Daily", "Weekly"]).ask()

                    try: # In case the user selects a periodicity where there is still no habit created or

                        if name == "Daily": # For daily periodicity
                            name = questionary.select("What habit do you want to analyze?", choices=get_counternameper_list(db, "Daily")).ask()
                            count = calculate_count(db, name)

                        else: # For weekly periodicity
                            name = questionary.select("What habit do you want to analyze?", choices=get_counternameper_list(db, "Weekly")).ask()
                            count = calculate_count(db, name)

                        streak = calculate_streak(db, name)[0]
                        start_date = calculate_streak(db, name)[1]
                        end_date = calculate_streak(db, name)[2]
                        print(f"{name} has been incremented {count} times")
                        print(f"The longest streak for the habit \"{name}\" is {streak}, starting at {start_date} and ending at {end_date}")

                    except (ValueError, UnboundLocalError): # Handling error when user selects a periodicity where there is still no habit
                        print("You still don't have any habit created for this periodicity or this habit has been incremented 0 times")

        elif choice == "Delete Habit":

            try:  # In case of trying to delete a habit with an empty db
                name = questionary.select("What habit do you want to analyze?", choices=get_countername_list(db)).ask()
                delete_habit(db, name)
                print(f"The habit \"{name}\" has been deleted")
            except ValueError:  # Handling error when user tries to delete a habit with an empty db
                print("There isn't any habit to delete")

        else:

            print("The program has been closed!")
            stop = True

if __name__ == "__main__":
    cli()