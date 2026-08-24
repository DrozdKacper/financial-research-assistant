from dotenv import load_dotenv

from financial_assistant.agent import create_llm_with_tools
from financial_assistant.chain import create_llm, create_rag_chain, PROMPT_TEMPLATE
from financial_assistant.config import load_config
from financial_assistant.graph import Context, create_graph
from financial_assistant.ingestion import load_and_process_documents
from financial_assistant.rag import create_embeddings, create_vector_store, create_retriever, load_vector_store
from financial_assistant.tools import get_current_stock_price, create_search_financial_documents_tool

load_dotenv()
config = load_config()

embeddings = create_embeddings(config)
vector_store = load_vector_store(embeddings, config)
retriever = create_retriever(vector_store, config)

llm = create_llm(config)

search_financial_documents = create_search_financial_documents_tool(retriever)

tools = [get_current_stock_price, search_financial_documents]
llm_with_tools = create_llm_with_tools(llm, tools)

graph = create_graph(tools)

prompt = PROMPT_TEMPLATE

result = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What was NVIDIA's total revenue in Q1 FY2027?"
            }
        ]
    },
    context=Context(
        retriever=retriever,
        llm=llm,
        llm_with_tools=llm_with_tools,
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