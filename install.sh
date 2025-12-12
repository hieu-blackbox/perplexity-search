#!/bin/bash

# Exit on error
set -e

# Process environment variables from command line arguments
for arg in "$@"; do
  export "$arg"
done

echo "Installing Python dependencies..."
python3.11 -m pip install -r requirements.txt

echo "Installation completed successfully!"
