class UserFriendlyErrors:
    @staticmethod
    def component_calculation_failed():
        return {
            "title": "Couldn't Calculate Component Values",
            "message": "The specifications you provided might be outside typical ranges. Try adjusting your requirements.",
            "suggestions": [
                "For filters, use cutoff frequencies between 10Hz and 100kHz",
                "For voltage dividers, ensure input voltage is higher than output",
                "Check that all values are positive numbers"
            ]
        }

    @staticmethod
    def unclear_circuit_description():
        return {
            "title": "Description Unclear",
            "message": "I couldn't identify what type of circuit you want. Try being more specific.",
            "suggestions": [
                "Start with the circuit type: 'Design a low-pass filter...'",
                "Include key specs: '...with 1kHz cutoff frequency'",
                "See examples below for reference"
            ]
        }

    @staticmethod
    def validation_failed(errors):
        return {
            "title": "Circuit Design Issues",
            "message": "The generated circuit has some problems:",
            "errors": errors,
            "suggestions": [
                "Try rephrasing your description",
                "Ensure all specifications are realistic",
                "Contact support if this persists"
            ]
        }

    @staticmethod
    def api_error():
        return {
            "title": "Service Temporarily Unavailable",
            "message": "We're having trouble processing your request right now.",
            "suggestions": [
                "Wait a moment and try again",
                "Try one of the example circuits below",
                "If this persists, please report the issue"
            ]
        }
