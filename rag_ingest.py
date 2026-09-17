import os
import json
import re

import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

POLICY_FOLDER = "policies"
VECTOR_DB_FOLDER = "vector_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

MAX_CHUNK_SIZE = 1200


# ============================================================
# LOAD POLICY DOCUMENTS
# ============================================================

def load_documents():

    documents = []

    for filename in sorted(
        os.listdir(POLICY_FOLDER)
    ):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(
            POLICY_FOLDER,
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        documents.append(
            {
                "filename": filename,
                "text": text
            }
        )

    return documents


# ============================================================
# SPLIT DOCUMENT INTO SECTIONS
# ============================================================

def split_into_sections(text):

    """
    Split the document using numbered headings.

    Example:

    2. ACCIDENTAL DAMAGE COVERAGE
    3. THEFT COVERAGE
    4. FIRE AND NATURAL CALAMITY COVERAGE
    """

    pattern = r"(?=\n\d+\.\s+[A-Z])"

    sections = re.split(
        pattern,
        text
    )

    sections = [
        section.strip()
        for section in sections
        if section.strip()
    ]

    return sections


# ============================================================
# SPLIT LARGE SECTIONS
# ============================================================

def split_large_section(text):

    """
    Split large sections at paragraph boundaries.

    This prevents sentences from being cut in the middle.
    """

    if len(text) <= MAX_CHUNK_SIZE:

        return [text]

    paragraphs = re.split(
        r"\n\s*\n",
        text
    )

    chunks = []

    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # If adding the next paragraph would exceed
        # the maximum size, save the current chunk.
        if (
            current_chunk
            and len(current_chunk)
            + len(paragraph)
            + 2
            > MAX_CHUNK_SIZE
        ):

            chunks.append(
                current_chunk.strip()
            )

            current_chunk = paragraph

        else:

            if current_chunk:

                current_chunk += "\n\n"

            current_chunk += paragraph

    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )

    return chunks


# ============================================================
# CREATE RAG CHUNKS
# ============================================================

def create_chunks(documents):

    chunks = []

    for document in documents:

        sections = split_into_sections(
            document["text"]
        )

        for section in sections:

            section_chunks = split_large_section(
                section
            )

            for section_chunk in section_chunks:

                chunks.append(
                    {
                        "chunk_id": len(chunks),

                        "filename":
                            document["filename"],

                        "text":
                            section_chunk
                    }
                )

    return chunks


# ============================================================
# CREATE FAISS VECTOR DATABASE
# ============================================================

def create_vector_database(chunks):

    print("\nLoading embedding model...")

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print(
        f"Creating embeddings for "
        f"{len(texts)} chunks..."
    )

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = embeddings.astype(
        "float32"
    )

    # ========================================================
    # COSINE SIMILARITY
    # ========================================================

    # Normalize document embeddings.
    faiss.normalize_L2(
        embeddings
    )

    dimension = embeddings.shape[1]

    # Inner Product on normalized vectors
    # is equivalent to cosine similarity.
    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    # ========================================================
    # SAVE DATABASE
    # ========================================================

    os.makedirs(
        VECTOR_DB_FOLDER,
        exist_ok=True
    )

    index_path = os.path.join(
        VECTOR_DB_FOLDER,
        "insurance_policies.index"
    )

    metadata_path = os.path.join(
        VECTOR_DB_FOLDER,
        "metadata.json"
    )

    faiss.write_index(
        index,
        index_path
    )

    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    print(
        "\n========== RAG INGESTION COMPLETE =========="
    )

    print(
        f"Documents loaded: {len(documents)}"
    )

    print(
        f"Total chunks: {len(chunks)}"
    )

    print(
        f"Embedding dimension: {dimension}"
    )

    print(
        "\nSimilarity metric: Cosine Similarity"
    )

    print(
        "\nVector database saved to:"
    )

    print(
        index_path
    )

    print(
        metadata_path
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    documents = load_documents()

    print(
        f"Documents found: {len(documents)}"
    )

    for document in documents:

        print(
            f"- {document['filename']}"
        )

    chunks = create_chunks(
        documents
    )

    print(
        f"\nTotal chunks created: {len(chunks)}"
    )

    create_vector_database(
        chunks
    )