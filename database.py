from typing import Tuple, List

Entry = Tuple[str, str, str, str, str, str]

CREATE_CATEGORIES = """CREATE TABLE IF NOT EXISTS categories (id SERIAL PRIMARY KEY, name TEXT);"""
CREATE_ENTRIES = """CREATE TABLE IF NOT EXISTS entries
(id SERIAL PRIMARY KEY, title TEXT, content TEXT, date TEXT, time TEXT, category_id INTEGER, FOREIGN KEY(category_id) 
REFERENCES categories (id));"""

INSERT_CATEGORY = "INSERT INTO categories (name) VALUES (%s) RETURNING id;"
INSERT_ENTRY = "INSERT INTO entries (title, content, date, time, category_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;"

SELECT_ALL_CATEGORIES = "SELECT id, * FROM categories;"
SELECT_ALL_ENTRIES = "SELECT id, * FROM entries;"

SELECT_CATEGORY = "SELECT id, * FROM categories WHERE id = %s;"
SELECT_ENTRY = "SELECT id, * FROM entries WHERE id = %s;"
SELECT_ENTRIES_OF_DATE = "SELECT id, * FROM entries WHERE date = %s;"
SELECT_A_CATEGORYS_ENTRIES_OF_DATE = "SELECT id, * FROM entries WHERE date = %s AND category_id = %s;"
SELECT_ENTRY_TITLES = "SELECT id, title, category_id FROM entries;"
SELECT_ENTRY_TITLES_OF_DATE = "SELECT id, title, category_id FROM entries WHERE date = %s;"
SELECT_A_CATEGORYS_TITLES_OF_DATE = "SELECT id, title FROM entries WHERE date = %s AND category_id = %s;"

SELECT_CATEGORY_TITLES = "SELECT id, title FROM entries WHERE category_id = %s;"
SELECT_CATEGORY_ENTRIES = "SELECT id, * FROM entries WHERE category_id = %s;"

SELECT_CATEGORY_ENTRIES_AS_PERCENTAGE = "SELECT category_id, " \
                                        "COUNT(category_id) AS entry_count, " \
                                        "RANK() OVER(ORDER BY COUNT(category_id) DESC), " \
                                        "COUNT(category_id) / SUM(COUNT(category_id)) OVER() * 100.0 AS percentage " \
                                        "FROM entries " \
                                        "GROUP BY category_id;"


def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CATEGORIES)
            cursor.execute(CREATE_ENTRIES)


def add_category(connection, category_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CATEGORY, (category_name,))
            category_id = cursor.fetchone()[0]
            return category_id


def add_entry(connection, entry_title, entry_content, entry_date, entry_time, category_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_ENTRY, (entry_title, entry_content, entry_date, entry_time, category_id))
            entry_id = cursor.fetchone()[0]
            return entry_id


def get_categories(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_CATEGORIES)
            return cursor.fetchall()


def get_entries(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_ENTRIES)
            return cursor.fetchall()


def get_category(connection, category_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CATEGORY, (category_id,))
            return cursor.fetchall()


def get_entry(connection, entry_id):
    entry_id_as_string = str(entry_id)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ENTRY, (entry_id_as_string,))
            return cursor.fetchall()


def get_titles(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ENTRY_TITLES)
            return cursor.fetchall()


def get_category_titles(connection, category_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CATEGORY_TITLES, (category_id,))
            return cursor.fetchall()


def get_category_entries(connection, category_id):
    category_id_as_string = str(category_id)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CATEGORY_ENTRIES, (category_id_as_string,))
            return cursor.fetchall()


def get_entries_of_date(connection, entry_date) -> List[Entry]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ENTRIES_OF_DATE, (entry_date,))
            return cursor.fetchall()


def get_titles_of_date(connection, entry_date) -> List[Entry]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ENTRY_TITLES_OF_DATE, (entry_date,))
            return cursor.fetchall()


def get_a_categorys_titles_of_date(connection, category_id, entry_date) -> List[Entry]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_A_CATEGORYS_TITLES_OF_DATE, (entry_date, category_id))
            return cursor.fetchall()


def get_a_categorys_entries_of_date(connection, category_id, entry_date) -> List[Entry]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_A_CATEGORYS_ENTRIES_OF_DATE, (entry_date, category_id))
            return cursor.fetchall()


def get_categorys_entries_as_percentage_of_all(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CATEGORY_ENTRIES_AS_PERCENTAGE)
            return cursor.fetchall()
