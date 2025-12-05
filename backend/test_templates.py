# backend/test_templates.py
import os
import sys
sys.path.append(os.path.dirname(__file__))

from skidl_templates import generate_rc_lowpass, generate_rc_highpass, generate_voltage_divider

# Create output directory
output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(output_dir, exist_ok=True)

# Test 1: RC Low-Pass Filter (1kHz cutoff)
print("Testing RC Low-Pass Filter...")
try:
    output1 = generate_rc_lowpass('1k', '159n', os.path.join(output_dir, 'test_lowpass.net'))
    print(f"✓ Low-pass filter netlist generated: {output1}")
except Exception as e:
    print(f"✗ Low-pass filter failed: {e}")

# Test 2: RC High-Pass Filter (1kHz cutoff)
print("\nTesting RC High-Pass Filter...")
try:
    output2 = generate_rc_highpass('1k', '159n', os.path.join(output_dir, 'test_highpass.net'))
    print(f"✓ High-pass filter netlist generated: {output2}")
except Exception as e:
    print(f"✗ High-pass filter failed: {e}")

# Test 3: Voltage Divider (9V to 5V)
print("\nTesting Voltage Divider...")
try:
    output3 = generate_voltage_divider('4.7k', '10k', os.path.join(output_dir, 'test_divider.net'))
    print(f"✓ Voltage divider netlist generated: {output3}")
except Exception as e:
    print(f"✗ Voltage divider failed: {e}")

print("\n=== Test Summary ===")
print("Check output/ directory for generated .net files")
print("Open these files in KiCad to verify schematics")
