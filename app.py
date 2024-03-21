import os
import psycopg2
from dotenv import load_dotenv
import datetime
import database

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font

import matplotlib.pyplot as plt

from scrollable_window import ViewTitlesDisplayWindow, ViewEntriesDisplayWindow, ViewACategorysTitlesDisplayWindow, \
    ViewCategoryEntriesDisplayWindow, ViewTitlesOfADateDisplayWindow, ViewEntriesOfADateDisplayWindow, \
    ViewACategorysTitlesOfADateDisplayWindow, ViewACategorysEntriesOfADateDisplayWindow, \
    ViewCategoryEntriesAsPercentageDisplayWindow, ScrollingColorKeyDisplayWindow

entry = ()
entries_preview = ()
entries_full_text = ()
categories = ()
titles = ()
category_titles = ()
category_entries_preview = ()
category_entries_full_text = ()
titles_of_date = ()
entries_of_date_preview = ()
entries_of_date_full_text = ()
category_titles_of_date = ()
category_entries_of_date_preview = ()
category_entries_of_date_full_text = ()
category_entries_as_percentage = []  # 0: category_number, 1: category_name, 2: category_entries, 3: percentage
colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "cyan", "magenta", "maroon",
          "green2", "turquoise", "sky blue", "gold", "coral", "magenta", "gray", "PeachPuff4"]  # 19 colors

load_dotenv()
DATABASE_URI = os.environ.get("DATABASE_URI")
connection = psycopg2.connect(DATABASE_URI)


class JournalRecorder(tk.Tk):
    global connection

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        load_dotenv()
        database.create_tables(connection)

        self.title("Journal Recorder")
        self.frames = dict()

        container = ttk.Frame(self)
        container.grid(padx=60, pady=30, sticky="EW")

        for FrameClass in (MainMenu, AddEntry, AddCategory, ViewEntry, ViewCategories, ViewTitles, ViewEntriesPreview,
                           ViewEntriesFullText, ViewCategoryTitles, ViewCategoryEntriesPreview,
                           ViewCategoryEntriesFullText, ViewTitlesOfDate, ViewEntriesOfDatePreview,
                           ViewEntriesOfDateFullText, ViewCategoryTitlesOfDate, ViewCategoryEntriesOfDatePreview,
                           ViewCategoryEntriesOfDateFullText, ViewCategoryEntriesAsPercentage, ViewPieChart, DeleteSomething):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(MainMenu)

    def show_frame(self, container):       # switches view from current frame to frame passed in container
        frame = self.frames[container]
        frame.tkraise()                    # puts this frame on top of the stack of frames


class MainMenu(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.add_entry_button = ttk.Button(
            self,
            text="Add New Entry",
            command=lambda: controller.show_frame(AddEntry)
        )  # switches to AddEntry class frame

        self.add_category_button = ttk.Button(
            self,
            text="Add New Category",
            command=lambda: controller.show_frame(AddCategory)
        )  # switches to AddCategory class frame

        self.view_entry_button = ttk.Button(
            self,
            text="View Entry by ID",
            command=lambda: controller.show_frame(ViewEntry)
        )  # switches to ViewEntry class frame

        self.view_categories_button = ttk.Button(
            self,
            text="View All Categories",
            command=lambda: controller.show_frame(ViewCategories)
        )  # switches to ViewCategories class frame

        self.view_titles_button = ttk.Button(
            self,
            text="View All Titles",
            command=lambda: controller.show_frame(ViewTitles)
        )  # switches to ViewTitles class frame

        self.view_entries_button = ttk.Button(
            self,
            text="View All Entries",
            command=lambda: controller.show_frame(ViewEntriesPreview)
        )  # switches to ViewEntries class frame

        self.view_category_titles_button = ttk.Button(
            self,
            text="View a Category's Titles",
            command=lambda: controller.show_frame(ViewCategoryTitles)
        )  # switches to ViewCategoryTitles class frame

        self.view_category_entries_button = ttk.Button(
            self,
            text="View a Category's Entries",
            command=lambda: controller.show_frame(ViewCategoryEntriesPreview)
        )  # switches to ViewCategoryEntriesPreview class frame

        self.view_titles_of_date_button = ttk.Button(
            self,
            text="View All Titles of a Certain Date",
            command=lambda: controller.show_frame(ViewTitlesOfDate)
        )  # switches to ViewTitlesOfDate class frame

        self.view_entries_of_date_button = ttk.Button(
            self,
            text="View All Entries of a Certain Date",
            command=lambda: controller.show_frame(ViewEntriesOfDatePreview)
        )  # switches to ViewEntriesOfDate class frame

        self.view_category_titles_of_date_button = ttk.Button(
            self,
            text="View a Category's Titles of a Certain Date",
            command=lambda: controller.show_frame(ViewCategoryTitlesOfDate)
        )  # switches to ViewCategoryTitlesOfDate class frame

        self.view_category_entries_of_date_button = ttk.Button(
            self,
            text="View a Category's Entries of a Certain Date",
            command=lambda: controller.show_frame(ViewCategoryEntriesOfDatePreview)
        )  # switches to ViewCategoryEntriesOfDate class frame

        self.view_category_entries_as_percentage_button = ttk.Button(
            self,
            text="View Category Entries as a Percentage of the Total",
            command=lambda: controller.show_frame(ViewCategoryEntriesAsPercentage)
        )  # switches to ViewCategoryEntriesAsPercentage class frame

        self.exit_app_button = ttk.Button(
            self,
            text="Exit",
            command=exit
        )  # exits the app

        self.delete_something_button = ttk.Button(
            self,
            text="Delete Something",
            command=lambda: controller.show_frame(DeleteSomething)
        )  # switches to DeleteSomething class frame

        self.add_entry_button.grid(row=0, column=0, sticky="EW")
        self.add_category_button.grid(row=1, column=0, sticky="EW")
        self.view_entry_button.grid(row=2, column=0, sticky="EW")
        self.view_categories_button.grid(row=3, column=0, sticky="EW")
        self.view_titles_button.grid(row=4, column=0, sticky="EW")
        self.view_entries_button.grid(row=5, column=0, sticky="EW")
        self.view_category_titles_button.grid(row=6, column=0, sticky="EW")
        self.view_category_entries_button.grid(row=7, column=0, sticky="EW")
        self.view_titles_of_date_button.grid(row=8, column=0, sticky="EW")
        self.view_entries_of_date_button.grid(row=9, column=0, sticky="EW")
        self.view_category_titles_of_date_button.grid(row=10, column=0, sticky="EW")
        self.view_category_entries_of_date_button.grid(row=11, column=0, sticky="EW")
        self.view_category_entries_as_percentage_button.grid(row=12, column=0, sticky="EW")
        self.exit_app_button.grid(row=13, column=0, sticky="EW")
        self.delete_something_button.grid(row=0, column=2, sticky="EW")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


class AddEntry(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.check_double_click_entry_reference = tuple()

        self.entry_category_label = ttk.Label(self, text="Category ID: ")
        self.entry_category_entry = ttk.Entry(self)

        self.entry_title_label = ttk.Label(self, text="Entry Title: ")
        self.entry_title_entry = ttk.Entry(self)

        self.entry_content_label = ttk.Label(self, text="Entry Content: ")
        self.entry_content_entry = ScrolledText(self, wrap=tk.WORD, font=("Segoe UI", 10))

        self.add_entry_button = ttk.Button(
            self,
            text="Add Entry",
            command=lambda: self.add_entry()
            )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.entry_category_label.grid(row=0, column=0, sticky="W")
        self.entry_category_entry.grid(row=0, column=1, sticky="EW")
        self.entry_title_label.grid(row=1, column=0, sticky="W")
        self.entry_title_entry.grid(row=1, column=1, sticky="EW")
        self.entry_content_label.grid(row=2, column=0, sticky="NW")
        self.entry_content_entry.grid(row=2, column=1, rowspan=2, sticky="NSEW")
        self.entry_content_entry.grid_columnconfigure(1, weight=5)
        self.entry_content_entry.grid_rowconfigure(2, weight=5)
        self.return_to_main_menu.grid(row=4, column=0, sticky="EW")
        self.add_entry_button.grid(row=4, column=1, sticky="EW")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=5)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def add_entry(self):
        entry_title = self.entry_title_entry.get()
        entry_content = self.entry_content_entry.get("1.0", "end-1c")
        entry_date = datetime.datetime.today().strftime("%Y-%m-%d")
        entry_time = datetime.datetime.today().strftime("%H:%M:%S")
        category_id = self.entry_category_entry.get()
        self.check_category_exists()

        if entry_title == "" or entry_content == "":
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter valid info into all fields.\n"
                                            "Don't leave any fields blank.")
            return
        try:
            dbl_click = self.check_for_double_click_entry(category_id, entry_title, entry_content)
            if dbl_click == 1:
                return
            if dbl_click == 0:
                try:
                    entry_id = database.add_entry(connection, entry_title, entry_content, entry_date, entry_time, category_id)
                except psycopg2.errors.InvalidTextRepresentation:
                    tk.messagebox.showerror(title="Invalid Input",
                                            message="Make sure you enter valid info into all fields.")
                    return
                if entry_id:
                    self.check_double_click_entry_reference = (category_id, entry_title, entry_content)
                    messagebox.showinfo(title="New Entry Added",
                                        message=f"The entry '{entry_title}' has been added with id: {entry_id}")
        finally:
            return

    def check_category_exists(self):
        # prevents the creation of an entry with an invalid category id
        category_id = self.entry_category_entry.get()
        try:
            categories_exist = database.get_category(connection, category_id)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter a valid category ID.")
            return
        if not categories_exist:
            tk.messagebox.showerror(title="Category Not Found",
                                    message="This category doesn't exist.")
            return

    def check_for_double_click_entry(self, category_id, entry_title, entry_content):
        if (category_id, entry_title, entry_content) == self.check_double_click_entry_reference:
            tk.messagebox.showerror(title="Double Click",
                                    message="This exact entry was just added.")
            return 1
        else:
            return 0


