from app.services.llm_service import LLMService

llm = LLMService()

response = llm.generate_answer(
    question="How do I read a CSV file using pandas?",
    context="""
Pandas can read CSV files using:

import pandas as pd

df = pd.read_csv("data.csv")
"""
)

print(response)