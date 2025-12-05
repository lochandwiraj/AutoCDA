#!/bin/bash

echo "🔒 AutoCDA Backup Deployment"
echo "=============================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install flask pydantic skidl python-dotenv requests

# Generate demo files
echo "🔧 Generating demo files..."
python3 generate_demo_files.py

# Start standalone server
echo "🚀 Starting standalone server..."
echo "Access at: http://localhost:5000"
python3 app_standalone.py
