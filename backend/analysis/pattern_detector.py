from netlist_parser import NetlistGraph
from typing import Dict, List

class CircuitPatternDetector:
    def __init__(self, netlist_graph: NetlistGraph):
        self.graph = netlist_graph
    
    def detect_rc_filter(self) -> Dict:
        """Detect RC low-pass or high-pass filter"""
        resistors = [c for c, data in self.graph.components.items() 
                     if data['type'] == 'resistor']
        capacitors = [c for c, data in self.graph.components.items() 
                      if data['type'] == 'capacitor']
        
        if len(resistors) >= 1 and len(capacitors) >= 1:
            # Check if R and C share a common node
            r_nets = set(self.graph.components[resistors[0]]['nets'])
            c_nets = set(self.graph.components[capacitors[0]]['nets'])
            
            common_nets = r_nets & c_nets
            
            if common_nets:
                # Determine filter type based on topology
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
        """Detect op-amp configuration (inverting/non-inverting)"""
        op_amps = [c for c, data in self.graph.components.items() 
                   if 'op' in data['type'].lower() or '741' in data['type']]
        
        if not op_amps:
            return None
        
        # Simplified detection - check feedback resistor
        # (In real implementation, analyze full topology)
        return {
            "type": "op_amp_circuit",
            "op_amp": op_amps[0],
            "config": "unknown"  # TODO: Detect inv/non-inv
        }
    
    def analyze_circuit(self) -> Dict:
        """Run all pattern detections"""
        results = {
            "floating_nodes": self.graph.find_floating_nodes(),
            "voltage_dividers": self.graph.detect_voltage_dividers(),
            "rc_filter": self.detect_rc_filter(),
            "op_amp_config": self.detect_op_amp_config()
        }
        return results