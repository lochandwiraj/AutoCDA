Write-Host "🚀 Setting up AutoCDA development environment (Windows PS)..."

# 1) Ensure uv exists (if not, install using curl)
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing uv..."
    iex "& { iwr -useb https://astral.sh/uv/install.ps1 }"
}

# 2) Create virtual environment with uv
Write-Host "🐍 Creating virtual environment..."
uv venv

# 3) Activate venv for this session
Write-Host "🔁 Activating virtualenv for this terminal..."
. .\.venv\Scripts\Activate.ps1

# 4) Install Python dependencies
Write-Host "📚 Installing dependencies..."
uv pip install -r requirements.txt

# 5) Create .env from example if missing
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "⚠️  .env created from .env.example. Edit .env to add API keys."
}

# 6) Start Docker services
Write-Host "🐳 Starting Docker services..."
docker compose up -d

# 7) Small wait for DB to start (improve with a real wait if needed)
Start-Sleep -Seconds 6

# 8) Initialize database
Write-Host "🗄️  Initializing database..."
python .\scripts\init_db.py

# 9) Run tests
Write-Host "🧪 Running pytest..."
pytest tests/ -v

Write-Host "✅ Development environment ready!"
Write-Host ""
Write-Host "To start the API server (in this terminal):"
Write-Host "  . .\.venv\Scripts\Activate.ps1"
Write-Host "  python app/main.py"
Write-Host ""
Write-Host "To start Temporal worker:"
Write-Host "  python temporal_workflows\worker.py"
