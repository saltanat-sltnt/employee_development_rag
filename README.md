# Employee Development RAG

This project is an early prototype of a Retrieval-Augmented Generation (RAG) system for employee development support.

The long-term goal is to build an HR chat assistant that can help employees choose suitable development activities based on company documents, previous development history, and the 70-20-10 development principle.

## Current Progress

At this stage, the project implements the indexing part of a RAG pipeline:

* Load a PDF document
* Extract text page by page
* Split the document into smaller chunks
* Generate embeddings using OpenAI embeddings
* Store the chunks and embeddings in a local Chroma vector database

The current sample document is the Nike 10-K report, used only for testing the RAG pipeline before replacing it with HR-related documents.

## Current Project Structure

```text
employee_development_rag/
├── build_index.py
├── config.py
├── nke-10k-2023.pdf
├── .gitignore
└── README.md
```

## Technologies Used

* Python
* LangChain
* ChromaDB
* OpenAI Embeddings
* PyPDF

## Current Pipeline

```text
PDF document
↓
Extract text from pages
↓
Split text into chunks
↓
Create embeddings
↓
Store chunks in Chroma vector database
```

## Next Steps

Planned next steps:

1. Implement the 2-step RAG chain:

   * retrieve relevant chunks
   * pass retrieved context to an LLM
   * generate an answer

2. Replace the sample Nike PDF with HR-related documents.

3. Add employee development history.

4. Add 70-20-10 development balance calculation.

5. Build a simple chat interface for employee questions.

## Notes

The current focus is to build the core RAG pipeline first, then gradually extend it into an HR development assistant.
