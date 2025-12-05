#!/usr/bin/env python3
"""
Demo rehearsal script with timing prompts
"""

import time
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.demo_script import DEMO_SCENARIOS, get_demo_transitions

def clear_screen():
    print("\n" * 50)

def countdown(seconds):
    """Visual countdown timer"""
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\rTime remaining: {i}s ")
        sys.stdout.flush()
        time.sleep(1)
    print("\n")

def rehearse_demo():
    """
    Interactive demo rehearsal with timing
    """
    print("=" * 60)
    print("AutoCDA Demo Rehearsal Script")
    print("=" * 60)
    print("\nPress ENTER when ready to start each section\n")
    
    transitions = get_demo_transitions()
    
    # Intro
    input("[PRESS ENTER] Hook (15 seconds)...")
    print("\nSAY: 'Imagine you're a hardware engineer starting a new project...'")
    countdown(15)
    
    input("[PRESS ENTER] Solution (30 seconds)...")
    print("\nSAY: 'That's AutoCDA. It converts natural language...'")
    countdown(30)
    
    # Demos
    print(f"\n{transitions['start']}")
    
    for idx, scenario in enumerate(DEMO_SCENARIOS):
        input(f"\n[PRESS ENTER] Demo {idx + 1}: {scenario.name} ({scenario.duration_seconds}s)...")
        print(f"\nINPUT: '{scenario.input_text}'")
        print("\nTALKING POINTS:")
        for point in scenario.talking_points:
            print(f"  - {point}")
        countdown(scenario.duration_seconds)
    
    # Close
    input("[PRESS ENTER] Differentiation (45 seconds)...")
    print("\nSAY: 'What makes AutoCDA different?...'")
    countdown(45)
    
    input("[PRESS ENTER] Vision (30 seconds)...")
    print("\nSAY: 'AutoCDA is just the beginning...'")
    countdown(30)
    
    input("[PRESS ENTER] Close (15 seconds)...")
    print("\nSAY: 'Live demo at [URL], source code on GitHub. Thank you!'")
    countdown(15)
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("Total time: ~5 minutes")
    print("=" * 60)

if __name__ == "__main__":
    try:
        rehearse_demo()
    except KeyboardInterrupt:
        print("\n\nRehearsal aborted.")
        sys.exit(0)
