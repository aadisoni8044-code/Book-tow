"""
JPS Script IDE Main Window
Constructs logo display, code editor, RUN button, and bottom terminal.
Executes JPS script asynchronously on background worker thread for responsiveness.
"""

import os
from PIL import Image

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSplitter, QFrame
)
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtCore import Qt, QThread, Signal, Slot

from jps_ide.ide import theme
from jps_ide.ide.editor import CodeEditor
from jps_ide.ide.terminal import TerminalWidget

from jps_ide.compiler.lexer import Lexer
from jps_ide.compiler.parser import Parser
from jps_ide.compiler.errors import JPSError, format_error
from jps_ide.compiler.runtime import Interpreter


class ScriptRunnerThread(QThread):
    """Background execution thread to prevent IDE freezing."""
    output_signal = Signal(str)
    error_signal = Signal(str)
    finished_signal = Signal()

    def __init__(self, code):
        super().__init__()
        self.code = code

    def run(self):
        try:
            lexer = Lexer(self.code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()

            interpreter = Interpreter(output_callback=self.emit_output)
            interpreter.execute(ast)
        except JPSError as e:
            self.error_signal.emit(format_error(e))
        except Exception as e:
            self.error_signal.emit(f"JPS Error [RuntimeError]: {str(e)}")
        finally:
            self.finished_signal.emit()

    def emit_output(self, msg):
        self.output_signal.emit(msg)


class MainWindow(QMainWindow):
    def __init__(self, logo_path=None):
        super().__init__()

        self.setWindowTitle("JPS Script Studio IDE")
        self.resize(1000, 750)
        self.setStyleSheet(theme.MAIN_STYLESHEET)

        self.logo_path = logo_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "jps_logo.png"
        )

        self.runner_thread = None
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # 1. Header with JPS Logo
        header_frame = QFrame()
        header_frame.setObjectName("HeaderPanel")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 5, 10, 5)

        self.logo_label = QLabel()
        self.load_logo()
        header_layout.addWidget(self.logo_label, 0, Qt.AlignCenter)

        main_layout.addWidget(header_frame)

        # 2. Main Splitter containing Code Editor and Terminal
        splitter = QSplitter(Qt.Vertical)

        # Top section: Code Editor
        self.editor = CodeEditor()
        splitter.addWidget(self.editor)

        # Middle section: RUN Button bar
        run_bar = QWidget()
        run_layout = QHBoxLayout(run_bar)
        run_layout.setContentsMargins(0, 4, 0, 4)

        self.run_button = QPushButton("RUN")
        self.run_button.setObjectName("RunButton")
        self.run_button.clicked.connect(self.run_script)
        run_layout.addWidget(self.run_button, 0, Qt.AlignCenter)

        # Bottom section: Terminal Container
        bottom_container = QWidget()
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(5)

        bottom_layout.addWidget(run_bar)

        self.terminal = TerminalWidget()
        bottom_layout.addWidget(self.terminal)

        splitter.addWidget(bottom_container)

        # Initial stretch sizes: Code editor takes majority of height
        splitter.setSizes([500, 250])

        main_layout.addWidget(splitter)

        # Load default example script into editor
        self.load_default_code()

    def load_logo(self):
        if os.path.exists(self.logo_path):
            try:
                # Load via PIL for high-fidelity scaling
                pil_img = Image.open(self.logo_path).convert("RGBA")
                pil_img.thumbnail((380, 70), Image.Resampling.LANCZOS)

                # Convert PIL image to QPixmap
                qimg = QImage(pil_img.tobytes(), pil_img.width, pil_img.height, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qimg)
                self.logo_label.setPixmap(pixmap)
                self.logo_label.setAlignment(Qt.AlignCenter)
            except Exception as e:
                self.logo_label.setText("JPS SCRIPT LOGO")
                self.logo_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #007ACC;")
        else:
            self.logo_label.setText("JPS SCRIPT")

    def load_default_code(self):
        default_code = (
            "import.game\n"
            "import.box\n\n"
            "a = size.game(1000, 1000)\n"
            "b = run.game()\n"
            "c = run.box()\n"
            "d = switch.box()\n\n"
            'print("Game Started:", a, b, c, d)\n'
        )
        self.editor.set_code(default_code)

    def run_script(self):
        if self.runner_thread and self.runner_thread.isRunning():
            return

        code = self.editor.get_code()
        self.terminal.clear_output()
        self.terminal.append_info("Executing JPS Script...")

        self.run_button.setEnabled(False)
        self.run_button.setText("RUNNING...")

        self.runner_thread = ScriptRunnerThread(code)
        self.runner_thread.output_signal.connect(self.on_script_output)
        self.runner_thread.error_signal.connect(self.on_script_error)
        self.runner_thread.finished_signal.connect(self.on_script_finished)
        self.runner_thread.start()

    @Slot(str)
    def on_script_output(self, msg):
        self.terminal.append_output(msg)

    @Slot(str)
    def on_script_error(self, err_msg):
        self.terminal.append_error(err_msg)

    @Slot()
    def on_script_finished(self):
        self.run_button.setEnabled(True)
        self.run_button.setText("RUN")
        self.terminal.append_info("Execution Finished.")
