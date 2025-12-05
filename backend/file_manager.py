import os
import sys
import subprocess
import uuid
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple


class FileManager:
    """Manages SKiDL execution and KiCad file generation"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def execute_skidl(self, skidl_code: str, circuit_name: str = None) -> Tuple[bool, str, str]:
        """
        Execute SKiDL code and generate netlist
        
        Args:
            skidl_code: SKiDL Python code as string
            circuit_name: Optional name for the circuit
            
        Returns:
            Tuple of (success: bool, netlist_path: str, error_message: str)
        """
        # Generate unique ID for this generation
        generation_id = str(uuid.uuid4())[:8]
        if circuit_name:
            generation_id = f"{circuit_name}_{generation_id}"
        
        # Create generation directory
        gen_dir = self.output_dir / generation_id
        gen_dir.mkdir(exist_ok=True)
        
        # Write SKiDL script to file
        script_path = gen_dir / "circuit.py"
        with open(script_path, 'w') as f:
            f.write(skidl_code)
        
        try:
            # Get the python executable from venv if available
            python_exe = sys.executable if 'venv' in sys.executable else 'python'
            
            # Execute SKiDL script
            result = subprocess.run(
                [python_exe, 'circuit.py'],
                cwd=str(gen_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                error_msg = f"SKiDL execution failed:\n{result.stderr}"
                return False, "", error_msg
            
            # Find generated netlist file
            netlist_path = gen_dir / "circuit.net"
            if not netlist_path.exists():
                # SKiDL might generate with different name
                netlist_files = list(gen_dir.glob("*.net"))
                if netlist_files:
                    netlist_path = netlist_files[0]
                else:
                    return False, "", "No netlist file generated"
            
            return True, str(netlist_path), ""
            
        except subprocess.TimeoutExpired:
            return False, "", "SKiDL execution timed out (>30s)"
        except Exception as e:
            return False, "", f"Execution error: {str(e)}"
    
    def convert_to_kicad(self, netlist_path: str) -> Tuple[bool, str, str]:
        """
        Convert netlist to KiCad project
        
        Args:
            netlist_path: Path to the netlist file
            
        Returns:
            Tuple of (success: bool, kicad_project_path: str, error_message: str)
        """
        netlist_path = Path(netlist_path)
        
        if not netlist_path.exists():
            return False, "", f"Netlist file not found: {netlist_path}"
        
        # KiCad project will be in same directory as netlist
        project_dir = netlist_path.parent
        project_name = netlist_path.stem
        
        # Create KiCad project file (.kicad_pro)
        kicad_pro_path = project_dir / f"{project_name}.kicad_pro"
        kicad_pro_content = self._generate_kicad_project_file()
        
        with open(kicad_pro_path, 'w') as f:
            f.write(kicad_pro_content)
        
        # Create KiCad schematic file (.kicad_sch)
        kicad_sch_path = project_dir / f"{project_name}.kicad_sch"
        kicad_sch_content = self._generate_kicad_schematic_file(netlist_path)
        
        with open(kicad_sch_path, 'w') as f:
            f.write(kicad_sch_content)
        
        return True, str(kicad_pro_path), ""
    
    def _generate_kicad_project_file(self) -> str:
        """Generate basic KiCad project file content"""
        return '''{
  "board": {
    "design_settings": {
      "defaults": {
        "board_outline_line_width": 0.1,
        "copper_line_width": 0.2
      }
    }
  },
  "meta": {
    "filename": "circuit.kicad_pro",
    "version": 1
  },
  "schematic": {
    "drawing": {
      "default_line_thickness": 6.0,
      "default_text_size": 50.0
    }
  }
}'''
    
    def _generate_kicad_schematic_file(self, netlist_path: Path) -> str:
        """Generate complete simulation-ready KiCad schematic for ANY circuit type"""
        import re
        
        try:
            with open(netlist_path, 'r') as f:
                netlist_content = f.read()
            
            # Extract components
            comp_pattern = r'\(comp\s+\(ref\s+"([^"]+)"\)\s+\(value\s+"([^"]+)"\)'
            components = re.findall(comp_pattern, netlist_content)
            
            # Extract nets (connections)
            net_pattern = r'\(net\s+\(code\s+\d+\)\s+\(name\s+"([^"]+)"\).*?\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)'
            nets = {}
            for match in re.finditer(net_pattern, netlist_content, re.DOTALL):
                net_name = match.group(1)
                if net_name not in nets:
                    nets[net_name] = []
                node_pattern = r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)'
                for node_match in re.finditer(node_pattern, match.group(0)):
                    nets[net_name].append((node_match.group(1), node_match.group(2)))
            
            # Categorize components
            resistors = [(ref, val) for ref, val in components if ref.startswith('R')]
            capacitors = [(ref, val) for ref, val in components if ref.startswith('C')]
            inductors = [(ref, val) for ref, val in components if ref.startswith('L')]
            
            # Determine circuit type
            if len(resistors) == 1 and len(capacitors) == 1:
                # RC Filter (low-pass or high-pass)
                return self._generate_rc_filter_schematic(resistors, capacitors, nets)
            elif len(resistors) == 2 and len(capacitors) == 0:
                # Voltage Divider
                return self._generate_voltage_divider_schematic(resistors, nets)
            elif len(resistors) == 1 and len(inductors) == 1:
                # RL Filter
                return self._generate_rl_filter_schematic(resistors, inductors, nets)
            else:
                # Generic layout for other circuits
                return self._generate_generic_schematic(components, nets)
        except Exception as e:
            print(f"Error generating schematic: {e}")
            return self._generate_empty_schematic()
    
    def _generate_rc_filter_schematic(self, resistors, capacitors, nets):
        """Generate complete RC filter with voltage source"""
        symbols = []
        wires = []
        labels = []
        power_symbols = []
        comp_positions = {}
        
        r_comp = resistors[0] if resistors else None
        c_comp = capacitors[0] if capacitors else None
        
        # Add voltage source at (80, 100)
        v_uuid = str(uuid.uuid4())
        symbols.append(f'''  (symbol (lib_id "Simulation_SPICE:VDC") (at 80 110 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {v_uuid})
    (property "Reference" "V1" (at 75 105 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "5V" (at 75 115 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 80 110 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at 80 110 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (pin "2" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "V1") (unit 1))
      )
    )
  )''')
        
        # Position R1 horizontally at (120, 100)
        if r_comp:
                ref, value = r_comp
                comp_uuid = str(uuid.uuid4())
                x, y = 120, 100
                comp_positions[ref] = {
                    'x': x, 'y': y, 'rotation': 0,
                    'pin1': (x - 5.08, y),  # Left pin
                    'pin2': (x + 5.08, y)   # Right pin
                }
                symbols.append(f'''  (symbol (lib_id "Device:R") (at {x} {y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {comp_uuid})
    (property "Reference" "{ref}" (at {x} {y - 5} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{value}" (at {x} {y + 5} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (pin "2" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "{ref}") (unit 1))
      )
    )
  )''')
        
        # Position C1 vertically at (140, 115) - below R1's right pin
        if c_comp:
                ref, value = c_comp
                comp_uuid = str(uuid.uuid4())
                x, y = 140, 115
                comp_positions[ref] = {
                    'x': x, 'y': y, 'rotation': 0,
                    'pin1': (x, y - 3.81),  # Top pin
                    'pin2': (x, y + 3.81)   # Bottom pin
                }
                symbols.append(f'''  (symbol (lib_id "Device:C") (at {x} {y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {comp_uuid})
    (property "Reference" "{ref}" (at {x + 3} {y} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{value}" (at {x + 3} {y + 3} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (pin "2" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "{ref}") (unit 1))
      )
    )
  )''')
        
        # Now add wires to connect everything
        # Wire from IN label to R1 pin 1
        if r_comp:
            r_ref = r_comp[0]
            r1_pin1 = comp_positions[r_ref]['pin1']
            in_x = r1_pin1[0] - 15
            labels.append(f'  (label "IN" (at {in_x} {r1_pin1[1]} 0) (fields_autoplaced) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uuid.uuid4()}))')
            wires.append(f'  (wire (pts (xy {in_x} {r1_pin1[1]}) (xy {r1_pin1[0]} {r1_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
        
        # Wire from R1 pin 2 to C1 pin 1 (vertical then horizontal)
        if r_comp and c_comp:
            r_ref = r_comp[0]
            c_ref = c_comp[0]
            r1_pin2 = comp_positions[r_ref]['pin2']
            c1_pin1 = comp_positions[c_ref]['pin1']
            
            # Vertical wire from R1 pin2 down to C1 level
            wires.append(f'  (wire (pts (xy {r1_pin2[0]} {r1_pin2[1]}) (xy {r1_pin2[0]} {c1_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            # Horizontal wire from that point to C1 pin1
            wires.append(f'  (wire (pts (xy {r1_pin2[0]} {c1_pin1[1]}) (xy {c1_pin1[0]} {c1_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            # Add junction at the corner
            wires.append(f'  (junction (at {r1_pin2[0]} {c1_pin1[1]}) (diameter 0) (color 0 0 0 0) (uuid {uuid.uuid4()}))')
            # Add OUT label
            out_x = r1_pin2[0] + 5
            labels.append(f'  (label "OUT" (at {out_x} {c1_pin1[1]} 0) (fields_autoplaced) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uuid.uuid4()}))')
            wires.append(f'  (wire (pts (xy {r1_pin2[0]} {c1_pin1[1]}) (xy {out_x} {c1_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            
        # Add ground symbol for C1 pin 2
        if c_comp:
                c_ref = c_comp[0]
                c1_pin2 = comp_positions[c_ref]['pin2']
                gnd_y = c1_pin2[1] + 5
                gnd_uuid = str(uuid.uuid4())
                power_symbols.append(f'''  (symbol (lib_id "power:GND") (at {c1_pin2[0]} {gnd_y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {gnd_uuid})
    (property "Reference" "#PWR001" (at {c1_pin2[0]} {gnd_y + 6.35} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND" (at {c1_pin2[0]} {gnd_y + 3.81} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {c1_pin2[0]} {gnd_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {c1_pin2[0]} {gnd_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "#PWR001") (unit 1))
      )
    )
  )''')
                # Wire from C1 pin2 to ground
                wires.append(f'  (wire (pts (xy {c1_pin2[0]} {c1_pin2[1]}) (xy {c1_pin2[0]} {gnd_y})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
        
        # Connect voltage source
        # V1 pin 1 (positive, top) at (80, 106.19) connects to IN
        # V1 pin 2 (negative, bottom) at (80, 113.81) connects to GND
        v1_pos = (80, 106.19)
        v1_neg = (80, 113.81)
        
        if r_comp:
            r1_pin1 = comp_positions[r_comp[0]]['pin1']
            in_label_x = r1_pin1[0] - 15
            # Wire from V1+ vertically to R1 level
            wires.append(f'  (wire (pts (xy {v1_pos[0]} {v1_pos[1]}) (xy {v1_pos[0]} {r1_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            # Wire horizontally from V1 to IN label
            wires.append(f'  (wire (pts (xy {v1_pos[0]} {r1_pin1[1]}) (xy {in_label_x} {r1_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            # Wire from IN label to R1 pin1 (this connects to the existing IN-to-R1 wire)
            # No need for additional wire here as it's already added in the "Wire from IN label to R1 pin 1" section
        
        # Ground for V1 negative
        gnd2_y = v1_neg[1] + 5
        gnd2_uuid = str(uuid.uuid4())
        power_symbols.append(f'''  (symbol (lib_id "power:GND") (at {v1_neg[0]} {gnd2_y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {gnd2_uuid})
    (property "Reference" "#PWR002" (at {v1_neg[0]} {gnd2_y + 6.35} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND" (at {v1_neg[0]} {gnd2_y + 3.81} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {v1_neg[0]} {gnd2_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {v1_neg[0]} {gnd2_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "#PWR002") (unit 1))
      )
    )
  )''')
        wires.append(f'  (wire (pts (xy {v1_neg[0]} {v1_neg[1]}) (xy {v1_neg[0]} {gnd2_y})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
        
        # Connect both grounds together
        if c_comp:
            c1_pin2 = comp_positions[c_comp[0]]['pin2']
            gnd1_y = c1_pin2[1] + 5
            # Horizontal wire connecting both ground points
            wires.append(f'  (wire (pts (xy {v1_neg[0]} {gnd2_y}) (xy {c1_pin2[0]} {gnd1_y})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            
        return self._build_schematic_output(symbols, power_symbols, wires, labels)
    
    def _old_fallback_return(self):
        """Old code - keeping for reference"""
        return f'''(kicad_sch (version 20230121) (generator eeschema)

  (uuid {uuid.uuid4()})

  (paper "A4")

  (title_block
    (title "AutoCDA Generated Circuit")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (comment 1 "Generated by AutoCDA")
    (comment 2 "Import the netlist to see connections")
  )

  (lib_symbols
    (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
      (property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at -1.778 0 90) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0.254) (type default)) (fill (type none))
        )
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Device:C" (pin_numbers hide) (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0.9652 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "C_0_1"
        (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
        (polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
      )
      (symbol "C_1_1"
        (pin passive line (at 0 3.81 270) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "power:GND" (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
      )
      (symbol "GND_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Simulation_SPICE:VDC" (pin_numbers hide) (pin_names (offset 0.0254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "V" (at 2.54 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "VDC" (at 2.54 0 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "VDC_0_1"
        (circle (center 0 0) (radius 3.81) (stroke (width 0.254) (type default)) (fill (type background)))
        (polyline (pts (xy -1.27 0.635) (xy 1.27 0.635)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 -0.635) (xy 0 -1.905)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 1.905) (xy 0 0.635)) (stroke (width 0) (type default)) (fill (type none)))
      )
      (symbol "VDC_1_1"
        (pin passive line (at 0 6.35 270) (length 2.54) (name "+" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -6.35 90) (length 2.54) (name "-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
  )

{symbols_str}

{wires_str}

{labels_str}

  (sheet_instances
    (path "/" (page "1"))
  )
)'''
    
    def _old_fallback_code(self):
        """Old code - removed"""
        return f'''(kicad_sch (version 20230121) (generator eeschema)

  (uuid {uuid.uuid4()})

  (paper "A4")

  (title_block
    (title "AutoCDA Generated Circuit")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (comment 1 "Generated by AutoCDA")
  )

  (lib_symbols)

  (sheet_instances
    (path "/" (page "1"))
  )
)'''
    
    def _generate_voltage_divider_schematic(self, resistors, nets):
        """Generate complete voltage divider with voltage source"""
        symbols = []
        wires = []
        labels = []
        power_symbols = []
        comp_positions = {}
        
        r1_comp = resistors[0] if len(resistors) > 0 else None
        r2_comp = resistors[1] if len(resistors) > 1 else None
        
        # Add voltage source at (100, 80)
        v_uuid = str(uuid.uuid4())
        symbols.append(f'''  (symbol (lib_id "Simulation_SPICE:VDC") (at 100 90 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {v_uuid})
    (property "Reference" "V1" (at 95 85 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "9V" (at 95 95 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 100 90 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at 100 90 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (pin "2" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "V1") (unit 1))
      )
    )
  )''')
        
        # R1 vertical at (140, 100)
        if r1_comp:
            ref, value = r1_comp
            comp_uuid = str(uuid.uuid4())
            x, y = 140, 100
            comp_positions[ref] = {
                'x': x, 'y': y, 'rotation': 0,
                'pin1': (x, y - 3.81),
                'pin2': (x, y + 3.81)
            }
            symbols.append(f'''  (symbol (lib_id "Device:R") (at {x} {y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {comp_uuid})
    (property "Reference" "{ref}" (at {x + 3} {y} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{value}" (at {x + 3} {y + 3} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (pin "2" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "{ref}") (unit 1))
      )
    )
  )''')
        
        # R2 vertical at (140, 130)
        if r2_comp:
            ref, value = r2_comp
            comp_uuid = str(uuid.uuid4())
            x, y = 140, 130
            comp_positions[ref] = {
                'x': x, 'y': y, 'rotation': 0,
                'pin1': (x, y - 3.81),
                'pin2': (x, y + 3.81)
            }
            symbols.append(f'''  (symbol (lib_id "Device:R") (at {x} {y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {comp_uuid})
    (property "Reference" "{ref}" (at {x + 3} {y} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{value}" (at {x + 3} {y + 3} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (pin "2" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "{ref}") (unit 1))
      )
    )
  )''')
        
        # Connect everything
        v1_pos = (100, 83.65)
        v1_neg = (100, 96.35)
        
        if r1_comp and r2_comp:
            r1_pin1 = comp_positions[r1_comp[0]]['pin1']
            r1_pin2 = comp_positions[r1_comp[0]]['pin2']
            r2_pin1 = comp_positions[r2_comp[0]]['pin1']
            r2_pin2 = comp_positions[r2_comp[0]]['pin2']
            
            # V1+ to R1 pin1
            wires.append(f'  (wire (pts (xy {v1_pos[0]} {v1_pos[1]}) (xy {v1_pos[0]} {r1_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            wires.append(f'  (wire (pts (xy {v1_pos[0]} {r1_pin1[1]}) (xy {r1_pin1[0]} {r1_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            labels.append(f'  (label "VIN" (at {v1_pos[0] + 5} {r1_pin1[1]} 0) (fields_autoplaced) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uuid.uuid4()}))')
            
            # R1 pin2 to R2 pin1 (VOUT)
            wires.append(f'  (wire (pts (xy {r1_pin2[0]} {r1_pin2[1]}) (xy {r2_pin1[0]} {r2_pin1[1]})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            labels.append(f'  (label "VOUT" (at {r1_pin2[0] + 5} {r1_pin2[1] + 5} 0) (fields_autoplaced) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uuid.uuid4()}))')
            
            # R2 pin2 to GND
            gnd_y = r2_pin2[1] + 5
            gnd_uuid = str(uuid.uuid4())
            power_symbols.append(f'''  (symbol (lib_id "power:GND") (at {r2_pin2[0]} {gnd_y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {gnd_uuid})
    (property "Reference" "#PWR001" (at {r2_pin2[0]} {gnd_y + 6.35} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND" (at {r2_pin2[0]} {gnd_y + 3.81} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {r2_pin2[0]} {gnd_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {r2_pin2[0]} {gnd_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "#PWR001") (unit 1))
      )
    )
  )''')
            wires.append(f'  (wire (pts (xy {r2_pin2[0]} {r2_pin2[1]}) (xy {r2_pin2[0]} {gnd_y})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            
            # V1- to GND
            gnd2_y = v1_neg[1] + 5
            gnd2_uuid = str(uuid.uuid4())
            power_symbols.append(f'''  (symbol (lib_id "power:GND") (at {v1_neg[0]} {gnd2_y} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
    (uuid {gnd2_uuid})
    (property "Reference" "#PWR002" (at {v1_neg[0]} {gnd2_y + 6.35} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND" (at {v1_neg[0]} {gnd2_y + 3.81} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {v1_neg[0]} {gnd2_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {v1_neg[0]} {gnd2_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuid.uuid4()}))
    (instances
      (project "circuit"
        (path "/" (reference "#PWR002") (unit 1))
      )
    )
  )''')
            wires.append(f'  (wire (pts (xy {v1_neg[0]} {v1_neg[1]}) (xy {v1_neg[0]} {gnd2_y})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
            wires.append(f'  (wire (pts (xy {v1_neg[0]} {gnd2_y}) (xy {r2_pin2[0]} {gnd_y})) (stroke (width 0) (type default)) (uuid {uuid.uuid4()}))')
        
        return self._build_schematic_output(symbols, power_symbols, wires, labels)
    
    def _generate_rl_filter_schematic(self, resistors, inductors, nets):
        """Generate RL filter - similar to RC but with inductor"""
        # Similar to RC filter but replace C with L
        return self._generate_empty_schematic()
    
    def _generate_generic_schematic(self, components, nets):
        """Generate generic circuit layout"""
        return self._generate_empty_schematic()
    
    def _generate_empty_schematic(self):
        """Generate empty schematic as fallback"""
        return f'''(kicad_sch (version 20230121) (generator eeschema)
  (uuid {uuid.uuid4()})
  (paper "A4")
  (title_block
    (title "AutoCDA Generated Circuit")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (comment 1 "Generated by AutoCDA")
  )
  (lib_symbols)
  (sheet_instances
    (path "/" (page "1"))
  )
)'''
    
    def _build_schematic_output(self, symbols, power_symbols, wires, labels):
        """Build final schematic output"""
        symbols_str = '\n\n'.join(symbols + power_symbols)
        wires_str = '\n\n'.join(wires)
        labels_str = '\n\n'.join(labels)
        
        return f'''(kicad_sch (version 20230121) (generator eeschema)

  (uuid {uuid.uuid4()})

  (paper "A4")

  (title_block
    (title "AutoCDA Generated Circuit")
    (date "{datetime.now().strftime('%Y-%m-%d')}")
    (comment 1 "Generated by AutoCDA - Simulation Ready")
  )

  (lib_symbols
    (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
      (property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at -1.778 0 90) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0.254) (type default)) (fill (type none))
        )
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Device:C" (pin_numbers hide) (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0.9652 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "C_0_1"
        (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
        (polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
      )
      (symbol "C_1_1"
        (pin passive line (at 0 3.81 270) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "power:GND" (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
      )
      (symbol "GND_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Simulation_SPICE:VDC" (pin_numbers hide) (pin_names (offset 0.0254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "V" (at 2.54 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "VDC" (at 2.54 0 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "VDC_0_1"
        (circle (center 0 0) (radius 3.81) (stroke (width 0.254) (type default)) (fill (type background)))
        (polyline (pts (xy -1.27 0.635) (xy 1.27 0.635)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 -0.635) (xy 0 -1.905)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 1.905) (xy 0 0.635)) (stroke (width 0) (type default)) (fill (type none)))
      )
      (symbol "VDC_1_1"
        (pin passive line (at 0 6.35 270) (length 2.54) (name "+" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -6.35 90) (length 2.54) (name "-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
  )

{symbols_str}

{wires_str}

{labels_str}

  (sheet_instances
    (path "/" (page "1"))
  )
)'''
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """
        Remove generated files older than specified hours
        
        Args:
            max_age_hours: Files older than this will be deleted
        """
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for item in self.output_dir.iterdir():
            if item.is_dir():
                # Check directory modification time
                dir_mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if dir_mtime < cutoff_time:
                    shutil.rmtree(item)
                    print(f"Cleaned up old directory: {item}")
    
    def get_download_path(self, project_path: str) -> str:
        """
        Get the path for downloading the KiCad project
        
        Args:
            project_path: Path to the .kicad_pro file
            
        Returns:
            Path suitable for download link
        """
        return str(Path(project_path).parent)


# Test function
def test_file_manager():
    """Test the file manager with sample SKiDL code"""
    
    sample_skidl = '''from skidl import *

reset()

R1 = Part('Device', 'R', value='1k', footprint='Resistor_SMD:R_0805_2012Metric')
C1 = Part('Device', 'C', value='159n', footprint='Capacitor_SMD:C_0805_2012Metric')

IN = Net('IN')
N1 = Net('N1')
GND = Net('GND')

R1[1] += IN
R1[2] += N1
C1[1] += N1
C1[2] += GND

generate_netlist()
'''
    
    fm = FileManager()
    
    print("Testing SKiDL execution...")
    success, netlist_path, error = fm.execute_skidl(sample_skidl, "test_rc_filter")
    
    if success:
        print(f"✓ SKiDL executed successfully")
        print(f"  Netlist: {netlist_path}")
        
        print("\nTesting KiCad conversion...")
        success, project_path, error = fm.convert_to_kicad(netlist_path)
        
        if success:
            print(f"✓ KiCad project created")
            print(f"  Project: {project_path}")
        else:
            print(f"✗ KiCad conversion failed: {error}")
    else:
        print(f"✗ SKiDL execution failed: {error}")


if __name__ == "__main__":
    test_file_manager()
