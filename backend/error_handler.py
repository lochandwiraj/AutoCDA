from functools import wraps
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CircuitError(Exception):
    """Base exception for circuit-related errors"""
    pass


class InputValidationError(CircuitError):
    """Raised when user input is invalid"""
    pass


class NLPError(CircuitError):
    """Raised when NLP processing fails"""
    pass


class GenerationError(CircuitError):
    """Raised when circuit generation fails"""
    pass


class ValidationError(CircuitError):
    """Raised when circuit validation fails"""
    pass


def handle_errors(func):
    """Decorator for consistent error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InputValidationError as e:
            logger.warning(f"Input validation error: {str(e)}")
            raise
        except NLPError as e:
            logger.error(f"NLP processing error: {str(e)}")
            raise
        except GenerationError as e:
            logger.error(f"Circuit generation error: {str(e)}")
            raise
        except ValidationError as e:
            logger.warning(f"Circuit validation error: {str(e)}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}: {str(e)}")
            raise CircuitError(f"An unexpected error occurred: {str(e)}")
    return wrapper
