from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime

# ------------------------
# CREATE REQUEST
# ------------------------
class CircuitDesignCreate(BaseModel):
    description: str = Field(..., min_length=5)
    constraints: Optional[dict] = None


# ------------------------
# COMPONENT
# ------------------------
class ComponentSchema(BaseModel):
    id: UUID
    component_type: str
    reference: str
    value: str
    unit: str
    nets: List[str]
    properties: Optional[Dict] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ------------------------
# SIMULATION RESULT
# ------------------------
class SimulationResultSchema(BaseModel):
    id: UUID
    simulation_type: str
    parameters: Optional[dict]
    result_data: Optional[dict]
    metrics: Optional[dict]
    plot_urls: Optional[List[str]]
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    model_config = {"from_attributes": True}


# ------------------------
# BASIC DESIGN RESPONSE
# ------------------------
class CircuitDesignResponse(BaseModel):
    id: UUID  # ← FIXED: UUID instead of str
    description: str
    status: str
    dsl_code: Optional[str]
    skidl_code: Optional[str]
    netlist: Optional[str]
    error_message: Optional[str]
    constraints: Optional[dict]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ------------------------
# DETAILED DESIGN RESPONSE
# ------------------------
class CircuitDesignDetail(CircuitDesignResponse):
    components: List[ComponentSchema] = []
    simulations: List[SimulationResultSchema] = []
