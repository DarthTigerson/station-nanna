#!/bin/bash

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew first."
        exit 1
    fi
    brew install vlc
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    sudo apt-get update
    sudo apt-get install -y vlc
else
    echo "Unsupported operating system"
    exit 1
fi

echo "VLC installed successfully"

# Check if PDM is installed
if ! command -v pdm &> /dev/null; then
    echo "PDM not found. Installing PDM..."
    python -m pip install --user pdm
fi

# Run PDM install
echo "Installing Python dependencies..."
pdm install

echo "Setup completed successfully!"

