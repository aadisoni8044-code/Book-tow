import re
import ast
import operator
from typing import Any, Callable, Dict, List, Set, Union, Tuple

class FormulaError(Exception):
    """Custom exception for spreadsheet formula errors."""
    def __init__(self, message: str, code: str = "#ERROR!"):
        super().__init__(message)
        self.code = code

class FormulaEngine:
    """
    Evaluates formulas without `eval` or `exec`.
    Supports arithmetic, cell references, ranges, and functions (SUM, AVERAGE, COUNT, MIN, MAX).
    """

    CELL_REF_REGEX = re.compile(r"^[A-Za-z]+[1-9][0-9]*$")
    RANGE_REF_REGEX = re.compile(r"([A-Za-z]+[1-9][0-9]*):([A-Za-z]+[1-9][0-9]*)")

    def __init__(self):
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

    @staticmethod
    def col_str_to_idx(col_str: str) -> int:
        """Converts column letter (e.g. 'A', 'Z', 'AA') to 0-indexed column integer."""
        col_str = col_str.upper()
        idx = 0
        for char in col_str:
            idx = idx * 26 + (ord(char) - ord('A') + 1)
        return idx - 1

    @staticmethod
    def col_idx_to_str(idx: int) -> str:
        """Converts 0-indexed column integer to column letter string."""
        col_str = ""
        idx += 1
        while idx > 0:
            idx, remainder = divmod(idx - 1, 26)
            col_str = chr(65 + remainder) + col_str
        return col_str

    @classmethod
    def parse_cell_ref(cls, cell_ref: str) -> Tuple[int, int]:
        """Parses cell string (e.g. 'B3') into (row_idx, col_idx). Returns 0-indexed coordinates."""
        match = re.match(r"^([A-Za-z]+)([1-9][0-9]*)$", cell_ref.strip())
        if not match:
            raise FormulaError(f"Invalid cell reference: {cell_ref}", "#REF!")
        col_str, row_str = match.groups()
        row_idx = int(row_str) - 1
        col_idx = cls.col_str_to_idx(col_str)
        return row_idx, col_idx

    @classmethod
    def expand_range(cls, start_cell: str, end_cell: str) -> List[Tuple[int, int]]:
        """Expands range reference (e.g., 'A1', 'B3') into list of (row_idx, col_idx) tuples."""
        r1, c1 = cls.parse_cell_ref(start_cell)
        r2, c2 = cls.parse_cell_ref(end_cell)

        start_row, end_row = min(r1, r2), max(r1, r2)
        start_col, end_col = min(c1, c2), max(c1, c2)

        coords = []
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                coords.append((r, c))
        return coords

    def preprocess_formula(self, expr: str) -> str:
        """
        Preprocesses formula string so ranges like A1:B2 are converted to RANGE("A1", "B2").
        """
        def replace_range(match):
            start, end = match.group(1), match.group(2)
            return f'RANGE("{start}", "{end}")'

        return self.RANGE_REF_REGEX.sub(replace_range, expr)

    def extract_references(self, formula_str: str) -> Set[str]:
        """
        Extracts all cell and range references from a formula string.
        """
        if not formula_str.startswith("="):
            return set()

        content = formula_str[1:].strip()
        refs = set()

        # Find ranges
        ranges = self.RANGE_REF_REGEX.findall(content)
        for r_start, r_end in ranges:
            for r, c in self.expand_range(r_start, r_end):
                refs.add(f"{self.col_idx_to_str(c)}{r + 1}")

        # Find individual cell references
        tokens = re.findall(r"\b[A-Za-z]+[1-9][0-9]*\b", content)
        for token in tokens:
            token_upper = token.upper()
            if self.CELL_REF_REGEX.match(token_upper):
                refs.add(token_upper)

        return refs

    def evaluate(self, formula_str: str, get_cell_value_fn: Callable[[int, int], Any], visited_cells: Set[Tuple[int, int]] = None) -> Any:
        """
        Evaluates a formula string given a callback `get_cell_value_fn(row_idx, col_idx)`.
        `visited_cells` tracks current evaluation stack to prevent circular references.
        """
        if visited_cells is None:
            visited_cells = set()

        if not str(formula_str).startswith("="):
            val_str = str(formula_str).strip()
            if not val_str:
                return ""
            try:
                if "." in val_str:
                    return float(val_str)
                return int(val_str)
            except ValueError:
                return val_str

        expr = formula_str[1:].strip()
        if not expr:
            return ""

        expr_prep = self.preprocess_formula(expr)

        try:
            parsed = ast.parse(expr_prep, mode='eval')
            return self._eval_ast_node(parsed.body, get_cell_value_fn, visited_cells)
        except SyntaxError:
            return "#SYNTAX!"
        except FormulaError as fe:
            return fe.code
        except ZeroDivisionError:
            return "#DIV/0!"
        except Exception:
            return "#ERROR!"

    def _eval_ast_node(self, node: ast.AST, get_cell_value_fn: Callable[[int, int], Any], visited: Set[Tuple[int, int]]) -> Any:
        if isinstance(node, ast.Constant):
            return node.value

        elif isinstance(node, ast.Name):
            var_name = node.id.upper()
            if self.CELL_REF_REGEX.match(var_name):
                r, c = self.parse_cell_ref(var_name)
                if (r, c) in visited:
                    raise FormulaError("Circular reference detected", "#CIRCULAR!")

                cell_val = get_cell_value_fn(r, c)
                if isinstance(cell_val, str) and cell_val.startswith("="):
                    new_visited = visited | {(r, c)}
                    cell_val = self.evaluate(cell_val, get_cell_value_fn, new_visited)

                if isinstance(cell_val, str) and cell_val.startswith("#"):
                    raise FormulaError(f"Error in cell reference: {cell_val}", cell_val)

                return self._to_number(cell_val)
            else:
                raise FormulaError(f"Unknown symbol: {var_name}", "#NAME?")

        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self.operators:
                operand = self._eval_ast_node(node.operand, get_cell_value_fn, visited)
                return self.operators[op_type](self._to_number(operand))
            raise FormulaError("Unsupported unary operation", "#ERROR!")

        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self.operators:
                left = self._to_number(self._eval_ast_node(node.left, get_cell_value_fn, visited))
                right = self._to_number(self._eval_ast_node(node.right, get_cell_value_fn, visited))
                return self.operators[op_type](left, right)
            raise FormulaError("Unsupported binary operation", "#ERROR!")

        elif isinstance(node, ast.Call):
            func_name = node.func.id.upper() if isinstance(node.func, ast.Name) else ""

            if func_name == "RANGE":
                # Returns list of numeric values in range
                if len(node.args) != 2 or not all(isinstance(a, ast.Constant) for a in node.args):
                    raise FormulaError("Invalid RANGE arguments", "#REF!")
                start_ref = node.args[0].value
                end_ref = node.args[1].value
                coords = self.expand_range(start_ref, end_ref)
                vals = []
                for r, c in coords:
                    if (r, c) in visited:
                        raise FormulaError("Circular reference", "#CIRCULAR!")
                    val = get_cell_value_fn(r, c)
                    if isinstance(val, str) and val.startswith("="):
                        val = self.evaluate(val, get_cell_value_fn, visited | {(r, c)})
                    if isinstance(val, str) and val.startswith("#"):
                        raise FormulaError(f"Error in cell reference: {val}", val)
                    num = self._to_number_or_none(val)
                    if num is not None:
                        vals.append(num)
                return vals

            args_values = []
            for arg in node.args:
                val = self._eval_ast_node(arg, get_cell_value_fn, visited)
                if isinstance(val, list):
                    args_values.extend(val)
                else:
                    num = self._to_number_or_none(val)
                    if num is not None:
                        args_values.append(num)

            return self._exec_function(func_name, args_values)

        raise FormulaError("Unsupported expression syntax", "#ERROR!")

    def _exec_function(self, func_name: str, values: List[Union[int, float]]) -> Union[int, float]:
        if func_name == "SUM":
            return sum(values) if values else 0
        elif func_name == "AVERAGE":
            return sum(values) / len(values) if values else 0
        elif func_name == "COUNT":
            return len(values)
        elif func_name == "MIN":
            return min(values) if values else 0
        elif func_name == "MAX":
            return max(values) if values else 0
        else:
            raise FormulaError(f"Unknown function: {func_name}", "#NAME?")

    def _to_number(self, val: Any) -> Union[int, float]:
        if val is None or val == "":
            return 0
        if isinstance(val, (int, float)):
            return val
        try:
            val_str = str(val).strip()
            if "." in val_str:
                return float(val_str)
            return int(val_str)
        except ValueError:
            raise FormulaError(f"Cannot convert '{val}' to number", "#VALUE!")

    def _to_number_or_none(self, val: Any) -> Union[int, float, None]:
        if val is None or val == "":
            return None
        if isinstance(val, (int, float)):
            return val
        try:
            val_str = str(val).strip()
            if "." in val_str:
                return float(val_str)
            return int(val_str)
        except ValueError:
            return None
