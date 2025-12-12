#!/usr/bin/env python3.11

import os
import sys
import json
import argparse
from typing import Optional
from dotenv import load_dotenv
import httpx
from mcp.server import FastMCP

# Load environment variables
load_dotenv()

# Configuration
MAX_TOKENS = 8192
TEMPERATURE = 0.2

# Parse command line arguments
parser = argparse.ArgumentParser(description='Perplexity Search MCP Server')
parser.add_argument('--model', type=str, default='sonar-pro', 
                    choices=['sonar', 'sonar-pro'],
                    help='Perplexity model to use (default: sonar-pro)')
args, _ = parser.parse_known_args()

MODEL = args.model
print(f"Using Perplexity model: {MODEL}", file=sys.stderr)

# Get port from environment
PORT = int(os.getenv("PORT", "3001"))

# Initialize FastMCP server
mcp = FastMCP(
    name="perplexity-search-server",
    host="0.0.0.0",
    port=PORT
)


@mcp.tool()
async def search(
    query: str,
    search_recency_filter: Optional[str] = None
) -> str:
    """
    Perform a web search using Perplexity's API, which provides detailed and 
    contextually relevant results with citations. By default, no time filtering 
    is applied to search results.
    
    Args:
        query: The search query to perform
        search_recency_filter: Filter search results by recency. 
                              Options: month, week, day, hour. 
                              If not specified, no time filtering is applied.
    
    Returns:
        JSON string containing search results with content and citations
    """
    # Validate search_recency_filter if provided
    if search_recency_filter and search_recency_filter not in ["month", "week", "day", "hour"]:
        return json.dumps({
            "error": f"Invalid search_recency_filter: {search_recency_filter}. Must be one of: month, week, day, hour"
        }, indent=2)
    
    try:
        # Build the payload
        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
        
        # Add optional parameters if provided
        if search_recency_filter:
            payload["search_recency_filter"] = search_recency_filter
        
        print(f"Using model: {MODEL}, max_tokens: {MAX_TOKENS}, temperature: {TEMPERATURE}", 
              file=sys.stderr)
        
        # Get API key from environment
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            return json.dumps({
                "error": "PERPLEXITY_API_KEY environment variable is not set"
            }, indent=2)
        
        # Make the API request
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
        
        # Format the response to only include content and citations
        formatted_response = {
            "content": data["choices"][0]["message"]["content"],
            "citations": data.get("citations", [])
        }
        
        return json.dumps(formatted_response, indent=2)
        
    except httpx.HTTPStatusError as e:
        error_message = f"Perplexity API error: {e.response.status_code}"
        try:
            error_data = e.response.json()
            error_message = f"Perplexity API error: {error_data.get('error', error_data.get('message', str(e)))}"
        except:
            pass
        
        return json.dumps({"error": error_message}, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error: {str(e)}"}, indent=2)


def main():
    """Main entry point."""
    print(f"Starting Perplexity Search MCP Server on port {PORT}...", file=sys.stderr)
    mcp.run()


if __name__ == "__main__":
    main()
