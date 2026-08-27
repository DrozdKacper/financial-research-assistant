import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    async with streamable_http_client(
        "http://127.0.0.1:8000/mcp"
    ) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            await session.initialize()

            response = await session.list_tools()

            print("Available tools:")

            for tool in response.tools:
                print(f"- {tool.name}: {tool.description}")

            result = await session.call_tool(
                "get_current_stock_price",
                {"ticker": "NVDA"},
            )

            print("\nTool result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())