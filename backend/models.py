from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from enum import Enum


class CircuitType(str, Enum):
    RC_LOWPASS = "rc_lowpass"
    RC_HIGHPASS = "rc_highpass"
    VOLTAGE_DIVIDER = "voltage_divider"


class ComponentType(str, Enum):
    RESISTOR = "resistor"
    CAPACITOR = "capacitor"


class Component(BaseModel):
    id: str = Field(..., description="Unique component identifier (e.g., R1, C1)")
    type: ComponentType = Field(..., description="Component type")
    value: str = Field(..., description="Component value with unit (e.g., 1k, 100n)")
    nets: List[str] = Field(..., min_items=2, max_items=2, description="Two nets this component connects")
    
    @validator('id')
    def validate_id(cls, v):
        if not v:
            raise ValueError("Component ID cannot be empty")
        if not v[0].isalpha():
            raise ValueError("Component ID must start with a letter")
        return v
    
    @validator('value')
    def validate_value(cls, v):
        if not v:
            raise ValueError("Component value cannot be empty")
        # Check if value contains at least one digit
        if not any(char.isdigit() for char in v):
            raise ValueError("Component value must contain numeric digits")
        return v
    
    @validator('nets')
    def validate_nets(cls, v):
        if len(v) != 2:
            raise ValueError("Component must have exactly 2 nets")
        if v[0] == v[1]:
            raise ValueError("Component cannot connect to the same net twice")
        return v


class Constraints(BaseModel):
    cutoff_freq: Optional[str] = Field(None, description="Cutoff frequency in Hz (for filters)")
    input_voltage: Optional[str] = Field(None, description="Input voltage in V (for dividers)")
    output_voltage: Optional[str] = Field(None, description="Output voltage in V (for dividers)")
    
    @validator('cutoff_freq', 'input_voltage', 'output_voltage')
    def validate_numeric_fields(cls, v):
        if v is not None:
            try:
                float(v)
            except ValueError:
                raise ValueError(f"Value must be numeric, got: {v}")
        return v


class Circuit(BaseModel):
    circuit_type: CircuitType = Field(..., description="Type of circuit to generate")
    components: List[Component] = Field(..., min_items=1, description="List of circuit components")
    constraints: Constraints = Field(..., description="Circuit design constraints")
    
    @validator('components')
    def validate_components(cls, v, values):
        if not v:
            raise ValueError("Circuit must have at least one component")
        
        # Check for duplicate IDs
        ids = [comp.id for comp in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Component IDs must be unique")
        
        # Check that circuit type matches component requirements
        circuit_type = values.get('circuit_type')
        if circuit_type:
            if circuit_type in [CircuitType.RC_LOWPASS, CircuitType.RC_HIGHPASS]:
                # Filter circuits must have at least 1 resistor and 1 capacitor
                types = [comp.type for comp in v]
                if ComponentType.RESISTOR not in types or ComponentType.CAPACITOR not in types:
                    raise ValueError("RC filter must have at least one resistor and one capacitor")
            elif circuit_type == CircuitType.VOLTAGE_DIVIDER:
                # Voltage divider must have at least 2 resistors
                resistor_count = sum(1 for comp in v if comp.type == ComponentType.RESISTOR)
                if resistor_count < 2:
                    raise ValueError("Voltage divider must have at least two resistors")
        
        return v
    
    @validator('constraints')
    def validate_constraints_match_circuit_type(cls, v, values):
        circuit_type = values.get('circuit_type')
        
        if circuit_type in [CircuitType.RC_LOWPASS, CircuitType.RC_HIGHPASS]:
            if not v.cutoff_freq:
                raise ValueError(f"{circuit_type.value} requires cutoff_freq in constraints")
        elif circuit_type == CircuitType.VOLTAGE_DIVIDER:
            if not v.input_voltage or not v.output_voltage:
                raise ValueError("voltage_divider requires input_voltage and output_voltage in constraints")
        
        return v
    
    def has_ground(self) -> bool:
        """Check if circuit has a GND net."""
        all_nets = []
        for comp in self.components:
            all_nets.extend(comp.nets)
        return "GND" in all_nets
    
    def get_floating_nets(self) -> List[str]:
        """Return list of nets that only connect to one component."""
        net_counts = {}
        for comp in self.components:
            for net in comp.nets:
                net_counts[net] = net_counts.get(net, 0) + 1
        
        return [net for net, count in net_counts.items() if count < 2]


# Validation function
def validate_circuit_json(circuit_json: Dict) -> tuple:
    """
    Validate circuit JSON against schema.
    Returns (Circuit object, list of errors)
    """
    errors = []
    
    try:
        circuit = Circuit(**circuit_json)
        
        # Additional checks
        if not circuit.has_ground():
            errors.append("WARNING: Circuit does not have a GND net")
        
        floating_nets = circuit.get_floating_nets()
        if floating_nets:
            errors.append(f"WARNING: Floating nets detected: {', '.join(floating_nets)}")
        
        return circuit, errors
        
    except Exception as e:
        errors.append(f"Validation error: {str(e)}")
        return None, errors
