import pytest
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_main_window_creation(qapp):
    window = MainWindow()
    assert window.windowTitle().startswith("Book/Tow 1.1")
    assert len(window.sheets) == 1
    assert window.sheets[0].sheet_name == "Sheet1"

def test_main_window_add_sheet(qapp):
    window = MainWindow()
    window.add_new_sheet()
    assert len(window.sheets) == 2
    assert window.sheets[1].sheet_name == "Sheet2"

def test_main_window_formula_commit(qapp):
    window = MainWindow()
    model = window.current_model()
    idx = model.index(0, 0) # A1

    window.formula_input.setText("100")
    window.commit_formula_input()
    assert model.data(idx) == "100"

    window.formula_input.setText("=50*2")
    window.commit_formula_input()
    assert model.data(idx) == "100"
