import os
import fnmatch
from datetime import datetime

# Cache to store search results
search_cache = {}

def update_cache(cache_key, results):
    """Update the cache with new results."""
    search_cache[cache_key] = results
    print(f"Cache updated for key: {cache_key}")

def create_cache_key(directory, file_name=None, file_type=None, creation_date=None):
    """Create a unique cache key based on search criteria."""
    return f"{directory}|{file_name}|{file_type}|{creation_date}"

def search_files(directory, file_name=None, file_content=None, file_type=None, creation_date=None):
    # Create a unique cache key based on search criteria
    cache_key = create_cache_key(directory, file_name, file_type, creation_date)
    
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
                    with open(full_path, 'r', errors='ignore') as file:
                        if file_content not in file.read():
                            continue
                except Exception as e:
                    print(f"Could not read file {full_path}: {e}")
                    continue

            results.append(full_path)

    # Store results in cache
    update_cache(cache_key, results)
    return results

def search_folders(directory, folder_name=None, creation_date=None):
    # Create a unique cache key based on search criteria
    cache_key = create_cache_key(directory, folder_name, None, creation_date)

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
    update_cache(cache_key, results)
    return results

if __name__ == "__main__":
    # Example usage
    search_directory = input("Enter the directory to search: ")

    # Searching for files
    files = search_files(search_directory, file_name='*.txt', file_content='example', file_type='.txt', creation_date=datetime(2023, 1, 1).date())
    print("Found files:", files)

    # Searching for folders
    folders = search_folders(search_directory, folder_name='*my_folder*', creation_date=datetime(2023, 1, 1).date())
    print("Found folders:", folders)