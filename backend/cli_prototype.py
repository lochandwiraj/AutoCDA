# backend/cli_prototype.py
import json
import os
import sys
sys.path.append(os.path.dirname(__file__))

from json_to_skidl import json_to_skidl

def simple_cli():
    """Simple CLI for testing the pipeline"""
    
    print("=== AutoCDA Prototype CLI ===\n")
    
    # Mock circuit JSON (simulating NLP output)
    test_circuits = {
        '1': {
            'type': 'rc_lowpass',
            'components': {
                'R1': {'value': '1k'},
                'C1': {'value': '159n'}
            },
            'description': 'RC Low-Pass Filter (1kHz cutoff)'
        },
        '2': {
            'type': 'rc_highpass',
            'components': {
                'R1': {'value': '1k'},
                'C1': {'value': '159n'}
            },
            'description': 'RC High-Pass Filter (1kHz cutoff)'
        },
        '3': {
            'type': 'voltage_divider',
            'components': {
                'R1': {'value': '4.7k'},
                'R2': {'value': '10k'}
            },
            'description': 'Voltage Divider (9V to 5V)'
        }
    }
    
    # Display options
    print("Available circuit types:")
    for key, circuit in test_circuits.items():
        print(f"{key}. {circuit['description']}")
    
    # Get user choice
    choice = input("\nSelect circuit (1-3): ").strip()
    
    if choice not in test_circuits:
        print("Invalid choice!")
        return
    
    # Process circuit
    circuit_json = test_circuits[choice]
    print(f"\nProcessing: {circuit_json['description']}")
    print(f"Circuit JSON: {json.dumps(circuit_json, indent=2)}")
    
    try:
        # Generate SKiDL and netlist
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        output_file = json_to_skidl(circuit_json, output_dir)
        
        print(f"\n✓ Success! Generated netlist at: {output_file}")
        print(f"\nTo view in KiCad:")
        print(f"1. Open KiCad")
        print(f"2. File > Import > Netlist")
        print(f"3. Select: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")

if __name__ == '__main__':
    simple_cli()
