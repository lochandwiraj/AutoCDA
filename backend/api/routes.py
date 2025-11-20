from fastapi import APIRouter
from api.components import router as components_router

router = APIRouter()
router.include_router(components_router)
