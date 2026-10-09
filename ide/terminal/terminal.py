from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtGui import QFont, QTextCursor, QColor
from PySide6.QtCore import Qt


class TerminalWidget(QWidget):
    """Integrated developer terminal widget at the bottom of the IDE."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TerminalWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Terminal Header
        header = QWidget(self)
        header.setStyleSheet("background-color: #252526; border-top: 1px solid #333333; border-bottom: 1px solid #2D2D2D;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 4, 12, 4)

        title = QLabel("TERMINAL", header)
        title.setFont(QFont("Consolas", 11, QFont.Bold))
        title.setStyleSheet("color: #CCCCCC;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.btn_clear = QPushButton("Clear Console", header)
        self.btn_clear.setFont(QFont("Segoe UI", 10))
        self.btn_clear.setCursor(Qt.PointingHandCursor)
        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #CCCCCC;
                border: 1px solid #444444;
                border-radius: 3px;
                padding: 3px 10px;
            }
            QPushButton:hover {
                background-color: #444444;
                color: #FFFFFF;
            }
        """)
        self.btn_clear.clicked.connect(self.clear_console)
        header_layout.addWidget(self.btn_clear)

        layout.addWidget(header)

        # Terminal Console Text View
        self.console = QTextEdit(self)
        self.console.setObjectName("TerminalView")
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 12))
        self.console.setLineWrapMode(QTextEdit.NoWrap)
        layout.addWidget(self.console)

    def append_stdout(self, text: str):
        self.console.setTextColor(QColor("#D4D4D4"))
        self.console.append(text)
        self._scroll_to_bottom()

    def append_stderr(self, text: str):
        self.console.setTextColor(QColor("#FF5555"))  # Red for errors
        self.console.append(text)
        self._scroll_to_bottom()

    def append_system(self, text: str):
        self.console.setTextColor(QColor("#00F0FF"))  # Electric cyan for runtime status
        self.console.append(text)
        self._scroll_to_bottom()

    def clear_console(self):
        self.console.clear()

    def _scroll_to_bottom(self):
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.console.setTextCursor(cursor)
