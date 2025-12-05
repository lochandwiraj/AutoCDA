"""
Day 4 Integration Test
Tests DSL generation, validation, and explanation together
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from dsl_generator import generate_dsl_from_json
from circuit_validator import validate_circuit, ValidationLevel
from explainer import generate_circuit_explanation


def test_complete_flow():
    """Test the complete Day 4 flow"""
    
    # Test circuit: RC Low-Pass Filter
    circuit = {
        "type": "rc_lowpass_filter",
        "constraints": {
            "cutoff_freq": "1kHz",
            "input_voltage": "5V"
        },
        "components": [
            {
                "id": "R1",
                "type": "resistor",
                "value": "1k",
                "nets": ["IN", "N1"]
            },
            {
                "id": "C1",
                "type": "capacitor",
                "value": "159nF",
                "nets": ["N1", "GND"]
            }
        ]
    }
    
    print("=" * 70)
    print("DAY 4 INTEGRATION TEST")
    print("=" * 70)
    print()
    
    # Step 1: Validate
    print("STEP 1: Validation")
    print("-" * 70)
    is_valid, messages = validate_circuit(circuit)
    print(f"Circuit Valid: {is_valid}")
    
    if messages:
        print("\nValidation Messages:")
        for msg in messages:
            print(f"  [{msg.level.value}] {msg.message}")
    else:
        print("  No validation issues found.")
    print()
    
    if not is_valid:
        print("❌ Validation failed. Cannot proceed.")
        return False
    
    # Step 2: Generate DSL
    print("STEP 2: DSL Generation")
    print("-" * 70)
    dsl = generate_dsl_from_json(circuit)
    print(dsl)
    print()
    
    # Step 3: Generate Explanation
    print("STEP 3: Explanation Generation")
    print("-" * 70)
    explanation = generate_circuit_explanation(circuit, dsl)
    print(explanation)
    print()
    
    print("=" * 70)
    print("✅ Day 4 Integration Test PASSED")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    success = test_complete_flow()
    exit(0 if success else 1)
