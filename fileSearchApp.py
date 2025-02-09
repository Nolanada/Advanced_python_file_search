import os
import json
from PyPDF2 import PdfFileReader
from docx import Document
import sqlite3

#CACHE_FILE = "search_cache.json"
CACHE_FILE="cache.db"


class Filesearch:
    # Define cache file path

    def __init__(self):
        self.cache = CACHE_FILE # Read the search cache from the json file
        #connecting to the db and creating the cursor
        self.conn = sqlite3.connect(self.cache)
        self.cursor=self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                results TEXT
            )
        ''')


    def read_cache(self):
        # Read the search cache from the json file
        """try:
            with open(CACHE_FILE, 'r', encoding='UTF-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}"""
        self.cursor.execute('SELECT key, results FROM cache')
        rows = self.cursor.fetchall()
        for row in rows:
            self.cache[row[0]] = row[1].split(';')
        return self.cache
        


    def write_cache(self,key,results):
        # Write the search cache to the JSON file
        '''with open(CACHE_FILE, 'w', encoding='UTF-8') as f:
            json.dump(self.cache, f, indent=4)'''
        self.cursor.execute('INSERT OR REPLACE INTO cache (key, results) VALUES (?, ?)', (key, ';'.join(results)))
        self.conn.commit()

    def search_file(self,root_dir, search_term,search_type="contains"):
        # Perform file search based on search type

        result = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if search_type == "startsWith" and filename.startswith(search_term):
                    result.append(filepath)
                elif search_type == "endsWith" and filename.endswith(search_term):
                    result.append(filepath)
                elif search_type == "contains" and search_term in filename:
                    result.append(filepath)
                elif search_type == "content":
                    try:
                        if self.search_in_file(filepath, search_term):
                            result.append(filepath)
                    except UnicodeDecodeError:
                        pass # Skip files that are not be read
        return result

    def search_in_file(self,filepath, search_term):
        if filepath.endswith('.txt'):
            return self.search_in_txt(filepath, search_term)
        elif filepath.endswith('.pdf'):
            return self.search_in_pdf(filepath, search_term)
        elif filepath.endswith('.docx'):
            return self.search_in_docx(filepath, search_term)
        return False

    def search_in_txt(self,filepath, search_term):
        try:
            with open(filepath, 'r', encoding='UTF-8') as f:
                return search_term in f.read()
        except UnicodeDecodeError:
            return False

    def search_in_pdf(self,filepath, search_term):
        try:
            with open(filepath, 'rb') as f:
                reader = PdfFileReader(f)
                for page_num in range(reader.numPages):
                    page = reader.getPage(page_num)
                    if search_term in page.extract_text():
                        return True
        except Exception:
            return False
        return False

    def search_in_docx(self,filepath, search_term):
        try:
            doc = Document(filepath)
            for paragraph in doc.paragraphs:
                if search_term in paragraph.text:
                    return True
        except Exception:
            return False
        return False
    '''def main(self):
        # this function handles user interaction
        cache = self.read_cache()
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

            cache_key = f"{root_dir}_{search_term}_{choice}"
            if cache_key in cache:
                print("Result found in cache:")
                for result in cache[cache_key]:
                    print(result)
            else:
                search_type = ["startsWith", "endsWith", "contains", "content"][choice - 1]
                print("Loading search...")
                results = search_file(root_dir, search_term, search_type)
                print("Search results")
                for result in results:
                    print(result)
                cache[cache_key] = results
                write_cache(cache)

    if __name__ == "__main__":
        main()'''