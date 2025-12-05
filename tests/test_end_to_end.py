import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.intent_extractor import IntentExtractor
from backend.dsl_generator import DSLGenerator
from backend.circuit_validator import CircuitValidator
from backend.json_to_skidl import generate_skidl_code
from backend.file_manager import FileManager

class TestEndToEnd:
    
    @pytest.fixture
    def test_circuits(self):
        return [
            {
                "name": "RC Low-Pass Filter",
                "input": "Design a low-pass RC filter with 1kHz cutoff frequency",
                "expected_components": ["resistor", "capacitor"]
            },
            {
                "name": "RC High-Pass Filter",
                "input": "Create a high-pass filter with 500Hz cutoff",
                "expected_components": ["resistor", "capacitor"]
            },
            {
                "name": "Voltage Divider",
                "input": "Design a voltage divider that converts 9V to 5V",
                "expected_components": ["resistor"]
            },
            {
                "name": "LED Current Limiter",
                "input": "Design an LED current limiter for 20mA at 9V supply",
                "expected_components": ["resistor"]
            },
            {
                "name": "Voltage Divider 12V to 3.3V",
                "input": "Voltage divider from 12V to 3.3V output",
                "expected_components": ["resistor"]
            }
        ]
    
    def test_full_pipeline(self, test_circuits):
        results = []
        
        for circuit in test_circuits:
            print(f"\nTesting: {circuit['name']}")
            
            try:
                # Stage 1: Intent Extraction
                extractor = IntentExtractor()
                circuit_json = extractor.extract_circuit_intent(circuit["input"])
                assert circuit_json is not None, f"Intent extraction failed for {circuit['name']}"
                print(f"✓ Intent extracted")
                
                # Stage 2: DSL Generation
                dsl_gen = DSLGenerator()
                dsl = dsl_gen.json_to_dsl(circuit_json)
                assert dsl is not None, f"DSL generation failed for {circuit['name']}"
                print(f"✓ DSL generated")
                
                # Stage 3: Validation
                validator = CircuitValidator()
                validation = validator.validate_circuit(circuit_json)
                assert validation["valid"], f"Validation failed: {validation.get('errors')}"
                print(f"✓ Validation passed")
                
                # Stage 4: SKiDL Generation
                skidl_code = generate_skidl_code(dsl)
                assert skidl_code is not None, f"SKiDL generation failed for {circuit['name']}"
                print(f"✓ SKiDL generated")
                
                # Stage 5: File Creation
                file_mgr = FileManager()
                success, netlist_path, _ = file_mgr.execute_skidl_code(skidl_code)
                assert success and Path(netlist_path).exists(), f"Netlist not created for {circuit['name']}"
                print(f"✓ Netlist created: {netlist_path}")
                
                results.append({
                    "name": circuit["name"],
                    "status": "PASS",
                    "netlist": netlist_path
                })
                
            except Exception as e:
                print(f"✗ Failed: {str(e)}")
                results.append({
                    "name": circuit["name"],
                    "status": "FAIL",
                    "error": str(e)
                })
        
        # Summary
        passed = sum(1 for r in results if r["status"] == "PASS")
        total = len(results)
        print(f"\n{'='*50}")
        print(f"RESULTS: {passed}/{total} tests passed")
        print(f"{'='*50}")
        
        for result in results:
            status_symbol = "✓" if result["status"] == "PASS" else "✗"
            print(f"{status_symbol} {result['name']}: {result['status']}")
        
        assert passed == total, f"Only {passed}/{total} tests passed"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
