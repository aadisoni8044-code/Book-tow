from typing import List, Optional
from ..lexer.token import Token, TokenType
from ..ast.nodes import (
    ASTNode, ProgramNode, ImportNode, AssignNode, CallNode,
    MemberAccessNode, LiteralNode, VariableNode, BinaryOpNode
)
from ..errors.exceptions import JPSSyntaxError


class Parser:
    """Parser for JPS Script tokens to AST."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF token

    def _advance(self) -> Token:
        token = self._peek()
        if self.pos < len(self.tokens):
            self.pos += 1
        return token

    def _match(self, token_type: TokenType) -> bool:
        if self._peek().type == token_type:
            self._advance()
            return True
        return False

    def _expect(self, token_type: TokenType, error_msg: str) -> Token:
        token = self._peek()
        if token.type != token_type:
            raise JPSSyntaxError(f"{error_msg} (got '{token.value}')", token.line)
        return self._advance()

    def parse(self) -> ProgramNode:
        statements: List[ASTNode] = []

        while self._peek().type != TokenType.EOF:
            # Skip empty lines
            if self._peek().type == TokenType.NEWLINE:
                self._advance()
                continue

            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)

            # Consume optional newline after statement
            if self._peek().type == TokenType.NEWLINE:
                self._advance()

        return ProgramNode(statements, line=1)

    def _parse_statement(self) -> ASTNode:
        tok = self._peek()

        # Import statement: import.box or import.game
        if tok.type == TokenType.IMPORT:
            line = tok.line
            self._advance()
            self._expect(TokenType.DOT, "Expected '.' after 'import'")
            module_tok = self._expect(TokenType.IDENTIFIER, "Expected module name after 'import.'")
            return ImportNode(module_tok.value, line=line)

        # Assignment or standalone function call / member expression
        if tok.type == TokenType.IDENTIFIER:
            # Peek ahead to see if it's an assignment: `var = expr`
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.ASSIGN:
                var_name = tok.value
                line = tok.line
                self._advance()  # consume identifier
                self._advance()  # consume '='
                val_node = self._parse_expression()
                return AssignNode(var_name, val_node, line=line)

        # Expression statement (e.g. print(...), body_2D.box(), etc.)
        expr = self._parse_expression()
        return expr

    def _parse_expression(self) -> ASTNode:
        return self._parse_additive()

    def _parse_additive(self) -> ASTNode:
        left = self._parse_multiplicative()

        while self._peek().type in (TokenType.PLUS, TokenType.MINUS):
            op_tok = self._advance()
            right = self._parse_multiplicative()
            left = BinaryOpNode(left, op_tok.value, right, line=op_tok.line)

        return left

    def _parse_multiplicative(self) -> ASTNode:
        left = self._parse_primary()

        while self._peek().type in (TokenType.MUL, TokenType.DIV):
            op_tok = self._advance()
            right = self._parse_primary()
            left = BinaryOpNode(left, op_tok.value, right, line=op_tok.line)

        return left

    def _parse_primary(self) -> ASTNode:
        tok = self._peek()

        # Literals
        if tok.type == TokenType.NUMBER:
            self._advance()
            val = float(tok.value) if "." in tok.value else int(tok.value)
            return LiteralNode(val, line=tok.line)

        if tok.type == TokenType.STRING:
            self._advance()
            return LiteralNode(tok.value, line=tok.line)

        # Parenthesized expression
        if tok.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        # Identifiers (variable, function call, dotted member call)
        if tok.type == TokenType.IDENTIFIER:
            name_parts = [tok.value]
            line = tok.line
            self._advance()

            # Handle dotted identifiers e.g. body_2D.box, size.box, run.box, switch.box, size.game, run.game
            while self._peek().type == TokenType.DOT:
                self._advance()  # consume '.'
                member_tok = self._expect(TokenType.IDENTIFIER, "Expected member name after '.'")
                name_parts.append(member_tok.value)

            full_name = ".".join(name_parts)

            # Check for function call with arguments: `func(...)`
            if self._peek().type == TokenType.LPAREN:
                self._advance()  # consume '('
                args = []
                if self._peek().type != TokenType.RPAREN:
                    args.append(self._parse_expression())
                    while self._peek().type == TokenType.COMMA:
                        self._advance()  # consume ','
                        args.append(self._parse_expression())
                self._expect(TokenType.RPAREN, f"Expected ')' after arguments for '{full_name}'")
                return CallNode(full_name, args, line=line)

            # If dotted name without parens e.g. `run.box` or `switch.box`
            if len(name_parts) > 1:
                return MemberAccessNode(name_parts[0], ".".join(name_parts[1:]), line=line)

            # Simple variable
            return VariableNode(full_name, line=line)

        raise JPSSyntaxError(f"Unexpected token '{tok.value}'", tok.line)
