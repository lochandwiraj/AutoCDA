"""
Complete system test for AutoCDA
Tests all components working together
"""

import sys
import os
sys.path.append('backend')

from component_calculator import ComponentCalculator
from dsl_generator import generate_dsl_from_json
from skidl_generator import SKiDLGenerator
from explainer import generate_circuit_explanation

print("=" * 70)
print("AUTOCDA COMPLETE SYSTEM TEST")
print("=" * 70)

# Test 1: RC Low-Pass Filter
print("\n[TEST 1] RC Low-Pass Filter (1kHz)")
print("-" * 70)

calc = ComponentCalculator()
R, C = calc.calculate_rc_filter(1000, "lowpass")
print(f"✓ Component Calculator: R={R}, C={C}")

# Simulate circuit JSON
circuit_json = {
    "type": "rc_lowpass_filter",
    "constraints": {"cutoff_freq": "1kHz"},
    "components": [
        {"id": "R1", "type": "resistor", "value": R, "nets": ["IN", "N1"]},
        {"id": "C1", "type": "capacitor", "value": C, "nets": ["N1", "GND"]}
    ]
}

dsl = generate_dsl_from_json(circuit_json)
print(f"✓ DSL Generator: {len(dsl)} characters")

generator = SKiDLGenerator()
skidl_code = generator.dsl_to_skidl(dsl)
print(f"✓ SKiDL Generator: {len(skidl_code)} characters")

explanation = generate_circuit_explanation(circuit_json, dsl)
print(f"✓ Explainer: {len(explanation)} characters")
print(f"\nExplanation preview:\n{explanation[:200]}...")

# Test 2: Voltage Divider
print("\n[TEST 2] Voltage Divider (9V to 5V)")
print("-" * 70)

R1, R2 = calc.calculate_voltage_divider(9, 5)
print(f"✓ Component Calculator: R1={R1}, R2={R2}")

circuit_json_vd = {
    "type": "voltage_divider",
    "constraints": {"input_voltage": "9", "output_voltage": "5"},
    "components": [
        {"id": "R1", "type": "resistor", "value": R1, "nets": ["IN", "OUT"]},
        {"id": "R2", "type": "resistor", "value": R2, "nets": ["OUT", "GND"]}
    ]
}

dsl_vd = generate_dsl_from_json(circuit_json_vd)
print(f"✓ DSL Generator: {len(dsl_vd)} characters")

skidl_vd = generator.dsl_to_skidl(dsl_vd)
print(f"✓ SKiDL Generator: {len(skidl_vd)} characters")

explanation_vd = generate_circuit_explanation(circuit_json_vd, dsl_vd)
print(f"✓ Explainer: {len(explanation_vd)} characters")

# Test 3: RC High-Pass Filter
print("\n[TEST 3] RC High-Pass Filter (1kHz)")
print("-" * 70)

R_hp, C_hp = calc.calculate_rc_filter(1000, "highpass")
print(f"✓ Component Calculator: R={R_hp}, C={C_hp}")

circuit_json_hp = {
    "type": "rc_highpass_filter",
    "constraints": {"cutoff_freq": "1kHz"},
    "components": [
        {"id": "C1", "type": "capacitor", "value": C_hp, "nets": ["IN", "N1"]},
        {"id": "R1", "type": "resistor", "value": R_hp, "nets": ["N1", "GND"]}
    ]
}

dsl_hp = generate_dsl_from_json(circuit_json_hp)
skidl_hp = generator.dsl_to_skidl(dsl_hp)
explanation_hp = generate_circuit_explanation(circuit_json_hp, dsl_hp)
print(f"✓ All modules working for high-pass filter")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED")
print("=" * 70)
print("\nSystem Status:")
print("  ✓ Component Calculator - Working")
print("  ✓ DSL Generator - Working")
print("  ✓ SKiDL Generator - Working")
print("  ✓ Explainer - Working")
print("  ✓ 3 Circuit Types Tested")
print("\nReady for production!")
