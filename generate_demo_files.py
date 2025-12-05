"""
Pre-generate demo circuit files for offline backup
"""

import os
from pathlib import Path
from datetime import datetime
from backend.intent_extractor import IntentExtractor
from backend.dsl_generator import DSLGenerator
from backend.skidl_generator import SKiDLGenerator
from backend.file_manager import FileManager

DEMO_DIR = Path('./demo_files')
DEMO_DIR.mkdir(exist_ok=True)

DEMO_CIRCUITS = [
    {
        'name': 'lowpass_1khz',
        'description': 'Design a low-pass RC filter with 1kHz cutoff frequency'
    },
    {
        'name': 'voltage_divider_9v_to_5v',
        'description': 'Create a voltage divider that converts 9V to 5V'
    },
    {
        'name': 'highpass_500hz',
        'description': 'Design a high-pass RC filter with 500Hz cutoff'
    },
    {
        'name': 'voltage_divider_12v_to_3v',
        'description': 'Create a voltage divider from 12V to 3.3V'
    }
]

def generate_demo_files():
    print("🔧 Generating pre-built demo files...")
    
    extractor = IntentExtractor()
    dsl_gen = DSLGenerator()
    skidl_gen = SKiDLGenerator()
    file_mgr = FileManager(output_dir=str(DEMO_DIR))
    
    for demo in DEMO_CIRCUITS:
        print(f"\nGenerating: {demo['name']}")
        
        try:
            # Extract intent
            circuit_json = extractor.extract_circuit_intent(demo['description'])
            
            # Generate DSL
            dsl = dsl_gen.json_to_dsl(circuit_json)
            
            # Generate SKiDL
            from backend.json_to_skidl import generate_skidl_code
            skidl_code = generate_skidl_code(dsl)
            
            # Execute
            success, netlist_path, _ = file_mgr.execute_skidl_code(skidl_code)
            
            if success:
                # Rename to friendly name
                old_path = Path(netlist_path)
                new_path = DEMO_DIR / f"{demo['name']}.net"
                if old_path.exists():
                    old_path.rename(new_path)
                
                # Save metadata
                meta_path = DEMO_DIR / f"{demo['name']}_meta.txt"
                with open(meta_path, 'w') as f:
                    f.write(f"Description: {demo['description']}\n")
                    f.write(f"Generated: {datetime.now().isoformat()}\n")
                    f.write(f"\nDSL:\n{dsl}\n")
                
                print(f"✅ Generated: {new_path.name}")
            else:
                print(f"❌ Failed to generate netlist")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n✅ Demo files saved to: {DEMO_DIR.absolute()}")
    print(f"Total files: {len(list(DEMO_DIR.glob('*.net')))}")

if __name__ == '__main__':
    generate_demo_files()
