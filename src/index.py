#!/usr/bin/env python3

import os
import sys
import requests
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from mcp import Server, Tool
from mcp.types import TextContent
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from mcp.server.sse import SSEServerTransport

# Model configuration
model_index = sys.argv.index('--model') if '--model' in sys.argv else -1
model = sys.argv[model_index + 1] if model_index != -1 else 'sonar-pro'

if model not in ['sonar', 'sonar-pro']:
    raise ValueError('Invalid model. Must be either "sonar" or "sonar-pro"')

print(f"Using Perplexity model: {model}", file=sys.stderr)

# Create MCP server
server = Server("perplexity-search-server")

@server.tool()
def search(query: str, search_recency_filter: Optional[str] = None) -> list[TextContent]:
    """
    Perform a web search using Perplexity's API, which provides detailed and contextually relevant results with citations.
    By default, no time filtering is applied to search results.
    """
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": query}],
        "max_tokens": 8192,
        "temperature": 0.2
    }

    # Add optional parameters if provided
    if search_recency_filter:
        payload["search_recency_filter"] = search_recency_filter

    print(f"Using model: {model}, max_tokens: 8192, temperature: 0.2", file=sys.stderr)

    try:
        response = requests.post('https://api.perplexity.ai/chat/completions', json=payload, headers={
            'Authorization': f'Bearer {os.getenv("PERPLEXITY_API_KEY")}',
            'Content-Type': 'application/json'
        })
        response.raise_for_status()

        data = response.json()

        # Format the response to only include content and citations
        formatted_response = {
            "content": data["choices"][0]["message"]["content"],
            "citations": data.get("citations", [])
        }

        return [TextContent(type="text", text=str(formatted_response))]
    except requests.RequestException as e:
        return [TextContent(type="text", text=f"Perplexity API error: {str(e)}")]

# Set up FastAPI app for SSE transport
app = FastAPI()

@app.get("/sse")
async def sse():
    transport = SSEServerTransport()
    await server.connect(transport)
    return StreamingResponse(transport.stream(), media_type="text/event-stream")

@app.post("/messages")
async def messages(request):
    # Handle POST messages for SSE transport
    transport = SSEServerTransport()
    await transport.handle_post_message(request)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3001))
    uvicorn.run(app, host="0.0.0.0", port=port)