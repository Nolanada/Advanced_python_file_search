from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, StringVar, OptionMenu
from tkinter.messagebox import showinfo
import os
import json
import time

#Define cache file path
CACHE_FILE = "search_cache.json"

# Function to read cache from file
def read_cache():
    # Read the search cache from the json file
    try:
        with open(CACHE_FILE, 'r', encoding='UTF-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to write cache from file
def write_cache(cache):
    # Write the search cache to the JSON file
    with open(CACHE_FILE, 'w', encoding='UTF-8') as f:
        json.dump(cache, f, indent=4)

# Function to perform file search 
def search_file(root_dir, search_term, search_type="contains"):
    # Perform file search based on search type
    result = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if search_type == "startsWith":
                if filename.startswith(search_term):
                    result.append(filepath)
            elif search_type == "endsWith":
                if filename.endswith(search_term):
                    result.append(filepath)
            elif search_type == "contains":
                if search_term in filename:
                    result.append(filepath)
            elif search_type == "content":
                try:
                    with open(filepath, 'r') as f:
                        if search_term in f.read():
                            result.append(filepath)
                except UnicodeDecodeError:
                    pass # Skip files that are not be read
    return result

def search_button_click():
    # handle the search button click event
    search_term = search_entry.get()
    root_dir = root_dir_entry.get()
    search_type = search_type_var.get()

    # Check if search result are cached
    cache_key = f"{root_dir}_{search_term}_{search_type}"
    if cache_key in cache:
        showinfo("Search Results", "Results found in cache\n".join(cache[cache_key]))
    else:
        results = search_file(root_dir, search_term, search_type)
        result_listbox.delete(0, 'end') # Clear previous results
        for result in results:
            result_listbox.insert('end', result)
            #update the cache
            cache[cache_key] = result
            write_cache(cache)


if __name__ == '__main__':
    cache = read_cache()

    # Create the main window
    root = Tk()
    root.title("File Search Engine")

    # Search term label and Entry
    search_term_label = Label(root, text="Search Term")
    search_term_label.grid(row=0, column=0, padx=5, pady=5)
    search_entry = Entry(root, width=50)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # Root directory label and entry
    root_dir_label = Label(root, text="Root Directory:")
    root_dir_label.grid(row=1, column=0, padx=5, pady=5)
    root_dir_entry = Entry(root, width=50)
    root_dir_entry.grid(row=1, column=1, padx=5, pady=5)

    # Search Type dropdown
    search_type_var = StringVar(root)
    search_type_var.set("contains") # Default value
    search_type_options = ["startsWith", "endsWith", "contains", "content"]
    search_type_dropdown = OptionMenu(root, search_type_var, *search_type_options)
    search_type_dropdown.grid(row=2, column=0, padx=5, pady=5)

    # Search Button
    search_button = Button(root, text="Search", command=search_button_click)
    search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Result Listbox
    result_listbox = Listbox(root, width=80, height=10)
    result_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    scrollbar = Scrollbar(root, orient="vertical", command=result_listbox.yview)
    scrollbar.grid(row=4, column=2, sticky="ns")
    result_listbox.config(yscrollcommand=scrollbar.set)

    root.mainloop()
    