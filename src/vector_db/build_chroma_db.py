from pathlib import Path
import json

import chromadb
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[2]

EMBEDDING_DIR = BASE_DIR / "embedding_output" / "embedding_output"
CHROMA_DIR = BASE_DIR / "vector_db" / "chroma"

EMBEDDING_PATH = EMBEDDING_DIR / "embeddings_text_embedding_3_large.npy"
METADATA_PATH = EMBEDDING_DIR / "chunks_metadata.jsonl"


def main():
    embeddings = np.load(EMBEDDING_PATH).astype("float32")

    chunks = []

    with METADATA_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    print("Embeddings:", embeddings.shape)
    print("Chunks:", len(chunks))

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = client.get_or_create_collection(
        name="legal_chunks",
        metadata={"hnsw:space": "cosine"},
    )

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        base_id = chunk.get("chunk_id") or "chunk"

        ids.append(f"{i:06d}__{base_id}")

        documents.append(chunk.get("child_text") or "")

        metadatas.append({
            "source_file": chunk.get("source_file") or "",
            "article": chunk.get("article") or "",
            "heading": chunk.get("heading") or "",
            "child_label": chunk.get("child_label") or "",
            "chunk_strategy": chunk.get("chunk_strategy") or "",
            "parent_text": chunk.get("parent_text") or "",
        })

    bad_ids = [item for item in ids if not isinstance(item, str)]
    print("Bad ids:", len(bad_ids))
    print("First bad ids:", bad_ids[:5])

    BATCH_SIZE = 500

    for start in range(0, len(chunks), BATCH_SIZE):
        end = start + BATCH_SIZE

        collection.upsert(
            ids=ids[start:end],
            documents=documents[start:end],
            embeddings=embeddings[start:end].tolist(),
            metadatas=metadatas[start:end],
        )

        print(f"Added {min(end, len(chunks))}/{len(chunks)}")

    print("Total in Chroma:", collection.count())


if __name__ == "__main__":
    main()