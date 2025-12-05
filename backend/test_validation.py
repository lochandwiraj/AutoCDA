import json
import sys
import os
sys.path.append(os.path.dirname(__file__))

from models import validate_circuit_json, Circuit


def test_validation():
    """Test validation with valid and invalid circuits."""
    
    # Valid RC lowpass filter
    valid_lowpass = {
        "circuit_type": "rc_lowpass",
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
                "value": "159n",
                "nets": ["N1", "GND"]
            }
        ],
        "constraints": {
            "cutoff_freq": "1000"
        }
    }
    
    # Invalid: missing cutoff_freq
    invalid_missing_constraint = {
        "circuit_type": "rc_lowpass",
        "components": [
            {"id": "R1", "type": "resistor", "value": "1k", "nets": ["IN", "N1"]},
            {"id": "C1", "type": "capacitor", "value": "159n", "nets": ["N1", "GND"]}
        ],
        "constraints": {}
    }
    
    # Invalid: duplicate IDs
    invalid_duplicate_ids = {
        "circuit_type": "rc_lowpass",
        "components": [
            {"id": "R1", "type": "resistor", "value": "1k", "nets": ["IN", "N1"]},
            {"id": "R1", "type": "capacitor", "value": "159n", "nets": ["N1", "GND"]}
        ],
        "constraints": {"cutoff_freq": "1000"}
    }
    
    # Invalid: component connects to same net twice
    invalid_same_net = {
        "circuit_type": "rc_lowpass",
        "components": [
            {"id": "R1", "type": "resistor", "value": "1k", "nets": ["IN", "IN"]},
            {"id": "C1", "type": "capacitor", "value": "159n", "nets": ["IN", "GND"]}
        ],
        "constraints": {"cutoff_freq": "1000"}
    }
    
    # Valid voltage divider
    valid_divider = {
        "circuit_type": "voltage_divider",
        "components": [
            {"id": "R1", "type": "resistor", "value": "2k", "nets": ["IN", "OUT"]},
            {"id": "R2", "type": "resistor", "value": "1k", "nets": ["OUT", "GND"]}
        ],
        "constraints": {
            "input_voltage": "9",
            "output_voltage": "3"
        }
    }
    
    test_cases = [
        ("Valid RC Lowpass", valid_lowpass, True),
        ("Invalid: Missing Constraint", invalid_missing_constraint, False),
        ("Invalid: Duplicate IDs", invalid_duplicate_ids, False),
        ("Invalid: Same Net Twice", invalid_same_net, False),
        ("Valid Voltage Divider", valid_divider, True),
    ]
    
    print("Testing Circuit Validation")
    print("=" * 60)
    
    for name, circuit_json, should_pass in test_cases:
        print(f"\n{name}")
        print("-" * 60)
        
        circuit, errors = validate_circuit_json(circuit_json)
        
        if circuit and not any("error" in e.lower() for e in errors):
            print("✓ PASSED validation")
            if errors:
                print("Warnings:")
                for error in errors:
                    print(f"  - {error}")
        else:
            print("✗ FAILED validation")
            for error in errors:
                print(f"  - {error}")
        
        expected = "PASS" if should_pass else "FAIL"
        actual = "PASS" if (circuit and not any("error" in e.lower() for e in errors)) else "FAIL"
        
        if expected == actual:
            print(f"Result: {actual} (as expected) ✓")
        else:
            print(f"Result: {actual} (expected {expected}) ✗")


if __name__ == "__main__":
    test_validation()
