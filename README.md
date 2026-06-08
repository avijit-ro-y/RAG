# 🇮🇳 Indian States RAG System

A complete Retrieval-Augmented Generation (RAG) system built from scratch using Python, ChromaDB, Sentence Transformers, and Google Gemini.

The project automatically collects information about Indian states from Wikipedia, transforms the data into vector embeddings, stores them in a vector database, retrieves relevant information based on user queries, and generates grounded responses using a Large Language Model (LLM).

The project also includes a comprehensive RAG evaluation framework for measuring retrieval quality, generation quality, and hallucination rates.

---

# Features

## Data Ingestion Pipeline

* Automated Wikipedia scraping
* Covers all Indian states
* Stores data locally for reuse
* Logging and error handling

## Text Processing

* Text cleaning and preprocessing
* Recursive text chunking
* Configurable chunk size and overlap

## Embedding Generation

* SentenceTransformer integration
* all-MiniLM-L6-v2 embeddings
* Efficient semantic representation

## Vector Database

* ChromaDB persistent storage
* Similarity-based retrieval
* Source diversification strategy
* Metadata tracking

## LLM Integration

* Google Gemini 2.0 Flash
* Context-aware answer generation
* Retrieval-Augmented Generation workflow

## Evaluation Framework

* Precision@K
* Recall@K
* Mean Reciprocal Rank (MRR)
* NDCG@K
* BLEU Score
* BERTScore
* Perplexity
* Hallucination Detection

---

# System Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                 DATA INGESTION LAYER                    │
└─────────────────────────────────────────────────────────┘

 Wikipedia
      │
      ▼
┌───────────────┐
│  Web Scraper  │
└───────────────┘
      │
      ▼
┌───────────────┐
│ Raw Text Data │
└───────────────┘
      │
      ▼
┌────────────────┐
│ Text Processor │
│ • Cleaning     │
│ • Chunking     │
└────────────────┘
      │
      ▼
┌────────────────┐
│   Embedder     │
│ SentenceTransf │
└────────────────┘
      │
      ▼
┌────────────────┐
│   ChromaDB     │
│ Vector Store   │
└────────────────┘

──────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────┐
│                  RETRIEVAL LAYER                        │
└─────────────────────────────────────────────────────────┘

 User Query
      │
      ▼
┌────────────────┐
│ Query Embedding│
└────────────────┘
      │
      ▼
┌────────────────┐
│ Similarity     │
│ Search         │
└────────────────┘
      │
      ▼
┌────────────────┐
│ Source-Aware   │
│ Retrieval      │
└────────────────┘
      │
      ▼
 Retrieved Chunks

──────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────┐
│                 GENERATION LAYER                        │
└─────────────────────────────────────────────────────────┘

 Retrieved Context
         +
 User Question
         │
         ▼
┌────────────────┐
│ Google Gemini  │
│     2.0 Flash  │
└────────────────┘
         │
         ▼
 Generated Answer

──────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────┐
│                EVALUATION LAYER                         │
└─────────────────────────────────────────────────────────┘

 Test Dataset
      │
      ▼
 Generated Responses
      │
      ▼
┌──────────────────────────────┐
│ Retrieval Evaluation         │
│ • Precision@K                │
│ • Recall@K                   │
│ • MRR                        │
│ • NDCG@K                     │
└──────────────────────────────┘

┌──────────────────────────────┐
│ Generation Evaluation        │
│ • BLEU                       │
│ • BERTScore                  │
│ • Perplexity                 │
│ • Hallucination Rate         │
└──────────────────────────────┘

      │
      ▼

 HTML Report + Visualizations
```

---

# Project Structure

```text
RAG/
│
├── core/
│   ├── __init__.py
│   ├── scraper.py
│   ├── text_processor.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── llm.py
│   ├── rag_brain.py
│   └── logger.py
│
├── evaluation/
│   ├── metrics.py
│   ├── report_generator.py
│   ├── test_datasets.py
│   └── reports/
│
├── data/
├── chroma_db/
├── logs/
│
├── config.py
├── main.py
├── evaluate.py
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd RAG
```

## Create Virtual Environment

```bash
python -m venv .RAG_env
```

## Activate Environment

Windows:

```bash
.RAG_env\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
LOG_LEVEL=INFO
```

---

# Running the Project

## Build Knowledge Base

```bash
python main.py --scrape
```

This will:

* Scrape Wikipedia
* Clean text
* Create chunks
* Generate embeddings
* Store vectors in ChromaDB

---

## Interactive Mode

```bash
python main.py
```

Example:

```text
Enter your question:
What are the tourist attractions in Kerala?
```

---

## Test Mode

```bash
python main.py --mode test
```

Runs predefined benchmark questions.

---

# Run Evaluation

```bash
python evaluate.py
```

Generate performance reports including:

* Retrieval metrics
* Generation metrics
* Hallucination analysis
* HTML reports

---

# Example Queries

* What are the main tourist attractions in Kerala?
* Tell me about the history of Tamil Nadu.
* What is the economy of Gujarat like?
* Which states are known for desert landscapes?
* Describe the culture and traditions of Rajasthan.

---

# Future Improvements

* Hybrid Search (BM25 + Vector Search)
* Query Expansion
* Cross-Encoder Re-ranking
* Multi-hop Retrieval
* Streamlit Frontend
* FastAPI Deployment
* Multi-language Support
* RAGAS Evaluation Integration

---

# Learning Outcomes

This project demonstrates:

* Web Scraping
* Natural Language Processing
* Embedding Models
* Vector Databases
* Retrieval-Augmented Generation (RAG)
* Large Language Models (LLMs)
* RAG Evaluation Methodologies
* Software Engineering Best Practices

---

# Author

**Avijit Roy**

B.Tech Computer Science Student

Interests:
Artificial Intelligence • Machine Learning • NLP • Retrieval-Augmented Generation • Applied Research
