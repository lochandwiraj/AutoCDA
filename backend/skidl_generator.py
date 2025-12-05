from typing import Dict, List, Any
import os


class SKiDLGenerator:
    """Generates SKiDL Python code from DSL representation"""
    
    def __init__(self):
        self.supported_components = {
            'resistor': 'R',
            'capacitor': 'C',
            'voltage_source': 'V',
            'ground': 'GND'
        }
    
    def dsl_to_skidl(self, dsl_string: str) -> str:
        """
        Convert DSL string to executable SKiDL Python code
        
        Args:
            dsl_string: Circuit description in DSL format
            
        Returns:
            Complete SKiDL Python script as string
        """
        lines = dsl_string.strip().split('\n')
        components = []
        constraints = []
        
        # Parse DSL
        for line in lines:
            line = line.strip()
            if line.startswith('COMP:'):
                components.append(self._parse_component(line))
            elif line.startswith('CONSTRAINT:'):
                constraints.append(self._parse_constraint(line))
        
        # Generate SKiDL code
        skidl_code = self._generate_header()
        skidl_code += self._generate_components(components)
        skidl_code += self._generate_connections(components)
        skidl_code += self._generate_footer()
        
        return skidl_code
    
    def _parse_component(self, line: str) -> Dict[str, Any]:
        """Parse a COMP line from DSL"""
        # Format: COMP: R1 resistor value=1k nets=(IN, N1)
        parts = line.replace('COMP:', '').strip().split()
        
        comp_id = parts[0]
        comp_type = parts[1]
        
        value = None
        nets = []
        
        # Join parts back to handle nets properly
        full_line = ' '.join(parts[2:])
        
        if 'value=' in full_line:
            value_part = full_line.split('value=')[1].split()[0]
            value = value_part
        
        if 'nets=' in full_line:
            nets_part = full_line.split('nets=')[1]
            nets_str = nets_part.strip('()')
            nets = [n.strip() for n in nets_str.split(',')]
        
        return {
            'id': comp_id,
            'type': comp_type,
            'value': value,
            'nets': nets
        }
    
    def _parse_constraint(self, line: str) -> Dict[str, str]:
        """Parse a CONSTRAINT line from DSL"""
        # Format: CONSTRAINT: cutoff=1kHz
        constraint_str = line.replace('CONSTRAINT:', '').strip()
        key, value = constraint_str.split('=')
        return {key.strip(): value.strip()}
    
    def _generate_header(self) -> str:
        """Generate SKiDL script header with imports and setup"""
        return '''from skidl import *

# Create circuit
reset()

'''
    
    def _generate_components(self, components: List[Dict[str, Any]]) -> str:
        """Generate component instantiation code"""
        code = "# Component definitions\n"
        
        for comp in components:
            comp_type = comp['type'].lower()
            comp_id = comp['id']
            value = comp['value']
            
            if comp_type == 'resistor':
                code += f"{comp_id} = Part('Device', 'R', value='{value}', footprint='Resistor_SMD:R_0805_2012Metric')\n"
            elif comp_type == 'capacitor':
                code += f"{comp_id} = Part('Device', 'C', value='{value}', footprint='Capacitor_SMD:C_0805_2012Metric')\n"
            elif comp_type == 'voltage_source':
                code += f"{comp_id} = Part('pspice', 'VSRC', value='{value}')\n"
            elif comp_type == 'ground':
                code += f"{comp_id} = Part('power', 'GND')\n"
        
        code += "\n"
        return code
    
    def _generate_connections(self, components: List[Dict[str, Any]]) -> str:
        """Generate net connection code"""
        code = "# Net connections\n"
        
        # Collect all unique nets
        all_nets = set()
        for comp in components:
            all_nets.update(comp['nets'])
        
        # Create net objects (including GND)
        for net_name in sorted(all_nets):
            if net_name:  # Skip empty net names
                code += f"{net_name} = Net('{net_name}')\n"
        
        code += "\n# Connect components to nets\n"
        
        # Connect each component to its nets
        for comp in components:
            comp_id = comp['id']
            nets = comp['nets']
            
            for pin_idx, net_name in enumerate(nets, start=1):
                if net_name:  # Skip empty net names
                    code += f"{comp_id}[{pin_idx}] += {net_name}\n"
        
        code += "\n"
        return code
    
    def _generate_footer(self) -> str:
        """Generate SKiDL script footer with netlist generation"""
        return '''# Generate netlist
generate_netlist()

print("SKiDL circuit generated successfully!")
'''


# Test function
def test_skidl_generator():
    """Test the SKiDL generator with sample DSL"""
    
    # Sample DSL for RC low-pass filter
    sample_dsl = """COMP: R1 resistor value=1k nets=(IN, N1)
COMP: C1 capacitor value=159n nets=(N1, GND)
CONSTRAINT: cutoff=1kHz"""
    
    generator = SKiDLGenerator()
    skidl_code = generator.dsl_to_skidl(sample_dsl)
    
    print("Generated SKiDL Code:")
    print("=" * 60)
    print(skidl_code)
    print("=" * 60)
    
    return skidl_code


if __name__ == "__main__":
    test_skidl_generator()
