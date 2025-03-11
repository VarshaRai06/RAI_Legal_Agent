import os
import json
import re

# Paths
PROCESSED_DIR = "data/processed"
CHUNKED_DIR = "data/chunks"

os.makedirs(CHUNKED_DIR, exist_ok=True)

# Updated regex pattern for section headings
SECTION_PATTERN = r"\n\d+\.\s[A-Za-z ,()'-]+?\.\u2014"

def split_text_by_sections(text):
    """Splits legal text into chunks based on section titles."""
    sections = re.split(SECTION_PATTERN, text)  # Split at detected section headings
    print("Number of sections:", len(sections))

    section_titles = re.findall(SECTION_PATTERN, text)
    print("Number of titles:", len(section_titles))

    # # Print extracted section titles
    # print("Section Titles:")
    # for title in section_titles:
    #     print(title.strip())

    chunks = []
    for i, section in enumerate(sections):
        if i < len(section_titles):
            cleaned_title = section_titles[i].strip()
            chunk = f"{cleaned_title}\n{section.strip()}"
            chunks.append(chunk)
        else:
            chunks.append(section.strip())

    return chunks


def process_json(file_path, output_file):
    """Loads extracted text JSON, chunks it by sections"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunked_data = {}

    for doc_name, text in data.items():
        print(f"🔹 Splitting {doc_name} into sections...")
        sections = split_text_by_sections(text)
        chunked_data[doc_name] = sections

    # Save chunked data
    output_path = os.path.join(CHUNKED_DIR, output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunked_data, f, indent=4)

    print(f"✅ Chunked data saved to: {output_path}")

if __name__ == "__main__":
    print("🔹 Processing Civil Law data...")
    process_json(os.path.join(PROCESSED_DIR, "civil_laws.json"), "civil_laws_chunks.json")

    print("🔹 Processing Criminal Law data...")
    process_json(os.path.join(PROCESSED_DIR, "criminal_laws.json"), "criminal_laws_chunks.json")
