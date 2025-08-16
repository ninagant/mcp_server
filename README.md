# MCP Server & Claude Integration

This project provides a set of Python scripts and server components for interacting with the MCP (Model Context Protocol) server, integrating with Anthropic's Claude LLM, and exposing tools via SSE and stdio transports.

## Project Structure

- `claude_llm.py`: Simple script to interact with Claude LLM via API.
- `llm_sse_client.py`: Client that connects to the MCP SSE server and invokes tools using Claude's output.
- `sse_mcp_server.py`: MCP server with SSE transport, exposes crypto tools.
- `sse_client.py`: Example client for connecting to the SSE server and invoking tools.
- `mcp_server_stdio.py`: MCP server using stdio transport.
- `stdio_client.py`: Client for interacting with the stdio MCP server.
- `requirements.txt`: Python dependencies for the project.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd mcp_server
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_claude_api_key_here
```

### 5. Run the MCP SSE Server

```bash
python sse_mcp_server.py
```

The server will start on port 8080. SSE endpoint: `http://localhost:8080/sse`

### 6. Run the SSE Client

```bash
python llm_sse_client.py
```

This will connect to the SSE server and invoke tools using Claude's output.

### 7. Run the Stdio MCP Server and Client

```bash
python mcp_server_stdio.py
python stdio_client.py
```

## Notes

- Ensure your Anthropic API key is valid and has sufficient quota.
- The crypto tools require a backend API running at `http://localhost:5001` (see `API_BASE_URL` in server scripts).
- You may need to adjust ports or endpoints depending on your environment.

## Requirements

See `requirements.txt` for all required Python packages.
