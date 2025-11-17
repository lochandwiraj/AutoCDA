from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from models.component import Component
from scripts.database import get_db

router = APIRouter(prefix="/api/components", tags=["components"])

@router.get("/search")
def search_components(
    query: Optional[str] = None,
    type: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Search components with full SQLAlchemy filters"""
    q = db.query(Component)

    if query:
        q = q.filter(Component.id.ilike(f"%{query}%"))

    if type:
        q = q.filter(Component.type == type)

    if min_value is not None:
        q = q.filter(Component.value_numeric >= min_value)

    if max_value is not None:
        q = q.filter(Component.value_numeric <= max_value)

    return q.limit(100).all()

@router.get("/{component_id}")
def get_component(component_id: str, db: Session = Depends(get_db)):
    comp = db.query(Component).filter(Component.id == component_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")
    return comp
