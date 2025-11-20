from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.circuit import CircuitDesign, SimulationResult, DesignStatus
from app.schemas.circuit import (
    CircuitDesignCreate,
    CircuitDesignResponse,
    CircuitDesignDetail,
    SimulationRequest,
    SimulationResultSchema
)

router = APIRouter()

# ---------------------------------------
# Create Design
# ---------------------------------------
@router.post("/", response_model=CircuitDesignResponse)
async def create_design(data: CircuitDesignCreate, db: Session = Depends(get_db)):
    design = CircuitDesign(
        description=data.description,
        constraints=data.constraints or {},
        status=DesignStatus.pending,
    )
    db.add(design)
    db.commit()
    db.refresh(design)
    return design

# ---------------------------------------
# Get Design by ID
# ---------------------------------------
@router.get("/{design_id}", response_model=CircuitDesignDetail)
async def get_design(design_id: str, db: Session = Depends(get_db)):
    design = db.query(CircuitDesign).filter(CircuitDesign.id == design_id).first()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return design

# ---------------------------------------
# List Designs
# ---------------------------------------
@router.get("/", response_model=list[CircuitDesignResponse])
async def list_designs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(CircuitDesign).offset(skip).limit(limit).all()
