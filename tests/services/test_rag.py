# from app.services.rag_service import RAGService

# rag = RAGService()

# response = rag.ask(
#     "How do I sort a dataframe in pandas?"
# )

# print("\nQUESTION")
# print(response["question"])

# print("\nANSWER")
# print(response["answer"])

# print("\nSOURCES")

# for source in response["sources"]:
#     print(
#         f"\n{source['title']} "
#         f"({source['score']})"
#     )


from app.services.rag_service import (
    RAGService
)


def test_rag():

    rag = RAGService()

    result = rag.ask(
        "How do I read a CSV file?"
    )

    assert "answer" in result