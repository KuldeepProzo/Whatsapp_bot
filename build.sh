#!/usr/bin/env bash

# Set correct Python version for Render
echo "python-3.11.8" > runtime.txt

echo "🔧 Installing dependencies..."
pip install --upgrade pip

# Install dependencies (use binary for pandas)
pip install --only-binary=:all: pandas
pip install -r requirements.txt

echo "✅ Build completed successfully!"
