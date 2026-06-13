from pathlib import Path
import pickle

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INDEX_FILE = (
    BASE_DIR / "app/db/faiss/index.faiss"
)

METADATA_FILE = (
    BASE_DIR / "app/db/faiss/metadata.pkl"
)

MODEL_NAME = "BAAI/bge-small-en-v1.5"


class VectorRepository:

    def __init__(self):

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            str(INDEX_FILE)
        )

        print("Loading metadata...")

        with open(
            METADATA_FILE,
            "rb"
        ) as f:

            self.metadata = pickle.load(f)

        print("Loading embedding model...")

        self.embedding_model = (
            SentenceTransformer(
                MODEL_NAME,
                device="mps"
            )
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        query_embedding = (
            self.embedding_model.encode(
                query,
                normalize_embeddings=True,
                convert_to_numpy=True
            )
            .astype("float32")
            .reshape(1, -1)
        )

        scores, indices = (
            self.index.search(
                query_embedding,
                top_k
            )
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            doc = self.metadata[idx]

            results.append(
                {
                    "score": float(score),
                    "question_id": doc["question_id"],
                    "title": doc["title"],
                    "document": doc["document"],
                    "tags": doc["tags"]
                }
            )

        return results