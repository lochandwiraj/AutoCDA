from skidl import Part, Net, generate_netlist

# Simple test circuit
r1 = Part('Device', 'R', value='1k', ref='R1')
c1 = Part('Device', 'C', value='100n', ref='C1')

gnd = Net('GND')
vin = Net('VIN')
n1 = Net('N1')

# R1: VIN ? N1
r1[1] += vin
r1[2] += n1

# C1: N1 ? GND
c1[1] += n1
c1[2] += gnd

try:
    nl = generate_netlist()
    print("? SKiDL generate_netlist() completed.")
except Exception as e:
    print("? SKiDL generate_netlist() failed:", e)

print("Parts created:", [p.ref for p in (r1, c1)])
