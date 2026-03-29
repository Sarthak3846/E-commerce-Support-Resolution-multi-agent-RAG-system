import json
import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "data/chunks.json"
INDEX_PATH = "vector_store/faiss_index.bin"
METADATA_PATH = "vector_store/metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def create_embeddings(model, texts):
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    return embeddings


def build_faiss_index(embeddings):
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)  # L2 distance
    index.add(embeddings)

    return index


def save_index(index):
    os.makedirs("vector_store", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)


def save_metadata(chunks):
    metadata = []

    for i, chunk in enumerate(chunks):
        metadata.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "source": chunk["source"]
        })

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def run_embedding_pipeline():
    print("Loading chunks...")
    chunks = load_chunks()

    texts = [c["text"] for c in chunks]

    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")
    embeddings = create_embeddings(model, texts)

    print("Building FAISS index...")
    index = build_faiss_index(embeddings)

    print("Saving index...")
    save_index(index)

    print("Saving metadata...")
    save_metadata(chunks)

    print("Done.")


if __name__ == "__main__":
    run_embedding_pipeline()