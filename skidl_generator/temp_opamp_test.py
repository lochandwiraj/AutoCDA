from integration.pipeline import SKiDLPipeline

pipeline = SKiDLPipeline()

dsl = {
    'components': [
        {'type': 'opamp', 'id': 'U1', 'model': 'LM741', 'nets': {}},
        {'type': 'resistor', 'id': 'RF', 'value': '10k', 'nets': ['OUT', 'IN-']},
        {'type': 'resistor', 'id': 'RIN', 'value': '1k', 'nets': ['IN-', 'GND']}
    ],
    'constraints': {'gain': 11}
}

print("\n=== OPAMP GENERATED CODE ===\n")
result = pipeline.generate_from_dsl(dsl)
print(result["skidl_code"])
print("\nSUCCESS:", result["success"])
print("\nERROR:", result.get("error"))
