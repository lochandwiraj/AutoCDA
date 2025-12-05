import re
import sys
import os
sys.path.append(os.path.dirname(__file__))

from error_handler import InputValidationError

MAX_INPUT_LENGTH = 500
MIN_INPUT_LENGTH = 10

FORBIDDEN_PATTERNS = [
    r'<script',
    r'javascript:',
    r'onerror=',
    r'onclick=',
]


def validate_user_input(text: str) -> str:
    """
    Validate and sanitize user input
    
    Args:
        text: Raw user input
        
    Returns:
        Sanitized text
        
    Raises:
        InputValidationError: If input is invalid
    """
    if not text or not isinstance(text, str):
        raise InputValidationError("Input must be a non-empty string")
    
    text = text.strip()
    
    # Check length
    if len(text) < MIN_INPUT_LENGTH:
        raise InputValidationError(
            f"Input too short. Please provide at least {MIN_INPUT_LENGTH} characters describing your circuit."
        )
    
    if len(text) > MAX_INPUT_LENGTH:
        raise InputValidationError(
            f"Input too long. Please keep your description under {MAX_INPUT_LENGTH} characters."
        )
    
    # Check for forbidden patterns (basic XSS prevention)
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            raise InputValidationError("Input contains forbidden characters or patterns")
    
    # Check if input contains at least some circuit-related terms
    circuit_keywords = [
        'circuit', 'filter', 'resistor', 'capacitor', 'voltage', 'current',
        'divider', 'amplifier', 'led', 'diode', 'transistor', 'design',
        'create', 'build', 'rc', 'lc', 'rl', 'low-pass', 'high-pass', 'lowpass', 'highpass'
    ]
    
    text_lower = text.lower()
    has_circuit_keyword = any(keyword in text_lower for keyword in circuit_keywords)
    
    if not has_circuit_keyword:
        raise InputValidationError(
            "Input doesn't appear to describe a circuit. Please include terms like "
            "'filter', 'resistor', 'capacitor', 'voltage divider', etc."
        )
    
    return text


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path separators and keep only basename
    filename = filename.replace('/', '').replace('\\', '').replace('..', '')
    
    # Keep only alphanumeric, dots, underscores, and hyphens
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    
    return filename
