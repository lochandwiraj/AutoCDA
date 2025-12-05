"""
Competitive analysis data for AutoCDA differentiation
"""

COMPETITIVE_LANDSCAPE = {
    "easyeda": {
        "name": "EasyEDA",
        "strengths": [
            "Large component library",
            "PCB layout integration",
            "Community sharing"
        ],
        "weaknesses": [
            "No natural language input",
            "Manual schematic placement",
            "Limited automation"
        ]
    },
    "circuitmaker": {
        "name": "CircuitMaker",
        "strengths": [
            "Professional-grade tool",
            "Version control",
            "Collaboration features"
        ],
        "weaknesses": [
            "Steep learning curve",
            "No AI assistance",
            "Manual design process"
        ]
    },
    "ltspice": {
        "name": "LTSpice",
        "strengths": [
            "Powerful simulation",
            "Free tool",
            "Industry standard"
        ],
        "weaknesses": [
            "No AI features",
            "Manual circuit entry",
            "Complex interface"
        ]
    }
}

AUTOCDA_DIFFERENTIATION = {
    "unique_features": [
        "Natural language to schematic conversion",
        "Explainable component value calculations",
        "Open-source EDA integration (SKiDL + KiCad)",
        "Zero manual component placement",
        "Formula-based transparency"
    ],
    "target_users": [
        "Hardware beginners learning circuit design",
        "Engineers doing rapid prototyping",
        "Students without EDA expertise",
        "Researchers exploring circuit concepts"
    ],
    "value_proposition": "AutoCDA eliminates the gap between design intent and working schematics by automating the entire translation from natural language to simulation-ready circuits."
}

def get_competitive_comparison():
    """
    Returns structured competitive comparison data
    """
    return {
        "competitors": COMPETITIVE_LANDSCAPE,
        "differentiation": AUTOCDA_DIFFERENTIATION
    }

def get_elevator_pitch():
    """
    Returns 30-second elevator pitch
    """
    return (
        "AutoCDA converts natural language circuit descriptions into working KiCad schematics. "
        "Unlike existing tools that require manual component placement and EDA expertise, "
        "AutoCDA automates the entire process from intent to schematic, with full explainability "
        "showing the formulas and reasoning behind every component value."
    )

def get_5_minute_pitch_structure():
    """
    Returns structured pitch outline with timing
    """
    return {
        "hook": {
            "duration_seconds": 15,
            "content": "Imagine you're a hardware engineer starting a new project. You need a low-pass filter. You spend an hour in KiCad placing components, calculating values, checking connections. What if you could just say 'design a 1kHz low-pass filter' and get a working schematic instantly?"
        },
        "solution": {
            "duration_seconds": 30,
            "content": "That's AutoCDA. It converts natural language into working electronic schematics. You describe your circuit in plain English, and it generates a complete KiCad schematic with properly calculated component values."
        },
        "demo": {
            "duration_seconds": 120,
            "examples": [
                {
                    "name": "Voltage Divider",
                    "time": 30,
                    "input": "Design a voltage divider that converts 9V to 5V"
                },
                {
                    "name": "RC Filter",
                    "time": 45,
                    "input": "Low-pass RC filter with 1kHz cutoff"
                },
                {
                    "name": "Live Custom",
                    "time": 30,
                    "input": "[Audience suggestion]"
                }
            ]
        },
        "differentiation": {
            "duration_seconds": 45,
            "content": "What makes AutoCDA different? First, only system going from natural language directly to production schematics. Second, explainability showing formulas and reasoning. Third, built on open-source tools making it accessible to everyone."
        },
        "vision": {
            "duration_seconds": 30,
            "content": "Our roadmap includes PCB layout automation, component sourcing, and multi-stage synthesis. The vision is making hardware design as accessible as software development."
        },
        "close": {
            "duration_seconds": 15,
            "content": "Live demo at [URL], source code on GitHub. Thank you!"
        }
    }
