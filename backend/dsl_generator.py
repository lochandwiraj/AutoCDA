"""
DSL Generator Module
Converts validated circuit JSON to AutoCDA DSL format
"""

from typing import Dict, List, Any
import json


class DSLGenerator:
    """Generates Domain-Specific Language representation from circuit JSON"""
    
    def __init__(self):
        self.dsl_lines = []
    
    def json_to_dsl(self, circuit_json: Dict[str, Any]) -> str:
        """
        Convert circuit JSON to DSL string
        
        Args:
            circuit_json: Validated circuit structure
            
        Returns:
            DSL string representation
        """
        self.dsl_lines = []
        
        # Add header comment
        circuit_type = circuit_json.get('type', 'unknown')
        self.dsl_lines.append(f"# AutoCDA DSL - {circuit_type}")
        self.dsl_lines.append("")
        
        # Add constraints if present
        if 'constraints' in circuit_json:
            self._add_constraints(circuit_json['constraints'])
            self.dsl_lines.append("")
        
        # Add components
        if 'components' in circuit_json:
            self._add_components(circuit_json['components'])
            self.dsl_lines.append("")
        
        # Add connections/nets
        if 'connections' in circuit_json:
            self._add_connections(circuit_json['connections'])
        
        return '\n'.join(self.dsl_lines)
    
    def _add_constraints(self, constraints: Dict[str, Any]):
        """Add constraint declarations to DSL"""
        self.dsl_lines.append("# Constraints")
        for key, value in constraints.items():
            self.dsl_lines.append(f"CONSTRAINT: {key}={value}")
    
    def _add_components(self, components: List[Dict[str, Any]]):
        """Add component declarations to DSL"""
        self.dsl_lines.append("# Components")
        for comp in components:
            comp_id = comp.get('id', 'UNKNOWN')
            comp_type = comp.get('type', 'UNKNOWN')
            value = comp.get('value', '')
            nets = comp.get('nets', [])
            
            # Format nets as tuple string
            nets_str = f"({', '.join(nets)})"
            
            # Build component line
            if value:
                comp_line = f"COMP: {comp_id} {comp_type} value={value} nets={nets_str}"
            else:
                comp_line = f"COMP: {comp_id} {comp_type} nets={nets_str}"
            
            self.dsl_lines.append(comp_line)
    
    def _add_connections(self, connections: List[Dict[str, Any]]):
        """Add explicit connection declarations to DSL"""
        self.dsl_lines.append("# Connections")
        for conn in connections:
            net_name = conn.get('net', 'UNKNOWN')
            nodes = conn.get('nodes', [])
            nodes_str = ', '.join(nodes)
            self.dsl_lines.append(f"NET: {net_name} connects [{nodes_str}]")


def generate_dsl_from_json(circuit_json: Dict[str, Any]) -> str:
    """
    Convenience function to generate DSL from circuit JSON
    
    Args:
        circuit_json: Circuit structure as dictionary
        
    Returns:
        DSL string
    """
    generator = DSLGenerator()
    return generator.json_to_dsl(circuit_json)


# Example usage and testing
if __name__ == "__main__":
    # Test with RC low-pass filter
    test_circuit = {
        "type": "rc_lowpass_filter",
        "constraints": {
            "cutoff_freq": "1kHz",
            "input_voltage": "5V"
        },
        "components": [
            {
                "id": "R1",
                "type": "resistor",
                "value": "1k",
                "nets": ["IN", "N1"]
            },
            {
                "id": "C1",
                "type": "capacitor",
                "value": "159n",
                "nets": ["N1", "GND"]
            }
        ],
        "connections": [
            {
                "net": "IN",
                "nodes": ["R1.1", "INPUT"]
            },
            {
                "net": "N1",
                "nodes": ["R1.2", "C1.1", "OUTPUT"]
            },
            {
                "net": "GND",
                "nodes": ["C1.2", "GROUND"]
            }
        ]
    }
    
    dsl_output = generate_dsl_from_json(test_circuit)
    print("Generated DSL:")
    print("=" * 50)
    print(dsl_output)
    print("=" * 50)