class AddCategory(ttk.Frame):  # Add a category to the database
    global connection

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.category_name = tk.StringVar()

        self.category_name_label = ttk.Label(self, text="Category Name: ")
        self.category_name_entry = ttk.Entry(self, textvariable=self.category_name)

        self.add_category_button = ttk.Button(
            self,
            text="Add Category",
            command=lambda: self.add_category()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.columnconfigure(2, weight=3)
        self.category_name_label.grid(row=0, column=0, sticky="W")
        self.category_name_entry.grid(row=0, column=1, columnspan=5, sticky="EW")
        self.add_category_button.grid(row=1, column=1, columnspan=2, sticky="EW")
        self.return_to_main_menu.grid(row=1, column=4, sticky="EW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def add_category(self):
        cat_name = self.category_name.get()
        already_exists = self.check_category_exists(cat_name)
        no_name_entered = self.check_category_name_entered(cat_name)

        if no_name_entered == 1:
            return

        if already_exists == 0:

            try:
                new_category_id = database.add_category(connection, cat_name)
            except psycopg2.errors.InvalidTextRepresentation:
                tk.messagebox.showerror(title="Invalid Input",
                                        message="Make sure you enter valid info into all fields.")
                return

            messagebox.showinfo(title="New Category Added",
                                message=f"The category '{cat_name}' has been added with id: {new_category_id}")

    def check_category_name_entered(self, cat_name):
        # Checks if the category name is empty or not.
        if cat_name == "" or cat_name == " " or cat_name == "  " or cat_name == "   ":
            tk.messagebox.showerror(title="Invalid Input",
                                    message="You must enter a category name.")
            return 1
        return 0

    def check_category_exists(self, cat_name):
        # Checks if the exact category name is already in the database
        cat_name_to_check = cat_name
        cats = database.get_categories(connection)
        for category in cats:
            for i in category:
                if i == cat_name_to_check:
                    tk.messagebox.showerror(title="Category Already Exists",
                                            message=f"The category '{cat_name}' already exists.")
                    return 1
        return 0


class ViewEntry(ttk.Frame):  # View a single entry by its ID

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.entry = ()
        self.entry_id_input_value = tk.StringVar()

        self.entry_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))

        self.entry_id_label = ttk.Label(self, text="Entry ID: ")
        self.entry_id_entry = ttk.Entry(self, textvariable=self.entry_id_input_value)

        self.view_entry_button = ttk.Button(
            self,
            text="View Entry",
            command=lambda: self.view_entry()
        )

        self.delete_content_button = ttk.Button(
            self,
            text="Clear Display Window",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.entry_id_label.grid(row=0, column=0, sticky="E")
        self.entry_id_entry.grid(row=0, column=1, sticky="EW")
        self.view_entry_button.grid(row=1, column=1, sticky="EW")
        self.delete_content_button.grid(row=1, column=3, sticky="EW")
        self.return_to_main_menu.grid(row=1, column=5, sticky="EW")
        self.entry_window.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=3)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def convert_entry_id_to_integer(self):
        # This is an ad hoc workaround to avoid the following error:
        # (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type integer: ""
        # entry_id is changed to an integer inside this function.
        # database.get_entry uses a string for the SQL query, so entry_id is then changed to a string in that function.
        entry_id_grabbed = self.entry_id_input_value.get()
        try:
            entry_id_as_integer = int(entry_id_grabbed)
        except ValueError:
            entry_id_as_integer = 0
        return entry_id_as_integer

    def view_entry(self):
        global entry
        no_duplication = ()
        user_input = self.entry_id_input_value.get()
        self.check_categories_exist()

        try:
            payload = database.get_entry(connection, user_input)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter a valid entry ID.")
            return

        if not payload:
            tk.messagebox.showerror(title="Not Found",
                                    message=f"No entry with id {user_input} exists.")
            return
        else:
            if payload == entry:       # if button is double-clicked,
                return no_duplication  # the entry is not duplicated in the display window.
            else:
                entry = payload
                formatted_payload = self.format_entry(payload)
                self.entry_window.insert(tk.END, formatted_payload)
                return formatted_payload

    def check_categories_exist(self):
        # prevents the creation of an entry before the creation of a category
        categories_exist = database.get_categories(connection)
        if not categories_exist:
            tk.messagebox.showerror(title="Database Requirement",
                                    message="No categories have been created yet,\n"
                                            "therefore no entries can be recorded.\n"
                                            "You must add a category first.")
            return
        else:
            return

    def format_entry(self, db_entry):
        entry_display = f"Entry ID: {db_entry[0][1]} | Title: {db_entry[0][2]}\n{db_entry[0][3]}\nDate: {db_entry[0][4]}" \
                        f" | Time: {db_entry[0][5]} | Category ID: {db_entry[0][6]}\n\n\n"
        return entry_display

    def delete_content(self):
        self.entry_window.delete(1.0, tk.END)
        self.entry_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))
        self.entry_window.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        return


class ViewCategories(ttk.Frame):
    # View all categories
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.categories_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))

        view_categories_button = ttk.Button(
            self,
            text="View All Categories",
            command=lambda: self.view_categories()
        )

        return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        view_categories_button.grid(row=0, column=0, sticky="EW")
        return_to_main_menu.grid(row=0, column=1, sticky="EW")
        self.categories_window.grid(row=1, column=0, columnspan=5, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_categories(self):
        global categories  # used to check for double-clicks
        no_duplication = ()
        db_categories = database.get_categories(connection)

        if not db_categories:
            tk.messagebox.showerror(title="No Categories",
                                    message="No categories have been created yet.")
            return
        else:
            if db_categories == categories:  # if button is double-clicked,
                return no_duplication        # the categories are not duplicated in the display window.
            else:
                categories = db_categories
                self.categories_window.delete(1.0, tk.END)
                self.categories_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))
                self.categories_window.grid(row=1, column=0, columnspan=5, rowspan=2, sticky="NSEW")
                for category in categories:
                    formatted_categories = self.format_categories(category)
                    self.categories_window.insert(tk.END, formatted_categories)
                return categories

    def format_categories(self, db_categories):
        category_display = f"Category ID: {db_categories[1]} | {db_categories[2]}\n"
        return category_display


