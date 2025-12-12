# Perplexity Search MCP - Usage Examples

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Server](#running-the-server)
5. [Using the Search Tool](#using-the-search-tool)
6. [Response Format](#response-format)
7. [Advanced Usage](#advanced-usage)

---

## Quick Start

```bash
# 1. Install dependencies
bash install.sh

# 2. Set your API key
export PERPLEXITY_API_KEY="your-api-key-here"

# 3. Run the server
python3.11 src/index.py
```

---

## Installation

### Method 1: Using the install script (Recommended)
```bash
bash install.sh
```

### Method 2: Manual installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or with Python 3.11 specifically
python3.11 -m pip install -r requirements.txt
```

### Method 3: Using setup.py
```bash
pip install -e .
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
PERPLEXITY_API_KEY=pplx-your-api-key-here

# Optional
PORT=3001
```

Or export them directly:

```bash
export PERPLEXITY_API_KEY="pplx-your-api-key-here"
export PORT=3001
```

### Get Your API Key

1. Go to [Perplexity AI](https://www.perplexity.ai/)
2. Sign up or log in
3. Navigate to API settings
4. Generate an API key

---

## Running the Server

### Option 1: Default (sonar-pro model)
```bash
python3.11 src/index.py
```

### Option 2: Using sonar model
```bash
python3.11 src/index.py --model sonar
```

### Option 3: Using the run script
```bash
bash run.sh
```

### Option 4: With custom port
```bash
PORT=8080 python3.11 src/index.py
```

### Option 5: Docker
```bash
# Build the image
docker build -t perplexity-search-mcp .

# Run the container
docker run -p 3001:3001 \
  -e PERPLEXITY_API_KEY=your-api-key \
  perplexity-search-mcp
```

### Expected Output
```
Using Perplexity model: sonar-pro
Starting Perplexity Search MCP Server on port 3001...
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3001 (Press CTRL+C to quit)
```

---

## Using the Search Tool

### Tool Definition

The server provides a `search` tool with the following parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | The search query to perform |
| `search_recency_filter` | string | No | Filter by recency: `month`, `week`, `day`, `hour` |

### Example 1: Basic Search

**Request:**
```json
{
  "tool": "search",
  "arguments": {
    "query": "What are the latest developments in AI?"
  }
}
```

**Response:**
```json
{
  "content": "Recent developments in AI include advances in large language models, multimodal AI systems, and improved reasoning capabilities...",
  "citations": [
    "https://example.com/ai-news-1",
    "https://example.com/ai-news-2"
  ]
}
```

### Example 2: Search with Recency Filter

**Request:**
```json
{
  "tool": "search",
  "arguments": {
    "query": "OpenAI announcements",
    "search_recency_filter": "week"
  }
}
```

**Response:**
```json
{
  "content": "In the past week, OpenAI announced several updates including...",
  "citations": [
    "https://openai.com/blog/announcement-1",
    "https://techcrunch.com/openai-news"
  ]
}
```

### Example 3: Recent News (Last 24 Hours)

**Request:**
```json
{
  "tool": "search",
  "arguments": {
    "query": "stock market today",
    "search_recency_filter": "day"
  }
}
```

### Example 4: Breaking News (Last Hour)

**Request:**
```json
{
  "tool": "search",
  "arguments": {
    "query": "breaking tech news",
    "search_recency_filter": "hour"
  }
}
```

---

## Response Format

### Success Response

```json
{
  "content": "The main answer content with detailed information...",
  "citations": [
    "https://source1.com/article",
    "https://source2.com/page",
    "https://source3.com/document"
  ]
}
```

### Error Response

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Messages

1. **Missing API Key:**
```json
{
  "error": "PERPLEXITY_API_KEY environment variable is not set"
}
```

2. **Invalid Recency Filter:**
```json
{
  "error": "Invalid search_recency_filter: invalid_value. Must be one of: month, week, day, hour"
}
```

3. **API Error:**
```json
{
  "error": "Perplexity API error: 401 - Invalid API key"
}
```

---

## Advanced Usage

### Using with MCP Clients

#### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "perplexity-search": {
      "command": "python3.11",
      "args": ["/path/to/perplexity-search-mcp/src/index.py"],
      "env": {
        "PERPLEXITY_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Using Different Models

**Sonar Model (Faster, Lower Cost):**
```json
{
  "mcpServers": {
    "perplexity-search": {
      "command": "python3.11",
      "args": [
        "/path/to/perplexity-search-mcp/src/index.py",
        "--model",
        "sonar"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Sonar-Pro Model (More Detailed, Higher Quality):**
```json
{
  "mcpServers": {
    "perplexity-search": {
      "command": "python3.11",
      "args": [
        "/path/to/perplexity-search-mcp/src/index.py",
        "--model",
        "sonar-pro"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Testing with cURL

#### Test the SSE Endpoint
```bash
curl -N http://localhost:3001/sse
```

#### Test Search via HTTP (if using HTTP transport)
```bash
curl -X POST http://localhost:3001/messages \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "search",
      "arguments": {
        "query": "Python programming best practices",
        "search_recency_filter": "month"
      }
    }
  }'
```

### Python Client Example

```python
import httpx
import json

async def search_perplexity(query: str, recency: str = None):
    """Example client function to call the search tool."""
    
    payload = {
        "method": "tools/call",
        "params": {
            "name": "search",
            "arguments": {
                "query": query
            }
        }
    }
    
    if recency:
        payload["params"]["arguments"]["search_recency_filter"] = recency
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:3001/messages",
            json=payload,
            timeout=60.0
        )
        return response.json()

# Usage
import asyncio

result = asyncio.run(search_perplexity(
    "What is FastAPI?",
    recency="week"
))
print(json.dumps(result, indent=2))
```

---

## Troubleshooting

### Server Won't Start

**Problem:** `ModuleNotFoundError: No module named 'mcp'`

**Solution:**
```bash
python3.11 -m pip install -r requirements.txt
```

### API Key Issues

**Problem:** `PERPLEXITY_API_KEY environment variable is not set`

**Solution:**
```bash
# Check if .env file exists
cat .env

# Or set it directly
export PERPLEXITY_API_KEY="your-api-key"
```

### Port Already in Use

**Problem:** `Address already in use`

**Solution:**
```bash
# Use a different port
PORT=8080 python3.11 src/index.py

# Or kill the process using port 3001
lsof -ti:3001 | xargs kill -9
```

### Python Version Issues

**Problem:** `python3.11: command not found`

**Solution:**
```bash
# Check available Python versions
python3 --version

# Use available version (must be 3.11+)
python3 src/index.py
```

---

## Model Comparison

| Feature | sonar | sonar-pro |
|---------|-------|-----------|
| Speed | Faster | Slower |
| Cost | Lower | Higher |
| Detail | Good | Excellent |
| Citations | Yes | Yes |
| Best For | Quick searches | In-depth research |

---

## API Limits

- **Rate Limits:** Check Perplexity's current rate limits
- **Token Limits:** Max 8192 tokens per request (configurable in code)
- **Timeout:** 60 seconds per request

---

## Support

For issues or questions:
1. Check the [MIGRATION.md](MIGRATION.md) for technical details
2. Review the [README.md](README.md) for basic setup
3. Open an issue on GitHub

---

## License

MIT License - See LICENSE file for details
