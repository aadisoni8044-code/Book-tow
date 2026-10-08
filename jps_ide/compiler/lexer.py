"""
JPS Script Lexer
Tokenizes JPS Script source code into a stream of tokens.
"""

import re
from jps_ide.compiler.errors import JPSSyntaxError

class TokenType:
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    COMMA = "COMMA"
    EQUALS = "EQUALS"
    DOT = "DOT"
    EOF = "EOF"

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, L{self.line}:C{self.column})"

KEYWORDS = {
    "import.box",
    "import.game",
    "body_2D.box",
    "size.box",
    "run.box",
    "switch.box",
    "size.game",
    "run.game",
    "print",
}

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line = 1
        self.column = 1
        self.pos = 0

    def tokenize(self):
        while self.pos < len(self.code):
            ch = self.code[self.pos]

            # Newlines
            if ch == '\n':
                self.line += 1
                self.column = 1
                self.pos += 1
                continue

            # Whitespace
            if ch.isspace():
                self.column += 1
                self.pos += 1
                continue

            # Comments (# ...)
            if ch == '#':
                while self.pos < len(self.code) and self.code[self.pos] != '\n':
                    self.pos += 1
                continue

            # Keywords with dots (import.box, import.game, body_2D.box, etc.)
            matched_kw = False
            for kw in sorted(KEYWORDS, key=len, reverse=True):
                if self.code.startswith(kw, self.pos):
                    # Ensure word boundary unless followed by punctuation or paren
                    end_pos = self.pos + len(kw)
                    if end_pos >= len(self.code) or not (self.code[end_pos].isalnum() or self.code[end_pos] == '_'):
                        self.tokens.append(Token(TokenType.KEYWORD, kw, self.line, self.column))
                        self.pos += len(kw)
                        self.column += len(kw)
                        matched_kw = True
                        break
            if matched_kw:
                continue

            # Single character symbols
            if ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            elif ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            elif ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            elif ch == '=':
                self.tokens.append(Token(TokenType.EQUALS, '=', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            elif ch == '.':
                self.tokens.append(Token(TokenType.DOT, '.', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue

            # Numbers
            if ch.isdigit():
                start_col = self.column
                num_str = ""
                while self.pos < len(self.code) and (self.code[self.pos].isdigit() or self.code[self.pos] == '.'):
                    num_str += self.code[self.pos]
                    self.pos += 1
                    self.column += 1
                val = float(num_str) if '.' in num_str else int(num_str)
                self.tokens.append(Token(TokenType.NUMBER, val, self.line, start_col))
                continue

            # Strings
            if ch in ('"', "'"):
                quote = ch
                start_col = self.column
                self.pos += 1
                self.column += 1
                str_val = ""
                while self.pos < len(self.code) and self.code[self.pos] != quote:
                    if self.code[self.pos] == '\n':
                        raise JPSSyntaxError("Unterminated string literal", self.line, start_col)
                    str_val += self.code[self.pos]
                    self.pos += 1
                    self.column += 1
                if self.pos >= len(self.code):
                    raise JPSSyntaxError("Unterminated string literal", self.line, start_col)
                self.pos += 1 # skip closing quote
                self.column += 1
                self.tokens.append(Token(TokenType.STRING, str_val, self.line, start_col))
                continue

            # Identifiers
            if ch.isalpha() or ch == '_':
                start_col = self.column
                ident = ""
                while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] in ('_', '.')):
                    # check if appending next char would form keyword
                    sub = ident + self.code[self.pos]
                    if sub in KEYWORDS and (self.pos + 1 >= len(self.code) or not (self.code[self.pos + 1].isalnum() or self.code[self.pos + 1] == '_')):
                        ident = sub
                        self.pos += 1
                        self.column += 1
                        break
                    ident += self.code[self.pos]
                    self.pos += 1
                    self.column += 1

                if ident in KEYWORDS:
                    self.tokens.append(Token(TokenType.KEYWORD, ident, self.line, start_col))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, ident, self.line, start_col))
                continue

            raise JPSSyntaxError(f"Unexpected character '{ch}'", self.line, self.column)

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
