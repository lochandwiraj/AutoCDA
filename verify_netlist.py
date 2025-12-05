import os

netlist_file = 'test_voltage_divider.net'

if os.path.exists(netlist_file):
    print(f"✓ Netlist file exists: {netlist_file}")
    
    # Read and display contents
    with open(netlist_file, 'r') as f:
        content = f.read()
        print("\nNetlist contents:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        
        # Check for expected components
        if 'R1' in content and 'R2' in content:
            print("✓ Components found in netlist")
        else:
            print("✗ Components missing from netlist")
else:
    print(f"✗ Netlist file not found: {netlist_file}")
