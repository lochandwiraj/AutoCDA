from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.circuit import CircuitDesign, DesignStatus
from app.schemas.circuit import (
    CircuitDesignCreate,
    CircuitDesignResponse,
    CircuitDesignDetail,
)

router = APIRouter()

# ---------------------------------------------------------
# CREATE CIRCUIT DESIGN
# ---------------------------------------------------------
@router.post("/", response_model=CircuitDesignResponse, status_code=status.HTTP_201_CREATED)
def create_circuit_design(
    design_data: CircuitDesignCreate,
    db: Session = Depends(get_db)
):
    design = CircuitDesign(
        description=design_data.description,
        constraints=design_data.constraints or {},
        status=DesignStatus.pending
    )

    db.add(design)
    db.commit()
    db.refresh(design)

    return design


# ---------------------------------------------------------
# LIST DESIGNS
# ---------------------------------------------------------
@router.get("/", response_model=list[CircuitDesignResponse])
def list_circuit_designs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(CircuitDesign).offset(skip).limit(limit).all()


# ---------------------------------------------------------
# GET DESIGN BY ID
# ---------------------------------------------------------
@router.get("/{design_id}", response_model=CircuitDesignDetail)
def get_circuit_design(
    design_id: UUID,
    db: Session = Depends(get_db)
):
    design = db.query(CircuitDesign).filter(CircuitDesign.id == design_id).first()

    if not design:
        raise HTTPException(status_code=404, detail="Circuit design not found")

    return design


# ---------------------------------------------------------
# UPDATE (Only description + constraints allowed for now)
# ---------------------------------------------------------
@router.put("/{design_id}", response_model=CircuitDesignResponse)
def update_circuit_design(
    design_id: UUID,
    update_data: CircuitDesignCreate,
    db: Session = Depends(get_db)
):
    design = db.query(CircuitDesign).filter(CircuitDesign.id == design_id).first()

    if not design:
        raise HTTPException(status_code=404, detail="Circuit design not found")

    design.description = update_data.description
    design.constraints = update_data.constraints or design.constraints

    db.commit()
    db.refresh(design)

    return design


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
@router.delete("/{design_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_circuit_design(
    design_id: UUID,
    db: Session = Depends(get_db)
):
    design = db.query(CircuitDesign).filter(CircuitDesign.id == design_id).first()

    if not design:
        raise HTTPException(status_code=404, detail="Circuit design not found")

    db.delete(design)
    db.commit()

    return None
