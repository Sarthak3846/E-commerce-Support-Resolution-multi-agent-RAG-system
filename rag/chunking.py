import os
import json

PROCESSED_DIR = "data/processed"
CHUNKED_OUTPUT = "data/chunks.json"

CHUNK_SIZE = 450
OVERLAP = 50


def load_documents():
    docs = []

    for file in os.listdir(PROCESSED_DIR):
        if file.endswith(".txt"):
            path = os.path.join(PROCESSED_DIR, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            docs.append({
                "text": text,
                "source": file
            })

    return docs


def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    words = text.split()
    chunks = []

    start = 0
    n = len(words)

    while start < n:
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        start += chunk_size - overlap

    return chunks


def create_chunks():
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = split_into_chunks(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{doc['source']}_chunk_{i}",
                "text": chunk,
                "source": doc["source"]
            })

    return all_chunks


def save_chunks(chunks):
    os.makedirs("data", exist_ok=True)

    with open(CHUNKED_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)


def run_chunking():
    chunks = create_chunks()
    save_chunks(chunks)

    print(f"Total chunks created: {len(chunks)}")


if __name__ == "__main__":
    run_chunking()