class ViewTitles(ttk.Frame):
    # View all entry titles
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.TitlesWindow = ViewTitlesDisplayWindow(self)  # scrollable window

        self.view_titles_button = ttk.Button(
            self,
            text="View All Titles",
            command=lambda: self.view_titles()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.view_titles_button.grid(row=0, column=0, sticky="EW")
        self.return_to_main_menu.grid(row=0, column=1, sticky="EW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)
        self.TitlesWindow.grid(row=1, column=0, columnspan=5, rowspan=2, sticky="NSEW")

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_titles(self):
        global titles  # used to check for double-clicks
        no_duplication = ()
        db_titles = database.get_titles(connection)
        db_category_names = database.get_categories(connection)

        if not db_titles:
            tk.messagebox.showerror(title="No Titles",
                                    message="No titles have been created yet.")
            return
        else:
            if db_titles == titles:  # if button is double-clicked,
                return no_duplication  # the titles are not duplicated in the display window.
            else:
                titles = db_titles
                self.TitlesWindow.delete(1, tk.END)
                self.TitlesWindow.scrollbar.grid_forget()
                self.TitlesWindow = ViewTitlesDisplayWindow(self)
                self.TitlesWindow.grid(row=1, column=0, columnspan=5, rowspan=2, sticky="NSEW")
                for title in titles:
                    cat_name = self.match_category_id_to_category_name(title[2], db_category_names)
                    formatted_titles = self.format_titles(title, cat_name)
                    self.TitlesWindow.update_entry_widgets(formatted_titles)
                return titles

    def format_titles(self, db_titles, category_name):
        title_display = f"ID: {db_titles[0]} | Title: {db_titles[1]}   (Category {db_titles[2]} - {category_name})"
        return title_display

    def match_category_id_to_category_name(self, category_id, db_category_names):  # returns the category name
        for category in db_category_names:
            if category_id == category[1]:
                return category[2]


class ViewEntriesPreview(ttk.Frame):
    # View all entries in the database
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.EntriesPreviewWindow = ViewEntriesDisplayWindow(self)  # scrollable window

        self.view_entries_preview_button = ttk.Button(
            self,
            text="View Entries With Previews",
            command=lambda: self.view_entries_preview()
        )

        self.view_entries_full_text_button = ttk.Button(
            self,
            text="View Entries Full Text",
            command=lambda: controller.show_frame(ViewEntriesFullText)
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.view_entries_preview_button.grid(row=0, column=0, sticky="EW")
        self.view_entries_full_text_button.grid(row=0, column=1, sticky="EW")
        self.return_to_main_menu.grid(row=0, column=4, sticky="EW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)
        self.EntriesPreviewWindow.grid(row=1, column=0, columnspan=6, rowspan=2, sticky="NSEW")

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_entries_preview(self):
        global entries_preview  # used to check for double-clicks
        no_duplication = ()
        db_entries = database.get_entries(connection)
        db_category_names = database.get_categories(connection)

        if not db_entries:
            tk.messagebox.showerror(title="No Entries",
                                    message="No entries have been created yet.")
            return
        else:
            if db_entries == entries_preview:  # if button is double-clicked,
                return no_duplication  # the entries are not duplicated in the display window.
            else:
                entries_preview = db_entries
                self.EntriesPreviewWindow.delete(1, tk.END)
                self.EntriesPreviewWindow.scrollbar.grid_forget()
                self.EntriesPreviewWindow = ViewEntriesDisplayWindow(self)  # scrollable window
                self.EntriesPreviewWindow.grid(row=1, column=0, columnspan=6, rowspan=2, sticky="NSEW")
                for e in entries_preview:
                    cat_name = self.match_category_id_to_category_name(e[6], db_category_names)
                    formatted_entries = self.format_entries(e, cat_name)
                    self.EntriesPreviewWindow.update_entry_widgets(formatted_entries)
                return entries_preview

    def format_entries(self, db_entries, category_name):
        entry_display = f"Entry ID: {db_entries[1]} | " \
                        f"Date: {db_entries[4]} | " \
                        f"Time: {db_entries[5]} | " \
                        f"Category ID: {db_entries[6]} ({category_name})\n" \
                        f"Title: {db_entries[2]}\n" \
                        f"{db_entries[3]}\n"
        return entry_display

    def match_category_id_to_category_name(self, category_id, db_category_names):  # returns the category name
        for category in db_category_names:
            if category_id == category[1]:
                return category[2]


class ViewEntriesFullText(ttk.Frame):
    # View all entries in the database
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.entries_full_text_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))

        self.view_entries_full_text_button = ttk.Button(
            self,
            text="View Entries Full Text",
            command=lambda: self.view_entries_full_text()
        )

        self.return_to_view_entries = ttk.Button(
            self,
            text="Back to View Entries with Previews",
            command=lambda: controller.show_frame(ViewEntriesPreview)
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.view_entries_full_text_button.grid(row=0, column=0, sticky="EW")
        self.return_to_view_entries.grid(row=0, column=2, sticky="EW")
        self.return_to_main_menu.grid(row=0, column=4, sticky="EW")
        self.entries_full_text_window.grid(row=1, column=0, columnspan=5, rowspan=2, sticky="NSEW")
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)

    def view_entries_full_text(self):
        global entries_full_text  # used to check for double-clicks
        no_duplication = ()
        db_entries = database.get_entries(connection)
        db_category_names = database.get_categories(connection)

        if not db_entries:
            tk.messagebox.showerror(title="No Entries",
                                    message="No entries have been created yet.")
            return
        else:
            if db_entries == entries_full_text:  # if button is double-clicked,
                return no_duplication  # the entries are not duplicated in the display window.
            else:
                entries_full_text = db_entries
                self.entries_full_text_window.destroy()
                self.entries_full_text_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))
                self.entries_full_text_window.grid(row=1, column=0, columnspan=5, rowspan=2, sticky="NSEW")
                for e in entries_full_text:
                    cat_name = self.match_category_id_to_category_name(e[6], db_category_names)
                    formatted_entries = self.format_entries(e, cat_name)
                    self.entries_full_text_window.insert(tk.END, formatted_entries)
                return entries_full_text

    def format_entries(self, db_entries, category_name):
        entry_display = f"Entry ID: {db_entries[1]} | " \
                        f"Date: {db_entries[4]} | " \
                        f"Time: {db_entries[5]} | " \
                        f"Category ID: {db_entries[6]} ({category_name})\n" \
                        f"Title: {db_entries[2]}\n" \
                        f"{db_entries[3]}\n\n"
        return entry_display

    def match_category_id_to_category_name(self, category_id, db_category_names):  # returns the category name
        for category in db_category_names:
            if category_id == category[1]:
                return category[2]


class ViewCategoryTitles(ttk.Frame):
    # View all titles in a category
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.category_id_input_value = tk.StringVar()

        self.CategoryTitlesWindow = ViewACategorysTitlesDisplayWindow(self)  # scrollable window

        self.category_id_label = ttk.Label(self, text="Category ID: ")
        self.category_id_entry = ttk.Entry(self, textvariable=self.category_id_input_value)

        self.view_category_titles_button = ttk.Button(
            self,
            text="View a Category's Titles",
            command=lambda: self.view_category_titles()
        )

        self.clear_display_window_button = ttk.Button(
            self,
            text="Clear Display Window",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.category_id_label.grid(row=0, column=0, sticky="E")
        self.category_id_entry.grid(row=0, column=1, sticky="EW")
        self.clear_display_window_button.grid(row=1, column=3, sticky="EW")
        self.view_category_titles_button.grid(row=1, column=1, sticky="EW")
        self.return_to_main_menu.grid(row=1, column=5, sticky="EW")
        self.CategoryTitlesWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=3)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_category_titles(self):
        global category_titles  # used to check for double-clicks
        no_duplication = ()
        user_input = self.category_id_input_value.get()

        try:
            db_titles = database.get_category_titles(connection, user_input)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter the correct category ID.")
            return

        db_category_name = database.get_category(connection, user_input)

        if not db_titles:
            tk.messagebox.showerror(title="No Titles In This Category",
                                    message="No titles have been created yet.")
            return
        else:
            if db_titles == category_titles:    # if button is double-clicked,
                return no_duplication  # the titles are not duplicated in the display window.
            else:
                category_name = db_category_name[0][2]
                header = f"Titles of Category {user_input}: {category_name}"
                footer = " "
                self.CategoryTitlesWindow.update_entry_widgets(header)
                cat_titles = db_titles
                for title in cat_titles:
                    formatted_titles = self.format_titles(title, user_input)
                    self.CategoryTitlesWindow.update_entry_widgets(formatted_titles)
                self.CategoryTitlesWindow.update_entry_widgets(footer)
                return titles

    def format_titles(self, db_titles, user_input):
        title_display = f"Category {user_input} | ID: {db_titles[0]} | Title: {db_titles[1]}"
        return title_display

    def delete_content(self):
        self.CategoryTitlesWindow.delete(1, tk.END)
        self.CategoryTitlesWindow.scrollbar.grid_forget()
        self.CategoryTitlesWindow = ViewACategorysTitlesDisplayWindow(self)
        self.CategoryTitlesWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        return


