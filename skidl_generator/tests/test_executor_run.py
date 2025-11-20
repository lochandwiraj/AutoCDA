from execution.executor import SKiDLExecutor

test_code = '''
from skidl import Part, Net, generate_netlist, SKIDL

r1 = Part('Device', 'R', value='1k', ref='R1', tool=SKIDL)
c1 = Part('Device', 'C', value='100n', ref='C1', tool=SKIDL)

gnd = Net('GND')
vin = Net('VIN')

r1[1] += vin
r1[2] += c1[1]
c1[2] += gnd

generate_netlist()
'''

ex = SKiDLExecutor(timeout=20)
success, netlist, info = ex.execute(test_code)
print("Success:", success)
if netlist:
    print("Netlist:", netlist[:200])
else:
    print("Error/Info:", info)
