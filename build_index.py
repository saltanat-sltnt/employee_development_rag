# creates Chroma index

import getpass
import os
import shutil
import pypdf

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    PDF_FILES,
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RESET_CHROMA_ON_BUILD,
)


def setup_openai_key():
    if not os.environ.get("OPENAI_API_KEY"):
        api_key = getpass.getpass("Enter OpenAI API key: ")
        if not api_key:
            raise ValueError("API key cannot be empty.")
        os.environ["OPENAI_API_KEY"] = api_key

# load pages of a single pdf


def load_pdf_pages(file_path) -> list[Document]:
    reader = pypdf.PdfReader(str(file_path))

    pages = []
    for i, page in enumerate(reader.pages):
        pages.append(
            Document(
                page_content=page.extract_text() or "",
                metadata={
                    "source": file_path.name,
                    "page_index": i,
                    "page_display": i+1,
                },
            )
        )

    return pages

# load all hr docs


def load_all_documents() -> list[Document]:
    all_docs = []

    for pdf_file in PDF_FILES:
        docs = load_pdf_pages(pdf_file)
        all_docs.extend(docs)

    return all_docs

# split docs into chunks


def split_documents(docs: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(docs)
    print(f"Split docs into {len(chunks)} chunks.")
    return chunks


def build_index():
    setup_openai_key()

    # delete old chroma db folder
    if RESET_CHROMA_ON_BUILD and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    embdeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embdeddings,
        persist_directory=str(CHROMA_DIR),
    )

    docs = load_all_documents()
    chunks = split_documents(docs)

    # add chunks to chroma db
    ids = vector_store.add_documents(documents=chunks)

    print(f"Added {len(chunks)} chunks to ChromaDB.")
    print(f"Chroma dir stored at {str(CHROMA_DIR)}")


if __name__ == "__main__":
    build_index()
