#!/usr/bin/env bash

# Force Render to use the correct Python version and install dependencies
echo "🔧 Installing dependencies..."
pip install --upgrade pip

# Install dependencies from requirements.txt (force binary wheels for pandas)
pip install --only-binary=:all: pandas
pip install -r requirements.txt

echo "✅ Build completed successfully!"
