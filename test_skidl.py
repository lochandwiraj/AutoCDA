from skidl import *

# Create a simple voltage divider circuit
def test_voltage_divider():
    # Reset SKiDL
    reset()
    
    # Define nets
    vin = Net('VIN')
    vout = Net('VOUT')
    gnd = Net('GND')
    
    # Define components
    r1 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_0805_2012Metric')
    r2 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_0805_2012Metric')
    
    # Connect components
    r1[1] += vin
    r1[2] += vout
    r2[1] += vout
    r2[2] += gnd
    
    # Generate netlist
    generate_netlist(file_='test_voltage_divider.net')
    print("✓ SKiDL netlist generated successfully")

if __name__ == '__main__':
    test_voltage_divider()
