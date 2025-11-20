#!/bin/bash

echo "🚀 Setting up AutoCDA development environment..."

if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo "🐍 Creating virtual environment..."
uv venv
source .venv/bin/activate

echo "📚 Installing dependencies..."
uv pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
fi

echo "🐳 Starting Docker services..."
docker-compose up -d

echo "⏳ Waiting for PostgreSQL..."
sleep 5

echo "🗄️  Initializing database..."
python scripts/init_db.py

echo "🧪 Running tests..."
pytest tests/ -v

echo "✅ Development environment ready!"
