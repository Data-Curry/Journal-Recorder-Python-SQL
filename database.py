import sqlite3
from typing import Tuple, List

Entry = Tuple[int, str, str, str, str]

CREATE_ENTRIES = """CREATE TABLE IF NOT EXISTS entries
(title TEXT, content TEXT, date TEXT, time TEXT);"""

INSERT_ENTRY = "INSERT INTO entries (title, content, date, time) VALUES (?, ?, ?, ?) RETURNING ROWID;"

SELECT_ALL_ENTRIES = "SELECT rowid, * FROM entries;"
SELECT_ENTRY = "SELECT * FROM entries WHERE rowid = ?;"
SELECT_ENTRIES_OF_DATE = "SELECT * FROM entries WHERE date = ?;"
SELECT_ENTRY_TITLES = "SELECT rowid, title FROM entries;"
SELECT_ENTRY_TITLES_OF_DATE = "SELECT rowid, title FROM entries WHERE date = ?;"


connection = sqlite3.connect("journal_data.db")


def create_table():
    with connection:
        connection.execute(CREATE_ENTRIES)


def add_entry(entry_title, entry_content, entry_date, entry_time):
    with connection:
        curse = connection.execute(INSERT_ENTRY, (entry_title, entry_content, entry_date, entry_time))
        entry_id = curse.fetchone()[0]
        print(f"Added entry with id {entry_id}")


def get_entries():
    with connection:
        curse = connection.execute(SELECT_ALL_ENTRIES)
        return curse.fetchall()


def get_entry(entry_id: int) -> List[Entry]:
    with connection:
        curse = connection.execute(SELECT_ENTRY, (entry_id,))
        return curse.fetchall()


def get_titles():
    with connection:
        curse = connection.execute(SELECT_ENTRY_TITLES)
        return curse.fetchall()


def get_entries_of_date(entry_date: str) -> List[Entry]:
    with connection:
        curse = connection.execute(SELECT_ENTRIES_OF_DATE, (entry_date,))
        return curse.fetchall()


def get_titles_of_date(entry_date: str) -> List[Entry]:
    with connection:
        curse = connection.execute(SELECT_ENTRY_TITLES_OF_DATE, (entry_date,))
        return curse.fetchall()