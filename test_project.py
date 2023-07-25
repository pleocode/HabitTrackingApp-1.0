from counter import Counter
from db import get_db, add_counter, increment_counter, get_counter_data
from analyse import calculate_count
import os

class TestCounter:

    def setup_method(self):
        self.db = get_db("test.db")

        add_counter(self.db, "teste_counter", "test_description")
        increment_counter(self.db, "test_counter", "2023-07-12")
        increment_counter(self.db, "test_counter", "2023-07-13")

        increment_counter(self.db, "test_counter", "2023-07-14")
        increment_counter(self.db, "test_counter", "2023-07-15")

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
        self.db.close()
        os.remove("test.db")
