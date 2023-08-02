import sqlite3
from datetime import date, datetime

def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS counter (
        name TEXT PRIMARY KEY,
        description TEXT,
        periodicity TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        date TEXT,
        counterName TEXT,
        FOREIGN KEY (counterName) REFERENCES counter(name))""")

    db.commit()

def add_counter(db, name, description, periodicity):
    cur = db.cursor()
    cur.execute('INSERT INTO counter VALUES (?, ?, ?)', (name, description, periodicity))
    db.commit()

def increment_counter(db, name, event_date=None):
    cur = db.cursor()
    if not event_date:
        event_date = str(date.today())
    cur.execute('INSERT INTO tracker VALUES (?, ?)', (event_date, name))
    db.commit()

def get_counter_data(db, name):
    cur = db.cursor()
    cur.execute('SELECT * FROM tracker WHERE counterName=?', (name,))
    return cur.fetchall()

def get_periodicity(db, name):
    cur = db.cursor()
    cur.execute('SELECT periodicity FROM counter WHERE name=?', (name,))
    return cur.fetchall()[0][0]

def get_countername_list(db):
    cur = db.cursor()
    cur.execute('select name from counter')
    all_counters = cur.fetchall()
    counters_set = set()
    for counters in all_counters:
        counters_set.add(counters[0])
    return list(counters_set)

def get_counternameper_list(db, periodicity):
    cur = db.cursor()
    cur.execute('select name from counter WHERE periodicity=?', (periodicity,))
    all_periodicity = cur.fetchall()
    periodicity_set = set()
    for periodicity in all_periodicity:
        periodicity_set.add(periodicity[0])
    return list(periodicity_set)

def single_habit_cut_list(db, name):
    cur = db.cursor()
    cur.execute('select * from tracker WHERE counterName=?', (name,))
    all_dates = cur.fetchall()
    date_set = set()
    for date in all_dates:
        date_set.add(datetime.strptime(date[0], '%Y-%m-%d').date())
    return sorted(list(date_set))

def delete_habit(db, name):
    cur = db.cursor()
    cur.execute('DELETE from tracker WHERE counterName=?', (name,))
    cur.execute('DELETE from counter WHERE name=?', (name,))
    db.commit()