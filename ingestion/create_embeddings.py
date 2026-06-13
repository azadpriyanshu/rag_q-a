from pathlib import Path
import pickle
import time

import faiss
import numpy as np
import pandas as pd
import torch

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data/processed/final_documents.parquet"
)

INDEX_FILE = (
    BASE_DIR
    / "app/db/faiss/index.faiss"
)

METADATA_FILE = (
    BASE_DIR
    / "app/db/faiss/metadata.pkl"
)

MODEL_NAME = "BAAI/bge-small-en-v1.5"

# M2 Air 16GB
BATCH_SIZE = 1024


def get_device():

    if torch.backends.mps.is_available():
        return "mps"

    return "cpu"


def main():

    start_time = time.time()

    print("Loading documents...")

    df = pd.read_parquet(INPUT_FILE)

    documents = df["document"].tolist()

    print(f"Documents: {len(documents):,}")

    device = get_device()

    print(f"Using device: {device}")
    print(f"Loading model: {MODEL_NAME}")

    model = SentenceTransformer(
        MODEL_NAME,
        device=device
    )

    print("Creating FAISS index...")

    dimension = 384

    index = faiss.IndexFlatIP(
        dimension
    )

    total_batches = (
        len(documents) + BATCH_SIZE - 1
    ) // BATCH_SIZE

    print(
        f"Batch Size: {BATCH_SIZE}"
    )

    print(
        f"Total Batches: {total_batches}"
    )

    print(
        "Generating embeddings and building index..."
    )

    for start in tqdm(
        range(0, len(documents), BATCH_SIZE),
        total=total_batches,
        desc="Embedding"
    ):

        batch = documents[
            start:start + BATCH_SIZE
        ]

        batch_embeddings = model.encode(
            batch,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
            batch_size=64
        ).astype("float32")

        index.add(
            batch_embeddings
        )

    print(
        f"Vectors in index: {index.ntotal:,}"
    )

    INDEX_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("Saving FAISS index...")

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    print("Saving metadata...")

    metadata = df[
        [
            "question_id",
            "title",
            "document",
            "tags"
        ]
    ].to_dict(
        orient="records"
    )

    with open(
        METADATA_FILE,
        "wb"
    ) as f:

        pickle.dump(
            metadata,
            f,
            protocol=pickle.HIGHEST_PROTOCOL
        )

    total_time = (
        time.time() - start_time
    ) / 60

    print()
    print("=" * 60)
    print("FAISS index created successfully")
    print(f"Total vectors: {index.ntotal:,}")
    print(f"Index saved to: {INDEX_FILE}")
    print(f"Metadata saved to: {METADATA_FILE}")
    print(f"Time Taken: {total_time:.2f} mins")
    print("=" * 60)


if __name__ == "__main__":
    main()