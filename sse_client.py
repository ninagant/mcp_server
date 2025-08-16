# sse_client.py
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # SSE server URL
    server_url = "http://localhost:8080/sse"
    
    print(f"Connecting to SSE server at {server_url}...")
    
    # Create the connection via SSE transport
    async with sse_client(url=server_url) as streams:
        # Create the client session with the streams
        async with ClientSession(*streams) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            response = await session.list_tools()
            print("Available tools:", [tool.name for tool in response.tools])
            
            # Call the get_all_coins tool
            result = await session.call_tool("get_all_coins")
            print("get_all_coins result:", result.content)
            
            # Call the get_coin_price tool
            result = await session.call_tool("get_coin_price", {"name": "btc"})
            print("get_coin_price result:", result.content)

if __name__ == "__main__":
    asyncio.run(main())