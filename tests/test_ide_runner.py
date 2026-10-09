import os
import pytest
from PySide6.QtWidgets import QApplication
from ide.app import JPSMainWindow


def test_ide_window_creation(qtbot=None):
    app = QApplication.instance() or QApplication([])
    window = JPSMainWindow()
    assert window.windowTitle() == "JPS Script Professional IDE"
    assert window.editor is not None
    assert window.terminal is not None
    assert window.header is not None


def test_ide_runner_execution(qtbot=None):
    app = QApplication.instance() or QApplication([])
    window = JPSMainWindow()
    window.editor.setPlainText('print("IDE_TEST_OK")')

    received_lines = []
    window.runner.stdout_received.connect(lambda line: received_lines.append(line))

    window.run_current_script()
    window.runner.process.waitForFinished(3000)

    assert "IDE_TEST_OK" in received_lines
