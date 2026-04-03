import os
from PyPDF2 import PdfReader

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        print(f"Unsupported file type: {ext}")
        return ""
    
def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        if len(reader.pages) == 0:
            return None
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""   

def extract_all(docs_folder):
    results = []

    files = os.listdir(docs_folder)
    if len(files) == 0:
        print("No files found in the docs folder.")
        return results
    
    for filename in files:
        filePath = os.path.join(docs_folder, filename)
        if os.path.isdir(filePath):
            continue

        text = extract_text(filePath)

        results.append({
            "file": filename,
            "text": text
        })

        return results

if __name__ == "__main__":
    docs_folder = "./docs"
    results = extract_all(docs_folder)
    for r in results:
        print(r)