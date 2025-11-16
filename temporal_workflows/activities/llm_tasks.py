# temporal_workflows/activities/llm_tasks.py
from app.services.llm_service import llm_service

async def generate_circuit_description(prompt: str) -> str:
    \"\"\"Temporal activity using OpenRouter LLM\"\"\"
    return await llm_service.generate(prompt)
