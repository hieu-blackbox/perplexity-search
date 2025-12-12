#!/bin/bash

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Run the server
echo "Starting Perplexity Search MCP Server (Python)..."
python3 src/index.py "$@"
