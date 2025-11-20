from passive_components import PassiveMapper

def run_tests():
    mapper = PassiveMapper()

    # Test: resistor creation
    r = mapper.create_resistor({
        'id': 'R1',
        'value': '10k',
        'nets': ['VIN', 'OUT']
    })
    print(f"? Created resistor: {r.ref} = {r.value}")

    # Test: capacitor creation
    c = mapper.create_capacitor({
        'id': 'C1',
        'value': '100n',
        'nets': ['N1', 'GND']
    })
    print(f"? Created capacitor: {c.ref} = {c.value}")

    # Test: parse_value
    num, unit = mapper.parse_value("10k")
    print(f"? Parsed value: {num} {unit}")

