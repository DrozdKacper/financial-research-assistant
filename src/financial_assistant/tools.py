import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI

load_dotenv()



def create_search_financial_documents_tool(
    retriever: VectorStoreRetriever,
):
    @tool
    def search_financial_documents(query: str) -> str:
        """
        Search financial reports for information needed to answer questions
        about financial results, risks, business performance, and other
        information disclosed in company filings.

        Args:
            query: A specific question or information to search for.

        Returns:
            Relevant excerpts from financial reports.
        """
        documents = retriever.invoke(query)

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        return context

    return search_financial_documents


