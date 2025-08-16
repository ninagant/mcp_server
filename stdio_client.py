
import os
import asyncio
import json
from contextlib import AsyncExitStack
import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Set your Claude API key as an environment variable
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

async def main():
    # Get the server script path (same directory as this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "mcp_server_stdio.py")
    
    # Create server parameters
    server_params = StdioServerParameters(
        command="python3",
        args=[server_path]
    )
    
    # Create the connection via stdio transport
    async with stdio_client(server_params) as streams:
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
