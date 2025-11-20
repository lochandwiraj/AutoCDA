import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, Enum, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class DesignStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class SimulationStatus(str, enum.Enum):
    running = "running"
    completed = "completed"
    failed = "failed"

class CircuitDesign(Base):
    __tablename__ = "circuit_designs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=True)
    description = Column(Text, nullable=False)

    dsl_code = Column(Text, nullable=True)
    skidl_code = Column(Text, nullable=True)
    netlist = Column(Text, nullable=True)

    constraints = Column(JSON, nullable=True)

    status = Column(Enum(DesignStatus), default=DesignStatus.pending)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    components = relationship("Component", back_populates="design")
    simulations = relationship("SimulationResult", back_populates="design")


class Component(Base):
    __tablename__ = "components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    design_id = Column(UUID(as_uuid=True), ForeignKey("circuit_designs.id"))

    component_type = Column(String)
    reference = Column(String)
    value = Column(String)
    unit = Column(String)

    nets = Column(JSON)
    properties = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

    design = relationship("CircuitDesign", back_populates="components")


class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    design_id = Column(UUID(as_uuid=True), ForeignKey("circuit_designs.id"))

    simulation_type = Column(String)
    parameters = Column(JSON)
    result_data = Column(JSON)
    metrics = Column(JSON)
    plot_urls = Column(JSON)

    status = Column(Enum(SimulationStatus), default=SimulationStatus.running)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    design = relationship("CircuitDesign", back_populates="simulations")
