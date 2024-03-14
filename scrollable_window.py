import tkinter as tk
from tkinter import ttk


class ViewTitlesDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewTitles class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=5, row=1, rowspan=3, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ViewEntriesDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewEntriesPreview class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=6, row=1, rowspan=3, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ViewACategorysTitlesDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewCategoryTitles class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=6, row=2, rowspan=2, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ViewCategoryEntriesDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewCategoryEntriesPreview class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=6, row=2, rowspan=2, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ViewTitlesOfADateDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewTitlesOfDate class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=6, row=2, rowspan=2, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ViewEntriesOfADateDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewEntriesOfDatePreview class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=6, row=2, rowspan=2, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ViewACategorysTitlesOfADateDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewCategoryTitlesOfDate class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=6, row=3, rowspan=2, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ViewACategorysEntriesOfADateDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewCategoryEntriesOfDatePreview class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=6, row=3, rowspan=2, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ViewCategoryEntriesAsPercentageDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewCategoryEntriesAsPercentage class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=4, row=1, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")


class ScrollingColorKeyDisplayWindow(tk.Canvas):
    # Scrollable display window used in ViewPieChart class
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(entry):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(entry):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.scrollbar.grid(column=4, row=1, rowspan=1, sticky="NSW")

        self.configure(yscrollcommand=self.scrollbar.set)
        self.yview_moveto(1.0)

    def update_entry_widgets(self, entry_tuple):
        entry_label = ttk.Label(
            self.display_frame,
            text=entry_tuple,
            anchor="w",
            justify="left"
        )

        entry_label.grid(sticky="NSEW")
