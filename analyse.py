from db import get_counter_data

def calculate_count(db, counter):
    """
    Calculate the count of the counter.

    :param db: an initialized sqlite3 database connection
    :param counter: name of the counter present in the db
    :return: length of the counter increment events
    """
    data = get_counter_data(db, counter)
    return len(data)