class ViewCategoryEntriesPreview(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.category_id_input_value = tk.StringVar()
        self.content_deleted = False

        self.ViewCategoryEntriesPreviewWindow = ViewCategoryEntriesDisplayWindow(self)  # scrollable window

        self.category_id_label = ttk.Label(self, text="Category ID: ")
        self.category_id_entry = ttk.Entry(self, textvariable=self.category_id_input_value)

        self.view_category_entries_preview_button = ttk.Button(
            self,
            text="View a Category's Entries - Preview",
            command=lambda: self.view_category_entries_preview()
        )

        self.view_category_entries_full_text_button = ttk.Button(
            self,
            text="View a Category's Entries - Full Text",
            command=lambda: controller.show_frame(ViewCategoryEntriesFullText)
        )

        self.delete_entry_content_button = ttk.Button(
            self,
            text="Delete Entry Content",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.category_id_label.grid(row=0, column=0, sticky="E")
        self.category_id_entry.grid(row=0, column=1, sticky="EW")
        self.delete_entry_content_button.grid(row=0, column=3, sticky="EW")
        self.view_category_entries_preview_button.grid(row=1, column=1, sticky="EW")
        self.view_category_entries_full_text_button.grid(row=1, column=3, sticky="EW")
        self.return_to_main_menu.grid(row=1, column=5, sticky="EW")
        self.ViewCategoryEntriesPreviewWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=3)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_category_entries_preview(self):
        global category_entries_preview  # used to check for double-clicks
        no_duplication = ()
        user_input = self.category_id_input_value.get()
        category_id_as_integer = self.convert_category_id_to_integer(user_input)

        try:
            payload = database.get_category_entries(connection, category_id_as_integer)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter the correct category ID.")
            return

        db_category_name = database.get_category(connection, user_input)

        if not payload:
            tk.messagebox.showerror(title="Category Entries Not Found",
                                    message="This category doesn't exist, or contains no entries.")
            return
        else:
            if payload == category_entries_preview:  # if button is double-clicked,
                return no_duplication                # the entries are not duplicated in the display window.
            else:
                category_entries_preview = payload
                category_name = db_category_name[0][2]
                header = f"Entries of Category {user_input}: {category_name}"
                footer = "\n______________________________________________________________________________________" \
                         "________________________________________________________________________________________" \
                         "________________________________\n\n"
                category_entries = payload
                self.ViewCategoryEntriesPreviewWindow.update_entry_widgets(header)
                for e in category_entries:
                    formatted_entries = self.format_entries(e, user_input)
                    self.ViewCategoryEntriesPreviewWindow.update_entry_widgets(formatted_entries)
                self.ViewCategoryEntriesPreviewWindow.update_entry_widgets(footer)
                return category_entries

    def format_entries(self, db_entry, user_input):
        entry_display = f"Category {user_input} | Entry ID: {db_entry[1]} | " \
                        f"Date: {db_entry[4]} | " \
                        f"Time: {db_entry[5]}\n" \
                        f"Title: {db_entry[2]}\n" \
                        f"{db_entry[3]}"
        return entry_display

    def convert_category_id_to_integer(self, cat_id):
        # This is an ad hoc workaround to avoid the following error:
        # (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type integer: ""
        # category_id is changed to an integer inside this function.
        # database.get_entry changes it back to a string within that function.
        try:
            category_id_as_integer = int(cat_id)
        except ValueError:
            category_id_as_integer = 0
        return category_id_as_integer

    def delete_content(self):
        global category_entries_preview
        self.ViewCategoryEntriesPreviewWindow.delete(1, tk.END)
        self.ViewCategoryEntriesPreviewWindow.scrollbar.grid_forget()
        category_entries_preview = ()
        self.ViewCategoryEntriesPreviewWindow = ViewCategoryEntriesDisplayWindow(self)  # scrollable window
        self.ViewCategoryEntriesPreviewWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        return category_entries_preview


class ViewCategoryEntriesFullText(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.category_id_input_value = tk.StringVar()

        self.category_id_label = ttk.Label(self, text="Category ID: ")
        self.category_id_entry = ttk.Entry(self, textvariable=self.category_id_input_value)

        self.view_category_entries_full_text_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))

        self.view_category_entries_full_text_button = ttk.Button(
            self,
            text="View Category Entries - Full Text",
            command=lambda: self.view_category_entries_full_text()
        )

        self.return_to_view_category_entries_preview = ttk.Button(
            self,
            text="Back to View Category Entries - Preview",
            command=lambda: controller.show_frame(ViewCategoryEntriesPreview)
        )

        self.delete_entry_content_button = ttk.Button(
            self,
            text="Delete Entry Content",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu_button = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.category_id_label.grid(row=0, column=0, sticky="E")
        self.category_id_entry.grid(row=0, column=1, sticky="EW")
        self.delete_entry_content_button.grid(row=0, column=3, sticky="EW")
        self.view_category_entries_full_text_button.grid(row=1, column=1, sticky="EW")
        self.return_to_view_category_entries_preview.grid(row=1, column=3, sticky="EW")
        self.return_to_main_menu_button.grid(row=1, column=5, sticky="EW")
        self.view_category_entries_full_text_window.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=3)

    def view_category_entries_full_text(self):
        global category_entries_full_text
        no_duplication = ()
        user_input = self.category_id_input_value.get()
        category_id_as_integer = self.convert_category_id_to_integer(user_input)
        db_entries = database.get_category_entries(connection, category_id_as_integer)
        db_category_name = database.get_category(connection, user_input)

        if not db_entries:
            tk.messagebox.showerror(title="No Entries",
                                    message="No entries have been created yet.")
            return

        else:
            if db_entries == category_entries_full_text:  # if button is double-clicked,
                return no_duplication                     # the entries are not duplicated in the display window.
            else:
                category_entries_full_text = db_entries

                category_name = db_category_name[0][2]
                header = f"Entries of Category {user_input}: {category_name}\n\n"
                footer = "________________________________________________________________________________________" \
                         "________________________________________________________________________________________" \
                         "______________________________\n\n\n"
                self.view_category_entries_full_text_window.insert(tk.END, header)
                for e in category_entries_full_text:
                    formatted_entries = self.format_entries(e, category_name)
                    self.view_category_entries_full_text_window.insert(tk.END, formatted_entries)
                self.view_category_entries_full_text_window.insert(tk.END, footer)
                return category_entries_full_text

    def format_entries(self, db_entries, category_name):
        entry_display = f"Entry ID: {db_entries[1]} | " \
                        f"Date: {db_entries[4]} | " \
                        f"Time: {db_entries[5]} | " \
                        f"Category ID: {db_entries[6]} ({category_name})\n" \
                        f"Title: {db_entries[2]}\n" \
                        f"{db_entries[3]}\n\n\n"
        return entry_display

    def convert_category_id_to_integer(self, cat_id):
        # This is an ad hoc workaround to avoid the following error:
        # (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type integer: ""
        int_cat_id = int(cat_id)
        return int_cat_id

    def delete_content(self):
        global category_entries_full_text
        self.view_category_entries_full_text_window.delete(1.0, tk.END)
        category_entries_full_text = ()
        return category_entries_full_text


