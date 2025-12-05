"""
Demo script generation and execution helpers
"""

from typing import List, Dict
import json

class DemoScenario:
    """Single demo scenario with timing"""
    
    def __init__(self, name: str, input_text: str, duration_seconds: int, talking_points: List[str]):
        self.name = name
        self.input_text = input_text
        self.duration_seconds = duration_seconds
        self.talking_points = talking_points
    
    def to_dict(self):
        return {
            "name": self.name,
            "input": self.input_text,
            "duration": self.duration_seconds,
            "points": self.talking_points
        }

# Pre-defined demo scenarios
DEMO_SCENARIOS = [
    DemoScenario(
        name="Simple Voltage Divider",
        input_text="Design a voltage divider that converts 9V to 5V",
        duration_seconds=30,
        talking_points=[
            "This is the simplest use case",
            "Watch how it calculates the resistor ratio",
            "Notice the explanation shows the formula"
        ]
    ),
    DemoScenario(
        name="RC Low-Pass Filter",
        input_text="Design a low-pass RC filter with cutoff frequency of 1kHz",
        duration_seconds=45,
        talking_points=[
            "Now a more complex circuit",
            "System calculates R and C values using fc = 1/(2πRC)",
            "Values are rounded to standard E12 series",
            "Schematic is simulation-ready in KiCad"
        ]
    ),
    DemoScenario(
        name="RC High-Pass Filter",
        input_text="Create a high-pass RC filter with 500Hz cutoff",
        duration_seconds=30,
        talking_points=[
            "Similar circuit, different configuration",
            "Notice how component placement differs",
            "Explanation clarifies high-pass vs low-pass"
        ]
    )
]

def get_demo_script():
    """
    Returns complete demo script with timing
    """
    return {
        "total_duration_seconds": sum(s.duration_seconds for s in DEMO_SCENARIOS),
        "scenarios": [s.to_dict() for s in DEMO_SCENARIOS]
    }

def get_demo_transitions():
    """
    Returns transition phrases between demos
    """
    return {
        "start": "Let me show you how this works with three examples",
        "between_demos": [
            "Now let's try something more complex",
            "Here's another example",
            "One more to show the flexibility"
        ],
        "to_custom": "Give me any circuit description and I'll generate it live",
        "end": "As you can see, from description to schematic in seconds"
    }

def get_backup_responses():
    """
    Returns fallback responses for demo failures
    """
    return {
        "api_slow": "While that's processing, let me show you a pre-generated example",
        "api_fail": "Let me switch to the video backup which shows the same flow",
        "internet_down": "I have a local version running, let me demonstrate with that",
        "total_failure": "Let me walk you through with these screenshots of successful generations"
    }

def export_demo_script_json(filepath: str = "demo_script.json"):
    """
    Export demo script to JSON for reference
    """
    from backend.competitive_analysis import get_5_minute_pitch_structure
    
    script_data = {
        "pitch_structure": get_5_minute_pitch_structure(),
        "demo_scenarios": get_demo_script(),
        "transitions": get_demo_transitions(),
        "backup_responses": get_backup_responses()
    }
    
    with open(filepath, 'w') as f:
        json.dump(script_data, f, indent=2)
    
    return filepath
