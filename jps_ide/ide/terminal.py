"""
JPS Terminal Widget
Console output pane for execution logs and errors.
"""

from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QColor, QTextCursor, QFont
from PySide6.QtCore import Qt

from jps_ide.ide import theme

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Terminal Header Bar
        header = QWidget()
        header.setStyleSheet(f"background-color: {theme.BG_PANEL}; border-bottom: 1px solid {theme.BORDER_COLOR};")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 4, 10, 4)

        title = QLabel("JPS Script Terminal")
        title.setStyleSheet(f"color: {theme.TEXT_PRIMARY}; font-weight: bold; font-size: 12px;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        clear_btn = QPushButton("Clear Output")
        clear_btn.setObjectName("ClearButton")
        clear_btn.clicked.connect(self.clear_output)
        header_layout.addWidget(clear_btn)

        layout.addWidget(header)

        # Output text area
        self.output_area = QTextEdit()
        self.output_area.setObjectName("Terminal")
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Consolas", 11))
        layout.addWidget(self.output_area)

    def append_output(self, text, color=theme.TEXT_PRIMARY):
        self.output_area.setTextColor(QColor(color))
        self.output_area.append(f"> {text}")
        self.output_area.moveCursor(QTextCursor.End)

    def append_info(self, text):
        self.append_output(text, color=theme.ACCENT_HOVER)

    def append_error(self, text):
        self.append_output(text, color=theme.ERROR_COLOR)

    def append_success(self, text):
        self.append_output(text, color=theme.SUCCESS_COLOR)

    def clear_output(self):
        self.output_area.clear()
