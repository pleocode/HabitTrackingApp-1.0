import questionary
from db import get_db, get_countername_list
from counter import Counter
from analyse import calculate_count

def cli():
    db = get_db()

    while True:
        if questionary.confirm("Are you ready to start?").ask() == True:
            break

    stop = False

    while not stop:
        choice = questionary.select("What do you want to do?", choices=["Create", "Increment", "Analyse", "Exit"]).ask()



        if choice == "Create":
            name = questionary.text("What is the name of your counter?").ask()
            desc = questionary.text("What is the description of your counter?").ask()
            counter = Counter(name, desc)
            counter.store(db)

        elif choice == "Increment":
            name = questionary.select("What counter do you want to increment?", choices=get_countername_list(db)).ask()
            counter = Counter(name, "no description")
            counter.increment()
            counter.add_event(db)

        elif choice == "Analyse":
            name = questionary.select("What counter do you want to analyze?", choices=get_countername_list(db)).ask()
            count = calculate_count(db, name)
            print(f"{name} has been incremented {count} times")

        else:
            print("The program has been closed!")
            stop = True

if __name__ == "__main__":
    cli()