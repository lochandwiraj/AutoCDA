# app/api/v1/llm_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import openrouter_generate

router = APIRouter(prefix="/api/v1/llm", tags=["LLM"])

class GenRequest(BaseModel):
    prompt: str

class GenResponse(BaseModel):
    response: dict

@router.post("/generate", response_model=GenResponse)
def generate(req: GenRequest):
    try:
        result = openrouter_generate(req.prompt)
        return GenResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
