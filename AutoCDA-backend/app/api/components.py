from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.component import Component
from app.schemas.component import (
    ComponentCreate,
    ComponentUpdate,
    ComponentResponse,
)

router = APIRouter()


@router.post("/", response_model=ComponentResponse, status_code=status.HTTP_201_CREATED)
def create_component(
    component: ComponentCreate,
    db: Session = Depends(get_db)
):
    db_component = Component(**component.model_dump())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component


@router.get("/", response_model=List[ComponentResponse])
def list_components(
    circuit_design_id: UUID = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Component)
    if circuit_design_id:
        query = query.filter(Component.circuit_design_id == circuit_design_id)
    components = query.offset(skip).limit(limit).all()
    return components


@router.get("/{component_id}", response_model=ComponentResponse)
def get_component(
    component_id: UUID,
    db: Session = Depends(get_db)
):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return component


@router.put("/{component_id}", response_model=ComponentResponse)
def update_component(
    component_id: UUID,
    component_update: ComponentUpdate,
    db: Session = Depends(get_db)
):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    update_data = component_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(component, field, value)

    db.commit()
    db.refresh(component)
    return component


@router.delete("/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_component(
    component_id: UUID,
    db: Session = Depends(get_db)
):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    db.delete(component)
    db.commit()
    return None
