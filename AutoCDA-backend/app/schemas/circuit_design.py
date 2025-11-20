from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel, Field


class CircuitDesignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    version: str = Field(default="1.0.0", max_length=50)
    status: str = Field(default="draft", max_length=50)
    design_data: Optional[Dict[str, Any]] = None
    user_id: Optional[UUID] = None


class CircuitDesignCreate(CircuitDesignBase):
    pass


class CircuitDesignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    version: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=50)
    design_data: Optional[Dict[str, Any]] = None


class CircuitDesignResponse(CircuitDesignBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
