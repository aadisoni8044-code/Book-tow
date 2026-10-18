"""
Unit tests for Formula Engine.
"""

import pytest
from app.formula_engine import (
    evaluate_formula, cell_name_to_coords, coords_to_cell_name, expand_range,
    ERR_DIV0, ERR_VALUE, ERR_REF, ERR_CIRCULAR, ERR_SYNTAX, ERR_NAME
)

def test_coords_conversion():
    assert cell_name_to_coords("A1") == (0, 0)
    assert cell_name_to_coords("Z100") == (99, 25)
    assert cell_name_to_coords("AA1") == (0, 26)
    assert coords_to_cell_name(0, 0) == "A1"
    assert coords_to_cell_name(99, 25) == "Z100"
    assert coords_to_cell_name(0, 26) == "AA1"

def test_range_expansion():
    assert expand_range("A1:B2") == ["A1", "B1", "A2", "B2"]
    assert expand_range("C5:C5") == ["C5"]

def test_basic_arithmetic():
    get_cell = lambda ref, v=None: 0
    assert evaluate_formula("=1+2", get_cell) == 3
    assert evaluate_formula("=10 - 4", get_cell) == 6
    assert evaluate_formula("=3 * 4", get_cell) == 12
    assert evaluate_formula("=20 / 4", get_cell) == 5
    assert evaluate_formula("=2 ^ 3", get_cell) == 8
    assert evaluate_formula("=(2 + 3) * 4", get_cell) == 20

def test_formula_errors():
    get_cell = lambda ref, v=None: 0
    assert evaluate_formula("=1/0", get_cell) == ERR_DIV0
    assert evaluate_formula("=UNKNOWNFUNC(1,2)", get_cell) == ERR_NAME
    assert evaluate_formula("=(1+2", get_cell) == ERR_SYNTAX

def test_cell_references_and_functions():
    cells = {
        "A1": 10,
        "A2": 20,
        "A3": 30,
        "B1": "=A1+A2",
        "B2": "=SUM(A1:A3)",
        "B3": "=AVERAGE(A1:A3)"
    }
    def get_cell(ref, visiting=None):
        val = cells.get(ref, 0)
        if isinstance(val, str) and val.startswith('='):
            return evaluate_formula(val, get_cell, visiting)
        return val

    assert evaluate_formula("=A1+A2", get_cell) == 30
    assert evaluate_formula("=B1*2", get_cell) == 60
    assert evaluate_formula("=SUM(A1:A3)", get_cell) == 60
    assert evaluate_formula("=AVERAGE(A1:A3)", get_cell) == 20
    assert evaluate_formula("=COUNT(A1:A3)", get_cell) == 3
    assert evaluate_formula("=MIN(A1:A3)", get_cell) == 10
    assert evaluate_formula("=MAX(A1:A3)", get_cell) == 30
