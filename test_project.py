from counter import Counter
from db import get_db, add_counter, increment_counter, get_counter_data, get_periodicity, single_habit_cut_list, get_countername_list
from analyse import calculate_count, calculate_streak, calculate_longest_streak
import os

class TestCounter:

    def setup_method(self): # creates a test database, adds a habit names "test_counter" and increments events for that habit
        self.db = get_db("test.db")

        add_counter(self.db, "test_counter", "test_description", "test_periodicity")
        increment_counter(self.db, "test_counter", "2023-07-12")
        increment_counter(self.db, "test_counter", "2023-07-13")

        increment_counter(self.db, "test_counter", "2023-07-14")
        increment_counter(self.db, "test_counter", "2023-07-15")

    def test_counter(self): # creates an instance of the "Counter" class and simulates storing, incrementing, adding event, resetting and deleting
        counter = Counter("test_counter_1", "test_description_1", "test_periodicity_1")
        counter.store(self.db)

        counter.increment()
        counter.add_event(self.db)
        counter.reset()
        counter.increment()
        counter.delete_habit(self.db)

    def test_db_counter(self): # compares the database data with the condition defined in the assert method
        data = get_counter_data(self.db, "test_counter")
        assert len(data) == 4

        count = calculate_count(self.db, "test_counter")
        assert count == 4

    def test_streak(self): # Tests the functions used for the calculation of the streak
        periodicity = get_periodicity(self.db, "test_counter") # tests if the returned periodicity matches the periodicity of the habit "test_counter"
        assert periodicity == "test_periodicity"

        dates = single_habit_cut_list(self.db, "test_counter") # tests if the length of the returned list matches the amount of dates that were incremented
        assert len(dates) == 4

        streak = calculate_streak(self.db, "test_counter") # tests if the length of the returned list matches the expected length
        assert len(streak) == 3

        countername_list = get_countername_list(self.db) # tests if the length of the returned list matches the expected length
        assert len(countername_list) == 1

        longest_streak = calculate_longest_streak(self.db) # tests if the length of the returned list matches the expected length
        assert len(longest_streak) == 4

    def teardown_method(self): # closes the db and removes it from the system
        self.db.close()
        os.remove("test.db")


















