#!/usr/bin/env python3

import asyncio
import json
import os
import sys
from typing import Any, Optional, List, Dict

import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent, CallToolResult, ErrorData
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response

# Load environment variables
load_dotenv()

# Configuration
MAX_TOKENS = 8192
TEMPERATURE = 0.2

# Parse model from command line arguments
model = "sonar-pro"
if "--model" in sys.argv:
    model_index = sys.argv.index("--model")
    if model_index + 1 < len(sys.argv):
        model = sys.argv[model_index + 1]

if model not in ["sonar", "sonar-pro"]:
    raise ValueError('Invalid model. Must be either "sonar" or "sonar-pro"')

print(f"Using Perplexity model: {model}", file=sys.stderr)

# Create MCP server
server = Server("perplexity-search-server")

# Store transport globally for message handling
transport: Optional[SseServerTransport] = None


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search",
            description="Perform a web search using Perplexity's API, which provides detailed and contextually relevant results with citations. By default, no time filtering is applied to search results.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to perform"
                    },
                    "search_recency_filter": {
                        "type": "string",
                        "description": "Filter search results by recency (options: month, week, day, hour). If not specified, no time filtering is applied.",
                        "enum": ["month", "week", "day", "hour"]
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool execution."""
    if name != "search":
        raise ValueError(f"Unknown tool: {name}")
    
    query = arguments.get("query")
    search_recency_filter = arguments.get("search_recency_filter")
    
    if not query:
        raise ValueError("Query parameter is required")
    
    try:
        # Build payload
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
        
        # Add optional parameters
        if search_recency_filter:
            payload["search_recency_filter"] = search_recency_filter
        
        print(f"Using model: {model}, max_tokens: {MAX_TOKENS}, temperature: {TEMPERATURE}", file=sys.stderr)
        
        # Make API request
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable is not set")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
        
        # Format the response
        formatted_response = {
            "content": data["choices"][0]["message"]["content"],
            "citations": data.get("citations", [])
        }
        
        return [
            TextContent(
                type="text",
                text=json.dumps(formatted_response, indent=2)
            )
        ]
    
    except httpx.HTTPStatusError as error:
        error_message = f"Perplexity API error: {error.response.status_code}"
        try:
            error_data = error.response.json()
            error_message = f"Perplexity API error: {error_data.get('error') or error_data.get('message') or str(error)}"
        except Exception:
            pass
        
        return [
            TextContent(
                type="text",
                text=error_message
            )
        ]
    except Exception as error:
        return [
            TextContent(
                type="text",
                text=f"Error: {str(error)}"
            )
        ]


# Create Starlette app for SSE transport
async def handle_sse(request: Request) -> Response:
    """Handle SSE connection."""
    global transport
    print("Received connection", file=sys.stderr)
    
    async with SseServerTransport("/messages") as sse_transport:
        transport = sse_transport
        await server.run(
            sse_transport.read_stream,
            sse_transport.write_stream,
            server.create_initialization_options()
        )
    
    return Response()


async def handle_messages(request: Request) -> Response:
    """Handle POST messages."""
    global transport
    print("Received message handle message", file=sys.stderr)
    
    if transport:
        await transport.handle_post_message(request)
    
    return Response()


# Create Starlette application
app = Starlette(
    routes=[
        Route("/sse", handle_sse),
        Route("/messages", handle_messages, methods=["POST"]),
    ]
)


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "3001"))
    print(f"Server is running on port {port}", file=sys.stderr)
    
    uvicorn.run(app, host="0.0.0.0", port=port)
