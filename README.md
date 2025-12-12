# Perplexity Search MCP (Python)

[![smithery badge](https://smithery.ai/badge/@arjunkmrm/perplexity-search)](https://smithery.ai/server/@arjunkmrm/perplexity-search)

A simple Model Context Protocol (MCP) server for Perplexity's web search with sonar or sonar-pro, implemented in Python.

## Features

- Provides a `search` tool for AI assistants to perform web searches
- Uses Perplexity's chat completions API with the sonar/sonar-pro models
- Built with FastAPI and MCP Python SDK
- SSE (Server-Sent Events) transport for real-time communication

## Tool: search

The server provides a `search` tool with the following input parameters:

- `query` (required): The search query to perform
- `search_recency_filter` (optional): Filter search results by recency (options: month, week, day, hour). If not specified, no time filtering is applied.

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the provided install script:

```bash
bash install.sh
```

## Configuration

### Environment Variables

Create a `.env` file or set the following environment variable:

- `PERPLEXITY_API_KEY`: Your Perplexity API key (required)
- `PORT`: Server port (optional, defaults to 3001)

### Model Selection

You can specify which Perplexity model to use with the `--model` flag:

```bash
python src/index.py --model sonar-pro  # Default
python src/index.py --model sonar
```

## Running the Server

### Using Python directly

```bash
python src/index.py
```

### Using the run script

```bash
bash run.sh
```

### With environment variables

```bash
PERPLEXITY_API_KEY=your-api-key python src/index.py
```

The server will start on `http://0.0.0.0:3001` by default.

## Docker

Build and run with Docker:

```bash
docker build -t perplexity-search-mcp .
docker run -p 3001:3001 -e PERPLEXITY_API_KEY=your-api-key perplexity-search-mcp
```

## Response Format

The response from the `search` tool includes:

- `content`: The search results content
- `citations`: Array of citations for the information

## API Endpoints

- `GET /sse` - SSE endpoint for MCP connection
- `POST /messages` - Message handling endpoint

## Migration from TypeScript

This project has been converted from TypeScript/Node.js to Python. The original TypeScript files (`package.json`, `tsconfig.json`, `src/index.ts`) are kept for reference but are no longer used. The Python implementation provides the same functionality with improved simplicity using the FastMCP framework.

## License

MIT 