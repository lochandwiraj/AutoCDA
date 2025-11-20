from .netlist_parser import NetlistGraph
from typing import Dict

class CircuitPatternDetector:
    def __init__(self, netlist_graph: NetlistGraph):
        self.graph = netlist_graph

    def detect_rc_filter(self) -> Dict:
        resistors = [c for c, d in self.graph.components.items()
                     if d["type"] == "resistor"]
        capacitors = [c for c, d in self.graph.components.items()
                      if d["type"] == "capacitor"]

        if resistors and capacitors:
            r_nets = set(self.graph.components[resistors[0]]["nets"])
            c_nets = set(self.graph.components[capacitors[0]]["nets"])

            common_nets = r_nets & c_nets

            if common_nets:
                if "GND" in c_nets:
                    return {
                        "type": "low_pass_filter",
                        "resistor": resistors[0],
                        "capacitor": capacitors[0],
                        "common_node": list(common_nets)[0]
                    }
                else:
                    return {
                        "type": "high_pass_filter",
                        "resistor": resistors[0],
                        "capacitor": capacitors[0]
                    }
        return None

    def detect_op_amp_config(self) -> Dict:
        op_amps = [
            c for c, d in self.graph.components.items()
            if "op" in d["type"].lower() or "741" in d["type"]
        ]
        if not op_amps:
            return None

        return {
            "type": "op_amp_circuit",
            "op_amp": op_amps[0],
            "config": "unknown"
        }

    def analyze_circuit(self) -> Dict:
        return {
            "floating_nodes": self.graph.find_floating_nodes(),
            "voltage_dividers": self.graph.detect_voltage_dividers(),
            "rc_filter": self.detect_rc_filter(),
            "op_amp_config": self.detect_op_amp_config()
        }
