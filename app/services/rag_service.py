# from app.services.retrieval_service import (
#     RetrievalService
# )

# from app.services.llm_service import (
#     LLMService
# )

# from app.core.config import settings

# from app.core.logging import logger


# class RAGService:

#     def __init__(self):

#         self.retriever = RetrievalService()

#         self.llm = LLMService()

#         self.similarity_threshold = (
#             settings.SIMILARITY_THRESHOLD
#         )

#         self.max_context_chars = (
#             settings.MAX_CONTEXT_CHARS
#         )

#     def ask(
#         self,
#         question: str,
#         top_k: int = 5
#     ) -> dict:

#         logger.info(
#             f"Question received: {question}"
#         )

#         docs = self.retriever.retrieve(
#             question=question,
#             top_k=top_k
#         )

#         docs = [
#             doc
#             for doc in docs
#             if doc["score"]
#             >= self.similarity_threshold
#         ]

#         logger.info(
#             f"Retrieved {len(docs)} relevant documents"
#         )

#         if not docs:

#             return {
#                 "question": question,
#                 "answer": (
#                     "I could not find a reliable answer "
#                     "in the knowledge base."
#                 ),
#                 "sources": []
#             }

#         context_parts = []

#         current_length = 0

#         for doc in docs:

#             chunk = (
#                 f"Title: {doc['title']}\n\n"
#                 f"{doc['document']}\n\n"
#                 f"{'=' * 50}\n"
#             )

#             if (
#                 current_length + len(chunk)
#                 > self.max_context_chars
#             ):
#                 break

#             context_parts.append(
#                 chunk
#             )

#             current_length += len(
#                 chunk
#             )

#         context = "\n".join(
#             context_parts
#         )

#         logger.info(
#             f"Context Length: {len(context)}"
#         )

#         try:

#             answer = self.llm.generate_answer(
#                 question=question,
#                 context=context
#             )

#             if (
#                 not answer
#                 or not answer.strip()
#             ):

#                 answer = (
#                     "I could not generate a response "
#                     "from the retrieved documents."
#                 )

#         except Exception as e:

#             logger.exception(
#                 f"LLM generation failed: {e}"
#             )

#             answer = (
#                 "An error occurred while generating "
#                 "the response."
#             )

#         return {
#             "question": question,
#             "answer": answer,
#             "sources": [
#                 {
#                     "title": doc["title"],
#                     "score": round(
#                         float(doc["score"]),
#                         4
#                     )
#                 }
#                 for doc in docs[:3]
#             ]
#         }


from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.core.config import settings
from app.core.logging import logger


class RAGService:

    def __init__(self):

        self.retriever = RetrievalService()
        self.llm = LLMService()

        self.similarity_threshold = settings.SIMILARITY_THRESHOLD
        self.max_context_chars = settings.MAX_CONTEXT_CHARS

    def ask(self, question: str, top_k: int = 5) -> dict:

        logger.info(f"Question received: {question}")

        # 1. Retrieve docs
        docs = self.retriever.retrieve(
            question=question,
            top_k=top_k
        )

        # 2. Safe filtering + cleanup
        clean_docs = []
        for doc in docs:
            try:
                score = float(doc.get("score", 0))

                if score >= self.similarity_threshold:
                    clean_docs.append({
                        "title": doc.get("title", "Unknown Title"),
                        "document": doc.get("document", ""),
                        "score": score
                    })
            except Exception:
                continue

        # 3. Sort by score (VERY IMPORTANT)
        clean_docs = sorted(
            clean_docs,
            key=lambda x: x["score"],
            reverse=True
        )

        logger.info(f"Retrieved {len(clean_docs)} relevant documents")

        if not clean_docs:
            return {
                "question": question,
                "answer": (
                    "I could not find relevant information "
                    "in the knowledge base for this question."
                ),
                "sources": []
            }

        # 4. Build better context (critical improvement)
        context_parts = []
        current_length = 0

        for doc in clean_docs:

            chunk = (
                f"SOURCE TITLE: {doc['title']}\n"
                f"CONTENT:\n{doc['document']}\n"
                f"---\n"
            )

            if current_length + len(chunk) > self.max_context_chars:
                continue

            context_parts.append(chunk)
            current_length += len(chunk)

        context = "\n".join(context_parts)

        logger.info(f"Context Length: {len(context)}")

        # 5. Stronger prompt discipline (VERY IMPORTANT FIX)
        enhanced_context = f"""
You are a helpful AI assistant.

Answer the question ONLY using the context below.
If the context is not enough, say you don't have enough information.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

        # 6. Generate answer safely
        try:
            answer = self.llm.generate_answer(
                question=question,
                context=enhanced_context
            )

            if not answer or not answer.strip():
                answer = (
                    "I could not generate a proper answer "
                    "from the available documents."
                )

        except Exception as e:
            logger.exception(f"LLM generation failed: {e}")
            answer = (
                "An error occurred while generating the response."
            )

        # 7. Return top sources
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "title": doc["title"],
                    "score": round(doc["score"], 4)
                }
                for doc in clean_docs[:3]
            ]
        }