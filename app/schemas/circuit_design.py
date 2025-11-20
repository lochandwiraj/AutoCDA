from pydantic import BaseModel
from uuid import UUID

class CircuitDesignBase(BaseModel):
    description: str

class CircuitDesignCreate(CircuitDesignBase):
    pass

class CircuitDesignResponse(CircuitDesignBase):
    id: UUID   # ← IMPORTANT

    class Config:
        from_attributes = True
