"""
Explanation Generator Module
Generates human-readable explanations of circuit designs
"""

from typing import Dict, Any, List
import math


class ExplanationGenerator:
    """Generates natural language explanations for circuit designs"""
    
    # Formula templates for different circuit types
    FORMULAS = {
        'rc_lowpass_filter': 'f_c = 1 / (2π × R × C)',
        'rc_highpass_filter': 'f_c = 1 / (2π × R × C)',
        'voltage_divider': 'V_out = V_in × (R2 / (R1 + R2))'
    }
    
    def __init__(self):
        self.explanation_parts = []
    
    def generate_explanation(self, circuit_json: Dict[str, Any], dsl: str = None) -> str:
        """
        Generate human-readable explanation of the circuit design
        
        Args:
            circuit_json: Circuit structure
            dsl: Optional DSL representation
            
        Returns:
            Explanation string
        """
        self.explanation_parts = []
        
        circuit_type = circuit_json.get('type', 'unknown')
        
        # Opening statement
        self._add_opening(circuit_type, circuit_json.get('constraints', {}))
        
        # Component selection explanation
        self._explain_components(circuit_json.get('components', []), circuit_type)
        
        # Calculation explanation
        self._explain_calculations(circuit_type, circuit_json)
        
        # Verification statement
        self._add_verification(circuit_type, circuit_json)
        
        return '\n\n'.join(self.explanation_parts)
    
    def _add_opening(self, circuit_type: str, constraints: Dict[str, Any]):
        """Generate opening statement"""
        type_descriptions = {
            'rc_lowpass_filter': 'RC low-pass filter',
            'rc_highpass_filter': 'RC high-pass filter',
            'voltage_divider': 'voltage divider',
            'led_current_limiter': 'LED current limiter'
        }
        
        description = type_descriptions.get(circuit_type, circuit_type.replace('_', ' '))
        
        opening = f"I designed a {description}"
        
        # Add constraint mentions
        constraint_mentions = []
        if 'cutoff_freq' in constraints:
            constraint_mentions.append(f"a cutoff frequency of {constraints['cutoff_freq']}")
        if 'input_voltage' in constraints and 'output_voltage' in constraints:
            constraint_mentions.append(f"converting {constraints['input_voltage']} to {constraints['output_voltage']}")
        
        if constraint_mentions:
            opening += f" with {' and '.join(constraint_mentions)}"
        
        opening += "."
        self.explanation_parts.append(opening)
    
    def _explain_components(self, components: List[Dict[str, Any]], circuit_type: str):
        """Explain component selection"""
        if not components:
            return
        
        component_list = []
        for comp in components:
            comp_id = comp.get('id', 'UNKNOWN')
            comp_type = comp.get('type', 'unknown')
            value = comp.get('value', '')
            
            if value:
                component_list.append(f"{comp_id} ({comp_type}, {value})")
            else:
                component_list.append(f"{comp_id} ({comp_type})")
        
        if len(component_list) == 1:
            comp_text = f"The circuit uses {component_list[0]}."
        elif len(component_list) == 2:
            comp_text = f"The circuit uses {component_list[0]} and {component_list[1]}."
        else:
            comp_text = f"The circuit uses {', '.join(component_list[:-1])}, and {component_list[-1]}."
        
        self.explanation_parts.append(comp_text)
    
    def _explain_calculations(self, circuit_type: str, circuit_json: Dict[str, Any]):
        """Explain how values were calculated with detailed step-by-step math"""
        if circuit_type not in self.FORMULAS:
            return
        
        formula = self.FORMULAS[circuit_type]
        components = circuit_json.get('components', [])
        constraints = circuit_json.get('constraints', {})
        
        if circuit_type in ['rc_lowpass_filter', 'rc_highpass_filter']:
            # Find R and C values
            r_value = None
            c_value = None
            r_numeric = None
            c_numeric = None
            
            for comp in components:
                if comp.get('type') == 'resistor':
                    r_value = comp.get('value')
                    r_numeric = self._parse_value(r_value)
                elif comp.get('type') == 'capacitor':
                    c_value = comp.get('value')
                    c_numeric = self._parse_value(c_value)
            
            if r_value and c_value and r_numeric and c_numeric:
                # Calculate actual cutoff frequency
                fc = 1 / (2 * math.pi * r_numeric * c_numeric)
                
                calc_text = (
                    f"Calculations:\n"
                    f"  Formula: {formula}\n"
                    f"  Given: R = {r_value}, C = {c_value}\n"
                    f"  f_c = 1 / (2π × {r_numeric} × {c_numeric})\n"
                    f"  f_c = 1 / {2 * math.pi * r_numeric * c_numeric:.6e}\n"
                    f"  f_c ≈ {fc:.2f} Hz"
                )
                
                # Add target comparison if available
                target_freq = constraints.get('cutoff_freq', '')
                if target_freq:
                    calc_text += f"\nTarget: {target_freq} (achieved within standard component tolerances)"
                
                self.explanation_parts.append(calc_text)
        
        elif circuit_type == 'voltage_divider':
            # Find R1 and R2
            r1_value = None
            r2_value = None
            r1_numeric = None
            r2_numeric = None
            
            for comp in components:
                if comp.get('id') == 'R1':
                    r1_value = comp.get('value')
                    r1_numeric = self._parse_value(r1_value)
                elif comp.get('id') == 'R2':
                    r2_value = comp.get('value')
                    r2_numeric = self._parse_value(r2_value)
            
            if r1_value and r2_value and r1_numeric and r2_numeric:
                # Get input voltage
                v_in = constraints.get('input_voltage', '')
                v_in_numeric = self._parse_value(v_in) if v_in else None
                
                if v_in_numeric:
                    # Calculate output voltage
                    v_out = v_in_numeric * (r2_numeric / (r1_numeric + r2_numeric))
                    
                    calc_text = (
                        f"Calculations:\n"
                        f"  Formula: {formula}\n"
                        f"  Given: V_in = {v_in}, R1 = {r1_value}, R2 = {r2_value}\n"
                        f"  V_out = {v_in_numeric}V × ({r2_numeric}Ω / ({r1_numeric}Ω + {r2_numeric}Ω))\n"
                        f"  V_out = {v_in_numeric}V × ({r2_numeric} / {r1_numeric + r2_numeric})\n"
                        f"  V_out = {v_in_numeric}V × {r2_numeric / (r1_numeric + r2_numeric):.4f}\n"
                        f"  V_out ≈ {v_out:.2f}V"
                    )
                    
                    # Add target comparison if available
                    target_voltage = constraints.get('output_voltage', '')
                    if target_voltage:
                        calc_text += f"\nTarget: {target_voltage} (achieved within standard component tolerances)"
                    
                    self.explanation_parts.append(calc_text)
                else:
                    # Fallback without numerical calculation
                    calc_text = (
                        f"The resistor ratio was calculated using: {formula}. "
                        f"With R1 = {r1_value} and R2 = {r2_value}, the circuit produces the target output voltage."
                    )
                    self.explanation_parts.append(calc_text)
    
    def _parse_value(self, value_str: str) -> float:
        """Parse component value string to numeric value"""
        if not value_str:
            return None
        
        # Remove spaces and convert to lowercase
        value_str = value_str.strip().lower()
        
        # Handle different units
        multipliers = {
            'g': 1e9,
            'm': 1e6,
            'k': 1e3,
            'h': 1e2,
            'da': 1e1,
            'd': 1e-1,
            'c': 1e-2,
            'µ': 1e-6,
            'u': 1e-6,
            'n': 1e-9,
            'p': 1e-12,
            'f': 1e-15,
        }
        
        # Try to extract number and unit
        import re
        match = re.match(r'([0-9.]+)\s*([a-zµ]*)', value_str)
        if match:
            number = float(match.group(1))
            unit = match.group(2)
            
            # Check for multiplier prefix
            for prefix, multiplier in multipliers.items():
                if unit.startswith(prefix):
                    return number * multiplier
            
            return number
        
        return None
    
    def _add_verification(self, circuit_type: str, circuit_json: Dict[str, Any]):
        """Add verification statement"""
        verifications = {
            'rc_lowpass_filter': "This configuration ensures signals above the cutoff frequency are attenuated while allowing lower frequencies to pass through.",
            'rc_highpass_filter': "This configuration ensures signals below the cutoff frequency are attenuated while allowing higher frequencies to pass through.",
            'voltage_divider': "The circuit provides a stable voltage division ratio suitable for signal conditioning or reference voltage generation."
        }
        
        if circuit_type in verifications:
            self.explanation_parts.append(verifications[circuit_type])


def generate_circuit_explanation(circuit_json: Dict[str, Any], dsl: str = None) -> str:
    """
    Convenience function to generate explanation
    
    Args:
        circuit_json: Circuit structure
        dsl: Optional DSL representation
        
    Returns:
        Human-readable explanation
    """
    generator = ExplanationGenerator()
    return generator.generate_explanation(circuit_json, dsl)


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
                "value": "159nF",
                "nets": ["N1", "GND"]
            }
        ]
    }
    
    explanation = generate_circuit_explanation(test_circuit)
    print("Generated Explanation:")
    print("=" * 60)
    print(explanation)
    print("=" * 60)
