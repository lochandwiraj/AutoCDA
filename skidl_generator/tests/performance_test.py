import time
import statistics
from integration.pipeline import SKiDLPipeline

class PerformanceBenchmark:
    
    def __init__(self):
        self.pipeline = SKiDLPipeline()
        self.results = []
    
    def measure_generation_time(self, dsl_data, iterations=10):
        # Measure time for DSL → SKiDL → Netlist
        times = []
        
        for _ in range(iterations):
            start = time.time()
            result = self.pipeline.generate_from_dsl(dsl_data)
            end = time.time()
            
            if result['success']:
                times.append(end - start)
        
        if not times:
            return {
                'mean': 0,
                'median': 0,
                'min': 0,
                'max': 0,
                'std_dev': 0
            }
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'min': min(times),
            'max': max(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }
    
    def benchmark_all_circuits(self):
        # Run benchmarks on different circuit types
        
        test_circuits = {
            'simple_rc': {
                'components': [
                    {'type': 'resistor', 'id': 'R1', 'value': '1k', 'nets': ['VIN', 'N1']},
                    {'type': 'capacitor', 'id': 'C1', 'value': '100n', 'nets': ['N1', 'GND']}
                ]
            },
            'voltage_divider': {
                'components': [
                    {'type': 'resistor', 'id': 'R1', 'value': '10k', 'nets': ['VIN', 'VOUT']},
                    {'type': 'resistor', 'id': 'R2', 'value': '10k', 'nets': ['VOUT', 'GND']}
                ]
            },
            'complex_filter': {
                'components': [
                    {'type': 'resistor', 'id': 'R1', 'value': '1k', 'nets': ['VIN', 'N1']},
                    {'type': 'capacitor', 'id': 'C1', 'value': '100n', 'nets': ['N1', 'N2']},
                    {'type': 'resistor', 'id': 'R2', 'value': '1k', 'nets': ['N2', 'VOUT']},
                    {'type': 'capacitor', 'id': 'C2', 'value': '100n', 'nets': ['VOUT', 'GND']}
                ]
            }
        }
        
        print("\n=== Performance Benchmark Results ===\n")
        
        for circuit_name, dsl in test_circuits.items():
            perf = self.measure_generation_time(dsl)
            print(f"{circuit_name}:")
            print(f"  Mean: {perf['mean']*1000:.2f}ms")
            print(f"  Median: {perf['median']*1000:.2f}ms")
            print(f"  Range: {perf['min']*1000:.2f}ms - {perf['max']*1000:.2f}ms")
            print(f"  Std Dev: {perf['std_dev']*1000:.2f}ms")
            print()
            
            if perf['mean'] > 5.0:
                print("  ⚠️  WARNING: Exceeds 5s target!\n")
            elif perf['mean'] < 1.0:
                print("  ✓ Excellent performance!\n")
            else:
                print("  ✓ Within target\n")

if __name__ == '__main__':
    benchmark = PerformanceBenchmark()
    benchmark.benchmark_all_circuits()
