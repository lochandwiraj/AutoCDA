from skidl import Part

class SemiconductorMapper:

    STANDARD_PARTS = {
        'diode': {
            '1N4148': 'Diode:D_DO-35_SOD27_P7.62mm_Horizontal',
            '1N4001': 'Diode:D_DO-41_SOD81_P10.16mm_Horizontal'
        },

        # Updated to match KiCad-9 symbol names
        'transistor': {
            '2N2222': ('Device', 'Q_NPN'),
            'BC547': ('Device', 'Q_NPN'),
            '2N3906': ('Device', 'Q_PNP')
        }
    }

    def create_diode(self, comp_data):
        part_num = comp_data.get("part_number", "1N4148")
        footprint = self.STANDARD_PARTS["diode"].get(part_num)

        d = Part(
            "Device",
            "D",
            ref=comp_data["id"],
            value=part_num,
            footprint=footprint
        )
        return d

    def create_transistor(self, comp_data):
        part_num = comp_data.get("part_number", "2N2222")

        # Safe fallback
        lib, part = self.STANDARD_PARTS["transistor"].get(
            part_num, 
            ("Device", "Q_NPN")
        )

        q = Part(
            lib,
            part,
            ref=comp_data["id"],
            value=part_num
        )
        return q
