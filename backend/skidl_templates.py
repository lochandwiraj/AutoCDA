# backend/skidl_templates.py
from skidl import *

def generate_rc_lowpass(r_value, c_value, output_file):
    """Generate SKiDL code for RC low-pass filter"""
    
    # Reset SKiDL environment
    reset()
    
    # Create nets
    vin = Net('VIN')
    vout = Net('VOUT')
    gnd = Net('GND')
    
    # Create components
    r1 = Part('Device', 'R', value=r_value, footprint='Resistor_SMD:R_0805_2012Metric')
    c1 = Part('Device', 'C', value=c_value, footprint='Capacitor_SMD:C_0805_2012Metric')
    
    # Connect components
    vin += r1[1]
    r1[2] += vout
    vout += c1[1]
    c1[2] += gnd
    
    # Generate netlist
    generate_netlist(file_=output_file)
    
    return output_file

def generate_rc_highpass(r_value, c_value, output_file):
    """Generate SKiDL code for RC high-pass filter"""
    
    reset()
    
    # Create nets
    vin = Net('VIN')
    vout = Net('VOUT')
    gnd = Net('GND')
    
    # Create components - capacitor first in high-pass
    c1 = Part('Device', 'C', value=c_value, footprint='Capacitor_SMD:C_0805_2012Metric')
    r1 = Part('Device', 'R', value=r_value, footprint='Resistor_SMD:R_0805_2012Metric')
    
    # Connect components
    vin += c1[1]
    c1[2] += vout
    vout += r1[1]
    r1[2] += gnd
    
    generate_netlist(file_=output_file)
    
    return output_file

def generate_voltage_divider(r1_value, r2_value, output_file):
    """Generate SKiDL code for voltage divider"""
    
    reset()
    
    # Create nets
    vin = Net('VIN')
    vout = Net('VOUT')
    gnd = Net('GND')
    
    # Create components
    r1 = Part('Device', 'R', value=r1_value, footprint='Resistor_SMD:R_0805_2012Metric')
    r2 = Part('Device', 'R', value=r2_value, footprint='Resistor_SMD:R_0805_2012Metric')
    
    # Connect components
    vin += r1[1]
    r1[2] += vout
    vout += r2[1]
    r2[2] += gnd
    
    generate_netlist(file_=output_file)
    
    return output_file
