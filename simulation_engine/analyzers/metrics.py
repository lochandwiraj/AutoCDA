import numpy as np
from typing import Dict, Optional, Tuple

class CircuitAnalyzer:
    """Extract meaningful metrics from simulation results"""
    
    @staticmethod
    def find_cutoff_frequency(frequencies: list, magnitudes: list, 
                             db_drop: float = -3.0) -> Optional[float]:
        freqs = np.array(frequencies)
        mags = np.array(magnitudes)
        
        if np.max(mags) > 10:
            mags_db = 20 * np.log10(mags + 1e-12)
        else:
            mags_db = mags
        
        max_mag = np.max(mags_db)
        target_mag = max_mag + db_drop
        
        idx = np.argmin(np.abs(mags_db - target_mag))
        return float(freqs[idx])
    
    @staticmethod
    def calculate_gain(magnitudes: list, unit: str = 'db') -> float:
        mags = np.array(magnitudes)
        
        if unit.lower() == 'db':
            if np.max(mags) > 10:
                return float(20 * np.log10(np.max(mags)))
            return float(np.max(mags))
        else:
            return float(np.max(mags))
    
    @staticmethod
    def calculate_bandwidth(frequencies: list, magnitudes: list) -> Tuple[float, float]:
        freqs = np.array(frequencies)
        mags = np.array(magnitudes)
        
        mags_db = 20 * np.log10(mags + 1e-12)
        max_mag = np.max(mags_db)
        target = max_mag - 3.0
        
        crossings = np.where(np.diff(np.sign(mags_db - target)))[0]
        
        if len(crossings) >= 2:
            return (float(freqs[crossings[0]]), float(freqs[crossings[-1]]))
        elif len(crossings) == 1:
            return (float(freqs[crossings[0]]), float(freqs[-1]))
        
        return (float(freqs[0]), float(freqs[-1]))
    
    @staticmethod
    def calculate_q_factor(frequencies: list, magnitudes: list) -> float:
        freqs = np.array(frequencies)
        mags = np.array(magnitudes)
        center_freq = float(freqs[np.argmax(mags)])
        lower, upper = CircuitAnalyzer.calculate_bandwidth(frequencies, magnitudes)
        bandwidth = upper - lower
        if bandwidth > 0:
            return float(center_freq / bandwidth)
        return 0.0
    
    @staticmethod
    def detect_circuit_type(frequencies: list, magnitudes: list) -> str:
        mags = np.array(magnitudes)
        mags_db = 20 * np.log10(mags + 1e-12)
        
        n = len(mags_db)
        if n < 10:
            return 'unknown'
        
        low_freq_gain = np.mean(mags_db[:n//10])
        high_freq_gain = np.mean(mags_db[-n//10:])
        mid_freq_gain = np.mean(mags_db[n//3:2*n//3])
        
        if low_freq_gain > high_freq_gain + 6:
            return 'lowpass'
        elif high_freq_gain > low_freq_gain + 6:
            return 'highpass'
        elif mid_freq_gain > low_freq_gain + 6 and mid_freq_gain > high_freq_gain + 6:
            return 'bandpass'
        elif mid_freq_gain < low_freq_gain - 6 and mid_freq_gain < high_freq_gain - 6:
            return 'bandstop'
        
        return 'allpass'
    
    @staticmethod
    def analyze_response(frequencies: list, magnitudes: list, phases: Optional[list] = None) -> Dict:
        metrics = {
            'circuit_type': CircuitAnalyzer.detect_circuit_type(frequencies, magnitudes),
            'dc_gain_db': CircuitAnalyzer.calculate_gain(magnitudes, 'db'),
            'max_gain_db': float(20 * np.log10(np.max(magnitudes) + 1e-12)),
        }
        
        if 'pass' in metrics['circuit_type']:
            cutoff = CircuitAnalyzer.find_cutoff_frequency(frequencies, magnitudes)
            metrics['cutoff_frequency_hz'] = cutoff
            metrics['cutoff_frequency_khz'] = cutoff / 1000.0
        
        lower, upper = CircuitAnalyzer.calculate_bandwidth(frequencies, magnitudes)
        metrics['bandwidth_hz'] = upper - lower
        
        if metrics['circuit_type'] == 'bandpass':
            metrics['q_factor'] = CircuitAnalyzer.calculate_q_factor(frequencies, magnitudes)
            metrics['center_frequency_hz'] = float(frequencies[np.argmax(magnitudes)])
        
        return metrics
