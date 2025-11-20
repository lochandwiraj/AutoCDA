import pytest
from analysis.netlist_parser import NetlistGraph
from analysis.pattern_detector import CircuitPatternDetector

def test_rc_lowpass_detection():
    graph = NetlistGraph()
    graph.add_component("R1", "resistor", "1k", ["IN", "OUT"])
    graph.add_component("C1", "capacitor", "100nF", ["OUT", "GND"])
    detector = CircuitPatternDetector(graph)
    result = detector.detect_rc_filter()
    assert result is not None
    assert result["type"] == "low_pass_filter"
    assert result["resistor"] == "R1"
    assert result["capacitor"] == "C1"

def test_voltage_divider_detection():
    graph = NetlistGraph()
    graph.add_component("R1", "resistor", "10k", ["VCC", "MID"])
    graph.add_component("R2", "resistor", "10k", ["MID", "GND"])
    dividers = graph.detect_voltage_dividers()
    assert len(dividers) == 1
    assert dividers[0]["middle_node"] == "MID"
