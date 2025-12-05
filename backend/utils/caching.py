"""
Request caching for common circuit descriptions
"""

import hashlib
import json
from typing import Optional, Dict

# In-memory cache for demo/common requests
REQUEST_CACHE = {}

def get_cache_key(description: str) -> str:
    """Generate cache key from circuit description"""
    normalized = description.lower().strip()
    return hashlib.md5(normalized.encode()).hexdigest()

def get_cached_result(description: str) -> Optional[Dict]:
    """Retrieve cached result if available"""
    cache_key = get_cache_key(description)
    if cache_key in REQUEST_CACHE:
        print(f"[Cache Hit] {description[:50]}...")
        return REQUEST_CACHE[cache_key]
    return None

def cache_result(description: str, result: Dict):
    """Cache a circuit generation result"""
    cache_key = get_cache_key(description)
    REQUEST_CACHE[cache_key] = result
    print(f"[Cache Store] {description[:50]}...")

def clear_cache():
    """Clear all cached results"""
    global REQUEST_CACHE
    REQUEST_CACHE = {}
    print("[Cache] Cleared")

def get_cache_size() -> int:
    """Get number of cached items"""
    return len(REQUEST_CACHE)

# Pre-cache common demo circuits
DEMO_CIRCUITS = {
    "design a low-pass rc filter with 1khz cutoff frequency": {
        "circuit_type": "rc_lowpass",
        "components": [
            {"id": "R1", "type": "resistor", "value": "1k"},
            {"id": "C1", "type": "capacitor", "value": "159n"}
        ],
        "explanation": "RC low-pass filter with 1kHz cutoff. Using f_c = 1/(2πRC), with R=1kΩ and C=159nF."
    },
    "create a voltage divider that converts 9v to 5v": {
        "circuit_type": "voltage_divider",
        "components": [
            {"id": "R1", "type": "resistor", "value": "1k"},
            {"id": "R2", "type": "resistor", "value": "1.25k"}
        ],
        "explanation": "Voltage divider from 9V to 5V. Using Vout = Vin × (R2/(R1+R2))."
    }
}

def preload_demo_cache():
    """Preload common demo circuits into cache"""
    for description, result in DEMO_CIRCUITS.items():
        cache_result(description, result)
    print(f"[Cache] Preloaded {len(DEMO_CIRCUITS)} demo circuits")
