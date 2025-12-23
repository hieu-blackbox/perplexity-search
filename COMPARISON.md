# TypeScript vs Python Implementation Comparison

This document compares the TypeScript and Python implementations of the Perplexity Search MCP server.

## Overview

Both implementations provide identical functionality through the Model Context Protocol (MCP), allowing AI assistants to perform web searches using Perplexity's API.

## Feature Parity

| Feature | TypeScript | Python | Notes |
|---------|-----------|--------|-------|
| MCP Protocol Support | ✅ | ✅ | Both use official MCP SDK |
| Search Tool | ✅ | ✅ | Identical interface |
| Model Selection | ✅ | ✅ | sonar and sonar-pro |
| Recency Filtering | ✅ | ✅ | month, week, day, hour |
| SSE Transport | ✅ | ✅ | Server-Sent Events over HTTP |
| Environment Variables | ✅ | ✅ | .env file support |
| Docker Support | ✅ | ✅ | Separate Dockerfiles |
| CLI Arguments | ✅ | ✅ | --model flag |
| Error Handling | ✅ | ✅ | Comprehensive error messages |
| Citations | ✅ | ✅ | Returns citations array |

## Technical Differences

### Language & Runtime

**TypeScript:**
- Runtime: Node.js 18+
- Package Manager: npm
- Build Step: Required (TypeScript → JavaScript)
- Type System: TypeScript static typing

**Python:**
- Runtime: Python 3.10+
- Package Manager: pip
- Build Step: Not required (interpreted)
- Type System: Python type hints

### Dependencies

**TypeScript:**
```json
{
  "@modelcontextprotocol/sdk": "0.5.0",
  "express": "^5.1.0",
  "axios": "^1.6.0",
  "dotenv": "^16.3.1",
  "zod-to-json-schema": "^3.23.5"
}
```

**Python:**
```
mcp>=0.9.0
httpx>=0.27.0
python-dotenv>=1.0.0
starlette>=0.37.0
uvicorn>=0.30.0
```

### Project Structure

**TypeScript:**
```
src/
  index.ts          # Main server file
dist/               # Compiled JavaScript (generated)
package.json        # Dependencies & scripts
tsconfig.json       # TypeScript configuration
```

**Python:**
```
src/
  server.py         # Main server file
requirements.txt    # Dependencies
setup.py            # Package setup
pyproject.toml      # Modern Python config
```

### Installation & Setup

**TypeScript:**
```bash
npm install
npm run build
npm start
```

**Python:**
```bash
pip install -r requirements.txt
python3.11 src/server.py
```

Or using the provided scripts:
```bash
./install-python.sh
./run-python.sh PERPLEXITY_API_KEY=your-key
```

### HTTP Framework

**TypeScript:**
- Framework: Express.js
- SSE Implementation: @modelcontextprotocol/sdk SSEServerTransport

**Python:**
- Framework: Starlette (ASGI)
- Server: Uvicorn
- SSE Implementation: mcp.server.sse.SseServerTransport

### API Client

**TypeScript:**
- HTTP Client: axios
- Async Pattern: Promises with async/await

**Python:**
- HTTP Client: httpx
- Async Pattern: asyncio with async/await

## Performance Considerations

### Startup Time
- **TypeScript**: Faster startup (pre-compiled JavaScript)
- **Python**: Slightly slower (interpreted, but negligible for server applications)

### Memory Usage
- **TypeScript**: ~50-100MB (Node.js runtime)
- **Python**: ~40-80MB (Python interpreter + dependencies)

### Request Handling
- Both implementations use async I/O
- Performance is primarily limited by Perplexity API response time
- Negligible difference in real-world usage

## Development Experience

### TypeScript Advantages
- ✅ Strong static typing catches errors at compile time
- ✅ Excellent IDE support and autocomplete
- ✅ Large ecosystem of Node.js packages
- ✅ Familiar to JavaScript developers

### Python Advantages
- ✅ No build step required
- ✅ Simpler deployment (single .py file)
- ✅ More concise code
- ✅ Familiar to Python/ML developers
- ✅ Better for data science workflows

## Deployment

### TypeScript
```dockerfile
FROM node:lts-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --ignore-scripts
COPY . .
RUN npm run build
CMD ["node", "dist/index.js"]
```

### Python
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["python", "src/server.py"]
```

## Configuration

Both implementations support identical configuration:

### Environment Variables
- `PERPLEXITY_API_KEY`: API key (required)
- `PORT`: Server port (default: 3001)

### Command Line Arguments
- `--model sonar`: Use sonar model
- `--model sonar-pro`: Use sonar-pro model (default)

### Smithery Configuration
Both have smithery.yaml files for easy integration with Smithery.ai

## Testing

### TypeScript
```bash
npm test                    # Run tests
npm run build              # Type checking
```

### Python
```bash
python -m pytest           # Run tests
python -m mypy src/        # Type checking
python -m py_compile src/server.py  # Syntax check
```

## Which Should You Choose?

### Choose TypeScript if:
- You're already using Node.js in your stack
- You prefer strong static typing
- Your team is more familiar with JavaScript/TypeScript
- You want compile-time error checking

### Choose Python if:
- You're already using Python in your stack
- You prefer simpler deployment (no build step)
- Your team is more familiar with Python
- You're integrating with Python-based ML/AI tools
- You want more concise code

## Migration Between Versions

Both implementations are API-compatible, so you can switch between them without changing your MCP client configuration. The tool interface, request/response formats, and behavior are identical.

## Conclusion

Both implementations are production-ready and provide identical functionality. The choice between them should be based on your team's expertise, existing infrastructure, and personal preference rather than technical capabilities.
