# Perplexity Search MCP (Python Version)

A Python implementation of the Model Context Protocol (MCP) server for Perplexity's web search with sonar or sonar-pro models.

## Features

- Provides a `search` tool for AI assistants to perform web searches
- Uses Perplexity's chat completions API with the sonar/sonar-pro models
- Built with Python using the MCP SDK
- SSE (Server-Sent Events) transport over HTTP

## Requirements

- Python 3.10 or higher (Python 3.11+ recommended)
- Perplexity API key

## Installation

### Using pip

```bash
# Install dependencies
pip install -r requirements.txt
```

### Using virtual environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root or set the following environment variable:

- `PERPLEXITY_API_KEY`: Your Perplexity API key (required)
- `PORT`: Server port (optional, defaults to 3001)

Example `.env` file:
```
PERPLEXITY_API_KEY=your-api-key-here
PORT=3001
```

## Usage

### Running the Server

```bash
# Run with default model (sonar-pro)
python src/server.py

# Run with specific model
python src/server.py --model sonar
python src/server.py --model sonar-pro
```

### Using the Installation Script

```bash
# Make the script executable
chmod +x install-python.sh

# Run installation
./install-python.sh PERPLEXITY_API_KEY=your-api-key-here
```

### Using the Run Script

```bash
# Make the script executable
chmod +x run-python.sh

# Run the server
./run-python.sh PERPLEXITY_API_KEY=your-api-key-here
```

## Tool: search

The server provides a `search` tool with the following input parameters:

- `query` (required): The search query to perform
- `search_recency_filter` (optional): Filter search results by recency
  - Options: `month`, `week`, `day`, `hour`
  - If not specified, no time filtering is applied

## Response Format

The response from the `search` tool includes:

- `content`: The search results content
- `citations`: Array of citations for the information

## API Endpoints

When running, the server exposes:

- `GET /sse`: SSE endpoint for establishing MCP connection
- `POST /messages`: Endpoint for sending messages to the MCP server

## Docker Support

Build and run using Docker:

```bash
# Build the image
docker build -f Dockerfile-python -t perplexity-search-mcp-python .

# Run the container
docker run -p 3001:3001 -e PERPLEXITY_API_KEY=your-api-key-here perplexity-search-mcp-python
```

## Development

### Project Structure

```
.
├── src/
│   └── server.py          # Main MCP server implementation
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup configuration
├── pyproject.toml        # Modern Python project configuration
├── .env.example          # Example environment variables
├── install-python.sh     # Installation script
├── run-python.sh         # Run script
└── README-PYTHON.md      # This file
```

### Dependencies

- `mcp`: Model Context Protocol SDK for Python
- `httpx`: Async HTTP client for API requests
- `python-dotenv`: Environment variable management
- `starlette`: ASGI framework for SSE transport
- `uvicorn`: ASGI server

## Comparison with TypeScript Version

This Python implementation provides the same functionality as the TypeScript version:

- ✅ Same MCP tool interface (`search`)
- ✅ Same Perplexity API integration
- ✅ Same model support (sonar, sonar-pro)
- ✅ Same SSE transport mechanism
- ✅ Same configuration options
- ✅ Compatible response format

## License

MIT

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
2. **API key not found**: Ensure `PERPLEXITY_API_KEY` is set in your `.env` file or environment
3. **Port already in use**: Change the `PORT` environment variable to use a different port
4. **Python version**: This project requires Python 3.10 or higher. On Amazon Linux 2023, install with: `sudo dnf install -y python3.11 python3.11-pip`

### Getting Help

If you encounter issues:
1. Check that your Perplexity API key is valid
2. Verify all dependencies are installed correctly
3. Check the server logs for error messages
4. Ensure your Python version is 3.10 or higher
