import json
import math
from simulation_engine.core.simulator import NgspiceSimulator
from simulation_engine.analyzers.metrics import CircuitAnalyzer

# 1) Build RC low-pass test netlist
test_netlist = """
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
"""

# 2) Run the simulation
sim = NgspiceSimulator()
result = sim.run_simulation(test_netlist, 'ac')

if not result['success']:
    print("Error:", result['error'])
    exit()

# 3) Read WRDATA file manually (real, imag)
freqs = []
mags = []
phases = []

with open("ac_output.txt") as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 3:
            try:
                fval = float(parts[0])
                real = float(parts[1])
                imag = float(parts[2])

                mag = math.sqrt(real**2 + imag**2)
                phase = math.atan2(imag, real)

                freqs.append(fval)
                mags.append(mag)
                phases.append(phase)
            except:
                pass

# 4) Analyze
metrics = CircuitAnalyzer.analyze_response(freqs, mags, phases)
print(json.dumps(metrics, indent=2))
