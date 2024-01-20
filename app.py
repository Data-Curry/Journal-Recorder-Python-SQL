from database import create_tables, add_entry, add_category, get_entries, get_entry, get_titles, get_entries_of_date, \
    get_titles_of_date, get_categories, get_category_titles, get_category, get_category_entries, \
    get_a_categorys_titles_of_date, get_a_categorys_entries_of_date
import datetime

menu = """Please select one of the following options:
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
13) Exit.

Your selection: """
welcome = "Welcome to the journal recorder."


def prompt_new_entry():                                                              # Adds a new entry to the database
    entry_category = input("What category is this entry for? Enter category id: ")
    entry_title = input("What is the entry title? ")
    entry_content = input("What is the entry? ")
    entry_date = datetime.datetime.today().strftime("%Y-%m-%d")
    entry_time = datetime.datetime.today().strftime("%H:%M:%S")

    add_entry(entry_title, entry_content, entry_date, entry_time, entry_category)


def prompt_new_category():                                                        # Adds a new category to the database
    category_name = input("What is the category name? ")
    add_category(category_name)


def view_categories():                                                            # Prints all categories and their ids
    received_list = get_categories()
    print("All categories:")
    for category_tuple in received_list:
        print(f"Category #{category_tuple[0]}: {category_tuple[2]}")
    print("\n")


def view_entries():                                                              # Prints all entries of all categories
    categories = get_categories()
    entries = get_entries()
    print("All entries...")
    for entry in entries:
        for i in range(len(categories)):
            if entry[6] == categories[i][0]:
                cat_name = categories[i][2]
                print(f"Entry #{entry[0]} {entry[4]} at {entry[5]} Category #{entry[6]}: {cat_name}\n"
                      f"Title: {entry[2]}\n{entry[3]}\n")


def view_entry(entry):                                                                          # Prints a single entry
    output = entry[0]  # extracts the tuple from the list
    print(f"Entry #{output[0]} of Category #{output[6]} | {output[4]} at {output[5]}\n"
          f"Title: {output[2]}\n{output[3]}\n")


def view_entry_titles():                                     # Prints all entry titles of all categories with their ids
    entry_titles = get_titles()
    print("All entry titles:")
    for entry in entry_titles:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def view_category_titles():                                      # Prints all entry titles of a category with their ids
    category_id = input("Enter the category id: ")
    category_name = get_category(category_id)[0][2]
    category_titles = get_category_titles(category_id)

    print(f"All titles of category {category_id}: {category_name}")
    for entry in category_titles:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def view_category_entries():                                          # Prints all entries of a category with their ids
    category_id = input("Enter the category id: ")
    category_name = get_category(category_id)[0][2]
    category_entries = get_category_entries(category_id)

    print(f"All entries of category {category_id}: {category_name}")
    for entry in category_entries:
        print(f"Entry #{entry[0]} {entry[4]} at {entry[5]}\nTitle: {entry[2]}\n{entry[3]}\n")
    print("\n")


def prompt_search_date():                              # Prints all entries of all categories entered on a certain date
    entry_date = input("Enter the date you would like to search for (YYYY-MM-DD): ")
    entries_of_date = get_entries_of_date(entry_date)
    print(f"All entries of {entry_date}:")
    for entry in entries_of_date:
        cat_name = get_category(entry[6])[0][2]
        print(f"{entry[5]} | entry #{entry[0]}: {entry[2]} | category #{entry[6]}: {cat_name}\n{entry[3]}")
    print("\n")


def prompt_search_titles_of_date():               # Prints all entry titles of all categories entered on a certain date
    entry_date = input("Enter the date you would like to search for (YYYY-MM-DD): ")
    entries_of_date = get_titles_of_date(entry_date)
    print(f"All titles of {entry_date}:")
    for entry in entries_of_date:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def prompt_search_a_categorys_titles_of_date():       # Prints all entry titles of a category entered on a certain date
    category_id = input("Enter the category id: ")
    entry_date = input("Enter the date you would like to search for (YYYY-MM-DD): ")
    cat_name = get_category(category_id)[0][2]
    entries_of_date = get_a_categorys_titles_of_date(category_id, entry_date)
    print(f"All titles of {entry_date} in category {category_id}: {cat_name}")
    for entry in entries_of_date:
        print(f"{entry[0]}: {entry[1]}")
    print("\n")


def prompt_search_a_categorys_entries_of_date():           # Prints all entries of a category entered on a certain date
    category_id = input("Enter the category id: ")
    entry_date = input("Enter the date you would like to search for (YYYY-MM-DD): ")
    cat_name = get_category(category_id)[0][2]
    entries_of_date = get_a_categorys_entries_of_date(category_id, entry_date)
    print(f"All entries of {entry_date} in category {category_id}: {cat_name}")
    for entry in entries_of_date:
        print(f"Entry #{entry[0]} {entry[4]} at {entry[5]}\nTitle: {entry[2]}\n{entry[3]}\n")
    print("\n")


print(welcome)
create_tables()

while (user_input := input(menu)) != "13":                                                         # The main menu loop
    if user_input == "1":
        prompt_new_entry()
    elif user_input == "2":
        prompt_new_category()
    elif user_input == "3":
        try:
            entry_id = input("Enter the entry id: ")
            view_entry(get_entry(entry_id))
        except:
            print("Entry not found.")
    elif user_input == "4":
        view_categories()
    elif user_input == "5":
        view_entry_titles()
    elif user_input == "6":
        view_entries()
    elif user_input == "7":
        view_category_titles()
    elif user_input == "8":
        view_category_entries()
    elif user_input == "9":
        prompt_search_titles_of_date()
    elif user_input == "10":
        prompt_search_date()
    elif user_input == "11":
        prompt_search_a_categorys_titles_of_date()
    elif user_input == "12":
        prompt_search_a_categorys_entries_of_date()
    else:
        print("Invalid input.  Please try again.")
