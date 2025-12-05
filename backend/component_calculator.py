import math
from typing import Tuple


class ComponentCalculator:
    """Calculate component values based on circuit constraints."""
    
    # Standard E12 resistor values (10% tolerance)
    E12_SERIES = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    
    # Common capacitor values (simplified)
    CAP_VALUES = [1, 1.5, 2.2, 3.3, 4.7, 6.8, 10, 15, 22, 33, 47, 68, 100, 150, 220, 330, 470, 680]
    
    @staticmethod
    def calculate_rc_filter(cutoff_freq: float, filter_type: str = "lowpass") -> Tuple[str, str]:
        """
        Calculate R and C values for RC filter.
        Formula: fc = 1 / (2 * π * R * C)
        
        Args:
            cutoff_freq: Cutoff frequency in Hz
            filter_type: "lowpass" or "highpass" (topology is same, just labeled differently)
        
        Returns:
            Tuple of (resistor_value, capacitor_value) as strings with units
        """
        # Choose a standard capacitor value first, then calculate R
        # Start with a reasonable capacitor value based on frequency range
        if cutoff_freq < 100:
            # Low frequency: use larger cap (microfarads)
            C_target = 1e-6  # 1uF
        elif cutoff_freq < 1000:
            # Mid frequency: use sub-microfarad
            C_target = 100e-9  # 100nF
        elif cutoff_freq < 10000:
            # Higher frequency: use tens of nanofarads
            C_target = 10e-9  # 10nF
        else:
            # Very high frequency: use picofarads
            C_target = 1e-9  # 1nF
        
        # Calculate required resistance
        # R = 1 / (2 * π * fc * C)
        R_calculated = 1 / (2 * math.pi * cutoff_freq * C_target)
        
        # Round to nearest E12 value
        R_standard = ComponentCalculator._nearest_e12(R_calculated)
        
        # Recalculate C with standard R for better accuracy
        C_final = 1 / (2 * math.pi * cutoff_freq * R_standard)
        
        # Round capacitor to standard value
        C_standard = ComponentCalculator._nearest_capacitor(C_final)
        
        # Format values with appropriate units
        R_str = ComponentCalculator._format_resistance(R_standard)
        C_str = ComponentCalculator._format_capacitance(C_standard)
        
        return (R_str, C_str)
    
    @staticmethod
    def calculate_voltage_divider(input_voltage: float, output_voltage: float) -> Tuple[str, str]:
        """
        Calculate R1 and R2 for voltage divider.
        Formula: Vout = Vin * R2 / (R1 + R2)
        
        Args:
            input_voltage: Input voltage in V
            output_voltage: Desired output voltage in V
        
        Returns:
            Tuple of (R1_value, R2_value) as strings with units
        """
        if output_voltage >= input_voltage:
            raise ValueError("Output voltage must be less than input voltage")
        
        # Choose R2 as a reasonable value (e.g., 1k to 10k range)
        # This affects current draw: lower R = more current
        R2_target = 10000  # 10k ohms (good balance)
        
        # Calculate R1: R1 = R2 * (Vin - Vout) / Vout
        ratio = (input_voltage - output_voltage) / output_voltage
        R1_calculated = R2_target * ratio
        
        # Round to nearest E12 values
        R1_standard = ComponentCalculator._nearest_e12(R1_calculated)
        R2_standard = ComponentCalculator._nearest_e12(R2_target)
        
        # Format values
        R1_str = ComponentCalculator._format_resistance(R1_standard)
        R2_str = ComponentCalculator._format_resistance(R2_standard)
        
        return (R1_str, R2_str)
    
    @staticmethod
    def _nearest_e12(value: float) -> float:
        """Find nearest E12 series value to the given resistance."""
        if value <= 0:
            raise ValueError("Resistance must be positive")
        
        # Find the appropriate decade
        decade = 10 ** math.floor(math.log10(value))
        normalized = value / decade
        
        # Find closest E12 value
        closest = min(ComponentCalculator.E12_SERIES, key=lambda x: abs(x - normalized))
        
        return closest * decade
    
    @staticmethod
    def _nearest_capacitor(value: float) -> float:
        """Find nearest standard capacitor value."""
        if value <= 0:
            raise ValueError("Capacitance must be positive")
        
        # Find the appropriate decade
        decade = 10 ** math.floor(math.log10(value))
        normalized = value / decade
        
        # Find closest standard value
        closest_normalized = min(ComponentCalculator.CAP_VALUES, key=lambda x: abs(x - normalized))
        
        return closest_normalized * decade
    
    @staticmethod
    def _format_resistance(ohms: float) -> str:
        """Format resistance value with appropriate unit."""
        if ohms >= 1e6:
            return f"{ohms/1e6:.1f}M"
        elif ohms >= 1e3:
            return f"{ohms/1e3:.1f}k"
        else:
            return f"{ohms:.1f}"
    
    @staticmethod
    def _format_capacitance(farads: float) -> str:
        """Format capacitance value with appropriate unit."""
        if farads >= 1e-6:
            return f"{farads*1e6:.1f}u"
        elif farads >= 1e-9:
            return f"{farads*1e9:.1f}n"
        elif farads >= 1e-12:
            return f"{farads*1e12:.1f}p"
        else:
            return f"{farads:.2e}"


def test_calculator():
    """Test component calculator with various inputs."""
    calc = ComponentCalculator()
    
    print("Testing Component Calculator")
    print("=" * 60)
    
    # Test RC filters
    print("\nRC Filter Calculations:")
    print("-" * 60)
    
    test_frequencies = [100, 1000, 5000, 10000]
    for freq in test_frequencies:
        R, C = calc.calculate_rc_filter(freq)
        print(f"Cutoff: {freq} Hz → R={R}, C={C}")
        
        # Verify calculation
        R_val = parse_value(R)
        C_val = parse_value(C)
        actual_fc = 1 / (2 * math.pi * R_val * C_val)
        error_pct = abs(actual_fc - freq) / freq * 100
        print(f"  Actual fc: {actual_fc:.1f} Hz (error: {error_pct:.2f}%)")
    
    # Test voltage dividers
    print("\nVoltage Divider Calculations:")
    print("-" * 60)
    
    test_dividers = [
        (9, 5),
        (12, 3.3),
        (5, 2.5),
        (24, 12)
    ]
    
    for vin, vout in test_dividers:
        R1, R2 = calc.calculate_voltage_divider(vin, vout)
        print(f"Vin: {vin}V → Vout: {vout}V → R1={R1}, R2={R2}")
        
        # Verify calculation
        R1_val = parse_value(R1)
        R2_val = parse_value(R2)
        actual_vout = vin * R2_val / (R1_val + R2_val)
        error_pct = abs(actual_vout - vout) / vout * 100
        print(f"  Actual Vout: {actual_vout:.2f}V (error: {error_pct:.2f}%)")


def parse_value(value_str: str) -> float:
    """Parse component value string to float (e.g., '1k' -> 1000)."""
    multipliers = {
        'M': 1e6,
        'k': 1e3,
        'u': 1e-6,
        'n': 1e-9,
        'p': 1e-12
    }
    
    value_str = value_str.strip()
    
    for suffix, mult in multipliers.items():
        if value_str.endswith(suffix):
            return float(value_str[:-1]) * mult
    
    return float(value_str)


if __name__ == "__main__":
    test_calculator()
