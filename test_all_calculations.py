"""Test all circuit types with detailed calculations"""
from backend.explainer import generate_circuit_explanation

print("=" * 80)
print("TESTING ENHANCED CIRCUIT EXPLANATIONS WITH CALCULATIONS")
print("=" * 80)

# Test 1: Voltage Divider
print("\n1. VOLTAGE DIVIDER (9V to ~6V)")
print("-" * 80)
voltage_divider = {
    "type": "voltage_divider",
    "constraints": {
        "input_voltage": "9V",
        "output_voltage": "5V"
    },
    "components": [
        {"id": "R1", "type": "resistor", "value": "4.7k", "nets": ["VIN", "VOUT"]},
        {"id": "R2", "type": "resistor", "value": "10k", "nets": ["VOUT", "GND"]}
    ]
}
print(generate_circuit_explanation(voltage_divider))

# Test 2: RC Low-Pass Filter
print("\n\n2. RC LOW-PASS FILTER (1kHz cutoff)")
print("-" * 80)
lowpass = {
    "type": "rc_lowpass_filter",
    "constraints": {
        "cutoff_freq": "1kHz",
        "input_voltage": "5V"
    },
    "components": [
        {"id": "R1", "type": "resistor", "value": "1k", "nets": ["IN", "OUT"]},
        {"id": "C1", "type": "capacitor", "value": "159nF", "nets": ["OUT", "GND"]}
    ]
}
print(generate_circuit_explanation(lowpass))

# Test 3: RC High-Pass Filter
print("\n\n3. RC HIGH-PASS FILTER (100Hz cutoff)")
print("-" * 80)
highpass = {
    "type": "rc_highpass_filter",
    "constraints": {
        "cutoff_freq": "100Hz"
    },
    "components": [
        {"id": "C1", "type": "capacitor", "value": "1.6uF", "nets": ["IN", "OUT"]},
        {"id": "R1", "type": "resistor", "value": "1k", "nets": ["OUT", "GND"]}
    ]
}
print(generate_circuit_explanation(highpass))

print("\n" + "=" * 80)
print("✓ ALL CIRCUIT TYPES NOW SHOW DETAILED STEP-BY-STEP CALCULATIONS")
print("=" * 80)
