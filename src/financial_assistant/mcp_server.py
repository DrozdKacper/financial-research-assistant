import os

import requests
from dotenv import load_dotenv
from mcp.server import MCPServer
import asyncio


load_dotenv()

mcp = MCPServer("financial-assistant")


@mcp.tool()
def get_current_stock_price(ticker: str) -> str:
    """Get the current market price of a stock for a given ticker symbol."""

    url = "https://api.twelvedata.com/price"

    params = {
        "symbol": ticker,
        "apikey": os.getenv("TWELVE_DATA_API_KEY"),
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return data["price"]


if __name__ == "__main__":
    asyncio.run(
        mcp.run_streamable_http_async(
            host="127.0.0.1",
            port=8000,
            streamable_http_path="/mcp",
            stateless_http=True,
        )
    )