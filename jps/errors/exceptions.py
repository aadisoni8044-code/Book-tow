"""JPS Script Custom Exceptions."""

class JPSError(Exception):
    """Base exception class for JPS Script errors."""
    def __init__(self, message: str, line: int = 1):
        self.message = message
        self.line = line
        super().__init__(self.formatted_message())

    def formatted_message(self) -> str:
        return f"JPS Error:\nLine {self.line}: {self.message}"


class JPSSyntaxError(JPSError):
    """Raised for syntax and parsing errors in JPS Script."""
    pass


class JPSRuntimeError(JPSError):
    """Raised for general runtime errors in JPS Script."""
    pass


class JPSNameError(JPSError):
    """Raised when an undefined identifier is accessed."""
    pass


class JPSImportError(JPSError):
    """Raised when an invalid or unknown module is imported."""
    pass
