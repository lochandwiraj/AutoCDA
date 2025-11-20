from skidl import Part, Net
import re

class PassiveMapper:
    """Maps DSL passive components to SKiDL objects"""

    multipliers = {
        'p': 1e-12,
        'n': 1e-9,
        'u': 1e-6,
        'm': 1e-3,
        'k': 1e3,
        'K': 1e3,
        'M': 1e6,
        'G': 1e9,
    }

    @staticmethod
    def parse_value(value_str):
        """Convert '1k', '100n', etc to numeric with unit."""
        s = value_str.strip()
        match = re.match(r'^([0-9]*\.?[0-9]+)([a-zA-Z]*)$', s)
        if not match:
            raise ValueError(f"Cannot parse: {value_str}")

        base = float(match.group(1))
        suffix = match.group(2)

        # Determine multiplier
        mult = PassiveMapper.multipliers.get(suffix[:1], 1)

        # Determine unit (O or F)
        unit = "O"
        if 'f' in suffix.lower():
            unit = "F"

        return base * mult, unit

    def create_resistor(self, comp_data):
        value_num, unit = self.parse_value(comp_data['value'])
        r = Part('Device', 'R',
                 ref=comp_data['id'],
                 value=comp_data['value'],
                 footprint='Resistor_SMD:R_0805_2012Metric')

        nets = comp_data.get("nets", [])
        if len(nets) > 0:
            r[1] += Net(nets[0])
        if len(nets) > 1:
            r[2] += Net(nets[1])

        return r

    def create_capacitor(self, comp_data):
        value_num, unit = self.parse_value(comp_data['value'])
        c = Part('Device', 'C',
                 ref=comp_data['id'],
                 value=comp_data['value'],
                 footprint='Capacitor_SMD:C_0805_2012Metric')

        nets = comp_data.get("nets", [])
        if len(nets) > 0:
            c[1] += Net(nets[0])
        if len(nets) > 1:
            c[2] += Net(nets[1])

        return c
