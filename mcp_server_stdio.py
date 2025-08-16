from typing import Any, Dict, List, Optional
import os
import httpx
from dotenv import load_dotenv
from anthropic import Anthropic
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# API Base URL
API_BASE_URL = "http://localhost:5001"

# Initialize FastMCP server
mcp = FastMCP("claude-tools")

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@mcp.tool()
async def get_all_coins() -> str:
    """Get the list of all available cryptocurrencies.

    Returns:
        A list of all available cryptocurrencies and their details
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/api/coins/")
            response.raise_for_status()
            coins = response.json()
            return str(coins)  # Convert to string for better formatting
    except Exception as e:
        return f"Error fetching coins: {str(e)}"

@mcp.tool()
async def get_coin_price(name: str) -> str:
    """Get the current price of a specific cryptocurrency.

    Args:
        name: The cryptocurrency symbol/name (e.g., 'btc' for Bitcoin)

    Returns:
        The current price information for the specified cryptocurrency
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/api/coins/price", params={"name": name})
            response.raise_for_status()
            price_info = response.json()
            return str(price_info)  # Convert to string for better formatting
    except Exception as e:
        return f"Error fetching price for {name}: {str(e)}"


if __name__ == "__main__":
    print("starting MCP server ...")
    mcp.run()
