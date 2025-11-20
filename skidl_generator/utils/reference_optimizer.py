class ReferenceDesignatorGenerator:
    \"\"\"Generate standard reference designators.\"\"\"
    
    PREFIXES = {
        'resistor': 'R',
        'capacitor': 'C',
        'inductor': 'L',
        'diode': 'D',
        'transistor': 'Q',
        'ic': 'U',
        'connector': 'J',
        'led': 'LED'
    }
    
    def __init__(self):
        self.counters = {prefix: 1 for prefix in self.PREFIXES.values()}
    
    def generate(self, component_type):
        prefix = self.PREFIXES.get(component_type.lower(), 'X')
        ref = f"{prefix}{self.counters[prefix]}"
        self.counters[prefix] += 1
        return ref