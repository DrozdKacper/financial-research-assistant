from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from financial_assistant.config import load_config
from langchain_core.documents import Document


def load_and_process_documents(path: str) -> list[Document]:
    config = load_config()

    chunk_size = config["chunking"]["chunk_size"]
    chunk_overlap = config["chunking"]["chunk_overlap"]

    loader = PyPDFLoader(path)
    docs = loader.load()

    for doc in docs:
        doc.metadata.update({
            "company": "NVIDIA",
            "ticker": "NVDA",
            "quarter": "Q1",
            "fiscal_year": 2027,
            "document_type": "10-Q",
        })

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    )

    chunks = text_splitter.split_documents(docs)

    return chunks
