import sys
sys.path.insert(0,"integration")
sys.path.insert(0,"mappers")
sys.path.insert(0,"templates")
sys.path.insert(0,"execution")
sys.path.insert(0,"processing")
sys.path.insert(0,"tests")

from integration.pipeline import SKiDLPipeline

pipeline = SKiDLPipeline()

dsl = {
    "components": [
        {"id": "R1", "type": "resistor", "value": "1k", "nets": ["N1", "N2"]},
        {"id": "C1", "type": "capacitor", "value": "10u", "nets": ["N2", "GND"]}
    ]
}

result = pipeline.generate_from_dsl(dsl)

print("\n===== SKIDL CODE =====")
print(result.get("skidl_code"))

print("\n===== RAW NETLIST =====")
print(result.get("netlist"))

print("\n===== PARSED NETLIST =====")
print(result.get("parsed"))

print("\n===== VALIDATION =====")
print(result.get("validation"))
