from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base, TimestampMixin


class Component(Base, TimestampMixin):
    __tablename__ = "components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    circuit_design_id = Column(UUID(as_uuid=True), ForeignKey("circuit_designs.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    component_type = Column(String(100), nullable=False)
    description = Column(Text)
    properties = Column(JSONB)
    position_x = Column(Float)
    position_y = Column(Float)

    circuit_design = relationship("CircuitDesign", back_populates="components")

    def __repr__(self):
        return f"<Component(id={self.id}, name={self.name}, type={self.component_type})>"
