from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base, TimestampMixin


class CircuitDesign(Base, TimestampMixin):
    __tablename__ = "circuit_designs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    version = Column(String(50), default="1.0.0")
    status = Column(String(50), default="draft")
    design_data = Column(JSONB)
    user_id = Column(UUID(as_uuid=True), index=True)

    components = relationship("Component", back_populates="circuit_design", cascade="all, delete-orphan")
    simulation_results = relationship("SimulationResult", back_populates="circuit_design", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CircuitDesign(id={self.id}, name={self.name}, status={self.status})>"
