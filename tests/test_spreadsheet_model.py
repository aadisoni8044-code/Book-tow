"""
Unit and integration tests for SpreadsheetModel and FileManager.
"""

import os
import pytest
from PySide6.QtWidgets import QApplication
from app.spreadsheet_model import SpreadsheetModel, CellStyle
from app.file_manager import FileManager

@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_spreadsheet_model_data_entry(qapp):
    model = SpreadsheetModel(rows=10, cols=10)
    idx_a1 = model.index(0, 0)
    idx_a2 = model.index(1, 0)
    idx_a3 = model.index(2, 0)

    model.setData(idx_a1, "10")
    model.setData(idx_a2, "25")
    model.setData(idx_a3, "=SUM(A1:A2)")

    assert model.get_raw_value(0, 0) == "10"
    assert model.get_computed_value(0, 0) == 10
    assert model.get_computed_value(2, 0) == 35

def test_spreadsheet_model_undo_redo(qapp):
    model = SpreadsheetModel(rows=10, cols=10)
    idx_a1 = model.index(0, 0)

    model.setData(idx_a1, "Hello")
    assert model.get_raw_value(0, 0) == "Hello"

    model.undo()
    assert model.get_raw_value(0, 0) == ""

    model.redo()
    assert model.get_raw_value(0, 0) == "Hello"

def test_cell_style_formatting(qapp):
    model = SpreadsheetModel(rows=10, cols=10)
    style = CellStyle()
    style.bold = True
    style.number_format = "Currency"

    model.set_cell_style(0, 0, style)
    retrieved = model.get_cell_style(0, 0)

    assert retrieved.bold is True
    assert retrieved.number_format == "Currency"

def test_file_manager_btow_save_load(tmp_path, qapp):
    file_path = os.path.join(tmp_path, "test_sheet.btow")

    sheets_data = [{
        "name": "Sheet1",
        "rows": 100,
        "cols": 26,
        "cells": {
            "A1": {"raw": "100", "style": {"bold": True}},
            "B1": {"raw": "=A1*2", "style": {}}
        }
    }]

    FileManager.save_btow(file_path, sheets_data)
    assert os.path.exists(file_path)

    loaded = FileManager.load_btow(file_path)
    assert len(loaded) == 1
    assert loaded[0]["name"] == "Sheet1"
    assert loaded[0]["cells"]["A1"]["raw"] == "100"

def test_file_manager_csv_export_import(tmp_path, qapp):
    csv_path = os.path.join(tmp_path, "test.csv")
    model = SpreadsheetModel(rows=10, cols=10)

    model.setData(model.index(0, 0), "Item")
    model.setData(model.index(0, 1), "Price")
    model.setData(model.index(1, 0), "Widget")
    model.setData(model.index(1, 1), "19.99")

    FileManager.export_csv(csv_path, model)
    assert os.path.exists(csv_path)

    model_imported = SpreadsheetModel(rows=10, cols=10)
    FileManager.import_csv(csv_path, model_imported)

    assert model_imported.get_computed_value(0, 0) == "Item"
    assert model_imported.get_computed_value(0, 1) == "Price"
    assert model_imported.get_computed_value(1, 1) in (19.99, "19.99")
