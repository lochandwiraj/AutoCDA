# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from datetime import datetime
import os

# attach local modules
from app.api.v1.llm_routes import router as llm_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AutoCDA API",
    description="Automatic Circuit Design Assistant - AI-powered circuit generation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
app.include_router(llm_router)

class CircuitRequest(BaseModel):
    description: str
    constraints: dict = {}
    user_id: str | None = None

class CircuitResponse(BaseModel):
    design_id: str
    status: str
    message: str
    workflow_id: str | None = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    services: dict

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "services": {
            "api": "up",
            "temporal": "unknown",
            "database": "unknown",
        }
    }

@app.get("/")
async def root():
    return {"message": "Welcome to AutoCDA API", "docs": "/docs", "health": "/health"}

@app.post("/api/v1/designs", response_model=CircuitResponse)
async def create_design(request: CircuitRequest):
    logger.info(f"Received design request: {request.description}")
    design_id = f"design-{datetime.utcnow().timestamp()}"
    # For Day1: store minimal response and return. Workflow to be started by Temporal in Day2.
    return CircuitResponse(design_id=design_id, status="processing", message="Circuit design generation started", workflow_id=f"workflow-{design_id}")

@app.get("/api/v1/designs/{design_id}")
async def get_design(design_id: str):
    return {"design_id": design_id, "status": "not_implemented"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(status_code=500, content={"message": "Internal server error", "detail": str(exc)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=os.getenv("API_HOST","0.0.0.0"), port=int(os.getenv("API_PORT",8000)), reload=True)
