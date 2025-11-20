import pytest
from integration.pipeline import SKiDLPipeline

class TestCircuitGeneration:
    
    def setup_method(self):
        self.pipeline = SKiDLPipeline()
    
    def test_voltage_divider(self):
        dsl = {
            "components": [
                {"type": "resistor", "id": "R1", "value": "10k", "nets": ["VIN", "VOUT"]},
                {"type": "resistor", "id": "R2", "value": "10k", "nets": ["VOUT", "GND"]}
            ]
        }
        result = self.pipeline.generate_from_dsl(dsl)
        assert result["success"]
        assert len(result["parsed"]["components"]) == 2
        print("✓ Voltage divider test passed")
    
    def test_rc_lowpass(self):
        dsl = {
            "components": [
                {"type": "resistor", "id": "R1", "value": "1k", "nets": ["VIN", "N1"]},
                {"type": "capacitor", "id": "C1", "value": "159n", "nets": ["N1", "GND"]}
            ],
            "constraints": {"cutoff_freq": 1000}
        }
        result = self.pipeline.generate_from_dsl(dsl)
        assert result["success"]
        assert result["validation"]["valid"]
        print("✓ RC lowpass test passed")
    
    def test_rc_highpass(self):
        dsl = {
            "components": [
                {"type": "capacitor", "id": "C1", "value": "159n", "nets": ["VIN", "N1"]},
                {"type": "resistor", "id": "R1", "value": "1k", "nets": ["N1", "GND"]}
            ],
            "constraints": {"cutoff_freq": 1000}
        }
        result = self.pipeline.generate_from_dsl(dsl)
        assert result["success"]
        print("✓ RC highpass test passed")
    
    def test_opamp_amplifier(self):
        dsl = {
            "components": [
                {"type": "opamp", "id": "U1", "model": "LM741", "nets": {}},
                {"type": "resistor", "id": "RF", "value": "10k", "nets": ["OUT", "IN-"]},
                {"type": "resistor", "id": "RIN", "value": "1k", "nets": ["IN-", "GND"]}
            ],
            "constraints": {"gain": 11}
        }
        result = self.pipeline.generate_from_dsl(dsl)
        assert result["success"]
        print("✓ Op-amp amplifier test passed")
    
    def test_bridge_rectifier(self):
        dsl = {
            "components": [
                {"type": "diode", "id": "D1", "part_number": "1N4001", "nets": ["AC1", "DC+"]},
                {"type": "diode", "id": "D2", "part_number": "1N4001", "nets": ["AC2", "DC+"]},
                {"type": "diode", "id": "D3", "part_number": "1N4001", "nets": ["DC-", "AC1"]},
                {"type": "diode", "id": "D4", "part_number": "1N4001", "nets": ["DC-", "AC2"]}
            ]
        }
        result = self.pipeline.generate_from_dsl(dsl)
        assert result["success"]
        assert len(result["parsed"]["components"]) == 4
        print("✓ Bridge rectifier test passed")

# Run all tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
