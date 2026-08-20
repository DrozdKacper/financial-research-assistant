from dotenv import load_dotenv

from financial_assistant.chain import create_llm, create_rag_chain, PROMPT_TEMPLATE
from financial_assistant.config import load_config
from financial_assistant.graph import graph, Context
from financial_assistant.ingestion import load_and_process_documents
from financial_assistant.rag import create_embeddings, create_vector_store, create_retriever, load_vector_store

load_dotenv()
config = load_config()

embeddings = create_embeddings(config)
vector_store = load_vector_store(embeddings, config)
retriever = create_retriever(vector_store, config)

llm = create_llm(config)
prompt = PROMPT_TEMPLATE

result = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What was NVIDIA's Data Center revenue in Q1 FY2027?"
            }
        ]
    },
    context=Context(
        retriever=retriever,
        llm=llm,
        prompt=prompt,
    )
)
print(result)

#chain = create_rag_chain(llm, retriever)
#docs = retriever.invoke("What was NVIDIA's Data Center revenue in Q1 FY2027?")

#for i, doc in enumerate(docs, 1):
#    print(f"\n--- Document {i} ---")
#    print(doc.page_content)
#answer = chain.invoke("What was NVIDIA's Data Center revenue in Q1 FY2027?")

#print(answer)