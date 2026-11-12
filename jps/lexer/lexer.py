from typing import List
from .token import Token, TokenType
from ..errors.exceptions import JPSSyntaxError


class Lexer:
    """Tokenizer for JPS Script code."""

    KEYWORDS = {
        "import": TokenType.IMPORT,
    }

    def __init__(self, source_code: str):
        self.source = source_code
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.column = 1

    def _peek(self) -> str:
        if self.pos >= self.length:
            return ""
        return self.source[self.pos]

    def _advance(self) -> str:
        if self.pos >= self.length:
            return ""
        char = self.source[self.pos]
        self.pos += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < self.length:
            char = self._peek()

            # Skip spaces and tabs (not newlines)
            if char in " \t\r":
                self._advance()
                continue

            # Newlines
            if char == "\n":
                start_line = self.line
                start_col = self.column
                self._advance()
                tokens.append(Token(TokenType.NEWLINE, "\n", start_line, start_col))
                continue

            # Comments
            if char == "#":
                while self.pos < self.length and self._peek() != "\n":
                    self._advance()
                continue

            start_line = self.line
            start_col = self.column

            # Numbers
            if char.isdigit():
                num_str = ""
                while self.pos < self.length and (self._peek().isdigit() or self._peek() == "."):
                    if self._peek() == ".":
                        # Peek ahead to verify it's a decimal number and not dot method access
                        if self.pos + 1 < self.length and not self.source[self.pos + 1].isdigit():
                            break
                    num_str += self._advance()
                tokens.append(Token(TokenType.NUMBER, num_str, start_line, start_col))
                continue

            # Identifiers and Keywords
            if char.isalpha() or char == "_":
                ident_str = ""
                while self.pos < self.length and (self._peek().isalnum() or self._peek() == "_"):
                    ident_str += self._advance()

                token_type = self.KEYWORDS.get(ident_str, TokenType.IDENTIFIER)
                tokens.append(Token(token_type, ident_str, start_line, start_col))
                continue

            # String literals
            if char in ('"', "'"):
                quote = self._advance()
                str_val = ""
                closed = False
                while self.pos < self.length:
                    curr = self._advance()
                    if curr == quote:
                        closed = True
                        break
                    elif curr == "\n":
                        raise JPSSyntaxError("Unterminated string literal before newline", start_line)
                    else:
                        str_val += curr
                if not closed:
                    raise JPSSyntaxError("Unterminated string literal", start_line)
                tokens.append(Token(TokenType.STRING, str_val, start_line, start_col))
                continue

            # Single character tokens
            if char == ".":
                self._advance()
                tokens.append(Token(TokenType.DOT, ".", start_line, start_col))
            elif char == "=":
                self._advance()
                tokens.append(Token(TokenType.ASSIGN, "=", start_line, start_col))
            elif char == ",":
                self._advance()
                tokens.append(Token(TokenType.COMMA, ",", start_line, start_col))
            elif char == "(":
                self._advance()
                tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col))
            elif char == ")":
                self._advance()
                tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col))
            elif char == "+":
                self._advance()
                tokens.append(Token(TokenType.PLUS, "+", start_line, start_col))
            elif char == "-":
                self._advance()
                tokens.append(Token(TokenType.MINUS, "-", start_line, start_col))
            elif char == "*":
                self._advance()
                tokens.append(Token(TokenType.MUL, "*", start_line, start_col))
            elif char == "/":
                self._advance()
                tokens.append(Token(TokenType.DIV, "/", start_line, start_col))
            else:
                unknown_char = self._advance()
                raise JPSSyntaxError(f"Unexpected character '{unknown_char}'", start_line)

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
