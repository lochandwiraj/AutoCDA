#!/usr/bin/env python3
"""
End-to-end integration test for AutoCDA backend pipeline
Tests: User Input -> Intent Extraction -> DSL -> SKiDL -> KiCad
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from skidl_generator import SKiDLGenerator
from file_manager import FileManager


def test_end_to_end_pipeline():
    """Test complete pipeline with RC low-pass filter"""
    
    print("=" * 70)
    print("AutoCDA Backend Integration Test")
    print("=" * 70)
    
    # Step 1: Define test input (simulating user input)
    user_input = "Design a 1kHz low-pass filter"
    print(f"\n[1] User Input: '{user_input}'")
    
    # Step 2: Simulated DSL (in real system, this comes from intent_extractor.py)
    test_dsl = """COMP: R1 resistor value=1k nets=(IN, N1)
COMP: C1 capacitor value=159n nets=(N1, GND)
CONSTRAINT: cutoff=1kHz"""
    
    print(f"\n[2] Generated DSL:")
    print("-" * 70)
    print(test_dsl)
    print("-" * 70)
    
    # Step 3: Convert DSL to SKiDL
    print("\n[3] Converting DSL to SKiDL...")
    generator = SKiDLGenerator()
    skidl_code = generator.dsl_to_skidl(test_dsl)
    
    print("✓ SKiDL code generated")
    print(f"   Length: {len(skidl_code)} characters")
    
    # Step 4: Execute SKiDL and generate netlist
    print("\n[4] Executing SKiDL code...")
    fm = FileManager(output_dir="output_test")
    
    success, netlist_path, error = fm.execute_skidl(skidl_code, "test_1khz_filter")
    
    if not success:
        print(f"✗ SKiDL execution FAILED")
        print(f"   Error: {error}")
        return False
    
    print(f"✓ Netlist generated: {netlist_path}")
    
    # Step 5: Convert to KiCad project
    print("\n[5] Creating KiCad project...")
    success, project_path, error = fm.convert_to_kicad(netlist_path)
    
    if not success:
        print(f"✗ KiCad conversion FAILED")
        print(f"   Error: {error}")
        return False
    
    print(f"✓ KiCad project created: {project_path}")
    
    # Step 6: Verify files exist
    print("\n[6] Verifying output files...")
    project_dir = Path(project_path).parent
    
    files_to_check = [
        ("Python script", project_dir / "circuit.py"),
        ("Netlist", project_dir / "circuit.net"),
        ("KiCad project", Path(project_path)),
        ("KiCad schematic", project_dir / f"{Path(project_path).stem}.kicad_sch")
    ]
    
    all_exist = True
    for file_desc, file_path in files_to_check:
        if file_path.exists():
            print(f"   ✓ {file_desc}: {file_path.name}")
        else:
            print(f"   ✗ {file_desc}: MISSING")
            all_exist = False
    
    # Final result
    print("\n" + "=" * 70)
    if all_exist:
        print("✓ INTEGRATION TEST PASSED")
        print(f"\nNext step: Open '{project_path}' in KiCad to verify schematic")
        print("=" * 70)
        return True
    else:
        print("✗ INTEGRATION TEST FAILED - Some files missing")
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = test_end_to_end_pipeline()
    sys.exit(0 if success else 1)
