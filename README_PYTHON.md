# Perplexity Search MCP (Python Version)

A Python implementation of the Model Context Protocol (MCP) server for Perplexity's web search with sonar or sonar-pro.

## Features

- Provides a `search` tool for AI assistants to perform web searches
- Uses Perplexity's chat completions API with the sonar/sonar-pro models
- Asynchronous implementation using httpx and uvicorn

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your PERPLEXITY_API_KEY
```

## Usage

Run the server with default model (sonar-pro):
```bash
python src/index.py
```

Run with specific model:
```bash
python src/index.py --model sonar
# or
python src/index.py --model sonar-pro
```

The server will start on port 3001 by default (configurable via PORT environment variable).

## Tool: search

The server provides a `search` tool with the following input parameters:

- `query` (required): The search query to perform
- `search_recency_filter` (optional): Filter search results by recency (options: month, week, day, hour). If not specified, no time filtering is applied.

## Configuration

### Environment Variables

- `PERPLEXITY_API_KEY`: Your Perplexity API key (required)
- `PORT`: Server port (default: 3001)

## Response Format

The response from the `search` tool includes:

- `content`: The search results content
- `citations`: Array of citations for the information

## Differences from TypeScript Version

- Uses Python's `mcp` library instead of `@modelcontextprotocol/sdk`
- Uses `httpx` for async HTTP requests instead of `axios`
- Uses `starlette` and `uvicorn` for the web server instead of `express`
- Decorators (`@server.list_tools()`, `@server.call_tool()`) instead of `setRequestHandler`

## License

MIT
