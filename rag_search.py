import os
import json

import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

VECTOR_DB_FOLDER = "vector_db"

INDEX_FILE = os.path.join(
    VECTOR_DB_FOLDER,
    "insurance_policies.index"
)

METADATA_FILE = os.path.join(
    VECTOR_DB_FOLDER,
    "metadata.json"
)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# LOAD RAG DATABASE
# ============================================================

def load_rag_database():

    print(
        "Loading FAISS vector database..."
    )

    index = faiss.read_index(
        INDEX_FILE
    )

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    print(
        f"Loaded {index.ntotal} vectors."
    )

    return index, metadata


# ============================================================
# SEARCH POLICY DOCUMENTS
# ============================================================

def search_policy(
    query,
    top_k=3
):

    index, metadata = (
        load_rag_database()
    )

    print(
        "\nLoading embedding model..."
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    # ========================================================
    # CREATE QUERY EMBEDDING
    # ========================================================

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype(
        "float32"
    )

    # Normalize query embedding
    # for cosine similarity.
    faiss.normalize_L2(
        query_embedding
    )

    # ========================================================
    # FAISS SEARCH
    # ========================================================

    similarities, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for similarity, index_id in zip(
        similarities[0],
        indices[0]
    ):

        if index_id == -1:
            continue

        chunk = metadata[index_id]

        results.append(
            {
                "filename":
                    chunk["filename"],

                "chunk_id":
                    chunk["chunk_id"],

                "similarity":
                    round(
                        float(similarity),
                        4
                    ),

                "text":
                    chunk["text"]
            }
        )

    return results


# ============================================================
# MAIN SEARCH INTERFACE
# ============================================================

def main():

    print(
        "\n===================================="
    )

    print(
        "      INSURANCE POLICY RAG SEARCH"
    )

    print(
        "===================================="
    )

    query = input(
        "\nEnter your policy question: "
    ).strip()

    if not query:

        print(
            "Please enter a question."
        )

        return

    results = search_policy(
        query,
        top_k=3
    )

    print(
        "\n========== RETRIEVED POLICY SECTIONS =========="
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n--- Result {i} ---"
        )

        print(
            f"Source: {result['filename']}"
        )

        print(
            f"Chunk ID: {result['chunk_id']}"
        )

        print(
            f"Cosine Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            "\nPolicy Text:"
        )

        print(
            result["text"]
        )

        print(
            "-" * 60
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()