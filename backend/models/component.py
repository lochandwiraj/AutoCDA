from sqlalchemy import Column, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Component(Base):
    __tablename__ = "components"
    
    id = Column(String, primary_key=True)  # e.g., "R_1K_0805"
    type = Column(String, index=True)  # resistor, capacitor, ic
    value = Column(String)  # "1k", "10uF"
    value_numeric = Column(Float)  # normalized value for filtering
    unit = Column(String)  # ohm, farad, henry
    tolerance = Column(String)  # "5%", "10%"
    footprint = Column(String)  # "0805", "SOIC-8"
    datasheet_url = Column(String, nullable=True)
    properties = Column(JSON)  # flexible metadata
    
    def __repr__(self):
        return f"<Component {self.id}: {self.value}>"