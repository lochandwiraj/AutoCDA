# app/services/llm_service.py
import requests
import os
from app.config.llm_config import settings

def openrouter_generate(prompt: str, max_tokens: int = 1024):
    key = settings.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in environment or .env")
    url = f"{settings.OPENROUTER_URL}/responses"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": settings.OPENROUTER_MODEL,
        "input": prompt,
        "max_tokens": max_tokens,
    }
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()
