from skidl import *
import math

def find_pin(part, names):
    """Find the first pin that matches any name in names."""
    for p in part.pins:
        if p.name in names:
            return p
    raise ValueError(f"No pin found for: {names}")

class CircuitTemplates:

    @staticmethod
    def rc_lowpass_filter(cutoff_freq_hz, impedance=1000):
        R = impedance
        C = 1 / (2 * math.pi * cutoff_freq_hz * R)

        r1 = Part('Device', 'R', value=f'{R}', ref='R1')
        c1 = Part('Device', 'C', value=f'{C*1e9:.1f}n', ref='C1')

        vin = Net('VIN')
        vout = Net('VOUT')
        gnd = Net('GND')

        vin += r1[1]
        r1[2] += vout, c1[1]
        c1[2] += gnd

        return {'components':[r1,c1],
                'nets':[vin,vout,gnd],
                'params':{'R':R,'C':C}}

    @staticmethod
    def voltage_divider(vin_voltage, vout_voltage, current_ma=1):
        r_total = (vin_voltage/current_ma) * 1000
        r2 = (vout_voltage/vin_voltage) * r_total
        r1 = r_total - r2

        r1p = Part('Device','R', value=f'{r1:.0f}', ref='R1')
        r2p = Part('Device','R', value=f'{r2:.0f}', ref='R2')

        vin = Net('VIN')
        vout = Net('VOUT')
        gnd = Net('GND')

        vin += r1p[1]
        r1p[2] += vout, r2p[1]
        r2p[2] += gnd

        return {'components':[r1p,r2p],
                'nets':[vin,vout,gnd],
                'params':{'R1':r1,'R2':r2}}

    @staticmethod
    def noninverting_opamp(gain, input_impedance=10000):
        r_in = input_impedance
        r_f = r_in * (gain - 1)

        u1 = Part('Amplifier_Operational','LM741', ref='U1')
        rf = Part('Device','R', value=f'{r_f:.0f}', ref='RF')
        rin = Part('Device','R', value=f'{r_in:.0f}', ref='RIN')

        vin = Net('VIN')
        vout = Net('VOUT')
        gnd = Net('GND')

        # Use extracted pin names:
        pin_in_plus  = find_pin(u1, ['+'])
        pin_in_minus = find_pin(u1, ['-'])
        pin_out      = find_pin(u1, ['~'])

        vin += pin_in_plus
        pin_in_minus += rin[1]
        rin[2] += gnd

        pin_out += vout, rf[1]
        rf[2] += pin_in_minus

        return {'components':[u1,rf,rin],
                'nets':[vin,vout,gnd],
                'params':{'gain':gain,'Rf':r_f,'Rin':r_in}}