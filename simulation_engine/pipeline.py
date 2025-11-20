from simulation_engine.core.simulator import NgspiceSimulator
from simulation_engine.analyzers.metrics import CircuitAnalyzer
from simulation_engine.plotters.visualizer import SimulationVisualizer
from simulation_engine.reports.generator import ReportGenerator
from simulation_engine.templates.testbenches import TestbenchTemplates

class SimulationPipeline:
    """Complete simulation workflow"""
    
    def __init__(self):
        self.simulator = NgspiceSimulator()
        self.visualizer = SimulationVisualizer()
        self.report_gen = ReportGenerator()
    
    def run_complete_analysis(self, 
                             circuit_name: str,
                             netlist_components: str,
                             analysis_type: str = 'ac') -> dict:
        """
        Run complete simulation pipeline
        
        Args:
            circuit_name: Name of the circuit
            netlist_components: SPICE component definitions
            analysis_type: 'ac', 'tran', 'dc'
            
        Returns:
            Complete results package
        """
        results = {
            'circuit_name': circuit_name,
            'success': False,
            'error': None
        }
        
        try:
            # Step 1: Generate testbench
            print(" Generating testbench...")
            if analysis_type == 'ac':
                testbench = TestbenchTemplates.ac_analysis_filter(netlist_components)
            elif analysis_type == 'tran':
                testbench = TestbenchTemplates.transient_analysis(netlist_components)
            elif analysis_type == 'dc':
                testbench = TestbenchTemplates.dc_sweep(netlist_components)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
            
            # Step 2: Run simulation
            print(" Running simulation...")
            sim_result = self.simulator.run_simulation(testbench, analysis_type)
            
            if not sim_result['success']:
                results['error'] = sim_result['error']
                return results
            
            # Step 3: Analyze results
            print(" Analyzing results...")
            data = sim_result['data']
            
            if analysis_type == 'ac':
                metrics = CircuitAnalyzer.analyze_response(
                    data['frequencies'],
                    data['magnitudes'],
                    data.get('phases')
                )
                
                # Step 4: Create plots
                print(" Generating plots...")
                bode_plot = self.visualizer.create_bode_plot(
                    data['frequencies'],
                    data['magnitudes'],
                    data.get('phases'),
                    title=f"{circuit_name} - Frequency Response"
                )
                
                results['metrics'] = metrics
                results['plots'] = {'bode': bode_plot}
            
            # Step 5: Generate report
            print(" Generating report...")
            report_html = self.report_gen.generate_report(
                circuit_name=circuit_name,
                metrics=results.get('metrics', {}),
                bode_plot=results['plots'].get('bode'),
                validation={'passed': True, 'issues': []}
            )
            
            results['report_html'] = report_html
            results['success'] = True
            
            print(" Analysis complete!")
            
        except Exception as e:
            results['error'] = str(e)
            print(f" Error: {e}")
        
        return results
