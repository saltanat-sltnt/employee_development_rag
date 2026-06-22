# creates Chroma index

from utils import setup_openai_key
import shutil
from loaders import load_all_documents

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    SOURCE_FILES,
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RESET_CHROMA_ON_BUILD,
)


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

    docs = load_all_documents(SOURCE_FILES)
    chunks = split_documents(docs)

    # add chunks to chroma db
    ids = vector_store.add_documents(documents=chunks)

    print(f"Added {len(chunks)} chunks to ChromaDB.")
    print(f"Chroma dir stored at {str(CHROMA_DIR)}")


if __name__ == "__main__":
    build_index()
