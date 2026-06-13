from app.repositories.vector_repository import (
    VectorRepository
)

repo = VectorRepository()

query = "How do I read a CSV file using pandas?"

results = repo.search(
    query=query,
    top_k=5
)

for i, result in enumerate(results, start=1):

    print()
    print("=" * 80)
    print(f"Result {i}")
    print("=" * 80)

    print("Score:", result["score"])
    print("Title:", result["title"])
    print("Tags:", result["tags"])

    print()

    print(
        result["document"][:1000]
    )