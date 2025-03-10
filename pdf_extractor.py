import os
import fitz  # PyMuPDF for PDF extraction
import json

# Define paths
CIVIL_LAW_DIR = "data/civil_laws"
CRIMINAL_LAW_DIR = "data/criminal_laws"
OUTPUT_DIR = "data/processed"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file while preserving sections."""
    doc = fitz.open(pdf_path)
    text_data = []

    for page in doc:
        text = page.get_text("text")
        if text.strip():
            text_data.append(text.strip())

    return "\n".join(text_data)

def process_pdfs(input_dir, output_file):
    """Processes all PDFs in a directory and saves extracted text."""
    extracted_data = {}

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            print(f"📖 Processing: {filename}")

            extracted_text = extract_text_from_pdf(pdf_path)
            extracted_data[filename] = extracted_text

    # Save extracted text as JSON
    output_path = os.path.join(OUTPUT_DIR, output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)

    print(f"✅ Extracted text saved to: {output_path}")

if __name__ == "__main__":
    print("🔹 Extracting Civil Law PDFs...")
    process_pdfs(CIVIL_LAW_DIR, "civil_laws.json")

    print("🔹 Extracting Criminal Law PDFs...")
    process_pdfs(CRIMINAL_LAW_DIR, "criminal_laws.json")
