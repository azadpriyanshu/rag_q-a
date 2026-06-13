from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/processed/python_questions.parquet"
OUTPUT_FILE = BASE_DIR / "data/processed/cleaned_questions.parquet"


def clean_html(html_text):

    if pd.isna(html_text):
        return ""

    soup = BeautifulSoup(str(html_text), "lxml")

    # preserve code blocks
    for code in soup.find_all("code"):
        code.replace_with(
            f"\nCODE:\n{code.get_text()}\n"
        )

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    return text


def main():

    print("Loading parquet...")

    df = pd.read_parquet(INPUT_FILE)

    tqdm.pandas()

    print("Cleaning question bodies...")

    df["question_body_clean"] = (
        df["question_body"]
        .progress_apply(clean_html)
    )

    print("Cleaning answers...")

    df["best_answer_clean"] = (
        df["best_answer"]
        .progress_apply(clean_html)
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
    print("=" * 50)
    print("Cleaning completed")
    print(f"Saved: {OUTPUT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()