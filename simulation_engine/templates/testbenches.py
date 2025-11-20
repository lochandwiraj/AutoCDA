class TestbenchTemplates:
    """Pre-made SPICE testbench templates"""

    @staticmethod
    def ac_analysis_filter(netlist_components: str,
                           start_freq: float = 1,
                           stop_freq: float = 100e3,
                           points_per_decade: int = 100) -> str:
        """Generate AC analysis testbench for filters"""

        return f"""
* Auto-generated AC Analysis Testbench
.title Filter Frequency Response

* Input source
Vin input 0 AC 1

{netlist_components}

* Analysis command
.ac dec {points_per_decade} {start_freq} {stop_freq}

.control
run
wrdata ac_output.txt frequency v(output)
.endc

.end
"""

    @staticmethod
    def transient_analysis(netlist_components: str,
                           sim_time: float = 10e-3,
                           step_time: float = 10e-6,
                           input_signal: str = "pulse") -> str:
        """Generate transient analysis testbench"""

        if input_signal == "pulse":
            source = "PULSE(0 5 0 1n 1n 5m 10m)"
        elif input_signal == "sine":
            source = "SIN(0 1 1k)"
        else:
            source = input_signal

        return f"""
* Auto-generated Transient Analysis
.title Transient Response

* Input source
Vin input 0 {source}

{netlist_components}

* Analysis
.tran {step_time} {sim_time}

.control
run
print time v(input) v(output)
.endc

.end
"""

    @staticmethod
    def dc_sweep(netlist_components: str,
                 start_v: float = 0,
                 stop_v: float = 5,
                 step_v: float = 0.1) -> str:
        """Generate DC sweep testbench"""

        return f"""
* Auto-generated DC Sweep
.title DC Analysis

* Variable voltage source
Vin input 0 DC 0

{netlist_components}

* DC sweep
.dc Vin {start_v} {stop_v} {step_v}

.control
run
print v(input) v(output)
.endc

.end
"""
