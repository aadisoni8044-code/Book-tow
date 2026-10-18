import pytest
from app.formula_engine import FormulaEngine, FormulaError

@pytest.fixture
def engine():
    return FormulaEngine()

def test_col_conversion(engine):
    assert FormulaEngine.col_str_to_idx("A") == 0
    assert FormulaEngine.col_str_to_idx("Z") == 25
    assert FormulaEngine.col_str_to_idx("AA") == 26
    assert FormulaEngine.col_idx_to_str(0) == "A"
    assert FormulaEngine.col_idx_to_str(25) == "Z"
    assert FormulaEngine.col_idx_to_str(26) == "AA"

def test_cell_parsing(engine):
    assert FormulaEngine.parse_cell_ref("A1") == (0, 0)
    assert FormulaEngine.parse_cell_ref("B10") == (9, 1)
    assert FormulaEngine.parse_cell_ref("Z100") == (99, 25)

def test_basic_arithmetic(engine):
    lookup = lambda r, c: None
    assert engine.evaluate("10", lookup) == 10
    assert engine.evaluate("=5 + 3", lookup) == 8
    assert engine.evaluate("=10 - 4", lookup) == 6
    assert engine.evaluate("=3 * 4", lookup) == 12
    assert engine.evaluate("=20 / 5", lookup) == 4
    assert engine.evaluate("=(2 + 3) * 4", lookup) == 20

def test_division_by_zero(engine):
    lookup = lambda r, c: None
    assert engine.evaluate("=10 / 0", lookup) == "#DIV/0!"

def test_cell_references(engine):
    grid = {
        (0, 0): "10",  # A1
        (0, 1): "20",  # B1
        (1, 0): "=A1 + B1", # A2
    }
    lookup = lambda r, c: grid.get((r, c), "")
    assert engine.evaluate("=A1", lookup) == 10
    assert engine.evaluate("=A1 + B1", lookup) == 30
    assert engine.evaluate("=A2", lookup) == 30

def test_circular_reference(engine):
    grid = {
        (0, 0): "=B1",  # A1
        (0, 1): "=A1",  # B1
    }
    lookup = lambda r, c: grid.get((r, c), "")
    assert engine.evaluate("=A1", lookup) == "#CIRCULAR!"

def test_sum_function(engine):
    grid = {
        (0, 0): "10", # A1
        (0, 1): "20", # B1
        (1, 0): "30", # A2
        (1, 1): "40", # B2
    }
    lookup = lambda r, c: grid.get((r, c), "")
    assert engine.evaluate("=SUM(A1:B2)", lookup) == 100
    assert engine.evaluate("=AVERAGE(A1:B2)", lookup) == 25
    assert engine.evaluate("=COUNT(A1:B2)", lookup) == 4
    assert engine.evaluate("=MIN(A1:B2)", lookup) == 10
    assert engine.evaluate("=MAX(A1:B2)", lookup) == 40
