#!/bin/bash

# AutoCDA Localhost Demo Server
# Use if internet fails at venue

echo "Starting AutoCDA localhost server..."
echo "This will run WITHOUT Claude API (offline mode)"
echo ""

cd "$(dirname "$0")"

# Set offline mode flag
export AUTOCDA_OFFLINE_MODE=true

# Use pre-generated examples only
export USE_CACHED_CIRCUITS=true

# Start server
echo "Server starting at http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python backend/api.py --host=0.0.0.0 --port=5000
