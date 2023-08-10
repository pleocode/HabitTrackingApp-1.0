from db import add_counter, increment_counter, delete_counter

class Counter:

    def __init__(self, name: str, description: str, periodicity: str): # creates the initializer
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def __str__(self):
        return f"{self.name}: {self.count}"

    def store(self, db): # Stores the data of our class in our "counter" DB when creating a new habit
        add_counter(db, self.name, self.description, self.periodicity)

    def add_event(self, db, date: str = None): # Stores the data in our "tracker" DB when incrementing a habit
        increment_counter(db, self.name, date)

    def delete_habit(self, db): # Deletes data from our "tracker" and "counter" DB when deleting a habit
        delete_counter(db, self.name)

