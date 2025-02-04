from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, StringVar, OptionMenu
from tkinter.messagebox import showinfo
from fileSearchApp import Filesearch
import os
import json
import time

class MainApp:
    # Function to read cache from file
    def __init__(self, root):
        self.root = root
        self.filesearch = Filesearch()  # Create an instance of Filesearch
        self.cache = self.filesearch.read_cache()

        # Create and place widgets
        self.create_widgets()   

    def search_button_click(self):
        # handle the search button click event
        self.search_term = self.search_entry.get()
        self.root_dir = self.root_dir_entry.get()
        self.search_type = self.search_type_var.get()

        # Check if search result are cached
        cache_key = f"{self.root_dir}_{self.search_term}_{self.search_type}"
        if cache_key in self.cache:
            showinfo("Search Results", "Results found in cache\n".join(self.cache[cache_key]))
        else:
            results = self.filesearch.search_file(self.root_dir, self.search_term, self.search_type)
            self.result_listbox.delete(0, 'end') # Clear previous results
            for result in results:
                self.result_listbox.insert('end', result)
            #update the cache
            self.cache[cache_key] = results
            self.filesearch.write_cache()

    def create_widgets(self):
        # Search term label and Entry
        search_term_label = Label(self.root, text="Search Term")
        search_term_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = Entry(self.root, width=50)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        # Root directory label and entry
        root_dir_label = Label(self.root, text="Root Directory:")
        root_dir_label.grid(row=1, column=0, padx=5, pady=5)
        self.root_dir_entry = Entry(self.root, width=50)
        self.root_dir_entry.grid(row=1, column=1, padx=5, pady=5)

        # Search Type dropdown
        self.search_type_var = StringVar(self.root)
        self.search_type_var.set("contains")  # Default value
        search_type_options = ["startsWith", "endsWith", "contains", "content"]
        search_type_dropdown = OptionMenu(self.root, self.search_type_var, *search_type_options)
        search_type_dropdown.grid(row=2, column=0, padx=5, pady=5)

        # Search Button
        search_button = Button(self.root, text="Search", command=self.search_button_click)
        search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Result Listbox
        self.result_listbox = Listbox(self.root, width=80, height=10)
        self.result_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.result_listbox.yview)
        self.scrollbar.grid(row=4, column=2, sticky="ns")
        self.result_listbox.config(yscrollcommand=self.scrollbar.set)

if __name__ == '__main__':
    # Create the main window
    root = Tk()
    root.title("File Search Engine")

    # Create an instance of MainApp
    app = MainApp(root)

    # Start the main event loop
    root.mainloop()