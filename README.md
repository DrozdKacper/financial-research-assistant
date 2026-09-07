# Financial Research Assistant

An agentic AI application for analyzing quarterly financial reports using Retrieval-Augmented Generation (RAG), LangGraph, and Model Context Protocol (MCP).

The application allows an LLM to autonomously decide which tools are required to answer a user's question. It can retrieve information from financial reports stored in a vector database and access external market data through an MCP server.

Note: The project is currently in early development, with additional features and capabilities planned.
## Features

* **Agentic RAG** for querying quarterly financial reports
* **LangGraph** for state-based agent orchestration
* **Tool calling** with LangChain `ToolNode`
* **MCP integration** for external tools
* **Pinecone** vector database for semantic retrieval
* **OpenAI API** for embeddings and LLM inference
* **PDF ingestion pipeline** for financial documents
* **Asynchronous execution** for MCP-enabled tools
* Ability to combine multiple tools in a single query
* Modular architecture separating ingestion, retrieval, agent, graph, and MCP components

## Architecture

```text
                         ┌──────────────────────┐
                         │       User Query     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      LangGraph       │
                         │   Agent Orchestrator  │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         │                      │
                         ▼                      ▼
              ┌──────────────────┐   ┌──────────────────┐
              │   RAG Tool        │   │    MCP Tool      │
              │                  │   │                  │
              │ Pinecone         │   │ Stock Price API  │
              │ Financial Docs   │   │ MCP Server       │
              └────────┬─────────┘   └────────┬─────────┘
                       │                      │
                       └──────────┬───────────┘
                                  │
                                  ▼
                         ┌──────────────────────┐
                         │     LLM Response     │
                         └──────────────────────┘
```

The agent can dynamically select one or multiple tools depending on the user's question.

For example, a single query can require both internal financial data and external market data:

> What is NVIDIA's current stock price and what was its total revenue in Q1 FY2027?

The agent can independently call:

1. `get_current_stock_price` through MCP
2. `search_financial_documents` through the local RAG pipeline

and combine the retrieved information into a single response.

## Technology Stack

| Component           | Technology           |
| ------------------- | -------------------- |
| Language            | Python               |
| LLM                 | OpenAI               |
| Agent orchestration | LangGraph            |
| LLM framework       | LangChain            |
| RAG                 | LangChain + Pinecone |
| Vector database     | Pinecone             |
| Embeddings          | OpenAI Embeddings    |
| External tools      | MCP                  |
| MCP transport       | Streamable HTTP      |
| API                 | Twelve Data          |
| Document format     | PDF                  |
| Version control     | Git                  |

## Project Structure

```text
financial-research-assistant/
│
├── data/
│   └── financial_reports/
│
├── src/
│   └── financial_assistant/
│       ├── agent.py
│       ├── chain.py
│       ├── config.py
│       ├── graph.py
│       ├── main.py
│       ├── mcp_client.py
│       ├── rag.py
│       └── tools.py
│
├── tests/
│
├── config.yaml
├── requirements.txt
├── .env
└── README.md
```

## How It Works

### 1. Document ingestion

Financial reports are loaded from PDF files and processed through an ingestion pipeline:

```text
PDF
 │
 ▼
Document Loader
 │
 ▼
Text Cleaning
 │
 ▼
Chunking
 │
 ▼
Metadata
 │
 ▼
Embeddings
 │
 ▼
Pinecone
```

Each document is split into smaller chunks and enriched with metadata such as:

```text
company: NVIDIA
ticker: NVDA
quarter: Q1
fiscal_year: 2027
document_type: 10-Q
```

The resulting chunks are embedded using OpenAI embeddings and stored in Pinecone.

### 2. Retrieval

When the user asks a question about a financial report, the agent can call the RAG tool:

```text
User Question
      │
      ▼
RAG Tool
      │
      ▼
Pinecone Retriever
      │
      ▼
Relevant Document Chunks
      │
      ▼
LLM
```

The retrieved context is then used by the LLM to generate an answer grounded in the financial report.

### 3. Agentic tool selection

Instead of always executing the same retrieval pipeline, the LLM determines whether a tool is required.

Available tools include:

* `search_financial_documents`
* `get_current_stock_price`

LangGraph manages the execution flow using a state-based graph.

