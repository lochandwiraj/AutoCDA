"""
Auto-generated circuit validation tests
"""
from analysis.netlist_parser import NetlistGraph
from analysis.pattern_detector import CircuitPatternDetector


def test_voltage_divider_validation():
    graph = NetlistGraph()
    graph.add_component("R1", "resistor", "10k", ['VCC', 'OUT'])
    graph.add_component("R2", "resistor", "10k", ['OUT', 'GND'])

    detector = CircuitPatternDetector(graph)
    result = detector.analyze_circuit()
    assert isinstance(result, dict)


def test_rc_lowpass_validation():
    graph = NetlistGraph()
    graph.add_component("R1", "resistor", "1k", ['IN', 'OUT'])
    graph.add_component("C1", "capacitor", "100nF", ['OUT', 'GND'])

    detector = CircuitPatternDetector(graph)
    result = detector.analyze_circuit()
    assert isinstance(result, dict)
