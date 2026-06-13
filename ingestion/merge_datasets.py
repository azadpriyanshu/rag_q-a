
from pathlib import Path
from tqdm import tqdm
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

QUESTIONS_FILE = BASE_DIR / "data/raw/Questions.csv"
ANSWERS_FILE = BASE_DIR / "data/raw/Answers.csv"
TAGS_FILE = BASE_DIR / "data/raw/Tags.csv"

OUTPUT_FILE = BASE_DIR / "data/processed/python_questions.parquet"


def load_python_question_ids():
    print("Loading Python question IDs...")

    tags_df = pd.read_csv(
        TAGS_FILE,
        encoding_errors="ignore"
    )

    python_ids = set(
        tags_df.loc[
            tags_df["Tag"].str.lower() == "python",
            "Id"
        ].unique()
    )

    print(f"Found {len(python_ids):,} Python questions")

    return python_ids, tags_df


def build_tags_mapping(tags_df):
    print("Building tag mappings...")

    return (
        tags_df
        .groupby("Id")["Tag"]
        .apply(list)
        .to_dict()
    )


def load_python_questions(python_ids):
    print("Loading questions...")

    question_chunks = []

    for chunk in tqdm(
        pd.read_csv(
            QUESTIONS_FILE,
            chunksize=50000,
            encoding_errors="ignore"
        ),
        desc="Questions"
    ):

        filtered_chunk = chunk[
            chunk["Id"].isin(python_ids)
        ]

        if not filtered_chunk.empty:
            question_chunks.append(filtered_chunk)

    questions_df = pd.concat(
        question_chunks,
        ignore_index=True
    )

    print(
        f"Filtered questions: {len(questions_df):,}"
    )

    return questions_df


def load_best_answers(python_ids):
    """
    Keep only the highest scored answer
    for every Python question.
    """

    print("Loading best answers...")

    best_answers = {}

    for chunk in tqdm(
        pd.read_csv(
            ANSWERS_FILE,
            chunksize=50000,
            encoding_errors="ignore"
        ),
        desc="Answers"
    ):

        chunk = chunk[
            chunk["ParentId"].isin(python_ids)
        ]

        if chunk.empty:
            continue

        for _, row in chunk.iterrows():

            qid = row["ParentId"]

            current_score = row["Score"]

            if pd.isna(current_score):
                current_score = 0

            if (
                qid not in best_answers
                or current_score > best_answers[qid]["score"]
            ):
                best_answers[qid] = {
                    "score": current_score,
                    "body": str(row["Body"])
                }

    print(
        f"Best answers found for "
        f"{len(best_answers):,} questions"
    )

    return best_answers


def merge_data(
    questions_df,
    best_answers,
    tag_map
):
    print("Creating final dataset...")

    records = []

    for _, row in tqdm(
        questions_df.iterrows(),
        total=len(questions_df),
        desc="Merging"
    ):

        qid = row["Id"]

        answer_data = best_answers.get(
            qid,
            {"score": 0, "body": ""}
        )

        records.append(
            {
                "question_id": qid,
                "title": str(row["Title"]),
                "question_body": str(row["Body"]),
                "question_score": row["Score"],
                "best_answer": answer_data["body"],
                "answer_score": answer_data["score"],
                "tags": tag_map.get(qid, [])
            }
        )

    return pd.DataFrame(records)


def main():

    python_ids, tags_df = (
        load_python_question_ids()
    )

    tag_map = build_tags_mapping(
        tags_df
    )

    questions_df = load_python_questions(
        python_ids
    )

    best_answers = load_best_answers(
        python_ids
    )

    final_df = merge_data(
        questions_df,
        best_answers,
        tag_map
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    final_df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("=" * 60)
    print("Dataset created successfully")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Rows: {len(final_df):,}")
    print(f"Columns: {len(final_df.columns)}")
    print("=" * 60)


if __name__ == "__main__":
    main()

