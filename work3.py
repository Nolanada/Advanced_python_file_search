import docx
import os

# Function to search in .docx files
def search_in_docx(file_path, search_term):
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            if search_term.lower() in para.text.lower():
                return f"Found '{search_term}' in paragraph: {para.text}"
        return "Not found in .docx file."
    except Exception:
        return "Error reading .docx file."

# Function to search in .doc files (Windows only)
def search_in_doc(file_path, search_term):
    try:
        import win32com.client as win32
        word = win32.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        if search_term.lower() in doc.Content.Text.lower():
            return f"Found '{search_term}' in the document."
        return "Not found in .doc file."
    except Exception:
        return "Error reading .doc file."

# Main function to search based on file type
def search_in_file(file_path, search_term):
    if not os.path.exists(file_path):
        return "File does not exist!"
    
    ext = file_path.split('.')[-1].lower()
    if ext == 'docx':
        return search_in_docx(file_path, search_term)
    elif ext == 'doc':
        return search_in_doc(file_path, search_term)
    else:
        return "Unsupported file type."

# User input for file path and search term
file_path = input("Enter the file path: ")
search_term = input("Enter the search term: ")

# Call the function and show result
print(search_in_file(file_path, search_term))
