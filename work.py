import os

def search_files(directory, search_name=None, search_content=None):
    matches = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check for name or content match
            if (search_name and search_name.lower() not in file.lower()) or \
               (search_content and not file_contains_content(os.path.join(root, file), search_content)):
                continue
            matches.append(os.path.join(root, file))

    return matches


def file_contains_content(file_path, search_content):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return search_content.lower() in f.read().lower()
    except Exception:
        return False


def get_search_query():
    search_type = input("Search by 'name' or 'content'? ").strip().lower()

    if search_type == 'name':
        return input("Enter file name (or part): ").strip(), None
    elif search_type == 'content':
        return None, input("Enter content to search for: ").strip()
    else:
        print("Invalid input, please try again.")
        return get_search_query()


def main():
    directory = input("Enter the directory to search in: ").strip()
    search_name, search_content = get_search_query()

    results = search_files(directory, search_name, search_content)

    if results:
        print("\nFound these files:")
        print("\n".join(results))
    else:
        print("No files found.")


if __name__ == "__main__":
    main()