from counter import Counter
from db import get_db, add_counter, increment_counter, get_counter_data
from analyse import calculate_count

class TestCounter:

    def setup_method(self):
        self.db = get_db("test.db")

        add_counter(self.db, "test_counter", "test_description")
        increment_counter(self.db, "test_counter", "2023-07-18")
        increment_counter(self.db, "test_counter", "2023-07-19")

        increment_counter(self.db, "test_counter", "2023-07-21")
        increment_counter(self.db, "test_counter", "2023-07-22")


    def test_counter(self):
        counter = Counter("test_counter_1", "test_description_1")
        counter.store(self.db)

        counter.increment()
        counter.add_event(self.db)
        counter.reset()
        counter.increment()

    def test_db_counter(self):
        data = get_counter_data(self.db, "test_counter")
        assert len(data) == 4

        count = calculate_count(self.db, "test_counter")
        assert count == 4

    def teardown_method(self):
        import os
        os.remove("test.db")