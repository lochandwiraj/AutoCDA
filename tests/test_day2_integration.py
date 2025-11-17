"""
Day 2 Integration Test: Component Library + Pattern Detection
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.component import Component, Base
from analysis.netlist_parser import NetlistGraph
from analysis.pattern_detector import CircuitPatternDetector

def test_full_component_to_pattern_flow():
    """Test complete flow: Load component -> Build graph -> Detect pattern"""
    
    # Setup test database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Add test components
    r1 = Component(
        id="R1",
        type="resistor",
        value="1k",
        value_numeric=1000,
        unit="ohm",
        footprint="0805"
    )
    c1 = Component(
        id="C1",
        type="capacitor",
        value="100nF",
        value_numeric=100e-9,
        unit="farad",
        footprint="0805"
    )
    session.add_all([r1, c1])
    session.commit()
    
    # Query components
    resistor = session.query(Component).filter_by(id="R1").first()
    capacitor = session.query(Component).filter_by(id="C1").first()
    
    assert resistor is not None
    assert capacitor is not None
    
    # Build circuit graph
    graph = NetlistGraph()
    graph.add_component(resistor.id, resistor.type, resistor.value, ["IN", "OUT"])
    graph.add_component(capacitor.id, capacitor.type, capacitor.value, ["OUT", "GND"])
    
    # Detect pattern
    detector = CircuitPatternDetector(graph)
    result = detector.detect_rc_filter()
    
    assert result is not None
    assert result["type"] == "low_pass_filter"
    
    print("✅ Full integration test passed!")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
