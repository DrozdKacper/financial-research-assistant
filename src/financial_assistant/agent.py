from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

def create_llm_with_tools(llm: ChatOpenAI, tools: list[BaseTool]):

    return llm.bind_tools(tools)
