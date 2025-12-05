# backend/test_cli_automated.py
import json
import os
import sys
sys.path.append(os.path.dirname(__file__))

from json_to_skidl import json_to_skidl

def test_all_circuits():
    """Automated test for all circuit types"""
    
    print("=== AutoCDA CLI Automated Test ===\n")
    
    test_circuits = [
        {
            'type': 'rc_lowpass',
            'components': {
                'R1': {'value': '1k'},
                'C1': {'value': '159n'}
            },
            'description': 'RC Low-Pass Filter (1kHz cutoff)'
        },
        {
            'type': 'rc_highpass',
            'components': {
                'R1': {'value': '1k'},
                'C1': {'value': '159n'}
            },
            'description': 'RC High-Pass Filter (1kHz cutoff)'
        },
        {
            'type': 'voltage_divider',
            'components': {
                'R1': {'value': '4.7k'},
                'R2': {'value': '10k'}
            },
            'description': 'Voltage Divider (9V to 5V)'
        }
    ]
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    results = []
    
    for i, circuit_json in enumerate(test_circuits, 1):
        print(f"Test {i}: {circuit_json['description']}")
        print("-" * 60)
        
        try:
            output_file = json_to_skidl(circuit_json, output_dir)
            
            if os.path.exists(output_file):
                print(f"✓ Netlist generated: {output_file}")
                results.append(True)
            else:
                print(f"✗ Netlist file not found")
                results.append(False)
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results.append(False)
        
        print()
    
    print("=" * 60)
    print(f"SUMMARY: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    return all(results)

if __name__ == '__main__':
    success = test_all_circuits()
    sys.exit(0 if success else 1)
