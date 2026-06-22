import pypdf
import pandas as pd

from pathlib import Path
from langchain_core.documents import Document


def load_pdf(file_path: Path) -> list[Document]:
    reader = pypdf.PdfReader(str(file_path))

    docs = []
    for i, page in enumerate(reader.pages):
        docs.append(
            Document(
                page_content=page.extract_text() or "",
                metadata={
                    "source": file_path.name,
                    "file_type": "pdf",
                    "page_index": i,
                    "page_display": i + 1,
                },
            )
        )

    return docs


def load_txt(file_path: Path) -> list[Document]:
    text = file_path.read_text(encoding="utf-8")

    return [
        Document(
            page_content=text,
            metadata={
                "source": file_path.name,
                "file_type": "txt",
            },
        )
    ]


def load_csv(file_path: Path) -> list[Document]:
    df = pd.read_csv(file_path)

    docs = []
    for i, row in df.iterrows():
        row_text = "\n".join(
            f"{column}: {value}"
            for column, value in row.items()
            if pd.notna(value)
        )

        docs.append(
            Document(
                page_content=row_text,
                metadata={
                    "source": file_path.name,
                    "file_type": "csv",
                    "row_index": int(i),
                },
            )
        )

    return docs


def load_excel(file_path: Path) -> list[Document]:
    sheets = pd.read_excel(file_path, sheet_name=None)

    docs = []
    for sheet_name, df in sheets.items():
        for i, row in df.iterrows():
            row_text = "\n".join(
                f"{column}: {value}"
                for column, value in row.items()
                if pd.notna(value)
            )

            docs.append(
                Document(
                    page_content=row_text,
                    metadata={
                        "source": file_path.name,
                        "file_type": "excel",
                        "sheet_name": str(sheet_name),
                        "row_index": int(i),
                    },
                )
            )

    return docs


def load_documents(file_path: Path) -> list[Document]:
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(file_path)

    if suffix == ".txt":
        return load_txt(file_path)

    if suffix == ".csv":
        return load_csv(file_path)

    if suffix in [".xlsx", ".xls"]:
        return load_excel(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")


def load_all_documents(source_files: list[Path]) -> list[Document]:
    all_docs = []

    for file_path in source_files:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        docs = load_documents(file_path)
        print(f"Loaded {len(docs)} document objects from {file_path.name}.")
        all_docs.extend(docs)

    return all_docs