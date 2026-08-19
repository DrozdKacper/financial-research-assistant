from dotenv import load_dotenv

from financial_assistant.chain import create_llm, create_rag_chain
from financial_assistant.config import load_config
from financial_assistant.ingestion import load_and_process_documents
from financial_assistant.rag import create_embeddings, create_vector_store, create_retriever

load_dotenv()
config = load_config()

chunks = load_and_process_documents("data/nvidia_q1_2027.pdf")
embeddings = create_embeddings(config)
vector_store = create_vector_store(chunks, embeddings, config)
retriever = create_retriever(vector_store, config)

llm = create_llm(config)
chain = create_rag_chain(llm, retriever)
docs = retriever.invoke("What was NVIDIA's Data Center revenue in Q1 FY2027?")

for i, doc in enumerate(docs, 1):
    print(f"\n--- Document {i} ---")
    print(doc.page_content)
answer = chain.invoke("What was NVIDIA's Data Center revenue in Q1 FY2027?")

print(answer)