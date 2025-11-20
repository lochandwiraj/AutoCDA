from skidl import Part, Net

class ActiveMapper:

    IC_PIN_MAPS = {
        "LM741": {
            "pins": 8,
            "pinout": {
                "OUT": 6,
                "IN+": 3,
                "IN-": 2,
                "V+": 7,
                "V-": 4
            }
        },
        "555": {
            "pins": 8,
            "pinout": {
                "GND": 1,
                "TRIG": 2,
                "OUT": 3,
                "RESET": 4,
                "CTRL": 5,
                "THR": 6,
                "DIS": 7,
                "VCC": 8
            }
        }
    }

    def create_opamp(self, comp_data):
        part_type = comp_data.get("type", "LM741")
        opamp = Part("Amplifier_Operational", part_type, ref=comp_data["id"])
        return opamp

    def create_555(self, comp_data):
        part_type = comp_data.get("type", "NE555P")  # very safe default
        ic = Part("Timer", part_type, ref=comp_data["id"])
        return ic
