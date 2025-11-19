from execution.error_handler import ErrorHandler, ErrorSeverity

sample_error = """
Traceback (most recent call last):
  File "circuit.py", line 10, in <module>
    r1 = Part('UnknownLib', 'R')
PartNotFound: No such library
"""

parsed = ErrorHandler.parse_error(sample_error)

print("Severity:", parsed.severity)
print("Message:", parsed.message)
print("Suggestion:", parsed.suggestion)
print("Raw:", parsed.context.get('raw_error')[:50] + "...")