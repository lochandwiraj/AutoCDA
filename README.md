# README.md

AutoCDA — AI-powered circuit design automation (Day 1 scaffold)

This repo contains a FastAPI app, Temporal workflow skeleton, and a PostgreSQL DB for the AutoCDA project.

Quickstart:
1. Copy .env.example to .env and set OPENROUTER_API_KEY
2. uv venv
3. . .\.venv\Scripts\Activate.ps1
4. uv pip install -r requirements.txt
5. docker compose up -d
6. python scripts/init_db.py
7. python -m uvicorn app.main:app --reload
8. python temporal_workflows/worker.py

API:
- Health: GET /health
- LLM generate: POST /api/v1/llm/generate  (body: {"prompt":"..."})
- Create design: POST /api/v1/designs
