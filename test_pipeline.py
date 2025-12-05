from skidl import *
import subprocess
import os

def generate_circuit():
    """Generate a simple RC filter circuit"""
    reset()
    
    # Define circuit
    vin = Net('VIN')
    vout = Net('VOUT')
    gnd = Net('GND')
    
    r1 = Part('Device', 'R', value='1k', footprint='Resistor_SMD:R_0805_2012Metric')
    c1 = Part('Device', 'C', value='159n', footprint='Capacitor_SMD:C_0805_2012Metric')
    
    # Connections for RC low-pass filter
    r1[1] += vin
    r1[2] += vout
    c1[1] += vout
    c1[2] += gnd
    
    # Generate files
    netlist_file = 'rc_filter.net'
    generate_netlist(file_=netlist_file)
    
    return netlist_file

def verify_pipeline():
    """Verify complete pipeline"""
    print("Starting end-to-end pipeline test...")
    print("-" * 50)
    
    # Step 1: Generate netlist
    print("\n1. Generating SKiDL netlist...")
    netlist_file = generate_circuit()
    
    if os.path.exists(netlist_file):
        print(f"   ✓ Netlist created: {netlist_file}")
    else:
        print(f"   ✗ Netlist creation failed")
        return False
    
    # Step 2: Verify netlist contents
    print("\n2. Verifying netlist contents...")
    with open(netlist_file, 'r') as f:
        content = f.read()
        if 'R1' in content and 'C1' in content and '1k' in content:
            print("   ✓ Components and values found")
        else:
            print("   ✗ Expected components missing")
            return False
    
    # Step 3: Manual KiCad import instruction
    print("\n3. KiCad import test:")
    print("   → Open KiCad")
    print("   → Create new project 'rc_filter_test'")
    print(f"   → Import netlist: {os.path.abspath(netlist_file)}")
    print("   → Verify R1 (1k) and C1 (159n) appear in schematic")
    
    print("\n" + "=" * 50)
    print("Pipeline test complete!")
    print("If KiCad import worked, pipeline is validated ✓")
    print("=" * 50)
    
    return True

if __name__ == '__main__':
    verify_pipeline()
