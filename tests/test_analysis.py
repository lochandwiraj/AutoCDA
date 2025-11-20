from simulation_engine.core.simulator import NgspiceSimulator
from simulation_engine.analyzers.metrics import CircuitAnalyzer
from simulation_engine.templates.testbenches import TestbenchTemplates

# Define circuit components
components = """
R1 input output 1k
C1 output 0 159nF
"""

# Generate testbench
testbench = TestbenchTemplates.ac_analysis_filter(components)

# Run simulation
sim = NgspiceSimulator()
result = sim.run_simulation(testbench, 'ac')

if result['success']:
    print("RAW:", result)
    print("RAW:", result)
    print("RAW:", result)
    # Analyze results
    data = result['data']
    metrics = CircuitAnalyzer.analyze_response(
        data['frequencies'],
        data['magnitudes'],
        data.get('phases')
    )
    
    print("?? Analysis Results:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
else:
    print(f"Error: {result['error']}")
