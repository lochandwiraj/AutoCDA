"""
Enhanced explanation generator with visualization support.
Bonus feature: Educational value and transparency.
"""

from typing import Dict, List
import json

class EnhancedExplainer:
    """Generate detailed explanations with formulas and reasoning."""
    
    def __init__(self):
        self.formulas = {
            "rc_lowpass": {
                "formula": "f_c = 1 / (2π × R × C)",
                "variables": {
                    "f_c": "Cutoff frequency (Hz)",
                    "R": "Resistance (Ω)",
                    "C": "Capacitance (F)"
                },
                "derivation": "At cutoff frequency, reactance equals resistance: X_C = R"
            },
            "rc_highpass": {
                "formula": "f_c = 1 / (2π × R × C)",
                "variables": {
                    "f_c": "Cutoff frequency (Hz)",
                    "R": "Resistance (Ω)",
                    "C": "Capacitance (F)"
                },
                "derivation": "Same as lowpass, but components are swapped in signal path"
            },
            "voltage_divider": {
                "formula": "V_out = V_in × (R2 / (R1 + R2))",
                "variables": {
                    "V_out": "Output voltage (V)",
                    "V_in": "Input voltage (V)",
                    "R1": "Upper resistor (Ω)",
                    "R2": "Lower resistor (Ω)"
                },
                "derivation": "Ohm's law applied to series resistors with voltage division"
            }
        }
    
    def generate_detailed_explanation(self, circuit_type: str, components: Dict,
                                  constraints: Dict, calculations: Dict) -> str:
        """Generate comprehensive explanation with formulas and reasoning."""
        
        explanation_parts = []
        
        # Introduction
        explanation_parts.append(f"## Circuit Design: {circuit_type.replace('_', ' ').title()}\n")
        
        # Design constraints
        explanation_parts.append("### Design Requirements")
        for key, value in constraints.items():
            explanation_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
        explanation_parts.append("")
        
        # Formula explanation
        if circuit_type in self.formulas:
            formula_info = self.formulas[circuit_type]
            explanation_parts.append("### Design Formula")
            explanation_parts.append(f"**{formula_info['formula']}**\n")
            
            explanation_parts.append("Where:")
            for var, desc in formula_info['variables'].items():
                explanation_parts.append(f"- {var}: {desc}")
            
            explanation_parts.append(f"\n**Theory:** {formula_info['derivation']}\n")
        
        # Component selection reasoning
        explanation_parts.append("### Component Selection")
        for comp_name, comp_data in components.items():
            value = comp_data.get('value', 'N/A')
            comp_type = comp_data.get('type', 'component')
            
            explanation_parts.append(f"**{comp_name}** ({comp_type}): {value}")
            
            # Add reasoning if available
            if comp_name in calculations:
                calc = calculations[comp_name]
                if 'reasoning' in calc:
                    explanation_parts.append(f"  - Reasoning: {calc['reasoning']}")
                if 'calculated_value' in calc:
                    explanation_parts.append(f"  - Calculated: {calc['calculated_value']}")
                if 'standard_value' in calc:
                    explanation_parts.append(f"  - Standard value selected: {calc['standard_value']}")
            
            explanation_parts.append("")
        
        # Verification
        explanation_parts.append("### Design Verification")
        if 'verification' in calculations:
            for check, result in calculations['verification'].items():
                status = "✓" if result.get('passed', False) else "✗"
                explanation_parts.append(f"{status} {check}: {result.get('message', 'OK')}")
        
        return "\n".join(explanation_parts)
    
    def generate_formula_visualization(self, circuit_type: str, values: Dict) -> Dict:
        """Generate data for formula visualization (for UI bonus)."""
        if circuit_type not in self.formulas:
            return {}
        
        formula_info = self.formulas[circuit_type]
        
        return {
            "formula": formula_info["formula"],
            "variables": formula_info["variables"],
            "values": values,
            "derivation": formula_info["derivation"],
            "visualization_type": "formula_breakdown"
        }

# Global explainer instance
explainer = EnhancedExplainer()
