"""
Input validation and sanitization for circuit descriptions
"""

import re
from typing import Dict, Tuple, Optional


class InputValidator:
    """Validates and sanitizes user circuit descriptions"""
    
    MAX_INPUT_LENGTH = 500
    MIN_INPUT_LENGTH = 10
    
    FORBIDDEN_PATTERNS = [
        r'<script',
        r'javascript:',
        r'on\w+\s*=',  # event handlers
        r'eval\(',
        r'exec\(',
    ]
    
    AMBIGUOUS_KEYWORDS = [
        'maybe', 'possibly', 'uncertain', 'not sure',
        'approximately', 'roughly', 'around'
    ]
    
    @staticmethod
    def validate_input(user_input: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validates user input and returns (is_valid, sanitized_input, error_message)
        """
        if not user_input or not user_input.strip():
            return False, None, "Input cannot be empty"
        
        # Length validation
        if len(user_input) > InputValidator.MAX_INPUT_LENGTH:
            return False, None, f"Input too long. Maximum {InputValidator.MAX_INPUT_LENGTH} characters allowed."
        
        if len(user_input.strip()) < InputValidator.MIN_INPUT_LENGTH:
            return False, None, f"Input too short. Please provide at least {InputValidator.MIN_INPUT_LENGTH} characters."
        
        # Security validation
        for pattern in InputValidator.FORBIDDEN_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                return False, None, "Input contains forbidden characters or patterns"
        
        # Sanitize
        sanitized = user_input.strip()
        sanitized = re.sub(r'\s+', ' ', sanitized)  # normalize whitespace
        
        # Check for special characters overload
        special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s\.,\-]', sanitized)) / len(sanitized)
        if special_char_ratio > 0.3:
            return False, None, "Input contains too many special characters"
        
        return True, sanitized, None
    
    @staticmethod
    def detect_ambiguity(user_input: str) -> Tuple[bool, Optional[str]]:
        """
        Detects ambiguous language in input
        Returns (is_ambiguous, suggestion)
        """
        lower_input = user_input.lower()
        
        for keyword in InputValidator.AMBIGUOUS_KEYWORDS:
            if keyword in lower_input:
                return True, f"Your description contains ambiguous language ('{keyword}'). Please provide specific values for better results."
        
        # Check for missing critical parameters
        if 'filter' in lower_input:
            if not any(unit in lower_input for unit in ['hz', 'khz', 'mhz']):
                return True, "Filter design requires a specific cutoff frequency (e.g., '1kHz', '500Hz')"
        
        if 'divider' in lower_input:
            if not any(char.isdigit() for char in user_input):
                return True, "Voltage divider requires specific voltage values (e.g., '9V to 5V')"
        
        return False, None
    
    @staticmethod
    def extract_constraints(user_input: str) -> Dict[str, str]:
        """
        Extracts key constraints from input for better prompt engineering
        """
        constraints = {}
        
        # Extract frequency values
        freq_pattern = r'(\d+(?:\.\d+)?)\s*(hz|khz|mhz)'
        freq_match = re.search(freq_pattern, user_input.lower())
        if freq_match:
            constraints['frequency'] = freq_match.group(0)
        
        # Extract voltage values
        voltage_pattern = r'(\d+(?:\.\d+)?)\s*v'
        voltage_matches = re.findall(voltage_pattern, user_input.lower())
        if voltage_matches:
            constraints['voltages'] = voltage_matches
        
        # Extract circuit type
        circuit_types = ['filter', 'divider', 'amplifier', 'rectifier', 'led']
        for ctype in circuit_types:
            if ctype in user_input.lower():
                constraints['circuit_type'] = ctype
                break
        
        return constraints
