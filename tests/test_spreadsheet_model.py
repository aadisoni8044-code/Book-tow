import pytest
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QModelIndex
from app.spreadsheet_model import SpreadsheetModel, CellData
from app.file_manager import FileManager, FileManagerError

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_spreadsheet_model_data_set_get(qapp):
    model = SpreadsheetModel("TestSheet")
    idx = model.index(0, 0) # A1

    assert model.data(idx, Qt.DisplayRole) is None

    model.setData(idx, "100", Qt.EditRole)
    assert model.data(idx, Qt.DisplayRole) == "100"
    assert model.data(idx, Qt.EditRole) == "100"

def test_spreadsheet_model_formula_evaluation(qapp):
    model = SpreadsheetModel("TestSheet")
    model.setData(model.index(0, 0), "10", Qt.EditRole) # A1
    model.setData(model.index(0, 1), "20", Qt.EditRole) # B1
    model.setData(model.index(1, 0), "=A1 + B1", Qt.EditRole) # A2

    assert model.data(model.index(1, 0), Qt.DisplayRole) == "30"

def test_file_manager_save_and_load(tmp_path, qapp):
    file_path = str(tmp_path / "test_doc.btow")
    model1 = SpreadsheetModel("Sheet1")
    model1.setData(model1.index(0, 0), "Hello Book/Tow", Qt.EditRole)
    model1.setData(model1.index(0, 1), "42", Qt.EditRole)

    model2 = SpreadsheetModel("Sheet2")
    model2.setData(model2.index(1, 1), "=5*5", Qt.EditRole)

    # Save
    FileManager.save_file(file_path, [model1, model2])
    assert os.path.exists(file_path)

    # Load
    loaded_models = FileManager.load_file(file_path)
    assert len(loaded_models) == 2
    assert loaded_models[0].sheet_name == "Sheet1"
    assert loaded_models[0].data(loaded_models[0].index(0, 0), Qt.DisplayRole) == "Hello Book/Tow"
    assert loaded_models[1].data(loaded_models[1].index(1, 1), Qt.DisplayRole) == "25"

def test_file_manager_csv_export_import(tmp_path, qapp):
    csv_path = str(tmp_path / "data.csv")
    model = SpreadsheetModel("CSVSheet")
    model.setData(model.index(0, 0), "Item", Qt.EditRole)
    model.setData(model.index(0, 1), "Cost", Qt.EditRole)
    model.setData(model.index(1, 0), "Widget", Qt.EditRole)
    model.setData(model.index(1, 1), "50", Qt.EditRole)

    FileManager.export_csv(csv_path, model)
    assert os.path.exists(csv_path)

    new_model = SpreadsheetModel("Imported")
    FileManager.import_csv(csv_path, new_model)
    assert new_model.data(new_model.index(0, 0), Qt.DisplayRole) == "Item"
    assert new_model.data(new_model.index(1, 1), Qt.DisplayRole) == "50"
