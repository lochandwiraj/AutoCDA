"""
Setup KiCad environment for SKiDL in serverless environments
"""
import os
import sys

def setup_kicad_paths():
    """Set up KiCad library paths for SKiDL"""
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kicad_libs = os.path.join(project_root, 'kicad_libs', 'symbols')
    
    # Set environment variables for KiCad symbol libraries
    os.environ['KICAD_SYMBOL_DIR'] = kicad_libs
    os.environ['KICAD6_SYMBOL_DIR'] = kicad_libs
    os.environ['KICAD7_SYMBOL_DIR'] = kicad_libs
    os.environ['KICAD8_SYMBOL_DIR'] = kicad_libs
    os.environ['KICAD9_SYMBOL_DIR'] = kicad_libs
    
    print(f"KiCad symbol directory set to: {kicad_libs}")
    
    # Verify the library exists
    device_lib = os.path.join(kicad_libs, 'Device.kicad_sym')
    if os.path.exists(device_lib):
        print(f"✓ Device library found: {device_lib}")
    else:
        print(f"✗ WARNING: Device library not found at {device_lib}")
    
    return kicad_libs

if __name__ == "__main__":
    setup_kicad_paths()
