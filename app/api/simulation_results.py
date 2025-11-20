from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.simulation_result import SimulationResult
from app.schemas.simulation_result import (
    SimulationResultCreate,
    SimulationResultUpdate,
    SimulationResultResponse,
)

router = APIRouter()


@router.post("/", response_model=SimulationResultResponse, status_code=status.HTTP_201_CREATED)
def create_simulation_result(
    simulation_result: SimulationResultCreate,
    db: Session = Depends(get_db)
):
    db_simulation_result = SimulationResult(**simulation_result.model_dump())
    db.add(db_simulation_result)
    db.commit()
    db.refresh(db_simulation_result)
    return db_simulation_result


@router.get("/", response_model=List[SimulationResultResponse])
def list_simulation_results(
    circuit_design_id: UUID = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(SimulationResult)
    if circuit_design_id:
        query = query.filter(SimulationResult.circuit_design_id == circuit_design_id)
    simulation_results = query.offset(skip).limit(limit).all()
    return simulation_results


@router.get("/{simulation_result_id}", response_model=SimulationResultResponse)
def get_simulation_result(
    simulation_result_id: UUID,
    db: Session = Depends(get_db)
):
    simulation_result = db.query(SimulationResult).filter(SimulationResult.id == simulation_result_id).first()
    if not simulation_result:
        raise HTTPException(status_code=404, detail="Simulation result not found")
    return simulation_result


@router.put("/{simulation_result_id}", response_model=SimulationResultResponse)
def update_simulation_result(
    simulation_result_id: UUID,
    simulation_result_update: SimulationResultUpdate,
    db: Session = Depends(get_db)
):
    simulation_result = db.query(SimulationResult).filter(SimulationResult.id == simulation_result_id).first()
    if not simulation_result:
        raise HTTPException(status_code=404, detail="Simulation result not found")

    update_data = simulation_result_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(simulation_result, field, value)

    db.commit()
    db.refresh(simulation_result)
    return simulation_result


@router.delete("/{simulation_result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_simulation_result(
    simulation_result_id: UUID,
    db: Session = Depends(get_db)
):
    simulation_result = db.query(SimulationResult).filter(SimulationResult.id == simulation_result_id).first()
    if not simulation_result:
        raise HTTPException(status_code=404, detail="Simulation result not found")

    db.delete(simulation_result)
    db.commit()
    return None
