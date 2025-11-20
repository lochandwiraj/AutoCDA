# docs/QUICKSTART.md

See README.md quickstart — use these steps to run locally.

1. Copy .env.example -> .env and add OPENROUTER_API_KEY
2. Activate venv and install requirements
3. Start Docker services (DB + Temporal + Temporal UI)
4. Initialize DB: python scripts/init_db.py
5. Start worker: python temporal_workflows/worker.py
6. Start API: python -m uvicorn app.main:app --reload
7. Test LLM: POST /api/v1/llm/generate
