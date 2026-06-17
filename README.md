# Python Q&A Assistant (RAG-based)

A Python-based Q&A Assistant built using FastAPI and Retrieval-Augmented Generation (RAG). It retrieves relevant context from a vector store and generates answers using an LLM.

## Features

* FastAPI backend for Q&A APIs
* Retrieval-Augmented Generation (RAG) pipeline
* Vector-based semantic search using FAISS
* Config-driven architecture
* Modular service layer (Retrieval + LLM)
* Semantic document retrieval with reranking support
* REST APIs with automatic Swagger documentation

---

## Project Structure

```text
python-qa-assistant/
│
├── app/
│   ├── api/                  # API endpoints
│   ├── core/                 # Configuration, logging, constants
│   ├── repositories/         # Data access layer
│   ├── schemas/              # Request/Response schemas
│   ├── services/             # RAG, retrieval, LLM services
│   ├── utils/                # Utility functions
│   └── main.py               # FastAPI entry point
│
├── ingestion/
│   ├── preprocess.py
│   ├── merge_datasets.py
│   ├── filter_documents.py
│   ├── build_documents.py
│   ├── create_embeddings.py
│   └── create_faiss_index.py
│
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

---

## Prerequisites

* Python 3.12+
* pip
* OpenAI API Key and/or Google Gemini API Key

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/azadpriyanshu/rag_q-a.git
cd python-qa-assistant
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

Mac/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory.

Example:

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key

SIMILARITY_THRESHOLD=0.75
MAX_CONTEXT_CHARS=12000
TOP_K_RESULTS=5
```

---

## Data Preparation & Embedding Generation

**Note:** Raw datasets, processed files, embeddings, and FAISS indexes are intentionally excluded from GitHub to keep the repository lightweight.

To use the application, you must prepare the dataset and generate embeddings locally.

### Step 1: Place Raw Dataset Files

Create the following structure:

```text
data/
└── raw/
    ├── Questions.csv
    ├── Answers.csv
    └── Tags.csv
```

### Step 2: Merge Raw Datasets

```bash
python ingestion/merge_datasets.py
```

### Step 3: Preprocess Data

```bash
python ingestion/preprocess.py
```

### Step 4: Filter Relevant Documents

```bash
python ingestion/filter_documents.py
```

### Step 5: Build Final Documents

```bash
python ingestion/build_documents.py
```

### Step 6: Generate Embeddings

```bash
python ingestion/create_embeddings.py
```

### Step 7: Create FAISS Index

```bash
python ingestion/create_faiss_index.py
```

After completing these steps, the FAISS index and metadata files will be generated locally and the application will be ready for querying.

---

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## API Documentation

Once the application is running:

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

### Base URL

```text
http://localhost:8000
```

---

## Example API Usage

### Request

```http
POST /query
```

```json
{
  "question": "What is RAG?"
}
```

### Response

```json
{
  "question": "What is RAG?",
  "answer": "RAG stands for Retrieval Augmented Generation...",
  "sources": [
    {
      "title": "Introduction to RAG",
      "score": 0.92
    }
  ]
}
```

---

## How It Works

1. User submits a question through the API.
2. The query is converted into embeddings.
3. Relevant documents are retrieved using vector similarity search.
4. Retrieved context is passed to the LLM.
5. The LLM generates a grounded response based on retrieved documents.
6. The final answer and source references are returned to the user.

---

## Tech Stack

* Python 3.12
* FastAPI
* FAISS
* OpenAI / Google Gemini
* Sentence Transformers
* Pandas
* Uvicorn

---

## Run Checklist

Before running the application:

* Virtual environment is activated
* Dependencies are installed
* Environment variables are configured
* Raw datasets are available
* Embeddings and FAISS index have been generated

Start command:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Notes

* Raw datasets are not included in this repository.
* Processed datasets, embeddings, and FAISS indexes are generated locally.
* The repository contains only source code and ingestion pipelines required to reproduce the complete system.