class ViewTitlesOfDate(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.entry_date_input_value = tk.StringVar()

        self.ViewTitlesOfDateWindow = ViewTitlesOfADateDisplayWindow(self)  # scrollable window

        self.entry_date_label = ttk.Label(self, text="Entry Date (YYYY-MM-DD): ")
        self.entry_date_entry = ttk.Entry(self, textvariable=self.entry_date_input_value)

        self.view_titles_of_date_button = ttk.Button(
            self,
            text="View All Titles of a Certain Date",
            command=lambda: self.view_titles_of_date()
        )

        self.clear_display_window_button = ttk.Button(
            self,
            text="Clear Display Window",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.entry_date_label.grid(row=0, column=0, sticky="W")
        self.entry_date_entry.grid(row=0, column=1, sticky="EW")
        self.clear_display_window_button.grid(row=1, column=3, sticky="EW")
        self.view_titles_of_date_button.grid(row=1, column=1, sticky="EW")
        self.return_to_main_menu.grid(row=1, column=5, sticky="EW")
        self.ViewTitlesOfDateWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=3)
        self.ViewTitlesOfDateWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_titles_of_date(self):
        global titles_of_date  # used to check for double-clicks
        no_duplication = ()
        user_input_date = self.entry_date_input_value.get()

        try:
            payload = database.get_titles_of_date(connection, user_input_date)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter the correct date and format.")
            return

        db_category_names = database.get_categories(connection)

        if not payload:
            tk.messagebox.showerror(title="No Titles Found",
                                    message="Make sure you entered the correct date and format.")
            return
        else:
            if payload == titles_of_date:  # if button is double-clicked,
                return no_duplication      # the titles are not duplicated in the display window.
            else:
                titles_of_date = payload
                header = f"Titles of {user_input_date}:"
                footer = f" "
                self.ViewTitlesOfDateWindow.update_entry_widgets(header)
                for title in titles_of_date:
                    cat_name = self.match_category_id_to_category_name(title[2], db_category_names)
                    formatted_payload = self.format_titles_of_date(title, cat_name)
                    self.ViewTitlesOfDateWindow.update_entry_widgets(formatted_payload)
                self.ViewTitlesOfDateWindow.update_entry_widgets(footer)
                return titles_of_date

    def format_titles_of_date(self, db_titles, category_name):
        title_display = f"ID: {db_titles[0]} | Title: {db_titles[1]}   (Category {db_titles[2]} - {category_name})"
        return title_display

    def match_category_id_to_category_name(self, category_id, db_category_names):  # returns the category name
        for category in db_category_names:
            if category_id == category[1]:
                return category[2]

    def delete_content(self):
        global titles_of_date
        self.ViewTitlesOfDateWindow.delete(1, tk.END)
        self.ViewTitlesOfDateWindow.scrollbar.grid_forget()
        titles_of_date = ()
        self.ViewTitlesOfDateWindow = ViewTitlesOfADateDisplayWindow(self)
        self.ViewTitlesOfDateWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        return titles_of_date


class ViewEntriesOfDatePreview(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.entry_date_input_value = tk.StringVar()

        self.ViewEntriesOfDatePreviewWindow = ViewEntriesOfADateDisplayWindow(self)  # scrollable window

        self.entry_date_label = ttk.Label(self, text="Entry Date (YYYY-MM-DD): ")
        self.entry_date_entry = ttk.Entry(self, textvariable=self.entry_date_input_value)

        self.view_entries_of_date_preview_button = ttk.Button(
            self,
            text="View All Entries of a Certain Date - Preview",
            command=lambda: self.view_entries_of_date_preview()
        )

        self.view_entries_of_date_full_text_button = ttk.Button(
            self,
            text="View Entries of a Certain Date - Full Text",
            command=lambda: controller.show_frame(ViewEntriesOfDateFullText)
        )

        self.delete_content_button = ttk.Button(
            self,
            text="Clear Entry Content Window",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.entry_date_label.grid(row=0, column=0, sticky="W")
        self.entry_date_entry.grid(row=0, column=1, sticky="EW")
        self.delete_content_button.grid(row=0, column=2, sticky="EW")
        self.view_entries_of_date_preview_button.grid(row=1, column=1, sticky="EW")
        self.view_entries_of_date_full_text_button.grid(row=1, column=2, sticky="EW")
        self.return_to_main_menu.grid(row=1, column=5, sticky="EW")
        self.ViewEntriesOfDatePreviewWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=3)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_entries_of_date_preview(self):
        global entries_of_date_preview  # used to check for double-clicks
        no_duplication = ()
        user_input_date = self.entry_date_input_value.get()
        db_category_names = database.get_categories(connection)

        try:
            payload = database.get_entries_of_date(connection, user_input_date)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter the correct date and format.")
            return

        if not payload:
            tk.messagebox.showerror(title="No Entries Found",
                                    message="Make sure you entered the correct date and format.")
            return
        else:
            if payload == entries_of_date_preview:  # if button is double-clicked,
                return no_duplication               # the entries are not duplicated in the display window.
            else:
                entries_of_date = payload
                self.ViewEntriesOfDatePreviewWindow.scrollbar.grid_forget()
                self.ViewEntriesOfDatePreviewWindow = ViewEntriesOfADateDisplayWindow(self)  # scrollable window
                self.ViewEntriesOfDatePreviewWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
                header = f"Entries of {user_input_date}:"
                footer = f" "
                self.ViewEntriesOfDatePreviewWindow.update_entry_widgets(header)
                for e in entries_of_date:
                    cat_name = self.match_category_id_to_category_name(e[6], db_category_names)
                    formatted_payload = self.format_entries_of_date(e, cat_name)
                    self.ViewEntriesOfDatePreviewWindow.update_entry_widgets(formatted_payload)
                self.ViewEntriesOfDatePreviewWindow.update_entry_widgets(footer)
                return entries_of_date

    def format_entries_of_date(self, db_entries, category_name):
        entry_display = f"Entry ID: {db_entries[1]} | " \
                        f"Time: {db_entries[5]} | " \
                        f"Category ID: {db_entries[6]} - {category_name}\n" \
                        f"Title: {db_entries[2]}\n" \
                        f"{db_entries[3]}"
        return entry_display

    def match_category_id_to_category_name(self, category_id, db_category_names):  # returns the category name
        for category in db_category_names:
            if category_id == category[1]:
                return category[2]

    def delete_content(self):
        global entries_of_date_preview
        self.ViewEntriesOfDatePreviewWindow.delete(1, tk.END)
        entries_of_date_preview = ()
        self.ViewEntriesOfDatePreviewWindow = ViewEntriesOfADateDisplayWindow(self)
        self.ViewEntriesOfDatePreviewWindow.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        return entries_of_date_preview


class ViewEntriesOfDateFullText(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.entry_date_input_value = tk.StringVar()

        self.entry_date_label = ttk.Label(self, text="Entry Date (YYYY-MM-DD): ")
        self.entry_date_entry = ttk.Entry(self, textvariable=self.entry_date_input_value)

        self.view_entries_of_date_full_text_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))

        self.view_entries_of_date_full_text_button = ttk.Button(
            self,
            text="View All Entries of a Certain Date - Full Text",
            command=lambda: self.view_entries_of_date_full_text()
        )

        self.delete_content_button = ttk.Button(
            self,
            text="Clear Entry Content Window",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.return_to_entries_of_date_preview = ttk.Button(
            self,
            text="Back to Entries of a Certain Date - Preview",
            command=lambda: controller.show_frame(ViewEntriesOfDatePreview)
        )

        self.entry_date_label.grid(row=0, column=0, sticky="W")
        self.entry_date_entry.grid(row=0, column=1, sticky="EW")
        self.delete_content_button.grid(row=0, column=3, sticky="EW")
        self.view_entries_of_date_full_text_button.grid(row=1, column=1, sticky="EW")
        self.return_to_entries_of_date_preview.grid(row=1, column=3, sticky="EW")
        self.return_to_main_menu.grid(row=1, column=5, sticky="EW")
        self.view_entries_of_date_full_text_window.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=3)

    def view_entries_of_date_full_text(self):
        global entries_of_date_full_text
        no_duplication = ()
        user_input_date = self.entry_date_input_value.get()
        db_category_names = database.get_categories(connection)

        try:
            payload = database.get_entries_of_date(connection, user_input_date)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter the correct date and format.")
            return

        if not payload:
            tk.messagebox.showerror(title="No Entries Found",
                                    message="Make sure you entered the correct date and format.")
            return
        else:
            if payload == entries_of_date_full_text:  # if button is double-clicked,
                return no_duplication                 # the entries are not duplicated in the display window.
            else:
                entries_of_date_full_text = payload
                header = f"Entries of {user_input_date}:\n\n"
                footer = f"\n"
                self.view_entries_of_date_full_text_window.insert(tk.END, header)
                cat_name_lookup = self.match_category_id_to_category_name(db_category_names)
                for e in entries_of_date_full_text:
                    for key, value in cat_name_lookup.items():
                        if e[6] == key:
                            cat_name = value
                    formatted_payload = self.format_entries_of_date_full_text(e, cat_name)
                    self.view_entries_of_date_full_text_window.insert(tk.END, formatted_payload)
                self.view_entries_of_date_full_text_window.insert(tk.END, footer)
                return entries_of_date_full_text

    def format_entries_of_date_full_text(self, db_entries, category_name):
        entry_display = f"Entry ID: {db_entries[1]} | " \
                        f"Time: {db_entries[5]} | " \
                        f"Category ID: {db_entries[6]} - {category_name}\n" \
                        f"Title: {db_entries[2]}\n" \
                        f"{db_entries[3]}\n\n"
        return entry_display

    def match_category_id_to_category_name(self, db_category_names):  # returns the category name
        id_name_match = {}
        for category in db_category_names:
            id_name_match[category[1]] = category[2]
        return id_name_match

    def delete_content(self):
        global entries_of_date_full_text
        self.view_entries_of_date_full_text_window.delete(1.0, tk.END)
        entries_of_date_full_text = ()
        return entries_of_date_full_text


class ViewCategoryTitlesOfDate(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.category_id_input_value = tk.StringVar()
        self.entry_date_input_value = tk.StringVar()

        self.ViewCategoryTitlesOfDateWindow = ViewACategorysTitlesOfADateDisplayWindow(self)  # scrollable window

        self.category_id_label = ttk.Label(self, text="Category ID: ")
        self.category_id_entry = ttk.Entry(self, textvariable=self.category_id_input_value)

        self.entry_date_label = ttk.Label(self, text="Entry Date (YYYY-MM-DD): ")
        self.entry_date_entry = ttk.Entry(self, textvariable=self.entry_date_input_value)

        self.view_category_titles_of_date_button = ttk.Button(
            self,
            text="View a Category's Titles of a Certain Date",
            command=lambda: self.view_category_titles_of_date()
        )

        self.clear_display_window_button = ttk.Button(
            self,
            text="Clear Display Window",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.category_id_label.grid(row=0, column=0, sticky="W")
        self.category_id_entry.grid(row=0, column=1, sticky="EW")
        self.clear_display_window_button.grid(row=2, column=3, sticky="EW")
        self.entry_date_label.grid(row=1, column=0, sticky="W")
        self.entry_date_entry.grid(row=1, column=1, sticky="EW")
        self.view_category_titles_of_date_button.grid(row=2, column=1, sticky="EW")
        self.return_to_main_menu.grid(row=2, column=5, sticky="EW")
        self.ViewCategoryTitlesOfDateWindow.grid(row=3, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(3, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(3, weight=3)
        self.rowconfigure(4, weight=3)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_category_titles_of_date(self):
        global category_titles_of_date  # used to check for double-clicks
        no_duplication = ()
        user_input_date = self.entry_date_input_value.get()
        user_input_category_id = self.convert_user_input_to_integer()

        try:
            payload = database.get_a_categorys_titles_of_date(connection, user_input_category_id, user_input_date)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter the correct input into all fields.")
            return

        db_category_name = database.get_category(connection, user_input_category_id)

        if not payload:
            tk.messagebox.showerror(title="No Titles Found",
                                    message="Make sure you entered the correct category, date and format.")
            return
        else:
            if payload == category_titles_of_date:  # if button is double-clicked,
                return no_duplication               # the titles are not duplicated in the display window.
            else:
                category_name = db_category_name[0][2]
                cat_titles_of_date = payload
                header = f"Category {user_input_category_id} ({category_name}) Titles on {user_input_date}:"
                footer = f" "
                self.ViewCategoryTitlesOfDateWindow.update_entry_widgets(header)
                for title in cat_titles_of_date:
                    formatted_payload = self.format_category_titles_of_date(title, user_input_category_id)
                    self.ViewCategoryTitlesOfDateWindow.update_entry_widgets(formatted_payload)
                self.ViewCategoryTitlesOfDateWindow.update_entry_widgets(footer)
                return titles_of_date

    def format_category_titles_of_date(self, db_titles, user_input_category_id):
        title_display = f"ID: {db_titles[0]} | Title: {db_titles[1]} (Category {user_input_category_id})"
        return title_display

    def convert_user_input_to_integer(self):
        # This is an ad hoc workaround to avoid the following error:
        # (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type integer: ""
        # category_id is changed to an integer inside this function.
        # database.get_a_categorys_titles_of_date changes it back to a string within that function.
        cat_id_grabbed = self.category_id_input_value.get()
        try:
            cat_id_as_integer = int(cat_id_grabbed)
        except ValueError:
            cat_id_as_integer = 0
        return cat_id_as_integer

    def delete_content(self):
        global category_titles_of_date
        self.ViewCategoryTitlesOfDateWindow.delete(1, tk.END)
        self.ViewCategoryTitlesOfDateWindow.scrollbar.grid_forget()
        category_titles_of_date = ()
        self.ViewCategoryTitlesOfDateWindow = ViewACategorysTitlesOfADateDisplayWindow(self)
        self.ViewCategoryTitlesOfDateWindow.grid(row=3, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        return category_titles_of_date


class ViewCategoryEntriesOfDatePreview(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.no_duplication = ()

        self.category_id_input_value = tk.StringVar()
        self.entry_date_input_value = tk.StringVar()

        self.ViewCategoryEntriesOfDatePreviewWindow = ViewACategorysEntriesOfADateDisplayWindow(self)  # scrollable window

        self.category_id_label = ttk.Label(self, text="Category ID: ")
        self.category_id_entry = ttk.Entry(self, textvariable=self.category_id_input_value)

        self.entry_date_label = ttk.Label(self, text="Entry Date (YYYY-MM-DD): ")
        self.entry_date_entry = ttk.Entry(self, textvariable=self.entry_date_input_value)

        self.view_category_entries_of_date_preview_button = ttk.Button(
            self,
            text="View a Category's Entries of a Certain Date - Previews",
            command=lambda: self.view_category_entries_of_date_preview()
        )

        self.view_category_entries_of_date_full_text_button = ttk.Button(
            self,
            text="View a Category's Entries of a Certain Date - Full Text",
            command=lambda: controller.show_frame(ViewCategoryEntriesOfDateFullText)
        )

        self.delete_content_button = ttk.Button(
            self,
            text="Clear Entry Content Window",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.category_id_label.grid(row=0, column=0, sticky="E")
        self.category_id_entry.grid(row=0, column=1, sticky="EW")
        self.entry_date_label.grid(row=1, column=0, sticky="E")
        self.entry_date_entry.grid(row=1, column=1, sticky="EW")
        self.delete_content_button.grid(row=0, column=3, rowspan=2, sticky="EW")
        self.view_category_entries_of_date_preview_button.grid(row=2, column=1, sticky="EW")
        self.view_category_entries_of_date_full_text_button.grid(row=2, column=3, sticky="EW")
        self.return_to_main_menu.grid(row=2, column=5, sticky="EW")
        self.ViewCategoryEntriesOfDatePreviewWindow.grid(row=3, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(3, weight=3)
        self.rowconfigure(4, weight=3)

    def view_category_entries_of_date_preview(self):
        global category_entries_of_date_preview  # used to check for double-clicks
        user_input_date = self.entry_date_input_value.get()
        user_input_category_id = self.category_id_input_value.get()

        try:
            payload = database.get_a_categorys_entries_of_date(connection, user_input_category_id, user_input_date)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter the correct input into all fields.")
            return

        db_category_name = database.get_category(connection, user_input_category_id)

        if not payload:
            tk.messagebox.showerror(title="No Entries Found",
                                    message="Make sure you entered the correct category, date and format.")
            return
        else:
            if payload == category_entries_of_date_preview:  # if button is double-clicked,
                return self.no_duplication                   # the entries are not duplicated in the display window.
            else:
                category_name = db_category_name[0][2]
                category_entries_of_date_preview = payload
                header = f"Category {user_input_category_id} ({category_name}) Entries on {user_input_date}:"
                footer = " "
                self.ViewCategoryEntriesOfDatePreviewWindow.update_entry_widgets(header)
                for e in category_entries_of_date_preview:
                    formatted_payload = self.format_category_entries_of_date_preview(e, user_input_category_id)
                    self.ViewCategoryEntriesOfDatePreviewWindow.update_entry_widgets(formatted_payload)
                self.ViewCategoryEntriesOfDatePreviewWindow.update_entry_widgets(footer)
                return category_entries_of_date_preview

    def format_category_entries_of_date_preview(self, db_entries, user_input_category_id):
        entry_display = f"Entry ID: {db_entries[1]} | Category {user_input_category_id} | " \
                        f"Date: {db_entries[4]} | Time: {db_entries[5]}\n" \
                        f"Title: {db_entries[2]}\n" \
                        f"{db_entries[3]}"
        return entry_display

    def delete_content(self):
        global category_entries_of_date_preview
        self.ViewCategoryEntriesOfDatePreviewWindow.delete(1, tk.END)
        self.ViewCategoryEntriesOfDatePreviewWindow.scrollbar.grid_forget()
        category_entries_of_date_preview = ()
        self.ViewCategoryEntriesOfDatePreviewWindow = ViewACategorysEntriesOfADateDisplayWindow(self)
        self.ViewCategoryEntriesOfDatePreviewWindow.grid(row=3, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        return category_entries_of_date_preview


class ViewCategoryEntriesOfDateFullText(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.category_id_input_value = tk.StringVar()
        self.entry_date_input_value = tk.StringVar()

        self.view_category_entries_of_date_display_window = tk.Text(self, wrap=tk.WORD, font=("Segoe UI", 10))

        self.category_id_label = ttk.Label(self, text="Category ID: ")
        self.category_id_entry = ttk.Entry(self, textvariable=self.category_id_input_value)

        self.entry_date_label = ttk.Label(self, text="Entry Date (YYYY-MM-DD): ")
        self.entry_date_entry = ttk.Entry(self, textvariable=self.entry_date_input_value)

        self.view_category_entries_of_date_full_text_button = ttk.Button(
            self,
            text="View a Category's Entries of a Certain Date - Full Text",
            command=lambda: self.view_category_entries_of_date_full_text()
        )

        self.return_to_category_entries_of_date_preview = ttk.Button(
            self,
            text="Back to Category Entries of a Certain Date - Previews",
            command=lambda: controller.show_frame(ViewCategoryEntriesOfDatePreview)
        )

        self.delete_content_button = ttk.Button(
            self,
            text="Clear Entry Content Window",
            command=lambda: self.delete_content()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.category_id_label.grid(row=0, column=0, sticky="E")
        self.category_id_entry.grid(row=0, column=1, sticky="EW")
        self.delete_content_button.grid(row=0, column=3, rowspan=2, sticky="EW")
        self.entry_date_label.grid(row=1, column=0, sticky="E")
        self.entry_date_entry.grid(row=1, column=1, sticky="EW")
        self.view_category_entries_of_date_full_text_button.grid(row=2, column=1, sticky="EW")
        self.return_to_category_entries_of_date_preview.grid(row=2, column=3, sticky="EW")
        self.return_to_main_menu.grid(row=2, column=5, sticky="EW")
        self.view_category_entries_of_date_display_window.grid(row=3, column=0, columnspan=6, rowspan=2, sticky="NSEW")
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(3, weight=3)

    def view_category_entries_of_date_full_text(self):
        global category_entries_of_date_full_text
        no_duplication = ()
        user_input_date = self.entry_date_input_value.get()
        user_input_category_id = self.category_id_input_value.get()

        try:
            payload = database.get_a_categorys_entries_of_date(connection, user_input_category_id, user_input_date)
        except psycopg2.errors.InvalidTextRepresentation:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Make sure you enter the correct input into all fields.")
            return

        db_category_name = database.get_category(connection, user_input_category_id)

        if not payload:
            tk.messagebox.showerror(title="No Entries Found",
                                    message="Make sure you entered the correct category, date and format.")
            return
        else:
            if payload == category_entries_of_date_full_text:
                return no_duplication
            else:
                category_name = db_category_name[0][2]
                category_entries_of_date_full_text = payload
                header = f"Category {user_input_category_id} ({category_name}) Entries on {user_input_date}:\n\n"
                footer = "\n________________________________________________________________________________________" \
                         "__________________________________________________________________________________________" \
                         "____________________________\n\n\n"
                self.view_category_entries_of_date_display_window.insert(tk.END, header)
                for e in category_entries_of_date_full_text:
                    formatted_payload = self.format_category_entries_of_date_full_text(e, user_input_category_id)
                    self.view_category_entries_of_date_display_window.insert(tk.END, formatted_payload)
                self.view_category_entries_of_date_display_window.insert(tk.END, footer)
                return category_entries_of_date_full_text

    def format_category_entries_of_date_full_text(self, db_entries, user_input_category_id):
        entry_display = f"Entry ID: {db_entries[1]} | Category {user_input_category_id} | " \
                        f"Date: {db_entries[4]} | Time: {db_entries[5]}\n" \
                        f"Title: {db_entries[2]}\n" \
                        f"{db_entries[3]}\n\n"
        return entry_display

    def delete_content(self):
        global category_entries_of_date_full_text
        self.view_category_entries_of_date_display_window.delete(1.0, tk.END)
        category_entries_of_date_full_text = ()
        return category_entries_of_date_full_text


class ViewCategoryEntriesAsPercentage(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.ViewCategoryEntriesAsPercentageWindow = ViewCategoryEntriesAsPercentageDisplayWindow(self)  # scrollable window

        self.view_category_entries_as_percentage_button = ttk.Button(
            self,
            text="View Category Entries as a Percentage of the Total",
            command=lambda: self.view_category_entries_as_percentage()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.view_pie_chart_button = ttk.Button(
            self,
            text="View Pie Chart",
            command=lambda: controller.show_frame(ViewPieChart)
        )

        self.view_matplotlib_pie_chart_button = ttk.Button(
            self,
            text="View Matplotlib Pie Chart",
            command=lambda: self.create_matplotlib_pie_chart()
        )

        self.view_category_entries_as_percentage_button.grid(row=0, column=0, sticky="EW")
        self.view_pie_chart_button.grid(row=0, column=1, sticky="EW")
        self.view_matplotlib_pie_chart_button.grid(row=0, column=2, sticky="EW")
        self.return_to_main_menu.grid(row=0, column=3, sticky="EW")
        self.ViewCategoryEntriesAsPercentageWindow.grid(row=1, column=0, columnspan=4, sticky="NSEW")
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(2, weight=1)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def view_category_entries_as_percentage(self):
        global category_entries_as_percentage
        payload = database.get_categorys_entries_as_percentage_of_all(connection)
        if not payload:
            tk.messagebox.showerror(title="No Entries Found",
                                    message="No entries have been created yet.")
            return
        else:
            if payload == category_entries_as_percentage:
                return
            else:
                category_entries_as_percentage = payload
                self.ViewCategoryEntriesAsPercentageWindow.scrollbar.grid_forget()
                self.ViewCategoryEntriesAsPercentageWindow = ViewCategoryEntriesAsPercentageDisplayWindow(self)
                self.ViewCategoryEntriesAsPercentageWindow.grid(row=1, column=0, columnspan=4, sticky="NSEW")
                self.format_category_entries_as_percentage()

    def get_category_names_for_iteration(self):
        db_category_names = database.get_categories(connection)
        category_names = {}
        for category in db_category_names:
            category_names[category[0]] = category[2]
        return category_names

    def format_category_entries_as_percentage(self):
        global category_entries_as_percentage
        entries_total = int(0)
        cat_names_dict = self.get_category_names_for_iteration()

        for i in category_entries_as_percentage:
            percent = round(i[3], 2)
            cat_num = i[0]
            cat_name = cat_names_dict[cat_num]
            num_entries = i[1]
            entries_total += num_entries
            self.ViewCategoryEntriesAsPercentageWindow.update_entry_widgets(
                f"{percent}% | Category#{cat_num}: {cat_name} ({num_entries} entries)"
            )

        self.ViewCategoryEntriesAsPercentageWindow.update_entry_widgets(f"Total number of entries: {entries_total}")

    def create_matplotlib_pie_chart(self):
        global category_entries_as_percentage
        cat_names = self.get_category_names_for_iteration()
        graph_values = self.generate_matplotlib_values()
        graph_labels = self.generate_matplotlib_labels(cat_names)
        graph_colors = self.generate_matplotlib_colors()
        fig, ax = plt.subplots()
        ax.pie(graph_values,
               labels=graph_labels,
               colors=graph_colors,
               autopct='%1.1f%%',
               startangle=90,
               pctdistance=.6,
               labeldistance=1.25
               )
        plt.show()

    def generate_matplotlib_values(self):
        global category_entries_as_percentage
        values = []
        for item in category_entries_as_percentage:
            values.append(int(item[3]))
        return values

    def generate_matplotlib_labels(self, names):
        global category_entries_as_percentage
        labels = []
        cat_names_dict = names
        for i in category_entries_as_percentage:
            cat_name = cat_names_dict[i[0]]
            tag = f"{i[0]}: {cat_name}\n{i[1]} entries"
            labels.append(tag)
        return labels

    def generate_matplotlib_colors(self):
        global category_entries_as_percentage
        global colors
        pie_colors = []
        num_colors = len(category_entries_as_percentage)
        for i in range(num_colors):
            pie_colors.append(colors[i])
        return pie_colors


class ViewPieChart(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.check_for_duplication = ()

        self.view_pie_chart_button = ttk.Button(
            self,
            text="View Pie Chart",
            command=lambda: self.create_pie_chart()
        )

        self.return_to_category_entries_as_percentage_button = ttk.Button(
            self,
            text="Back to Text View",
            command=lambda: controller.show_frame(ViewCategoryEntriesAsPercentage)
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.pie_canvas = tk.Canvas(self, width=250, height=250)
        self.color_key_canvas = tk.Canvas(self, width=800, height=400)

        self.scrolling_color_key = ScrollingColorKeyDisplayWindow(self)  # scrollable window
        self.cat_string = ""

        self.view_pie_chart_button.grid(row=0, column=0, sticky="EW")
        self.return_to_category_entries_as_percentage_button.grid(row=0, column=2, sticky="EW")
        self.return_to_main_menu.grid(row=0, column=3, sticky="EW")
        self.pie_canvas.grid(row=1, column=0, sticky="NSEW")
        self.color_key_canvas.grid(row=1, column=1, columnspan=3, sticky="NSEW")
        self.scrolling_color_key.grid(row=1, column=1, columnspan=3, sticky="NSEW")
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=1)

    def create_pie_chart(self):
        global category_entries_as_percentage
        if category_entries_as_percentage == self.check_for_duplication:
            return
        else:
            self.check_for_duplication = category_entries_as_percentage
        graph_values = self.generate_values()
        graph_colors = self.generate_colors()
        st = 0
        coord = 10, 10, 225, 225
        for val, col in zip(graph_values, graph_colors):
            self.pie_canvas.create_arc(coord, start=st, extent=val*3.6, fill=col)
            st += val*3.6
        self.create_color_key(graph_colors)

    def generate_colors(self):
        global category_entries_as_percentage
        global colors
        pie_colors = []
        num_colors = len(category_entries_as_percentage)
        for i in range(num_colors):
            pie_colors.append(colors[i])
        return pie_colors

    def generate_values(self):
        global category_entries_as_percentage
        values = []
        for item in category_entries_as_percentage:
            values.append(float(item[3]))
        return values

    def get_category_names_for_iteration(self):
        db_category_names = database.get_categories(connection)
        category_names = {}
        for category in db_category_names:
            category_names[category[0]] = category[2]
        return category_names

    def create_color_key(self, graph_colors):
        global category_entries_as_percentage
        cat_names_dict = self.get_category_names_for_iteration()

        for item in category_entries_as_percentage:
            i = category_entries_as_percentage.index(item)
            rating = i + 1                                  # The first category is 1, not 0.
            cat_name = cat_names_dict[item[0]]
            cat_percentage = round(item[3], 2)
            self.cat_string = f"{rating}: {graph_colors[i]} | Category #{item[0]} {cat_name}: {cat_percentage}%"
            self.scrolling_color_key.update_entry_widgets(self.cat_string)


class DeleteSomething(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.header_label = ttk.Label(self, text="These options will permanently delete entries and categories.  "
                                                 "EXERCISE CAUTION.", font=("Segoe UI", 16))

        self.delete_entry_label = ttk.Label(self, text="Delete Entry by ID: ")
        self.delete_entry_entry = ttk.Entry(self)

        self.delete_category_label = ttk.Label(self, text="Delete Category by ID: ")
        self.delete_category_entry = ttk.Entry(self)

        self.delete_entry_button = ttk.Button(
            self,
            text="Delete Entry",
            command=lambda: self.delete_entry()
        )

        self.delete_category_button = ttk.Button(
            self,
            text="Delete Category",
            command=lambda: self.delete_category()
        )

        self.return_to_main_menu = ttk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        self.header_label.grid(row=0, column=1, columnspan=2, rowspan=2, sticky="EW")
        self.delete_entry_label.grid(row=2, column=0, sticky="E")
        self.delete_entry_entry.grid(row=2, column=1, sticky="W")
        self.delete_entry_button.grid(row=2, column=2, columnspan=2, sticky="EW")
        self.delete_category_label.grid(row=3, column=0, sticky="E")
        self.delete_category_entry.grid(row=3, column=1, sticky="W")
        self.delete_category_button.grid(row=3, column=2, columnspan=2, sticky="EW")
        self.return_to_main_menu.grid(row=5, column=1, columnspan=2, sticky="EW")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

    def delete_entry(self):
        entry_id = self.delete_entry_entry.get()
        if not entry_id:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Please enter an entry ID.")
            return
        else:
            try:
                title = database.get_entry(connection, entry_id)
                database.delete_entry(connection, entry_id)
            except psycopg2.errors.InvalidTextRepresentation:
                tk.messagebox.showerror(title="Invalid Input",
                                        message="Please enter a valid entry ID.")
                return
            if not title:
                tk.messagebox.showerror(title=f"Entry {entry_id} Not Found",
                                        message="Please enter a valid entry ID.")
                return
            else:
                tk.messagebox.showinfo(title="Entry Deleted",
                                       message=f"Entry ID {entry_id} has been deleted.\nTitle: {title[0][2]}")

    def delete_category(self):
        category_id = self.delete_category_entry.get()
        if not category_id:
            tk.messagebox.showerror(title="Invalid Input",
                                    message="Please enter a category ID.")
            return
        else:
            try:
                category_exists = database.get_category(connection, category_id)
                if not category_exists:
                    tk.messagebox.showerror(title="Category Not Found",
                                            message="Please enter a valid category ID.")
                    return
                if category_exists:
                    try:
                        rows_deleted = database.delete_entries_of_category(connection, category_id)
                        database.delete_category(connection, category_id)
                        tk.messagebox.showinfo(title="Category Deleted",
                                               message=f"Category ID {category_id} and "
                                                       f"{rows_deleted} entries have been deleted.")
                    except psycopg2.errors.InvalidTextRepresentation: \
                        tk.messagebox.showerror(title="Invalid Input",
                                                message="Please enter a valid category ID.")
                    return
            finally:
                return


root = JournalRecorder()
root.geometry("1200x750")
root.resizable(False, False)

font.nametofont("TkDefaultFont").configure(size=10)

style = ttk.Style(root)

root.columnconfigure(0, weight=1)

database.create_tables(connection)

style.theme_use("clam")

root.mainloop()
