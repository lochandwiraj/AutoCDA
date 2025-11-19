from passive_components import PassiveMapper
from active_components import ActiveMapper
from semiconductor_components import SemiconductorMapper
from power_nets import PowerNetMapper

def test_all_mappers():
    passive = PassiveMapper()
    active = ActiveMapper()
    semi = SemiconductorMapper()
    power = PowerNetMapper()

    # Passive
    r1 = passive.create_resistor({'id': 'R1', 'value': '10k'})
    c1 = passive.create_capacitor({'id': 'C1', 'value': '100n'})

    # Active
    u1 = active.create_opamp({'id': 'U1', 'type': 'LM741'})

    # Semiconductor
    d1 = semi.create_diode({'id': 'D1', 'part_number': '1N4148'})

    # Power Nets
    nets = power.create_power_nets()

    assert r1.ref == 'R1'
    assert u1.ref == 'U1'
    assert 'GND' in nets
    assert 'VCC' in nets

    print('? All mappers working!')

if __name__ == '__main__':
    test_all_mappers()
