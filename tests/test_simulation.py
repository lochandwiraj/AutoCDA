from simulation_engine.core.simulator import NgspiceSimulator

netlist = '''
.title RC Filter

Vin input 0 AC 1
R1 input output 1k
C1 output 0 159n

.ac dec 100 1 100k

.control
run
wrdata ac_output.txt v(output)
.endc

.end
'''

sim = NgspiceSimulator()
result = sim.run_simulation(netlist, 'ac')

if result['success']:
    print("Simulation successful!")
    print("Data points:", len(result['data']['frequencies']))
else:
    print("Error:", result['error'])
