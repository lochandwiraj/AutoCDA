# app/models.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, JSON, Boolean, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

def gen_uuid():
    return str(uuid.uuid4())

class CircuitDesign(Base):
    __tablename__ = "circuit_designs"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    constraints = Column(JSON, nullable=True)
    dsl = Column(JSON, nullable=True)
    skidl_code = Column(Text, nullable=True)
    schematic_path = Column(String, nullable=True)
    netlist_path = Column(String, nullable=True)
    status = Column(String, default="pending")
    workflow_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

class Component(Base):
    __tablename__ = "components"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    parameters = Column(JSON, nullable=True)
    footprint = Column(String, nullable=True)
    datasheet_url = Column(String, nullable=True)
    in_stock = Column(Boolean, default=True)
    price = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class SimulationResult(Base):
    __tablename__ = "simulation_results"
    id = Column(String, primary_key=True, default=gen_uuid)
    design_id = Column(String, ForeignKey("circuit_designs.id"))
    simulation_type = Column(String)
    parameters = Column(JSON, nullable=True)
    results = Column(JSON, nullable=True)
    plots = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
