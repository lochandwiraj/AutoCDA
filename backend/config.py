"""
Application configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # API Keys
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    
    # File paths
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', './output_api')
    TEMP_DIR = os.getenv('TEMP_DIR', './temp')
    
    # Rate limiting
    MAX_REQUESTS_PER_HOUR = int(os.getenv('MAX_REQUESTS_PER_HOUR', 100))
    
    # Timeouts
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    SKIDL_EXECUTION_TIMEOUT = int(os.getenv('SKIDL_EXECUTION_TIMEOUT', 10))
    
    # Security
    MAX_INPUT_LENGTH = int(os.getenv('MAX_INPUT_LENGTH', 500))
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/autocda.log')
    
    # Feature flags
    ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'true').lower() == 'true'
    ENABLE_TELEMETRY = os.getenv('ENABLE_TELEMETRY', 'false').lower() == 'true'
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        errors = []
        
        if not Config.OPENROUTER_API_KEY:
            errors.append("OPENROUTER_API_KEY not set")
        
        if not os.path.exists(Config.OUTPUT_DIR):
            try:
                os.makedirs(Config.OUTPUT_DIR)
            except Exception as e:
                errors.append(f"Cannot create OUTPUT_DIR: {str(e)}")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
