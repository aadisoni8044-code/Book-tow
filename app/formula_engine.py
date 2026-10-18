"""
Formula Engine for Book/Tow 1.1.
Evaluates spreadsheet formulas without using eval/exec.
Supports arithmetic, cell references, cell ranges, and standard functions.
"""

import re
import math

class FormulaError(Exception):
    def __init__(self, code, message=""):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")

ERR_DIV0 = "#DIV/0!"
ERR_VALUE = "#VALUE!"
ERR_REF = "#REF!"
ERR_CIRCULAR = "#CIRCULAR!"
ERR_SYNTAX = "#SYNTAX!"
ERR_NAME = "#NAME?"


def cell_name_to_coords(cell_name):
    """
    Converts cell string like 'A1' or 'B10' to zero-indexed (row, col) tuple.
    'A1' -> (0, 0)
    'Z100' -> (99, 25)
    'AA1' -> (0, 26)
    """
    match = re.match(r'^([A-Za-z]+)([1-9][0-9]*)$', cell_name.strip())
    if not match:
        raise FormulaError(ERR_REF, f"Invalid cell coordinate '{cell_name}'")

    col_str, row_str = match.groups()
    col_str = col_str.upper()

    col = 0
    for char in col_str:
        col = col * 26 + (ord(char) - ord('A') + 1)
    col -= 1

    row = int(row_str) - 1
    return row, col


def coords_to_cell_name(row, col):
    """
    Converts zero-indexed (row, col) tuple to cell string like 'A1'.
    (0, 0) -> 'A1'
    (0, 26) -> 'AA1'
    """
    col_num = col + 1
    col_str = ""
    while col_num > 0:
        col_num, remainder = divmod(col_num - 1, 26)
        col_str = chr(ord('A') + remainder) + col_str

    return f"{col_str}{row + 1}"


def expand_range(range_str):
    """
    Expands range string like 'A1:C3' into list of cell names ['A1', 'A2', ..., 'C3'].
    """
    if ':' not in range_str:
        return [range_str.strip().upper()]

    parts = range_str.split(':')
    if len(parts) != 2:
        raise FormulaError(ERR_REF, f"Invalid range '{range_str}'")

    r1, c1 = cell_name_to_coords(parts[0])
    r2, c2 = cell_name_to_coords(parts[1])

    start_r, end_r = min(r1, r2), max(r1, r2)
    start_c, end_c = min(c1, c2), max(c1, c2)

    cells = []
    for r in range(start_r, end_r + 1):
        for c in range(start_c, end_c + 1):
            cells.append(coords_to_cell_name(r, c))
    return cells


class Token:
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    CELL = 'CELL'
    RANGE = 'RANGE'
    FUNC = 'FUNC'
    OP = 'OP'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    COMMA = 'COMMA'
    COLON = 'COLON'

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


def tokenize(expression):
    """
    Tokenizes formula string (excluding initial '=').
    """
    tokens = []
    i = 0
    length = len(expression)

    while i < length:
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch in '+-*/^':
            tokens.append(Token(Token.OP, ch))
            i += 1
            continue

        if ch == '(':
            tokens.append(Token(Token.LPAREN, '('))
            i += 1
            continue

        if ch == ')':
            tokens.append(Token(Token.RPAREN, ')'))
            i += 1
            continue

        if ch == ',':
            tokens.append(Token(Token.COMMA, ','))
            i += 1
            continue

        if ch == '"':
            # String literal
            start = i + 1
            i += 1
            while i < length and expression[i] != '"':
                i += 1
            if i >= length:
                raise FormulaError(ERR_SYNTAX, "Unterminated string literal")
            tokens.append(Token(Token.STRING, expression[start:i]))
            i += 1
            continue

        if ch.isdigit() or ch == '.':
            # Number literal
            start = i
            while i < length and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            num_str = expression[start:i]
            try:
                val = float(num_str) if '.' in num_str else int(num_str)
                tokens.append(Token(Token.NUMBER, val))
            except ValueError:
                raise FormulaError(ERR_VALUE, f"Invalid number '{num_str}'")
            continue

        if ch.isalpha() or ch == '_':
            start = i
            while i < length and (expression[i].isalnum() or expression[i] == '_'):
                i += 1
            ident = expression[start:i]

            # Check if followed by ':' -> part of range
            # Check if followed by '(' -> function call
            # Otherwise -> cell reference or error

            # Skip spaces to check next character
            peek = i
            while peek < length and expression[peek].isspace():
                peek += 1

            if peek < length and expression[peek] == '(':
                tokens.append(Token(Token.FUNC, ident.upper()))
                i = peek
            elif peek < length and expression[peek] == ':':
                # Range start, e.g., A1:C5
                # Consume range end
                range_start = ident
                peek += 1 # skip ':'
                while peek < length and expression[peek].isspace():
                    peek += 1
                end_start = peek
                while peek < length and (expression[peek].isalnum() or expression[peek] == '_'):
                    peek += 1
                range_end = expression[end_start:peek]
                tokens.append(Token(Token.RANGE, f"{range_start}:{range_end}".upper()))
                i = peek
            else:
                # Cell reference
                tokens.append(Token(Token.CELL, ident.upper()))
                i = peek
            continue

        raise FormulaError(ERR_SYNTAX, f"Unexpected character '{ch}'")

    return tokens


