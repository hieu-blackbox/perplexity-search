#!/bin/bash

# Exit on error
set -e

# Process environment variables from command line arguments
for arg in "$@"; do
  export "$arg"
done

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running installation..."
    ./install-python.sh "$@"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if PERPLEXITY_API_KEY is set
if [ -z "$PERPLEXITY_API_KEY" ]; then
    if [ -f ".env" ]; then
        echo "Loading environment variables from .env file..."
        export $(cat .env | grep -v '^#' | xargs)
    else
        echo "Warning: PERPLEXITY_API_KEY is not set and .env file not found."
        echo "Please set PERPLEXITY_API_KEY environment variable or create a .env file."
        exit 1
    fi
fi

# Detect Python command
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "Starting Python MCP server with provided environment variables..."
$PYTHON_CMD src/server.py "$@"
