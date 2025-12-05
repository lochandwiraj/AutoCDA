# offline_circuits.py
# Pre-generated circuit data for offline demo

CACHED_CIRCUITS = {
    "voltage_divider_9v_5v": {
        "input": "Design a voltage divider that converts 9V to 5V",
        "explanation": """I designed a voltage divider using two resistors to convert 9V to 5V.

Component Selection:
- R1: 3.9kΩ (E12 series)
- R2: 5.6kΩ (E12 series)

Calculation:
Using the voltage divider formula: Vout = Vin × R2/(R1+R2)
Vout = 9V × 5.6kΩ/(3.9kΩ + 5.6kΩ) = 5.31V

This gives us 5.31V output, which is within 6% of the target 5V - acceptable tolerance for most applications.

The resistor values were selected from the standard E12 series to ensure availability and standard sizing.""",
        "schematic_path": "/output/voltage_divider_9v_5v.kicad_sch",
        "components": [
            {"ref": "R1", "value": "3.9k", "type": "resistor"},
            {"ref": "R2", "value": "5.6k", "type": "resistor"}
        ]
    },
    
    "rc_lowpass_1khz": {
        "input": "Low-pass RC filter with 1kHz cutoff frequency",
        "explanation": """I designed a low-pass RC filter with 1kHz cutoff frequency using one resistor and one capacitor.

Component Selection:
- R1: 1.6kΩ (E12 series)
- C1: 100nF (standard value)

Calculation:
Using the cutoff frequency formula: fc = 1/(2πRC)
Solving for our target: 1000Hz = 1/(2π × R × C)

With C = 100nF, R = 1/(2π × 1000 × 100×10⁻⁹) = 1.59kΩ

Selected R = 1.6kΩ (closest E12 value), giving actual fc = 995Hz (0.5% error).

This filter will attenuate frequencies above 1kHz by -20dB/decade, providing clean low-frequency signal output.""",
        "schematic_path": "/output/rc_lowpass_1khz.kicad_sch",
        "components": [
            {"ref": "R1", "value": "1.6k", "type": "resistor"},
            {"ref": "C1", "value": "100n", "type": "capacitor"}
        ]
    },
    
    "led_current_limiter": {
        "input": "LED current limiter for 5V supply with 20mA",
        "explanation": """I designed an LED current limiting circuit for a 5V supply targeting 20mA current.

Component Selection:
- R1: 150Ω (E12 series)
- LED: Standard LED (Vf ≈ 2V)

Calculation:
Using Ohm's law with LED forward voltage:
R = (Vsupply - Vled) / Iled
R = (5V - 2V) / 0.02A = 150Ω

Selected R = 150Ω (exact E12 value), giving exactly 20mA current.

Power dissipation: P = I²R = (0.02)² × 150 = 0.06W
Using 1/4W resistor provides comfortable safety margin.

This ensures the LED operates within safe current limits and provides consistent brightness.""",
        "schematic_path": "/output/led_current_limiter.kicad_sch",
        "components": [
            {"ref": "R1", "value": "150", "type": "resistor"},
            {"ref": "D1", "value": "LED", "type": "led"}
        ]
    }
}

def get_cached_circuit(input_text):
    """
    Match user input to cached circuit
    Returns cached circuit data or None
    """
    input_lower = input_text.lower()
    
    if "voltage divider" in input_lower and "9" in input_lower and "5" in input_lower:
        return CACHED_CIRCUITS["voltage_divider_9v_5v"]
    
    if "low-pass" in input_lower or "lowpass" in input_lower:
        if "1khz" in input_lower or "1000" in input_lower:
            return CACHED_CIRCUITS["rc_lowpass_1khz"]
    
    if "led" in input_lower and "current" in input_lower:
        return CACHED_CIRCUITS["led_current_limiter"]
    
    return None
