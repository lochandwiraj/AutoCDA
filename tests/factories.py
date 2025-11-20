from faker import Faker
import random

fake = Faker()

class CircuitFactory:
    """Generate test circuits programmatically"""
    
    @staticmethod
    def voltage_divider(r1_value="10k", r2_value="10k"):
        return {
            "components": [
                {"id": "R1", "type": "resistor", "value": r1_value, "nets": ["VCC", "OUT"]},
                {"id": "R2", "type": "resistor", "value": r2_value, "nets": ["OUT", "GND"]}
            ],
            "constraints": {"input_voltage": "5V"}
        }
    
    @staticmethod
    def rc_lowpass(cutoff_freq=1000):
        R = 1000
        C = 1 / (2 * 3.14159 * cutoff_freq * R)
        return {
            "components": [
                {"id": "R1", "type": "resistor", "value": f"{R}", "nets": ["IN", "OUT"]},
                {"id": "C1", "type": "capacitor", "value": f"{C*1e9:.1f}nF", "nets": ["OUT", "GND"]}
            ],
            "constraints": {"cutoff_freq": f"{cutoff_freq}Hz"}
        }
    
    @staticmethod
    def random_circuit(num_components=5):
        components = []
        nets = ["VCC", "GND", "N1", "N2", "N3"]
        
        for i in range(num_components):
            comp_type = random.choice(["resistor", "capacitor"])
            value = (
                f"{random.randint(1, 100)}k"
                if comp_type == "resistor"
                else f"{random.randint(1, 1000)}nF"
            )
            selected_nets = random.sample(nets, 2)
            components.append({
                "id": f"{comp_type[0].upper()}{i+1}",
                "type": comp_type,
                "value": value,
                "nets": selected_nets
            })
        return {"components": components}
