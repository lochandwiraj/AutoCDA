#!/bin/bash

echo "🚀 Starting AutoCDA with React Frontend"
echo "========================================"
echo ""

# Check if backend is running
if ! curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "⚠️  Backend not running. Starting backend..."
    echo ""
    cd "$(dirname "$0")"
    python backend/api.py &
    BACKEND_PID=$!
    echo "✓ Backend started (PID: $BACKEND_PID)"
    sleep 3
else
    echo "✓ Backend already running"
fi

echo ""
echo "🎨 Starting React frontend..."
cd client
npm run dev
