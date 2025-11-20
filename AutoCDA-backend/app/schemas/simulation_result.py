from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class SimulationResultBase(BaseModel):
    simulation_type: str = Field(..., min_length=1, max_length=100)
    status: str = Field(default="pending", max_length=50)
    success: bool = Field(default=False)
    execution_time: Optional[float] = None
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class SimulationResultCreate(SimulationResultBase):
    circuit_design_id: UUID


class SimulationResultUpdate(BaseModel):
    simulation_type: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = Field(None, max_length=50)
    success: Optional[bool] = None
    execution_time: Optional[float] = None
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class SimulationResultResponse(SimulationResultBase):
    id: UUID
    circuit_design_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
