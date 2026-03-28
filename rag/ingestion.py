import os
import re

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"


def ensure_dirs():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


def clean_text(text: str) -> str:
    """
    Structure-preserving cleaning:
    - Keep headings, bullets, rules
    - Remove extra whitespace and junk symbols
    - Normalize formatting
    """

    # Normalize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove weird non-text characters (but keep punctuation)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Trim
    text = text.strip()

    return text


def process_file(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned = clean_text(raw_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)


def run_ingestion():
    ensure_dirs()

    files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".txt")]

    for file in files:
        input_path = os.path.join(RAW_DATA_DIR, file)
        output_path = os.path.join(PROCESSED_DATA_DIR, file)

        process_file(input_path, output_path)
        print(f"Processed: {file}")


if __name__ == "__main__":
    run_ingestion()