#!/usr/bin/env python3
"""
Export demo materials to JSON files for study and reference
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.demo_script import export_demo_script_json
from backend.qa_responses import export_qa_study_guide

def main():
    print("=" * 60)
    print("Exporting Demo Materials")
    print("=" * 60)
    
    # Export demo script
    print("\n1. Exporting demo script...")
    demo_file = export_demo_script_json("demo_script.json")
    print(f"   ✓ Created: {demo_file}")
    
    # Export Q&A guide
    print("\n2. Exporting Q&A study guide...")
    qa_file = export_qa_study_guide("qa_study_guide.json")
    print(f"   ✓ Created: {qa_file}")
    
    print("\n" + "=" * 60)
    print("Export Complete!")
    print("=" * 60)
    print("\nFiles created:")
    print("  - demo_script.json")
    print("  - qa_study_guide.json")
    print("\nUse these files to prepare for your presentation.")
    print("=" * 60)

if __name__ == "__main__":
    main()
