from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
settings = get_settings()
from app.core.logging import logger
from app.api import health, circuit_designs, components, simulation_results

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Documentation available at: /docs")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


@app.get("/")
async def root():
    return {
        "message": "Circuit Design API",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs"
    }