class Parser:
    """
    Parser and Evaluator for tokenized spreadsheet formulas.
    """
    def __init__(self, tokens, get_cell_value_fn, visiting=None):
        self.tokens = tokens
        self.pos = 0
        self.get_cell_value = get_cell_value_fn
        self.visiting = visiting or set()

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None):
        tok = self.current()
        if not tok:
            raise FormulaError(ERR_SYNTAX, "Unexpected end of formula")
        if expected_type and tok.type != expected_type:
            raise FormulaError(ERR_SYNTAX, f"Expected {expected_type}, got {tok.type}")
        self.pos += 1
        return tok

    def parse(self):
        if not self.tokens:
            return ""
        res = self.expr()
        if self.pos < len(self.tokens):
            raise FormulaError(ERR_SYNTAX, "Unexpected extra tokens in formula")
        return res

    def expr(self):
        res = self.term()
        while self.current() and self.current().type == Token.OP and self.current().value in ('+', '-'):
            op = self.consume().value
            right = self.term()
            res = self.apply_op(op, res, right)
        return res

    def term(self):
        res = self.factor()
        while self.current() and self.current().type == Token.OP and self.current().value in ('*', '/'):
            op = self.consume().value
            right = self.factor()
            res = self.apply_op(op, res, right)
        return res

    def factor(self):
        res = self.power()
        while self.current() and self.current().type == Token.OP and self.current().value == '^':
            op = self.consume().value
            right = self.power()
            res = self.apply_op(op, res, right)
        return res

    def power(self):
        tok = self.current()
        if not tok:
            raise FormulaError(ERR_SYNTAX, "Unexpected end of expression")

        # Unary + / -
        if tok.type == Token.OP and tok.value in ('+', '-'):
            op = self.consume().value
            val = self.power()
            return -val if op == '-' else val

        if tok.type == Token.NUMBER:
            self.consume()
            return tok.value

        if tok.type == Token.STRING:
            self.consume()
            return tok.value

        if tok.type == Token.CELL:
            cell_ref = self.consume().value
            if cell_ref in self.visiting:
                raise FormulaError(ERR_CIRCULAR, f"Circular reference detected at {cell_ref}")
            val = self.get_cell_value(cell_ref, self.visiting)
            return self.coerce_num(val)

        if tok.type == Token.FUNC:
            return self.func_call()

        if tok.type == Token.LPAREN:
            self.consume(Token.LPAREN)
            val = self.expr()
            self.consume(Token.RPAREN)
            return val

        raise FormulaError(ERR_SYNTAX, f"Invalid token '{tok.value}'")

    def func_call(self):
        func_tok = self.consume(Token.FUNC)
        func_name = func_tok.value
        self.consume(Token.LPAREN)

        args = []
        if self.current() and self.current().type != Token.RPAREN:
            args.append(self.arg_expr())
            while self.current() and self.current().type == Token.COMMA:
                self.consume(Token.COMMA)
                args.append(self.arg_expr())

        self.consume(Token.RPAREN)
        return self.eval_func(func_name, args)

    def arg_expr(self):
        tok = self.current()
        if tok and tok.type == Token.RANGE:
            self.consume()
            range_cells = expand_range(tok.value)
            values = []
            for cell_ref in range_cells:
                if cell_ref in self.visiting:
                    raise FormulaError(ERR_CIRCULAR, f"Circular reference at {cell_ref}")
                val = self.get_cell_value(cell_ref, self.visiting)
                if val is not None and val != "":
                    values.append(self.coerce_num(val))
            return values
        else:
            val = self.expr()
            return [val] if isinstance(val, (int, float, str)) else val

    def eval_func(self, name, args):
        # Flatten argument lists
        flat_args = []
        for arg in args:
            if isinstance(arg, list):
                flat_args.extend(arg)
            else:
                flat_args.append(arg)

        # Filter numeric args for statistical functions
        num_args = [a for a in flat_args if isinstance(a, (int, float))]

        if name == 'SUM':
            return sum(num_args) if num_args else 0
        elif name == 'AVERAGE':
            if not num_args:
                raise FormulaError(ERR_DIV0, "AVERAGE of empty set")
            return sum(num_args) / len(num_args)
        elif name == 'COUNT':
            return len(num_args)
        elif name == 'MIN':
            if not num_args:
                return 0
            return min(num_args)
        elif name == 'MAX':
            if not num_args:
                return 0
            return max(num_args)
        elif name == 'ABS':
            if len(flat_args) != 1:
                raise FormulaError(ERR_VALUE, "ABS requires 1 argument")
            return abs(self.coerce_num(flat_args[0]))
        elif name == 'ROUND':
            if len(flat_args) not in (1, 2):
                raise FormulaError(ERR_VALUE, "ROUND requires 1 or 2 arguments")
            val = self.coerce_num(flat_args[0])
            digits = int(self.coerce_num(flat_args[1])) if len(flat_args) == 2 else 0
            return round(val, digits)
        elif name == 'IF':
            if len(args) < 2 or len(args) > 3:
                raise FormulaError(ERR_VALUE, "IF requires 2 or 3 arguments")
            cond = flat_args[0] if len(flat_args) > 0 else 0
            true_val = flat_args[1] if len(flat_args) > 1 else ""
            false_val = flat_args[2] if len(flat_args) > 2 else ""
            return true_val if bool(cond) else false_val
        else:
            raise FormulaError(ERR_NAME, f"Unknown function '{name}'")

    def coerce_num(self, val):
        if val is None or val == "":
            return 0
        if isinstance(val, (int, float)):
            return val
        if isinstance(val, str):
            val_clean = val.strip()
            if not val_clean:
                return 0
            try:
                return float(val_clean) if '.' in val_clean else int(val_clean)
            except ValueError:
                raise FormulaError(ERR_VALUE, f"Cannot convert '{val}' to number")
        return 0

    def apply_op(self, op, left, right):
        left_num = self.coerce_num(left)
        right_num = self.coerce_num(right)

        if op == '+':
            return left_num + right_num
        elif op == '-':
            return left_num - right_num
        elif op == '*':
            return left_num * right_num
        elif op == '/':
            if right_num == 0:
                raise FormulaError(ERR_DIV0, "Division by zero")
            return left_num / right_num
        elif op == '^':
            return left_num ** right_num
        else:
            raise FormulaError(ERR_SYNTAX, f"Unknown operator '{op}'")


def evaluate_formula(formula_str, get_cell_value_fn, visiting=None):
    """
    Evaluates formula string like '=A1+SUM(B1:B5)'.
    """
    if not formula_str or not formula_str.startswith('='):
        return formula_str

    expr = formula_str[1:].strip()
    if not expr:
        return ""

    try:
        tokens = tokenize(expr)
        parser = Parser(tokens, get_cell_value_fn, visiting)
        res = parser.parse()
        # Format whole numbers as ints if float without decimals
        if isinstance(res, float) and res.is_integer():
            return int(res)
        return res
    except FormulaError as fe:
        return fe.code
    except Exception as e:
        return ERR_VALUE
