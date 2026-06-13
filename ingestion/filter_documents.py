from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/processed/documents.parquet"
OUTPUT_FILE = BASE_DIR / "data/processed/final_documents.parquet"

TOP_K_DOCUMENTS = 100_000


def main():

    print("Loading documents...")

    df = pd.read_parquet(INPUT_FILE)

    print(f"Original records: {len(df):,}")

    # Keep only answered questions
    df = df[
        df["answer_score"] > 0
    ]

    print(
        f"After answer_score filter: {len(df):,}"
    )

    # Sort by quality
    df = df.sort_values(
        by=["answer_score", "question_score"],
        ascending=False
    )

    # Keep top documents
    df = df.head(TOP_K_DOCUMENTS)

    print(
        f"Final selected documents: {len(df):,}"
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("=" * 60)
    print("Filtering completed")
    print(f"Saved: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()