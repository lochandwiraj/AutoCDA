"""
Demo script for AutoCDA presentation
Provides quick access to demo scenarios
"""

# Demo Scenario 1: RC Filter (30 seconds)
DEMO_1_INPUT = "Design a low-pass RC filter with 1kHz cutoff frequency"
DEMO_1_EXPECTED = "R1=1kΩ, C1=159nF, Complete circuit with voltage source"

# Demo Scenario 2: Voltage Divider (30 seconds)
DEMO_2_INPUT = "Create a voltage divider that converts 9V to 5V"
DEMO_2_EXPECTED = "R1 and R2 with proper ratio, voltage source included"

# Demo Scenario 3: High-Pass Filter (30 seconds)
DEMO_3_INPUT = "Design a high-pass RC filter with 500Hz cutoff"
DEMO_3_EXPECTED = "C1 and R1 configured for high-pass, with power supply"

def print_demo_script():
    print("=" * 60)
    print("AUTOCDA DEMO SCRIPT")
    print("=" * 60)
    print("\n[0:00-0:15] INTRODUCTION")
    print("'AutoCDA converts natural language to circuit schematics'")
    print("\n[0:15-0:45] DEMO 1: RC Filter")
    print(f"Input: '{DEMO_1_INPUT}'")
    print("Show: Complete circuit with all connections, voltage source, ground")
    print("\n[0:45-1:15] DEMO 2: Voltage Divider")
    print(f"Input: '{DEMO_2_INPUT}'")
    print("Show: Calculation explanation, component values")
    print("\n[1:15-1:45] DEMO 3: High-Pass Filter")
    print(f"Input: '{DEMO_3_INPUT}'")
    print("Show: Download ZIP, open in KiCad, ready to simulate")
    print("\n[1:45-2:00] CLOSE")
    print("'Visit http://localhost:8501 to try it yourself'")
    print("=" * 60)

if __name__ == "__main__":
    print_demo_script()
