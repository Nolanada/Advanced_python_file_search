""" A FILE SEARCH ENGINE APP WITH PYTHON """
import os
import json

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


# Main Function
def main():
    # this function handles user interaction
    cache = read_cache()
    while True:
        print("\n Search Options:")
        print("1. Search by filename (startWith)")
        print("2. Search by filename (endsWith)")
        print("3. Search by filename (contains)")
        print("4. Search by file content")
        print("5. Exit")

        choice = int(input("Enter your choice (1-5): "))
        if choice == 5:
            break

        search_term = input("Enter Search Term: ")
        root_dir = input("Enter root directory to search: ")

        #check if search result are cached 
        cache_key = f"{root_dir}_{search_term}_{choice}"
        if cache_key in cache:
            print("Result found in cache:")
            for result in cache[cache_key]:
                print(result)
        else:
            if choice == 1:
                search_type = "startsWith"
            elif choice == 2:
                search_type = "endsWith"
            elif choice == 3:
                search_type = "contains"
            elif choice == 4:
                search_type = "content"
            else:
                print("Invalid choice.")
                continue

            print("Loading search...")
            results = search_file(root_dir, search_term, search_type)
            print("Search results")
            for result in results:
                print(result)
            # Then we update the cache
            cache[cache_key] = results
            write_cache(cache)


if __name__ == "__main__":
    main()