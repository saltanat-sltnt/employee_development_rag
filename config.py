# filenames, settings
from pathlib import Path

# project dir
BASE_DIR = Path(__file__).parent

# paths of pdf files to index (hr docs)
PDF_FILES = [
    BASE_DIR / "nke-10k-2023.pdf",
]

# chroma db
CHROMA_DIR = BASE_DIR / "chromo_lanchain_db"

# chroma collection name
COLLECTION_NAME = "example_collection"

# embedding model
EMBEDDING_MODEL = "text-embedding-3-small"

# chunking settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# if true, delete old Chroma DB before rebuilding
RESET_CHROMA_ON_BUILD = True
