from database import create_table, add_entry, get_entries, get_entry, get_titles, get_entries_of_date, get_titles_of_date
import datetime

menu = """Please select one of the following options:
1) Add a new entry.
2) View all entry titles.
3) View all entry titles of a certain date.
4) View an entry by id.
5) View all entries of a certain date.
6) View all entries.
7) Exit.

Your selection: """
welcome = "Welcome to the journal recorder."


def prompt_new_entry():
    entry_title = input("What is the entry title? ")
    entry_content = input("What is the entry? ")
    entry_date = datetime.datetime.today().strftime("%Y-%m-%d")
    entry_time = datetime.datetime.today().strftime("%H:%M:%S")

    add_entry(entry_title, entry_content, entry_date, entry_time)


def view_entries(entries):
    for entry in entries:
        print(f"Entry #{entry[0]}\n{entry[3]} at {entry[4]}\n{entry[1]}\n{entry[2]}\n")


def view_entry(entry):
    putout = entry[0]
    print(f"Entry #{entry_id}\n{putout[2]} at {putout[3]}\n{putout[0]}\n{putout[1]}\n\n")


def view_entry_titles(entry_titles):
    for entry in entry_titles:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def prompt_search_date():
    entry_date = input("Enter the date you would like to search for (YYYY-MM-DD): ")
    entries_of_date = get_entries_of_date(entry_date)
    print(f"All entries of {entry_date}:")
    for entry in entries_of_date:
        # print(entry)
        print(f"{entry[3]}: {entry[0]}\n{entry[1]}")
    print("\n")


def prompt_search_titles_of_date():
    entry_date = input("Enter the date you would like to search for (YYYY-MM-DD): ")
    entries_of_date = get_titles_of_date(entry_date)
    print(f"All titles of {entry_date}:")
    for entry in entries_of_date:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


print(welcome)
create_table()

while (user_input := input(menu)) != "7":
    if user_input == "1":
        prompt_new_entry()
    elif user_input == "2":
        view_entry_titles(get_titles())
    elif user_input == "3":
        prompt_search_titles_of_date()
    elif user_input == "4":
        entry_id = int(input("Enter the entry id: "))
        try:
            view_entry(get_entry(entry_id))
        except:
            print("Entry not found.")
    elif user_input == "5":
        prompt_search_date()
    elif user_input == "6":
        view_entries(get_entries())
    else:
        print("Invalid input.  Please try again.")

