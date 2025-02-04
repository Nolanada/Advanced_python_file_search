# THE FULL APPLICATION IS ON THE MAIN BRANCH

# The cache is stored in a JSON file (search_cache.json)


# PYTHON FILE SEARCH ENGINE
# TERMINAL APPLICATION (More Stable) IN main.py file
# interface APPLICATION IN fileSearchapp.py file

# File Search Engine

## Overview
The File Search Engine is a Python application that allows users to search for files within a specified directory. It supports searching by filename (starts with, ends with, contains) and by file content. The application can search through text files (`.txt`), PDF files (`.pdf`), and Word documents (`.docx`).

## Features
- Search by filename (starts with, ends with, contains)
- Search by file content
- Supports `.txt`, `.pdf`, and `.docx` file formats
- Caching of search results to improve performance

## Requirements
- Python 3.6 or higher
- `PyPDF2` library
- `python-docx` library
- `tkinter` library (usually included with Python)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Nolanada/Advanced_python_file_search.git
    cd filesearchengine
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```sh
    python main.py
    ```

2. The main window of the application will appear.

3. Enter the search term in the "Search Term" field.

4. Enter the root directory to search in the "Root Directory" field.

5. Select the search type from the dropdown menu:
    - `startsWith`: Search for files whose names start with the search term.
    - `endsWith`: Search for files whose names end with the search term.
    - `contains`: Search for files whose names contain the search term.
    - `content`: Search for files whose content contains the search term.

6. Click the "Search" button to start the search.

7. The search results will be displayed in the listbox. If the results are found in the cache, a message will be shown.

## File Structure
- [main.py]: The main application file that contains the GUI and handles user interactions.
- [fileSearchApp.py]: Contains the `Filesearch` class that performs the file search operations.
- `requirements.txt`: Lists the required Python packages.

## Example
Here is an example of how to use the application:

1. Open the application by running `python main.py`.
2. Enter `wordtest` in the "Search Term" field.
3. Enter `C:\Users\Directory\Documents` in the "Root Directory" field.
4. Select `contains` from the dropdown menu.
5. Click the "Search" button.
6. The application will search for files in the specified directory that contain `example` in their names or content and display the results.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
If you have any questions or issues, please open an issue on the GitHub repository or contact the project maintainer at mbeumobriand@gmail.com.