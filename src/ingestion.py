import os
import PyPDF2

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}")
        return ""

def process_all_pdfs():
    pdf_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".pdf")]
    
    if not pdf_files:
        print("No PDFs found in data/raw — drop your notification PDFs there first")
        return []

    documents = []
    for filename in pdf_files:
        path = os.path.join(RAW_DIR, filename)
        print(f"Processing: {filename}")
        text = extract_text_from_pdf(path)
        if text:
            documents.append({
                "filename": filename,
                "text": text
            })
            print(f"  Extracted {len(text)} characters")
        else:
            print(f"  Skipped — no text extracted")

    print(f"\nTotal documents processed: {len(documents)}")
    return documents

if __name__ == "__main__":
    process_all_pdfs()