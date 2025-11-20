from sqlalchemy import Column, String, Text, Float, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base, TimestampMixin


class SimulationResult(Base, TimestampMixin):
    __tablename__ = "simulation_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    circuit_design_id = Column(UUID(as_uuid=True), ForeignKey("circuit_designs.id"), nullable=False, index=True)
    simulation_type = Column(String(100), nullable=False)
    status = Column(String(50), default="pending")
    success = Column(Boolean, default=False)
    execution_time = Column(Float)
    result_data = Column(JSONB)
    error_message = Column(Text)

    circuit_design = relationship("CircuitDesign", back_populates="simulation_results")

    def __repr__(self):
        return f"<SimulationResult(id={self.id}, type={self.simulation_type}, status={self.status})>"
