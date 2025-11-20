from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class ComponentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    component_type: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None


class ComponentCreate(ComponentBase):
    circuit_design_id: UUID


class ComponentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    component_type: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None


class ComponentResponse(ComponentBase):
    id: UUID
    circuit_design_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
