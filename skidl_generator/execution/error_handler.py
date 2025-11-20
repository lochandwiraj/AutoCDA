from enum import Enum

class ErrorSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ExecutionError:
    
    def __init__(self, severity, message, context=None, suggestion=None):
        self.severity = severity
        self.message = message
        self.context = context or {}
        self.suggestion = suggestion
    
    def to_dict(self):
        return {
            'severity': self.severity.value,
            'message': self.message,
            'context': self.context,
            'suggestion': self.suggestion
        }

class ErrorHandler:
    
    COMMON_ERRORS = {
        'ModuleNotFoundError': 'SKiDL library not properly installed',
        'PartNotFound': 'Component not found in KiCad library',
        'NetError': 'Invalid net connection',
        'ValueError': 'Invalid component value'
    }
    
    @staticmethod
    def parse_error(error_text):
        """Extract meaningful error info from traceback"""
        for error_type, explanation in ErrorHandler.COMMON_ERRORS.items():
            if error_type in error_text:
                return ExecutionError(
                    ErrorSeverity.ERROR,
                    explanation,
                    {'raw_error': error_text},
                    ErrorHandler.get_suggestion(error_type)
                )
        
        return ExecutionError(
            ErrorSeverity.ERROR,
            "Unknown execution error",
            {'raw_error': error_text}
        )
    
    @staticmethod
    def get_suggestion(error_type):
        suggestions = {
            'PartNotFound': 'Try using a standard component like "Device:R"',
            'NetError': 'Ensure all nets are properly connected',
            'ValueError': 'Check component value format (e.g., 1k, 100n)'
        }
        return suggestions.get(error_type, 'Review the circuit description')