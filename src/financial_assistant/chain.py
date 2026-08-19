from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = ChatPromptTemplate.from_template("""
Use only the provided context to answer the question.
If the answer cannot be determined from the context, say that you are unsure.

Context: {context}
Question: {question}
""")

def create_llm(config: dict) -> ChatOpenAI:

    return ChatOpenAI(model=config["llm"]["model"], temperature=config["llm"]["temperature"])


def create_rag_chain(llm: ChatOpenAI, retriever: VectorStoreRetriever) -> Runnable:

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | PROMPT_TEMPLATE
        | llm
        | StrOutputParser()
    )

    return chain