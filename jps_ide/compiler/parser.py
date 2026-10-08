"""
JPS Script Parser
Parses tokens into Abstract Syntax Tree (AST).
"""

from jps_ide.compiler.lexer import TokenType
from jps_ide.compiler.ast import ProgramNode, ImportNode, AssignNode, CallNode, IdentifierNode, LiteralNode
from jps_ide.compiler.errors import JPSSyntaxError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def advance(self):
        tok = self.current_token()
        self.pos += 1
        return tok

    def peek_next(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return self.tokens[-1]

    def match(self, token_type, value=None):
        tok = self.current_token()
        if tok.type == token_type:
            if value is None or tok.value == value:
                self.advance()
                return tok
        return None

    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)

    def parse_statement(self):
        tok = self.current_token()

        # Import statements: import.box or import.game
        if tok.type == TokenType.KEYWORD and tok.value in ("import.box", "import.game"):
            self.advance()
            mod_name = tok.value.split('.')[1]
            return ImportNode(mod_name, tok.line, tok.column)

        # Assignment: identifier = expression
        if tok.type == TokenType.IDENTIFIER and self.peek_next().type == TokenType.EQUALS:
            var_name = tok.value
            line, col = tok.line, tok.column
            self.advance() # ident
            self.advance() # =
            expr = self.parse_expression()
            return AssignNode(var_name, expr, line, col)

        # Standalone expression / Function call
        expr = self.parse_expression()
        return expr

    def parse_expression(self):
        tok = self.current_token()

        # Function / Method calls or simple references
        if tok.type in (TokenType.KEYWORD, TokenType.IDENTIFIER):
            callee_name = tok.value
            line, col = tok.line, tok.column
            self.advance()

            # Optional parenthesis for call e.g., run.box vs run.box() vs size.game(1000, 1000)
            if self.current_token().type == TokenType.LPAREN:
                self.advance() # (
                args = []
                if self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current_token().type == TokenType.COMMA:
                        self.advance() # ,
                        args.append(self.parse_expression())

                if self.current_token().type != TokenType.RPAREN:
                    raise JPSSyntaxError(f"Expected closing ')' after arguments", line, col)
                self.advance() # )
                return CallNode(callee_name, args, line, col)

            # Property reference / function reference call without parentheses e.g. run.box
            if '.' in callee_name or callee_name.startswith("run."):
                return CallNode(callee_name, [], line, col)

            return IdentifierNode(callee_name, line, col)

        if tok.type in (TokenType.NUMBER, TokenType.STRING):
            self.advance()
            return LiteralNode(tok.value, tok.line, tok.column)

        raise JPSSyntaxError(f"Unexpected token '{tok.value}'", tok.line, tok.column)
