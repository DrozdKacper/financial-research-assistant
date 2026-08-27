import asyncio

from dotenv import load_dotenv

from financial_assistant.agent import create_llm_with_tools
from financial_assistant.chain import create_llm, PROMPT_TEMPLATE
from financial_assistant.config import load_config
from financial_assistant.graph import Context, create_graph
from financial_assistant.rag import (
    create_embeddings,
    create_retriever,
    load_vector_store,
)
from financial_assistant.tools import create_search_financial_documents_tool
from financial_assistant.mcp_client import get_mcp_tools


async def main():

    load_dotenv()
    config = load_config()

    embeddings = create_embeddings(config)
    vector_store = load_vector_store(embeddings, config)
    retriever = create_retriever(vector_store, config)

    llm = create_llm(config)


    search_financial_documents = create_search_financial_documents_tool(
        retriever
    )


    mcp_tools = await get_mcp_tools()


    tools = [
        search_financial_documents,
        *mcp_tools,
    ]

    llm_with_tools = create_llm_with_tools(
        llm,
        tools,
    )

    graph = create_graph(tools)

    prompt = PROMPT_TEMPLATE

    result = await graph.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is NVIDIA's current stock price and what was its total revenue in Q1 FY2027?",
                }
            ]
        },
        context=Context(
            retriever=retriever,
            llm=llm,
            llm_with_tools=llm_with_tools,
            prompt=prompt,
        ),
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())