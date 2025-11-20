from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.circuit_design import CircuitDesign
from app.schemas.circuit_design import (
    CircuitDesignCreate,
    CircuitDesignUpdate,
    CircuitDesignResponse,
)

router = APIRouter()


@router.post("/", response_model=CircuitDesignResponse, status_code=status.HTTP_201_CREATED)
def create_circuit_design(
    circuit_design: CircuitDesignCreate,
    db: Session = Depends(get_db)
):
    db_circuit_design = CircuitDesign(**circuit_design.model_dump())
    db.add(db_circuit_design)
    db.commit()
    db.refresh(db_circuit_design)
    return db_circuit_design


@router.get("/", response_model=List[CircuitDesignResponse])
def list_circuit_designs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    circuit_designs = db.query(CircuitDesign).offset(skip).limit(limit).all()
    return circuit_designs


@router.get("/{circuit_design_id}", response_model=CircuitDesignResponse)
def get_circuit_design(
    circuit_design_id: UUID,
    db: Session = Depends(get_db)
):
    circuit_design = db.query(CircuitDesign).filter(CircuitDesign.id == circuit_design_id).first()
    if not circuit_design:
        raise HTTPException(status_code=404, detail="Circuit design not found")
    return circuit_design


@router.put("/{circuit_design_id}", response_model=CircuitDesignResponse)
def update_circuit_design(
    circuit_design_id: UUID,
    circuit_design_update: CircuitDesignUpdate,
    db: Session = Depends(get_db)
):
    circuit_design = db.query(CircuitDesign).filter(CircuitDesign.id == circuit_design_id).first()
    if not circuit_design:
        raise HTTPException(status_code=404, detail="Circuit design not found")

    update_data = circuit_design_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(circuit_design, field, value)

    db.commit()
    db.refresh(circuit_design)
    return circuit_design


@router.delete("/{circuit_design_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_circuit_design(
    circuit_design_id: UUID,
    db: Session = Depends(get_db)
):
    circuit_design = db.query(CircuitDesign).filter(CircuitDesign.id == circuit_design_id).first()
    if not circuit_design:
        raise HTTPException(status_code=404, detail="Circuit design not found")

    db.delete(circuit_design)
    db.commit()
    return None
