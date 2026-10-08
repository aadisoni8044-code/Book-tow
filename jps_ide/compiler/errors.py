"""
JPS Script Error System
Custom error types and formatting for JPS Script execution.
"""

class JPSError(Exception):
    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        line_str = f"Line {self.line}: " if self.line is not None else ""
        return f"JPS Error [{self.__class__.__name__}]: {line_str}{self.message}"

class JPSSyntaxError(JPSError):
    pass

class JPSNameError(JPSError):
    pass

class JPSRuntimeError(JPSError):
    pass

class JPSImportError(JPSError):
    pass

class JPSTypeError(JPSError):
    pass

def format_error(err):
    if isinstance(err, JPSError):
        return str(err)
    return f"JPS Error [RuntimeError]: {str(err)}"
