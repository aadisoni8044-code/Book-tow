import os
import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt

from .theme.styles import DARK_THEME_QSS
from .widgets.header import HeaderBar
from .editor.code_editor import JPSCodeEditor
from .terminal.terminal import TerminalWidget
from .runner.script_runner import ScriptRunner


class JPSMainWindow(QMainWindow):
    """Main window for JPS Script Professional IDE."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("JPS Script Professional IDE")
        self.resize(1100, 750)

        # Apply Dark Theme QSS
        self.setStyleSheet(DARK_THEME_QSS)

        # Central Widget & Main Layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header Bar
        self.header = HeaderBar(self)
        self.header.run_requested.connect(self.run_current_script)
        main_layout.addWidget(self.header)

        # Vertical Splitter: Code Editor (Top) + Terminal Console (Bottom)
        splitter = QSplitter(Qt.Vertical, self)

        self.editor = JPSCodeEditor(splitter)
        self.terminal = TerminalWidget(splitter)

        splitter.addWidget(self.editor)
        splitter.addWidget(self.terminal)

        # 70% editor, 30% terminal
        splitter.setSizes([520, 220])

        main_layout.addWidget(splitter)

        # Script Runner
        self.runner = ScriptRunner(self)
        self.runner.stdout_received.connect(self.terminal.append_stdout)
        self.runner.stderr_received.connect(self.terminal.append_stderr)
        self.runner.system_received.connect(self.terminal.append_system)

        # Load default sample code
        self._load_default_code()

    def _load_default_code(self):
        sample_path = os.path.join(os.path.dirname(__file__), "..", "examples", "game.jap")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
        else:
            default_script = (
                "import.game\n"
                "import.box\n\n"
                "a = size.game(1000,1000)\n"
                "b = run.game()\n"
                "c = run.box()\n"
                "d = switch.box()\n\n"
                "print(a,b,c,d)\n"
            )
            self.editor.setPlainText(default_script)

    def run_current_script(self):
        code = self.editor.toPlainText()
        self.runner.run_script(code)
