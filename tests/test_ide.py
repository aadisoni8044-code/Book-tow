"""
GUI / Automated IDE test suite
"""

import pytest
from PySide6.QtWidgets import QApplication
from jps_ide.ide.main_window import MainWindow

@pytest.fixture(scope="session")
def app():
    return QApplication.instance() or QApplication([])

def test_main_window_init(app):
    win = MainWindow()
    assert win.windowTitle() == "JPS Script Studio IDE"
    assert win.editor.get_code() != ""
    assert win.run_button.text() == "RUN"

def test_script_execution_flow(app):
    win = MainWindow()
    test_code = 'import.box\na = body_2D.box()\nprint("Test Output", a)\n'
    win.editor.set_code(test_code)
    win.run_script()
    win.runner_thread.wait(2000)
    app.processEvents()

    terminal_text = win.terminal.output_area.toPlainText()
    assert "Test Output" in terminal_text
    assert "[JPS Box #1 Created]" in terminal_text
