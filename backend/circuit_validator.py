"""
Circuit Validation Module
Validates circuit structure for electrical correctness
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class ValidationLevel(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationMessage:
    level: ValidationLevel
    message: str
    component_id: str = None


class CircuitValidator:
    """Validates circuit JSON for basic electrical correctness"""
    
    VALID_COMPONENT_TYPES = {
        'resistor', 'capacitor', 'inductor', 'diode', 'led',
        'transistor', 'voltage_source', 'current_source'
    }
    
    REQUIRED_GROUND_TYPES = {'rc_filter', 'rc_lowpass_filter', 'rc_highpass_filter'}
    
    def __init__(self):
        self.messages: List[ValidationMessage] = []
        self.has_errors = False
    
    def validate(self, circuit_json: Dict[str, Any]) -> Tuple[bool, List[ValidationMessage]]:
        """
        Validate circuit structure
        
        Args:
            circuit_json: Circuit structure to validate
            
        Returns:
            Tuple of (is_valid, list of validation messages)
        """
        self.messages = []
        self.has_errors = False
        
        # Check required fields
        self._check_required_fields(circuit_json)
        
        # Validate components
        if 'components' in circuit_json:
            self._validate_components(circuit_json['components'])
            
            # Check for floating nodes
            self._check_floating_nodes(circuit_json['components'])
            
            # Check for ground node if required
            circuit_type = circuit_json.get('type', circuit_json.get('circuit_type', ''))
            if circuit_type in self.REQUIRED_GROUND_TYPES:
                self._check_ground_exists(circuit_json['components'])
        
        return (not self.has_errors, self.messages)
    
    def _add_message(self, level: ValidationLevel, message: str, component_id: str = None):
        """Add a validation message"""
        self.messages.append(ValidationMessage(level, message, component_id))
        if level == ValidationLevel.ERROR:
            self.has_errors = True
    
    def _check_required_fields(self, circuit_json: Dict[str, Any]):
        """Check that required top-level fields exist"""
        if 'type' not in circuit_json and 'circuit_type' not in circuit_json:
            self._add_message(ValidationLevel.ERROR, "Missing 'type' or 'circuit_type' field in circuit")
        
        if 'components' not in circuit_json or not circuit_json['components']:
            self._add_message(ValidationLevel.ERROR, "Circuit must have at least one component")
    
    def _validate_components(self, components: List[Dict[str, Any]]):
        """Validate individual components"""
        component_ids = set()
        
        for idx, comp in enumerate(components):
            # Check required component fields
            if 'id' not in comp:
                self._add_message(ValidationLevel.ERROR, f"Component at index {idx} missing 'id'")
                continue
            
            comp_id = comp['id']
            
            # Check for duplicate IDs
            if comp_id in component_ids:
                self._add_message(ValidationLevel.ERROR, f"Duplicate component ID: {comp_id}", comp_id)
            component_ids.add(comp_id)
            
            # Check component type
            if 'type' not in comp:
                self._add_message(ValidationLevel.ERROR, f"Component {comp_id} missing 'type'", comp_id)
            elif comp['type'] not in self.VALID_COMPONENT_TYPES:
                self._add_message(ValidationLevel.WARNING,
                                 f"Component {comp_id} has unrecognized type: {comp['type']}",
                                 comp_id)
            
            # Check nets
            if 'nets' not in comp:
                self._add_message(ValidationLevel.ERROR, f"Component {comp_id} missing 'nets'", comp_id)
            elif not isinstance(comp['nets'], list):
                self._add_message(ValidationLevel.ERROR, f"Component {comp_id} 'nets' must be a list", comp_id)
            elif len(comp['nets']) < 2:
                self._add_message(ValidationLevel.ERROR,
                                 f"Component {comp_id} must connect to at least 2 nets",
                                 comp_id)
            
            # Check component value
            if 'value' in comp:
                self._validate_component_value(comp_id, comp['type'], comp['value'])
    
    def _validate_component_value(self, comp_id: str, comp_type: str, value: str):
        """Validate component value format and range"""
        if not value:
            self._add_message(ValidationLevel.WARNING,
                             f"Component {comp_id} has empty value",
                             comp_id)
            return
        
        # Check for valid units (basic check)
        valid_endings = ['k', 'M', 'G', 'm', 'u', 'n', 'p', 'F', 'H']
        
        # Extract numeric part
        numeric_part = ''.join(c for c in value if c.isdigit() or c == '.')
        
        if not numeric_part:
            self._add_message(ValidationLevel.WARNING,
                             f"Component {comp_id} value '{value}' has no numeric part",
                             comp_id)
            return
        
        try:
            num_value = float(numeric_part)
            if num_value <= 0:
                self._add_message(ValidationLevel.ERROR,
                                 f"Component {comp_id} value must be positive",
                                 comp_id)
        except ValueError:
            self._add_message(ValidationLevel.WARNING,
                             f"Component {comp_id} value '{value}' cannot be parsed",
                             comp_id)
    
    def _check_floating_nodes(self, components: List[Dict[str, Any]]):
        """Check for nets that connect to only one component (floating nodes)"""
        net_connections = {}
        
        for comp in components:
            comp_id = comp.get('id', 'UNKNOWN')
            nets = comp.get('nets', [])
            
            for net in nets:
                if net not in net_connections:
                    net_connections[net] = []
                net_connections[net].append(comp_id)
        
        # Check for nets with only one connection
        for net, connected_comps in net_connections.items():
            if len(connected_comps) < 2:
                self._add_message(ValidationLevel.WARNING,
                                 f"Net '{net}' connects to only one component: {connected_comps[0]}")
    
    def _check_ground_exists(self, components: List[Dict[str, Any]]):
        """Check if ground node exists in the circuit"""
        has_ground = False
        
        for comp in components:
            nets = comp.get('nets', [])
            if any(net.upper() in ['GND', 'GROUND', '0'] for net in nets):
                has_ground = True
                break
        
        if not has_ground:
            self._add_message(ValidationLevel.ERROR,
                             "Circuit requires a ground (GND) node but none found")


def validate_circuit(circuit_json: Dict[str, Any]) -> Tuple[bool, List[ValidationMessage]]:
    """
    Convenience function to validate a circuit
    
    Args:
        circuit_json: Circuit structure to validate
        
    Returns:
        Tuple of (is_valid, list of validation messages)
    """
    validator = CircuitValidator()
    return validator.validate(circuit_json)


# Example usage and testing
if __name__ == "__main__":
    # Test with valid circuit
    valid_circuit = {
        "type": "rc_lowpass_filter",
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
        ]
    }
    
    print("Testing VALID circuit:")
    is_valid, messages = validate_circuit(valid_circuit)
    print(f"Valid: {is_valid}")
    for msg in messages:
        print(f"  [{msg.level.value}] {msg.message}")
    print()
    
    # Test with invalid circuit (floating node)
    invalid_circuit = {
        "type": "rc_lowpass_filter",
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
                "nets": ["FLOATING", "GND"]
            }
        ]
    }
    
    print("Testing INVALID circuit (floating node):")
    is_valid, messages = validate_circuit(invalid_circuit)
    print(f"Valid: {is_valid}")
    for msg in messages:
        print(f"  [{msg.level.value}] {msg.message}")
