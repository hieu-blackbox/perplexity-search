# Python Quick Start Guide

Get the Perplexity Search MCP server running in Python in under 5 minutes.

## Prerequisites

- Python 3.10 or higher (Python 3.11+ recommended)
- Perplexity API key ([Get one here](https://www.perplexity.ai/settings/api))

## Installation

### Option 1: Using the Installation Script (Recommended)

```bash
# Make the script executable
chmod +x install-python.sh

# Run installation
./install-python.sh
```

### Option 2: Manual Installation

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Option 3: System-wide Installation

```bash
# Install dependencies globally (not recommended for production)
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```bash
echo "PERPLEXITY_API_KEY=your-api-key-here" > .env
```

Or export the environment variable:

```bash
export PERPLEXITY_API_KEY=your-api-key-here
```

## Running the Server

### Option 1: Using the Run Script

```bash
# Make the script executable
chmod +x run-python.sh

# Run with environment variable
./run-python.sh PERPLEXITY_API_KEY=your-api-key-here

# Or if you have a .env file
./run-python.sh
```

### Option 2: Direct Python Execution

```bash
# Activate virtual environment (if using one)
source venv/bin/activate

# Run with default model (sonar-pro)
python3.11 src/server.py

# Run with specific model
python3.11 src/server.py --model sonar
python3.11 src/server.py --model sonar-pro
```

### Option 3: Using Environment Variables

```bash
# Set environment variables and run
PERPLEXITY_API_KEY=your-api-key-here PORT=3001 python3.11 src/server.py
```

## Verify Installation

Once the server is running, you should see:

```
Using Perplexity model: sonar-pro
Server is running on port 3001
```

The server exposes two endpoints:
- `GET http://localhost:3001/sse` - SSE endpoint for MCP connection
- `POST http://localhost:3001/messages` - Message handling endpoint

## Using with MCP Clients

### Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "perplexity-search": {
      "command": "python3.11",
      "args": ["/path/to/perplexity-search-mcp/src/server.py"],
      "env": {
        "PERPLEXITY_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Other MCP Clients

Configure your MCP client to connect to:
- **SSE URL**: `http://localhost:3001/sse`
- **Messages URL**: `http://localhost:3001/messages`

## Testing the Search Tool

Once connected to an MCP client, you can use the `search` tool:

```
Search for: "latest developments in AI"
```

With recency filter:
```
Search for: "Python 3.12 new features" with recency filter: "month"
```

## Docker Deployment

### Build the Image

```bash
docker build -f Dockerfile-python -t perplexity-search-mcp-python .
```

### Run the Container

```bash
docker run -p 3001:3001 \
  -e PERPLEXITY_API_KEY=your-api-key-here \
  perplexity-search-mcp-python
```

### With Custom Model

```bash
docker run -p 3001:3001 \
  -e PERPLEXITY_API_KEY=your-api-key-here \
  perplexity-search-mcp-python \
  python src/server.py --model sonar
```

## Troubleshooting

### Python Version Issues

If you get "Python 3.10 or higher is required":

**On Amazon Linux 2023:**
```bash
sudo dnf install -y python3.11 python3.11-pip
```

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

**On macOS:**
```bash
brew install python@3.11
```

### Import Errors

Make sure all dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### API Key Not Found

Ensure your API key is set:
```bash
# Check if it's set
echo $PERPLEXITY_API_KEY

# Set it if not
export PERPLEXITY_API_KEY=your-api-key-here
```

### Port Already in Use

Change the port:
```bash
PORT=3002 python3.11 src/server.py
```

### Virtual Environment Issues

If virtual environment activation fails:
```bash
# Remove old venv
rm -rf venv

# Create new one
python3.11 -m venv venv

# Activate and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

- Read the full [Python README](README-PYTHON.md)
- Compare with [TypeScript version](COMPARISON.md)
- Check out the [API documentation](README.md)
- Deploy to production using Docker

## Support

For issues or questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review the [full documentation](README-PYTHON.md)
3. Open an issue on GitHub

## License

MIT
