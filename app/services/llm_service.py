# import google.generativeai as genai

# from app.core.config import settings


# class LLMService:

#     def __init__(self):

#         genai.configure(
#             api_key=settings.GOOGLE_API_KEY
#         )

#         self.model = genai.GenerativeModel(
#             settings.LLM_MODEL
#         )

#     def generate_answer(
#         self,
#         question: str,
#         context: str
#     ):

#         prompt = f"""
# You are an expert Python tutor.

# Use ONLY the provided Stack Overflow context.

# Give a direct answer first.

# Rules:
# - Maximum 10 lines.
# - Prefer code examples.
# - Do not explain unnecessary details.
# - Use bullet points only when required.
# - Be concise and practical.

# If the answer is not present in the context, say:

# "I could not find a reliable answer in the knowledge base."

# Context:
# {context}

# Question:
# {question}

# Answer:
# """

#         response = self.model.generate_content(
#             prompt
#         )

#         return response.text


import google.generativeai as genai

from app.core.config import settings


class LLMService:

    def __init__(self):

        genai.configure(
            api_key=settings.GOOGLE_API_KEY
        )

        self.model = genai.GenerativeModel(
            settings.LLM_MODEL
        )

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = f"""
You are an expert Python tutor.

Use ONLY the provided Stack Overflow context.

Rules:
- Give a direct answer first.
- Maximum 10 lines.
- Prefer code examples.
- Do not explain unnecessary details.
- Be concise and practical.
- Do not make up information.
- If code exists in the context, prefer using that code.

If the answer cannot be found in the context, respond exactly:

I could not find a reliable answer in the knowledge base.

==================================================
CONTEXT
==================================================

{context}

==================================================
QUESTION
==================================================

{question}

==================================================
ANSWER
==================================================
"""

        response = self.model.generate_content(
                   prompt,
        generation_config={
                "temperature": 0.2,
                "max_output_tokens": 1024,
        }
    )

        print("=" * 80)
        print(response)
        print("=" * 80)

        return response.text