```text
START
  │
  ▼
Chatbot
  │
  ├── No tool call ───────────────► END
  │
  └── Tool call
        │
        ▼
      ToolNode
        │
        ▼
      Chatbot
        │
        ▼
       END
```

### 4. MCP integration

External functionality is exposed through an MCP server.

The MCP server provides the following tool:

```text
get_current_stock_price(ticker)
```

The tool retrieves current market data from the Twelve Data API.

The MCP server uses Streamable HTTP and exposes the MCP endpoint at:

```text
/mcp
```

The application loads the remote MCP tools using `langchain-mcp-adapters` and makes them available to the LangGraph agent alongside local RAG tools.

### 5. Multi-tool reasoning

The agent can call multiple tools during a single interaction.

For example:

```text
User:
What is NVIDIA's current stock price and what was its total
revenue in Q1 FY2027?
```

The agent can produce tool calls equivalent to:

```text
get_current_stock_price("NVDA")

search_financial_documents(
    "NVIDIA Q1 FY2027 total revenue"
)
```

The results are then returned to the LLM, which combines them into the final response.

## Example

### Financial report question

**Question**

```text
What was NVIDIA's total revenue in Q1 FY2027?
```

**Answer**

```text
NVIDIA's total revenue in Q1 FY2027 was
$81.615 billion.
```

The answer is generated using information retrieved from the NVIDIA quarterly report stored in Pinecone.

### External market data

**Question**

```text
What is NVIDIA's current stock price?
```

The agent recognizes that current market data is required and calls the MCP tool:

```text
get_current_stock_price("NVDA")
```

### Combined query

**Question**

```text
What is NVIDIA's current stock price and what was its
total revenue in Q1 FY2027?
```

The agent can call both tools and combine the results:

```text
MCP
 │
 └── Current NVDA price

RAG
 │
 └── Q1 FY2027 revenue

        │
        ▼

       LLM
        │
        ▼
 Combined answer
```



## Testing

The agent was tested with three main scenarios.

### RAG tool

```text
What was NVIDIA's total revenue in Q1 FY2027?
```

Expected behavior:

```text
search_financial_documents
        ↓
Pinecone
        ↓
NVIDIA 10-Q context
        ↓
LLM
```

### MCP tool

```text
What is NVIDIA's current stock price?
```

Expected behavior:

```text
get_current_stock_price
        ↓
MCP Server
        ↓
Twelve Data API
        ↓
LLM
```

### Multi-tool query

```text
What is NVIDIA's current stock price and what was its
total revenue in Q1 FY2027?
```

Expected behavior:

```text
                 ┌── RAG Tool ──► Financial Report
User ─► Agent ───┤
                 └── MCP Tool ──► Market Data
                        │
                        ▼
                       LLM
                        │
                        ▼
                  Combined Answer
```

This verifies that the agent can select and execute multiple tools within a single interaction.

## Design Principles

The project was designed around several principles:

### Separation of concerns

Each layer has a clearly defined responsibility:

* **RAG** — retrieval of information from financial documents
* **Tools** — expose application capabilities
* **MCP** — external tool integration
* **LangGraph** — orchestration and state management
* **LLM** — reasoning and final response generation

### Tool-based architecture

Instead of embedding all functionality directly into the agent, capabilities are exposed as tools.

This allows new functionality to be added without significantly changing the core agent architecture.

### Modularity

The application is divided into independent components for:

* configuration
* document processing
* retrieval
* LLM creation
* tools
* MCP integration
* graph orchestration

This makes individual components easier to test, replace, and extend.

## Future Improvements

Planned improvements include:

* evaluation layer for RAG and agent responses
* automated retrieval and answer quality evaluation
* additional financial data MCP tools
* MCP resources and prompts where they provide meaningful functionality
* improved observability and tracing
* additional financial reports and companies
* Dockerized deployment
* automated testing and CI/CD improvements

## Learning Objectives

This project was built to gain practical experience with:

* Retrieval-Augmented Generation
* Agentic AI
* LLM tool calling
* LangGraph state-based orchestration
* MCP
* Vector databases
* semantic search
* document processing
* asynchronous Python
* API integrations
* modular AI application architecture

## Author

**Kacper Drozd**

GitHub: [DrozdKacper](https://github.com/DrozdKacper)
