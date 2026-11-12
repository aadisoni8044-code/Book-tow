from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt

class SearchBar(QWidget):
    """In-editor search bar overlay for Ctrl+F search."""

    search_requested = Signal(str, bool)  # text, forward
    closed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SearchBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        lbl = QLabel("Find:", self)
        layout.addWidget(lbl)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search code...")
        self.search_input.textChanged.connect(self._on_search_changed)
        self.search_input.returnPressed.connect(self._on_find_next)
        layout.addWidget(self.search_input)

        self.btn_next = QPushButton("Next", self)
        self.btn_next.setFixedWidth(50)
        self.btn_next.clicked.connect(self._on_find_next)
        layout.addWidget(self.btn_next)

        self.btn_prev = QPushButton("Prev", self)
        self.btn_prev.setFixedWidth(50)
        self.btn_prev.clicked.connect(self._on_find_prev)
        layout.addWidget(self.btn_prev)

        self.btn_close = QPushButton("✕", self)
        self.btn_close.setFixedWidth(26)
        self.btn_close.clicked.connect(self.hide_search)
        layout.addWidget(self.btn_close)

        self.hide()

    def show_search(self):
        self.show()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def hide_search(self):
        self.hide()
        self.closed.emit()

    def _on_search_changed(self, text: str):
        if text:
            self.search_requested.emit(text, True)

    def _on_find_next(self):
        text = self.search_input.text()
        if text:
            self.search_requested.emit(text, True)

    def _on_find_prev(self):
        text = self.search_input.text()
        if text:
            self.search_requested.emit(text, False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide_search()
        else:
            super().keyPressEvent(event)
