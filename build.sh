# Render Build Script
#!/usr/bin/env bash
# Build script for Render

set -o errexit  # exit on error

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p models
mkdir -p static/uploads
mkdir -p logs

echo "Build completed successfully!"