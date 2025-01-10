import os
import fnmatch
from datetime import datetime

# Cache to store search results
search_cache = {}

def search_files(directory, file_name=None, file_content=None, file_type=None, creation_date=None):
    cache_key = (directory, file_name, file_content, file_type, creation_date)
    
    # Check if results are already cached
    if cache_key in search_cache:
        print("Returning cached results...")
        return search_cache[cache_key]

    results = []

    # Walk through the directory
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            # Check file name
            if file_name and not fnmatch.fnmatch(filename, file_name):
                continue

            # Check file type
            if file_type and not filename.endswith(file_type):
                continue

            # Check creation date
            if creation_date:
                creation_time = os.path.getctime(full_path)
                creation_date_obj = datetime.fromtimestamp(creation_time).date()
                if creation_date_obj != creation_date:
                    continue

            # Check file content
            if file_content:
                try:
                    with open(full_path, 'rb', errors='ignore') as file:
                        if file_content not in file.read():
                            continue
                except Exception as e:
                    print(f"Could not read file {full_path}: {e}")
                    continue

            results.append(full_path)

    # Store results in cache
    search_cache[cache_key] = results
    return results

def search_folders(directory, folder_name=None, creation_date=None):
    cache_key = (directory, folder_name, creation_date)

    # Check if results are already cached
    if cache_key in search_cache:
        print("Returning cached results...")
        return search_cache[cache_key]

    results = []

    # Walk through the directory
    for dirpath, dirnames, _ in os.walk(directory):
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)

            # Check folder name
            if folder_name and not fnmatch.fnmatch(dirname, folder_name):
                continue

            # Check creation date
            if creation_date:
                creation_time = os.path.getctime(full_path)
                creation_date_obj = datetime.fromtimestamp(creation_time).date()
                if creation_date_obj != creation_date:
                    continue

            results.append(full_path)

    # Store results in cache
    search_cache[cache_key] = results
    return results

def display_menu():
    print("\nWelcome to the Advanced Search App!")
    print("Please choose an option:")
    print("1. Search for Files")
    print("2. Search for Folders")
    print("3. Exit")

def get_file_search_criteria():
    file_name = input("Enter file name pattern (e.g., *.txt) or press Enter to skip: ")
    file_content = input("Enter a keyword to search in file content or press Enter to skip: ")
    file_type = input("Enter file type (e.g., .txt) or press Enter to skip: ")
    creation_date_input = input("Enter creation date (YYYY-MM-DD) or press Enter to skip: ")

    creation_date = None
    if creation_date_input:
        creation_date = datetime.strptime(creation_date_input, "%Y-%m-%d").date()

    return file_name, file_content, file_type, creation_date

def get_folder_search_criteria():
    folder_name = input("Enter folder name pattern (e.g., *my_folder*) or press Enter to skip: ")
    creation_date_input = input("Enter creation date (YYYY-MM-DD) or press Enter to skip: ")

    creation_date = None
    if creation_date_input:
        creation_date = datetime.strptime(creation_date_input, "%Y-%m-%d").date()

    return folder_name, creation_date

if __name__ == "__main__":
    while True:
        display_menu()
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            search_directory = input("Enter the directory to search: ")
            file_name, file_content, file_type, creation_date = get_file_search_criteria()
            files = search_files(search_directory, file_name, file_content, file_type, creation_date)
            print("Found files:", files)

        elif choice == '2':
            search_directory = input("Enter the directory to search: ")
            folder_name, creation_date = get_folder_search_criteria()
            folders = search_folders(search_directory, folder_name, creation_date)
            print("Found folders:", folders)

        elif choice == '3':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
            