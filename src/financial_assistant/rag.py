
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

def create_embeddings(config: dict) -> OpenAIEmbeddings:

    return OpenAIEmbeddings(model=config["embedding"]["model"])

def create_vector_store(chunks: list[Document], embeddings: OpenAIEmbeddings, config: dict) -> PineconeVectorStore:

    vector_store = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=config["pinecone"]["index_name"],
        namespace=config["pinecone"]["namespace"],
    )

    return vector_store

def create_retriever(vector_store: PineconeVectorStore, config: dict) -> VectorStoreRetriever:

    retriever = vector_store.as_retriever(
        search_type=config["retrieval"]["search_type"],
        search_kwargs={"k": config["retrieval"]["top_k"]},
    )

    return retriever

def load_vector_store(embeddings: OpenAIEmbeddings, config: dict) -> PineconeVectorStore:

    return PineconeVectorStore(
        index_name=config["pinecone"]["index_name"],
        embedding=embeddings,
        namespace=config["pinecone"]["namespace"],
    )