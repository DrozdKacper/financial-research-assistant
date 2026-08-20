from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from dataclasses import dataclass
from langgraph.runtime import Runtime

class State(TypedDict):

    messages: Annotated[list, add_messages]
    documents: list[Document]

@dataclass
class Context:
    retriever: VectorStoreRetriever
    llm: ChatOpenAI
    prompt: ChatPromptTemplate


def retrieve(state: State, runtime: Runtime[Context]):

    last_message = state["messages"][-1].content

    documents = runtime.context.retriever.invoke(last_message)

    return {"documents": documents}


def chatbot(state: State, runtime: Runtime[Context]):

    context = ""

    for document in state["documents"]:
        context += document.page_content + "\n"

    question = state["messages"][-1].content

    prompt_value = runtime.context.prompt.invoke({"question": question, "context": context})

    response = runtime.context.llm.invoke(prompt_value)

    return {"messages": [response]}


graph_builder = StateGraph(State)

graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()