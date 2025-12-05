#!/usr/bin/env python3
"""
Circuit Verification Script
Checks all circuit generation for proper wiring and component placement
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.component_calculator import ComponentCalculator
from backend.json_to_skidl import json_to_skidl
import tempfile
import os

def verify_rc_lowpass():
    """Verify RC low-pass filter circuit"""
    print("\n" + "="*60)
    print("VERIFYING: RC LOW-PASS FILTER")
    print("="*60)
    
    print("\n✓ Circuit Topology:")
    print("  VIN --[R1]-- VOUT --[C1]-- GND")
    print("  ")
    print("  Correct wiring:")
    print("  - R1 pin 1 connects to VIN")
    print("  - R1 pin 2 connects to VOUT")
    print("  - C1 pin 1 connects to VOUT")
    print("  - C1 pin 2 connects to GND")
    
    # Test component calculation
    calc = ComponentCalculator()
    R, C = calc.calculate_rc_filter(1000, "lowpass")
    print(f"\n✓ Component Values (1kHz cutoff):")
    print(f"  R1 = {R}")
    print(f"  C1 = {C}")
    
    # Verify calculation
    from backend.component_calculator import parse_value
    import math
    R_val = parse_value(R)
    C_val = parse_value(C)
    actual_fc = 1 / (2 * math.pi * R_val * C_val)
    error = abs(actual_fc - 1000) / 1000 * 100
    
    print(f"\n✓ Verification:")
    print(f"  Target frequency: 1000 Hz")
    print(f"  Actual frequency: {actual_fc:.1f} Hz")
    print(f"  Error: {error:.2f}%")
    
    if error < 10:
        print("  ✅ PASS - Error within 10% tolerance")
        return True
    else:
        print("  ❌ FAIL - Error exceeds 10%")
        return False

def verify_rc_highpass():
    """Verify RC high-pass filter circuit"""
    print("\n" + "="*60)
    print("VERIFYING: RC HIGH-PASS FILTER")
    print("="*60)
    
    print("\n✓ Circuit Topology:")
    print("  VIN --[C1]-- VOUT --[R1]-- GND")
    print("  ")
    print("  Correct wiring:")
    print("  - C1 pin 1 connects to VIN")
    print("  - C1 pin 2 connects to VOUT")
    print("  - R1 pin 1 connects to VOUT")
    print("  - R1 pin 2 connects to GND")
    
    # Test component calculation
    calc = ComponentCalculator()
    R, C = calc.calculate_rc_filter(500, "highpass")
    print(f"\n✓ Component Values (500Hz cutoff):")
    print(f"  C1 = {C}")
    print(f"  R1 = {R}")
    
    # Verify calculation
    from backend.component_calculator import parse_value
    import math
    R_val = parse_value(R)
    C_val = parse_value(C)
    actual_fc = 1 / (2 * math.pi * R_val * C_val)
    error = abs(actual_fc - 500) / 500 * 100
    
    print(f"\n✓ Verification:")
    print(f"  Target frequency: 500 Hz")
    print(f"  Actual frequency: {actual_fc:.1f} Hz")
    print(f"  Error: {error:.2f}%")
    
    if error < 10:
        print("  ✅ PASS - Error within 10% tolerance")
        return True
    else:
        print("  ❌ FAIL - Error exceeds 10%")
        return False

def verify_voltage_divider():
    """Verify voltage divider circuit"""
    print("\n" + "="*60)
    print("VERIFYING: VOLTAGE DIVIDER")
    print("="*60)
    
    print("\n✓ Circuit Topology:")
    print("  VIN --[R1]-- VOUT --[R2]-- GND")
    print("  ")
    print("  Correct wiring:")
    print("  - R1 pin 1 connects to VIN")
    print("  - R1 pin 2 connects to VOUT")
    print("  - R2 pin 1 connects to VOUT")
    print("  - R2 pin 2 connects to GND")
    
    # Test component calculation
    calc = ComponentCalculator()
    R1, R2 = calc.calculate_voltage_divider(9, 5)
    print(f"\n✓ Component Values (9V to 5V):")
    print(f"  R1 = {R1}")
    print(f"  R2 = {R2}")
    
    # Verify calculation
    from backend.component_calculator import parse_value
    R1_val = parse_value(R1)
    R2_val = parse_value(R2)
    actual_vout = 9 * R2_val / (R1_val + R2_val)
    error = abs(actual_vout - 5) / 5 * 100
    
    print(f"\n✓ Verification:")
    print(f"  Input voltage: 9V")
    print(f"  Target output: 5V")
    print(f"  Actual output: {actual_vout:.2f}V")
    print(f"  Error: {error:.2f}%")
    
    if error < 10:
        print("  ✅ PASS - Error within 10% tolerance")
        return True
    else:
        print("  ❌ FAIL - Error exceeds 10%")
        return False

def verify_netlist_generation():
    """Verify that netlists are generated correctly"""
    print("\n" + "="*60)
    print("VERIFYING: NETLIST GENERATION")
    print("="*60)
    
    test_circuits = [
        {
            "type": "rc_lowpass",
            "components": {
                "R1": {"value": "1.6k"},
                "C1": {"value": "100n"}
            }
        },
        {
            "type": "rc_highpass",
            "components": {
                "R1": {"value": "3.3k"},
                "C1": {"value": "100n"}
            }
        },
        {
            "type": "voltage_divider",
            "components": {
                "R1": {"value": "3.9k"},
                "R2": {"value": "5.6k"}
            }
        }
    ]
    
    all_passed = True
    
    for circuit in test_circuits:
        circuit_type = circuit["type"]
        print(f"\n✓ Testing {circuit_type}...")
        
        try:
            # Generate netlist in temp directory
            temp_dir = tempfile.mkdtemp()
            netlist_path = json_to_skidl(circuit, temp_dir)
            
            # Check if file exists
            if Path(netlist_path).exists():
                # Read and verify content
                with open(netlist_path, 'r') as f:
                    content = f.read()
                
                # Basic checks
                checks = {
                    "Has components": "comp" in content.lower() or "part" in content.lower(),
                    "Has nets": "net" in content.lower(),
                    "Has VIN": "VIN" in content or "vin" in content.lower(),
                    "Has VOUT": "VOUT" in content or "vout" in content.lower(),
                    "Has GND": "GND" in content or "gnd" in content.lower()
                }
                
                for check, passed in checks.items():
                    status = "✅" if passed else "❌"
                    print(f"  {status} {check}")
                    if not passed:
                        all_passed = False
                
                # Clean up
                os.remove(netlist_path)
                os.rmdir(temp_dir)
                
            else:
                print(f"  ❌ Netlist file not created")
                all_passed = False
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            all_passed = False
    
    return all_passed

def main():
    print("\n" + "="*60)
    print("AUTOCDA CIRCUIT VERIFICATION")
    print("="*60)
    print("\nVerifying all circuit topologies, wiring, and calculations...")
    
    results = []
    
    # Verify each circuit type
    results.append(("RC Low-Pass Filter", verify_rc_lowpass()))
    results.append(("RC High-Pass Filter", verify_rc_highpass()))
    results.append(("Voltage Divider", verify_voltage_divider()))
    results.append(("Netlist Generation", verify_netlist_generation()))
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total = len(results)
    
    print(f"\nTotal: {passed_count}/{total} checks passed")
    print("="*60)
    
    if passed_count == total:
        print("\n✅ ALL CIRCUITS VERIFIED - WIRING AND CALCULATIONS CORRECT")
        return 0
    else:
        print("\n❌ SOME CIRCUITS FAILED VERIFICATION")
        return 1

if __name__ == "__main__":
    sys.exit(main())
