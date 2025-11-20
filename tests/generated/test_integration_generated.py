"""
Auto-generated integration tests
"""
from tests.factories import CircuitFactory
from analysis.netlist_parser import NetlistGraph
from analysis.pattern_detector import CircuitPatternDetector


def test_simple_filter_design_workflow():
    circuit = CircuitFactory.rc_lowpass()
    graph = NetlistGraph()
    for comp in circuit["components"]:
        graph.add_component(comp["id"], comp["type"], comp["value"], comp["nets"])
    detector = CircuitPatternDetector(graph)
    result = detector.analyze_circuit()
    assert isinstance(result, dict)
