import os
import psycopg2
from dotenv import load_dotenv
import datetime

import database

DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "
MENU_PROMPT = """Please select one of the following options:
1) Add an entry.
2) Add a category.
3) View an entry by id.
4) View all categories.
5) View all titles.
6) View all entries.

   ** Viewing by category **
7) View a category's titles.
8) View a category's entries.

    ** Viewing by date **
9) View all titles of a certain date.
10) View all entries of a certain date
11) View a category's titles of a certain date.
12) View a category's entries of a certain date.

    ** Viewing by percentage **
13) View category entries as a percentage of the total.
14) Exit.

Enter your selection: """
welcome = "Welcome to the journal recorder."


def prompt_new_entry(connection):
    # Adds a new entry to the database
    check_for_categories = database.get_categories(connection)
    if not check_for_categories:
        print("No categories have been created yet. You must create an entry category first.\n")
        return
    entry_category = input("What category is this entry for? Enter category id: ")
    entry_title = input("What is the entry title? ")
    entry_content = input("What is the entry? ")
    entry_date = datetime.datetime.today().strftime("%Y-%m-%d")
    entry_time = datetime.datetime.today().strftime("%H:%M:%S")

    database.add_entry(connection, entry_title, entry_content, entry_date, entry_time, entry_category)
    print("\n")


def prompt_new_category(connection):
    # Adds a new category to the database
    category_name = input("What is the category name? ")
    database.add_category(connection, category_name)
    print("\n")


def view_categories(connection):
    # Prints all categories and their ids
    received_list = database.get_categories(connection)
    if not received_list:
        print("No categories have been created yet.\n")
        return
    print("All categories:")
    for category_tuple in received_list:
        print(f"Category #{category_tuple[0]}: {category_tuple[2]}")
    print("\n")


def view_entries(connection):
    # Prints all entries of all categories
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    entries = database.get_entries(connection)
    if not entries:
        print("No entries have been recorded yet.\n")
        return
    print("All entries...")
    for entry in entries:
        for i in range(len(categories)):
            if entry[6] == categories[i][0]:
                cat_name = categories[i][2]
                print(f"Entry #{entry[0]} {entry[4]} at {entry[5]} Category #{entry[6]}: {cat_name}\n"
                      f"Title: {entry[2]}\n{entry[3]}\n")


def view_entry(connection):
    # Prints a single entry
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    entry_id = input("Enter the entry id: ")
    entry = database.get_entry(connection, entry_id)
    if not entry:
        print(f"No entry with id {entry_id} exists.\n")
        return
    output = entry[0]  # extracts the tuple from the returned list
    print(f"Entry #{output[0]} of Category #{output[6]} | {output[4]} at {output[5]}\n"
          f"Title: {output[2]}\n{output[3]}\n")


def view_entry_titles(connection):
    # Prints all entry titles of all categories with their ids
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    entry_titles = database.get_titles(connection)
    if not entry_titles:
        print("No entries have been recorded yet.\n")
        return
    print("All entry titles:")
    for entry in entry_titles:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def view_category_titles(connection):
    # Prints all entry titles of a category with their ids
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    category_id = input("Enter the category id: ")
    try:
        category_name = database.get_category(connection, category_id)[0][2]
    except IndexError:
        print(f"No category with id {category_id} exists.\n")
        return
    if not category_name:
        print(f"No category with id {category_id} exists.\n")
        return
    category_titles = database.get_category_titles(connection, category_id)
    if not category_titles:
        print(f"No entries have been recorded for category {category_id} yet.\n")
        return
    print(f"All titles of category {category_id}: {category_name}")
    for entry in category_titles:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def view_category_entries(connection):
    # Prints all entries of a category
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    category_id = input("Enter the category id: ")
    try:
        category_name = database.get_category(connection, category_id)[0][2]
    except IndexError:
        print(f"No category with id {category_id} exists.\n")
        return
    if not category_name:
        print(f"No category with id {category_id} exists.\n")
        return
    category_entries = database.get_category_entries(connection, category_id)
    if not category_entries:
        print(f"No entries have been recorded for category {category_id} yet.\n")
        return
    print(f"All entries of category {category_id}: {category_name}")
    for entry in category_entries:
        print(f"Entry #{entry[0]} {entry[4]} at {entry[5]}\nTitle: {entry[2]}\n{entry[3]}\n")
    print("\n")


