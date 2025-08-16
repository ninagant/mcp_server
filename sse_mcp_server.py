from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.server import Server
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
import uvicorn
import httpx

# Create the MCP server
mcp = FastMCP("SSE Example Server")
API_BASE_URL = "http://localhost:5001"

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
            print(f"price_info={price_info}")
            return str(price_info)  # Convert to string for better formatting
    except Exception as e:
        return f"Error fetching price for {name}: {str(e)}"

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can serve the MCP server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

if __name__ == "__main__":
    # Get the underlying MCP server
    mcp_server = mcp._mcp_server
    
    # Create Starlette app with SSE support
    starlette_app = create_starlette_app(mcp_server, debug=True)
    
    port = 8080
    print(f"Starting MCP server with SSE transport on port {port}...")
    print(f"SSE endpoint available at: http://localhost:{port}/sse")
    
    # Run the server using uvicorn
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)