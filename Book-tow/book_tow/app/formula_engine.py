"""A deliberately small, safe arithmetic formula evaluator."""

import ast
import operator
import re


class FormulaError(ValueError):
    """Raised when a formula is invalid or cannot be calculated."""


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_RANGE_PATTERN = re.compile(r"\b([A-Z]+[1-9][0-9]*):([A-Z]+[1-9][0-9]*)\b")
_CELL_PATTERN = re.compile(r"^[A-Z]+[1-9][0-9]*$")


def evaluate_formula(formula, get_cell):
    """Evaluate arithmetic and SUM formulas using get_cell(address)."""
    if not isinstance(formula, str) or not formula.startswith("="):
        raise FormulaError("A formula must begin with '='.")

    expression = formula[1:].strip()
    if not expression:
        raise FormulaError("The formula is empty.")
    if len(expression) > 4096:
        raise FormulaError("The formula is too long.")
    expression = _RANGE_PATTERN.sub(
        lambda match: 'RANGE("{}","{}")'.format(match.group(1), match.group(2)),
        expression.upper(),
    )

    try:
        tree = ast.parse(expression, mode="eval")
        return _evaluate_node(tree.body, get_cell)
    except FormulaError:
        raise
    except (ArithmeticError, RecursionError, SyntaxError, TypeError, ValueError) as error:
        raise FormulaError(str(error) or "Invalid formula.") from error


def _evaluate_node(node, get_cell):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.Name) and _CELL_PATTERN.fullmatch(node.id):
        return _numeric_value(get_cell(node.id))

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _evaluate_node(node.operand, get_cell)
        return value if isinstance(node.op, ast.UAdd) else -value

    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate_node(node.left, get_cell)
        right = _evaluate_node(node.right, get_cell)
        return _BINARY_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == "RANGE" and len(node.args) == 2:
            first = _string_argument(node.args[0])
            last = _string_argument(node.args[1])
            return [
                get_cell(address)
                for address in _expand_range(first, last)
            ]
        if node.func.id == "SUM" and not node.keywords:
            total = 0
            for argument in node.args:
                if isinstance(argument, ast.Name) and _CELL_PATTERN.fullmatch(argument.id):
                    values = [_numeric_value(get_cell(argument.id), blank_as_zero=True)]
                else:
                    values = _evaluate_node(argument, get_cell)
                if isinstance(values, list):
                    for value in values:
                        total += _numeric_value(value, blank_as_zero=True)
                else:
                    total += _numeric_value(values, blank_as_zero=True)
            return total

    raise FormulaError("Unsupported formula expression.")


def _numeric_value(value, blank_as_zero=False):
    if value is None or value == "":
        if blank_as_zero:
            return 0
        raise FormulaError("A formula references an empty cell.")
    if isinstance(value, bool):
        raise FormulaError("A formula reference is not a number.")
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return float(value) if "." in value else int(value)
        except ValueError as error:
            raise FormulaError("A formula reference is not a number.") from error
    raise FormulaError("A formula reference is not a number.")


def _string_argument(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    raise FormulaError("Invalid cell range.")


def _expand_range(first, last):
    first_row, first_column = parse_address(first)
    last_row, last_column = parse_address(last)
    if first_row > last_row or first_column > last_column:
        raise FormulaError("The SUM range must run from top-left to bottom-right.")
    if (last_row - first_row + 1) * (last_column - first_column + 1) > 100_000:
        raise FormulaError("The SUM range is too large.")
    return [
        "{}{}".format(column_name(column), row)
        for row in range(first_row, last_row + 1)
        for column in range(first_column, last_column + 1)
    ]


def parse_address(address):
    match = re.fullmatch(r"([A-Z]+)([1-9][0-9]*)", address)
    if not match:
        raise FormulaError("Invalid cell address.")
    column = 0
    for character in match.group(1):
        column = column * 26 + ord(character) - ord("A") + 1
    return int(match.group(2)), column


def column_name(number):
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result
