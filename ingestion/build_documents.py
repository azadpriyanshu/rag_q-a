from pathlib import Path
import pandas as pd
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/processed/cleaned_questions.parquet"
OUTPUT_FILE = BASE_DIR / "data/processed/documents.parquet"


def create_document(row):

    tags = ", ".join(
        [str(tag) for tag in row["tags"]]
    )

    document = f"""
Title:
{row["title"]}

Tags:
{tags}

Question:
{row["question_body_clean"]}

Answer:
{row["best_answer_clean"]}
""".strip()

    return document


def main():

    print("Loading cleaned dataset...")

    df = pd.read_parquet(INPUT_FILE)

    tqdm.pandas()

    print("Building retrieval documents...")

    df["document"] = (
        df.progress_apply(
            create_document,
            axis=1
        )
    )

    output_df = df[
        [
            "question_id",
            "title",
            "document",
            "question_score",
            "answer_score",
            "tags"
        ]
    ]

    output_df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("=" * 50)
    print(f"Saved: {OUTPUT_FILE}")
    print(f"Rows: {len(output_df):,}")
    print("=" * 50)


if __name__ == "__main__":
    main()