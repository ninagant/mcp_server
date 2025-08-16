# sse_client.py
import asyncio
import anthropic
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
import os
import re

# Load environment variables
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY environment variable not set. Please set it before running the script.")
client = anthropic.Anthropic(api_key=api_key)

def parse_llm_response(llm_response):
    # Extract the invoke name
    invoke_match = re.search(r'<invoke name="([^"]+)">', llm_response)
    tool_name = invoke_match.group(1) if invoke_match else None

    # Extract the parameter name and value
    param_match = re.search(r'<parameter name="([^"]+)">([^<]+)</parameter>', llm_response)
    param_name = param_match.group(1) if param_match else None
    param_value = param_match.group(2) if param_match else None

    # Build tool_args as a dict
    tool_args = {param_name: param_value} if param_name and param_value else {}

    return tool_name, tool_args


async def main():
    # SSE server URL
    server_url = "http://localhost:8080/sse"
    user_message = "What is the price of BYZZ?"
    result = None
    
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

            try:
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000, # Max tokens for Claude's response
                    messages=[
                        {"role": "user", "content": f"User query: {user_message} Available tools: {response.tools}"}
                    ]
                )
                llm_response = message.content[0].text # Access the text content of the response

                # Parse LLM's response to identify tool call
                tool_name, tool_args = parse_llm_response(llm_response)
                print(f"Tool Name: {tool_name}, Tool Args: {tool_args}")
                
                # Call the tool via the MCP session
                tool_output = await session.call_tool(tool_name, tool_args)
                result = tool_output.content if tool_output else "No content returned from tool call."
            except anthropic.APIError as e:
                print(f"Anthropic API Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            if result:
                print(f"User: {user_message}")
                print(f"Claude: {result}")            

if __name__ == "__main__":
    asyncio.run(main())