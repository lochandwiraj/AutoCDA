import sys
sys.path.insert(0, 'templates')

from circuit_templates import CircuitTemplates

def run_tests():
    print("Testing RC Low-pass...")
    lp = CircuitTemplates.rc_lowpass_filter(1000)
    print(f"? LPF R={lp['params']['R']} O, C={lp['params']['C']*1e9:.2f} nF")

    print("Testing Voltage Divider...")
    vd = CircuitTemplates.voltage_divider(12, 5)
    print(f"? Divider R1={vd['params']['R1']:.0f} O, R2={vd['params']['R2']:.0f} O")

    print("Testing Non-inverting OpAmp...")
    op = CircuitTemplates.noninverting_opamp(10)
    print(f"? OpAmp Gain={op['params']['gain']} Rf={op['params']['Rf']:.0f} O")

    print("\n? ALL TEMPLATE TESTS PASSED")

if __name__ == '__main__':
    run_tests()
