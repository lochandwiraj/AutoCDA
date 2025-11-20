import subprocess
import tempfile
from pathlib import Path
from typing import Dict
import math

class NgspiceSimulator:
    def __init__(self, timeout: int = 60):
        self.timeout = timeout

    def run_simulation(self, netlist: str, analysis_type: str = "ac") -> Dict:
        try:
            # Make temp SPICE file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cir", mode="w") as f:
                f.write(netlist)
                netlist_path = Path(f.name)

            # WRDATA output always written to CWD
            wr_path = Path("ac_output.txt")
            if wr_path.exists():
                wr_path.unlink()

            # Run ngspice
            cmd = ["ngspice", "-b", str(netlist_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)

            if result.returncode != 0:
                return {"success": False, "error": result.stderr}

            # Parse WRDATA file
            if wr_path.exists():
                content = wr_path.read_text()
                data = self._parse_wrdata(content)
                return {"success": True, "data": data}

            return {"success": False, "error": "ac_output.txt not found"}

        except Exception as e:
            return {"success": False, "error": str(e)}

            







    def _parse_wrdata(self, content: str) -> Dict:
        """
        Parse AC analysis output with 6 columns:
        freq  real_out  imag_out  real_in  imag_in  extra?
        """
        frequencies = []
        magnitudes = []
        phases = []

        for line in content.splitlines():
            parts = line.split()

            # Require at least 5 numeric columns: freq, out(real/imag), in(real/imag)
            if len(parts) >= 5:
                try:
                    f = float(parts[0])
                    real_out = float(parts[1])
                    imag_out = float(parts[2])
                    real_in = float(parts[3])
                    imag_in = float(parts[4])

                    mag_out = math.sqrt(real_out**2 + imag_out**2)
                    mag_in = math.sqrt(real_in**2 + imag_in**2)

                    if mag_in == 0:
                        continue

                    gain = mag_out / mag_in
                    phase = math.atan2(imag_out, real_out)

                    frequencies.append(f)
                    magnitudes.append(gain)
                    phases.append(phase)

                except:
                    pass

        return {
            "frequencies": frequencies,
            "magnitudes": magnitudes,
            "phases": phases
        }

