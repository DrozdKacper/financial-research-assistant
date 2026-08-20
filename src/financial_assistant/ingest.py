from dotenv import load_dotenv

from financial_assistant.config import load_config
from financial_assistant.ingestion import load_and_process_documents
from financial_assistant.rag import create_embeddings, create_vector_store

load_dotenv()
config = load_config()

chunks = load_and_process_documents("data/nvidia_q1_2027.pdf")
embeddings = create_embeddings(config)
vector_store = create_vector_store(chunks, embeddings, config)