def prompt_view_titles_of_date(connection):
    # Prints all entry titles of all categories entered on a certain date
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    entry_date = input("Enter the date you would like to see all titles for (YYYY-MM-DD): ")
    entries_of_date = database.get_titles_of_date(connection, entry_date)
    if not entries_of_date:
        print(f"No entries have been recorded for {entry_date} yet.\nMake sure that you entered the date correctly.\n")
        return
    print(f"All titles of {entry_date}:")
    for entry in entries_of_date:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def prompt_view_date(connection):
    # Prints all entries of all categories entered on a certain date
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    entry_date = input("Enter the date you would like to see all entries for (YYYY-MM-DD): ")
    entries_of_date = database.get_entries_of_date(connection, entry_date)
    if not entries_of_date:
        print(f"No entries have been recorded for {entry_date} yet.\nMake sure you entered the date correctly.")
        return
    print(f"All entries of {entry_date}:")
    for entry in entries_of_date:
        cat_name = database.get_category(connection, entry[6])[0][2]
        print(f"{entry[5]} | entry #{entry[0]}: {entry[2]} | category #{entry[6]}: {cat_name}\n{entry[3]}")
    print("\n")


def prompt_view_a_categorys_titles_of_date(connection):
    # Prints all entry titles of a category entered on a certain date
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    category_id = input("Enter the category id: ")
    entry_date = input(f"Enter the date you would like to see category #{category_id} titles for (YYYY-MM-DD): ")
    try:
        cat_name = database.get_category(connection, category_id)[0][2]
    except IndexError:
        print(f"No category with id {category_id} exists.\n")
        return
    if not cat_name:
        print(f"No category with id {category_id} exists.\n")
        return
    entries_of_date = database.get_a_categorys_titles_of_date(connection, category_id, entry_date)
    if not entries_of_date:
        print(f"No entries have been recorded for category {category_id} on {entry_date} yet.\n"
              f"Make sure you entered the date correctly.\n")
        return
    print(f"All titles of {entry_date} in category {category_id}: {cat_name}")
    for entry in entries_of_date:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def prompt_view_a_categorys_entries_of_date(connection):
    # Prints all entries of a category entered on a certain date
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    category_id = input("Enter the category id: ")
    entry_date = input(f"Enter the date you would like to see category #{category_id} entries for (YYYY-MM-DD): ")
    try:
        cat_name = database.get_category(connection, category_id)[0][2]
    except IndexError:
        print(f"No category with id {category_id} exists.\n")
        return
    if not cat_name:
        print(f"No category with id {category_id} exists.\n")
        return
    entries_of_date = database.get_a_categorys_entries_of_date(connection, category_id, entry_date)
    if not entries_of_date:
        print(f"No entries have been recorded for category {category_id} on {entry_date} yet.\n"
              f"Make sure you entered the date correctly.\n")
        return
    print(f"All entries of {entry_date} in category {category_id}: {cat_name}")
    for entry in entries_of_date:
        print(f"Entry #{entry[0]} {entry[4]} at {entry[5]}\nTitle: {entry[2]}\n{entry[3]}\n")
    print("\n")


def prompt_view_category_entries_as_percentage(connection):
    # Prints the number of entries in a category as a percentage of the total number of entries
    categories = database.get_categories(connection)
    if not categories:
        print("No categories have been created yet, therefore no entries can be recorded.\nAdd a category first.\n")
        return
    entries_as_percentage = database.get_categorys_entries_as_percentage_of_all(connection)
    if not entries_as_percentage:
        print("No entries have been recorded yet.")
    else:
        print("All categories ranked by number of entries:")
        for item in entries_as_percentage:
            cat_name = database.get_category(connection, item[0])[0][2]
            print(f"{round(item[3], 2)}% | Category#{item[0]}: {cat_name} ({item[1]} entries)")
    print("\n")


MENU_OPTIONS = {
    "1": prompt_new_entry,
    "2": prompt_new_category,
    "3": view_entry,
    "4": view_categories,
    "5": view_entry_titles,
    "6": view_entries,
    "7": view_category_titles,
    "8": view_category_entries,
    "9": prompt_view_titles_of_date,
    "10": prompt_view_date,
    "11": prompt_view_a_categorys_titles_of_date,
    "12": prompt_view_a_categorys_entries_of_date,
    "13": prompt_view_category_entries_as_percentage
}


def menu():
    database_uri = input(DATABASE_PROMPT)
    if not database_uri:
        load_dotenv()
        database_uri = os.environ["DATABASE_URI"]

    connection = psycopg2.connect(database_uri)
    database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "14":
        try:
            MENU_OPTIONS[selection](connection)
        except KeyError:
            print("Invalid input. Please try again.")


print(welcome)
menu()
