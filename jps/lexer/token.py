from enum import Enum, auto

class TokenType(Enum):
    # Keywords / Commands
    IMPORT = auto()

    # Identifiers & Literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # Symbols & Operators
    DOT = auto()
    ASSIGN = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()

    NEWLINE = auto()
    EOF = auto()


class Token:
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, Line {self.line}:{self.column})"
