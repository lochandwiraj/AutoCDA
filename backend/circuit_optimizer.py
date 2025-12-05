"""
Circuit optimization for standard component values.
Bonus feature: Real-world practicality and technical sophistication.
"""

import math
from typing import Tuple, Dict

class ComponentOptimizer:
    """Optimize component values to standard E12/E24 series."""
    
    # E12 series (10% tolerance)
    E12_SERIES = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    
    # E24 series (5% tolerance)
    E24_SERIES = [
        1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
        3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
    ]
    
    def __init__(self, use_e24: bool = False):
        self.series = self.E24_SERIES if use_e24 else self.E12_SERIES
    
    def find_nearest_standard_value(self, target: float, component_type: str = "resistor") -> Tuple[float, str]:
        """Find nearest standard component value."""
        if target <= 0:
            return target, "Invalid value"
        
        # Determine magnitude
        magnitude = 10 ** math.floor(math.log10(target))
        normalized = target / magnitude
        
        # Find closest standard value
        closest = min(self.series, key=lambda x: abs(x - normalized))
        standard_value = closest * magnitude
        
        # Format with appropriate suffix
        formatted = self._format_value(standard_value, component_type)
        
        return standard_value, formatted
    
    def _format_value(self, value: float, component_type: str) -> str:
        """Format value with appropriate suffix (k, M, µ, n, p)."""
        if component_type == "resistor":
            if value >= 1e6:
                return f"{value/1e6:.1f}M"
            elif value >= 1e3:
                return f"{value/1e3:.1f}k"
            else:
                return f"{value:.1f}Ω"
        
        elif component_type == "capacitor":
            if value >= 1e-6:
                return f"{value*1e6:.1f}µF"
            elif value >= 1e-9:
                return f"{value*1e9:.1f}nF"
            elif value >= 1e-12:
                return f"{value*1e12:.1f}pF"
            else:
                return f"{value:.2e}F"
        
        return f"{value:.2e}"
    
    def optimize_rc_pair(self, target_freq: float, preferred_r_range: Tuple[float, float] = (1e3, 100e3)) -> Dict:
        """Optimize R and C values for target frequency."""
        # Target: f = 1/(2π*R*C)
        # Prefer resistor in reasonable range (1k - 100k)
        
        best_error = float('inf')
        best_r = None
        best_c = None
        
        # Try different resistor values in preferred range
        for r_base in self.series:
            for r_mult in [1e3, 10e3, 100e3]:  # 1k, 10k, 100k
                r = r_base * r_mult
                if preferred_r_range[0] <= r <= preferred_r_range[1]:
                    # Calculate required C
                    c_calc = 1 / (2 * math.pi * r * target_freq)
                    
                    # Find standard C value
                    c_standard, c_formatted = self.find_nearest_standard_value(c_calc, "capacitor")
                    
                    # Calculate actual frequency
                    f_actual = 1 / (2 * math.pi * r * c_standard)
                    error = abs(f_actual - target_freq) / target_freq
                    
                    if error < best_error:
                        best_error = error
                        best_r = r
                        best_c = c_standard
        
        r_standard, r_formatted = self.find_nearest_standard_value(best_r, "resistor")
        c_standard, c_formatted = self.find_nearest_standard_value(best_c, "capacitor")
        
        actual_freq = 1 / (2 * math.pi * r_standard * c_standard)
        
        return {
            "resistor": {
                "value": r_standard,
                "formatted": r_formatted,
                "calculated_value": best_r
            },
            "capacitor": {
                "value": c_standard,
                "formatted": c_formatted,
                "calculated_value": best_c
            },
            "actual_frequency": actual_freq,
            "target_frequency": target_freq,
            "error_percent": abs(actual_freq - target_freq) / target_freq * 100,
            "reasoning": f"Selected standard E12 values. Actual frequency: {actual_freq:.1f} Hz (error: {abs(actual_freq - target_freq) / target_freq * 100:.2f}%)"
        }

# Global optimizer instance
optimizer = ComponentOptimizer(use_e24=False)
