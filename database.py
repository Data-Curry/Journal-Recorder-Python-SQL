import sqlite3
from typing import Tuple, List

Entry = Tuple[str, str, str, str, str, str]

CREATE_CATEGORIES = """CREATE TABLE IF NOT EXISTS categories (id SERIAL PRIMARY KEY, name TEXT);"""
CREATE_ENTRIES = """CREATE TABLE IF NOT EXISTS entries
(id SERIAL PRIMARY KEY, title TEXT, content TEXT, date TEXT, time TEXT, category_id INTEGER, FOREIGN KEY(category_id) 
REFERENCES categories (rowid));"""

INSERT_CATEGORY = "INSERT INTO categories (name) VALUES (?) RETURNING ROWID;"
INSERT_ENTRY = "INSERT INTO entries (title, content, date, time, category_id) VALUES (?, ?, ?, ?, ?) RETURNING ROWID;"

SELECT_ALL_CATEGORIES = "SELECT rowid, * FROM categories;"
SELECT_ALL_ENTRIES = "SELECT rowid, * FROM entries;"

SELECT_CATEGORY = "SELECT rowid, * FROM categories WHERE rowid = ?;"
SELECT_ENTRY = "SELECT rowid, * FROM entries WHERE rowid = ?;"
SELECT_ENTRIES_OF_DATE = "SELECT rowid, * FROM entries WHERE date = ?;"
SELECT_A_CATEGORYS_ENTRIES_OF_DATE = "SELECT rowid, * FROM entries WHERE date = ? AND category_id = ?;"
SELECT_ENTRY_TITLES = "SELECT rowid, title FROM entries;"
SELECT_ENTRY_TITLES_OF_DATE = "SELECT rowid, title FROM entries WHERE date = ?;"
SELECT_A_CATEGORYS_TITLES_OF_DATE = "SELECT rowid, title FROM entries WHERE date = ? AND category_id = ?;"

SELECT_CATEGORY_TITLES = "SELECT rowid, title FROM entries WHERE category_id = ?;"
SELECT_CATEGORY_ENTRIES = "SELECT rowid, * FROM entries WHERE category_id = ?;"


connection = sqlite3.connect("journal_data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_CATEGORIES)
        connection.execute(CREATE_ENTRIES)


def add_category(category_name: str):
    with connection:
        cursor = connection.execute(INSERT_CATEGORY, (category_name,))
        category_id = cursor.fetchone()[0]
        print(f"Added category {category_name} with id {category_id}")


def add_entry(entry_title, entry_content, entry_date, entry_time, category_id):
    with connection:
        cursor = connection.execute(INSERT_ENTRY, (entry_title, entry_content, entry_date, entry_time, category_id))
        entry_id = cursor.fetchone()[0]
        print(f"Added entry {entry_title} with id {entry_id}")


def get_categories():
    with connection:
        cursor = connection.execute(SELECT_ALL_CATEGORIES)
        return cursor.fetchall()


def get_entries():
    with connection:
        cursor = connection.execute(SELECT_ALL_ENTRIES)
        return cursor.fetchall()


def get_category(category_id: str):
    with connection:
        cursor = connection.execute(SELECT_CATEGORY, (category_id,))
        return cursor.fetchall()


def get_entry(entry_id: str):
    with connection:
        cursor = connection.execute(SELECT_ENTRY, (entry_id,))
        return cursor.fetchall()


def get_titles():
    with connection:
        cursor = connection.execute(SELECT_ENTRY_TITLES)
        return cursor.fetchall()


def get_category_titles(category_id: str):
    with connection:
        cursor = connection.execute(SELECT_CATEGORY_TITLES, (category_id,))
        return cursor.fetchall()


def get_category_entries(category_id: str):
    with connection:
        cursor = connection.execute(SELECT_CATEGORY_ENTRIES, (category_id,))
        return cursor.fetchall()


def get_entries_of_date(entry_date: str) -> List[Entry]:
    with connection:
        cursor = connection.execute(SELECT_ENTRIES_OF_DATE, (entry_date,))
        return cursor.fetchall()


def get_titles_of_date(entry_date: str) -> List[Entry]:
    with connection:
        cursor = connection.execute(SELECT_ENTRY_TITLES_OF_DATE, (entry_date,))
        return cursor.fetchall()


def get_a_categorys_titles_of_date(category_id: str, entry_date: str) -> List[Entry]:
    with connection:
        cursor = connection.execute(SELECT_A_CATEGORYS_TITLES_OF_DATE, (entry_date, category_id))
        return cursor.fetchall()


def get_a_categorys_entries_of_date(category_id: str, entry_date: str) -> List[Entry]:
    with connection:
        cursor = connection.execute(SELECT_A_CATEGORYS_ENTRIES_OF_DATE, (entry_date, category_id))
        return cursor.fetchall()
