from dataclasses import dataclass
from typing import Annotated

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.runtime import Runtime
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]
    documents: list[Document]


@dataclass
class Context:
    retriever: VectorStoreRetriever
    llm: ChatOpenAI
    llm_with_tools: ChatOpenAI
    prompt: ChatPromptTemplate


def chatbot(state: State, runtime: Runtime[Context]):
    response = runtime.context.llm_with_tools.invoke(
        state["messages"]
    )

    return {"messages": [response]}


def route_tools(state: State):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


def create_graph(tools):

    graph_builder = StateGraph(State)

    graph_builder.add_node("chatbot", chatbot)

    tool_node = ToolNode(tools)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge(START, "chatbot")

    graph_builder.add_conditional_edges(
        "chatbot",
        route_tools,
        {
            "tools": "tools",
            END: END
        }
    )

    graph_builder.add_edge("tools", "chatbot")

    return graph_builder.compile()