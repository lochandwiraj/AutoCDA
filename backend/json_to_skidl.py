# backend/json_to_skidl.py
from typing import Dict, Any
import os
import sys
sys.path.append(os.path.dirname(__file__))

from skidl_templates import generate_rc_lowpass, generate_rc_highpass, generate_voltage_divider

def json_to_skidl(circuit_json: Dict[str, Any], output_dir: str = '../output') -> str:
    """
    Convert circuit JSON to SKiDL code and generate netlist
    
    Args:
        circuit_json: Dictionary containing circuit type and component values
        output_dir: Directory to save output files
        
    Returns:
        Path to generated netlist file
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    circuit_type = circuit_json.get('type', '').lower()
    components = circuit_json.get('components', {})
    
    # Generate unique filename
    output_file = os.path.join(output_dir, f'{circuit_type}_{id(circuit_json)}.net')
    
    try:
        if circuit_type == 'rc_lowpass':
            r_value = components.get('R1', {}).get('value', '1k')
            c_value = components.get('C1', {}).get('value', '159n')
            return generate_rc_lowpass(r_value, c_value, output_file)
            
        elif circuit_type == 'rc_highpass':
            r_value = components.get('R1', {}).get('value', '1k')
            c_value = components.get('C1', {}).get('value', '159n')
            return generate_rc_highpass(r_value, c_value, output_file)
            
        elif circuit_type == 'voltage_divider':
            r1_value = components.get('R1', {}).get('value', '4.7k')
            r2_value = components.get('R2', {}).get('value', '10k')
            return generate_voltage_divider(r1_value, r2_value, output_file)
            
        else:
            raise ValueError(f"Unsupported circuit type: {circuit_type}")
            
    except Exception as e:
        raise RuntimeError(f"SKiDL generation failed: {str(e)}")
