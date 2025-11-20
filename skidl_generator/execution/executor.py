import subprocess
import tempfile
import os
from pathlib import Path

class SKiDLExecutor:

    def __init__(self, timeout=30):
        self.timeout = timeout
        self.pythonpath = r'C:\autocda\.venv\Lib\site-packages'

    def execute(self, skidl_code):
        with tempfile.TemporaryDirectory() as tmpdir:
            code_file = Path(tmpdir) / "circuit.py"

            # Inject KICAD6 compatibility
            patched = "from skidl import set_default_tool\nset_default_tool('kicad6')\n\n" + skidl_code
            code_file.write_text(patched)

            env = os.environ.copy()
            env["PYTHONPATH"] = self.pythonpath

            try:
                result = subprocess.run(
                    ["python", str(code_file)],
                    cwd=tmpdir,
                    capture_output=True,
                    timeout=self.timeout,
                    text=True,
                    env=env
                )

                netlist_file = Path(tmpdir) / "circuit.net"
                if netlist_file.exists():
                    return True, netlist_file.read_text(), result.stderr
                else:
                    return False, None, result.stderr

            except subprocess.TimeoutExpired:
                return False, None, f"Execution timeout ({self.timeout}s)"
            except Exception as e:
                return False, None, str(e)
