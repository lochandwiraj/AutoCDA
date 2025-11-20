# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
import os

# -----------------------------
# Load settings & loggers
# -----------------------------
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

# -----------------------------
# Routers (both sets merged)
# -----------------------------
from app.api import (
    health,
    circuit_designs,
    components,
    simulation_results
)

# Friend’s v1 LLM endpoints
from app.api.v1.llm_routes import router as llm_router


# ---------------------------------------------------------
# FastAPI Instance
# ---------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Include Core Routers
# ---------------------------------------------------------
app.include_router(health.router, tags=["health"])

app.include_router(
    circuit_designs.router,
    prefix=f"{settings.API_V1_PREFIX}/circuit-designs",
    tags=["circuit-designs"]
)

app.include_router(
    components.router,
    prefix=f"{settings.API_V1_PREFIX}/components",
    tags=["components"]
)

app.include_router(
    simulation_results.router,
    prefix=f"{settings.API_V1_PREFIX}/simulation-results",
    tags=["simulation-results"]
)

# ---------------------------------------------------------
# Include LLM Router (friend’s API)
# ---------------------------------------------------------
app.include_router(llm_router, prefix="/api/v1", tags=["llm"])


# ---------------------------------------------------------
# Health check (friend's version kept too)
# ---------------------------------------------------------
@app.get("/health/full")
async def full_health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.PROJECT_VERSION,
        "services": {
            "api": "up",
            "database": "unknown",
            "temporal": "unknown",
        }
    }


# ---------------------------------------------------------
# Startup / Shutdown Events
# ---------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info("Documentation available at /docs")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------
@app.get("/")
async def root():
    return {
        "message": "Circuit Design API",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "health": "/health/full",
    }


# ---------------------------------------------------------
# Global Exception Handler (kept from friend)
# ---------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(status_code=500, content={
        "message": "Internal server error",
        "detail": str(exc)
    })


# ---------------------------------------------------------
# For running standalone
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True,
    )
