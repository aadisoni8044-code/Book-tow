from PySide6.QtWidgets import (
    QToolBar, QComboBox, QToolButton, QColorDialog, QMenu, QWidget, QHBoxLayout, QLabel
)
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtCore import Signal, Qt

from app.theme import PRIMARY_ORANGE, HOVER_ORANGE, LIGHT_ORANGE_BG

class MainToolbar(QToolBar):
    """
    Toolbar providing spreadsheet formatting, font control, alignment, colors, borders, and formula shortcuts.
    """
    font_changed = Signal(str)
    font_size_changed = Signal(int)
    bold_toggled = Signal(bool)
    italic_toggled = Signal(bool)
    underline_toggled = Signal(bool)
    align_changed = Signal(str)
    text_color_changed = Signal(str)
    bg_color_changed = Signal(str)
    number_format_changed = Signal(str)
    insert_formula_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__("Formatting Toolbar", parent)
        self.setMovable(False)
        self.setFloatable(False)
        self.init_ui()

    def init_ui(self):
        # Font Family
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Segoe UI", "Arial", "Calibri", "Comic Sans MS", "Courier New", "Georgia", "Times New Roman", "Verdana"])
        self.font_combo.currentTextChanged.connect(self.font_changed.emit)
        self.addWidget(self.font_combo)

        self.addSeparator()

        # Font Size
        self.size_combo = QComboBox()
        sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]
        self.size_combo.addItems([str(s) for s in sizes])
        self.size_combo.setCurrentText("10")
        self.size_combo.currentTextChanged.connect(lambda s: self.font_size_changed.emit(int(s)))
        self.addWidget(self.size_combo)

        self.addSeparator()

        # Bold
        self.bold_btn = QToolButton()
        self.bold_btn.setText("B")
        self.bold_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.bold_btn.setCheckable(True)
        self.bold_btn.setToolTip("Bold (Ctrl+B)")
        self.bold_btn.toggled.connect(self.bold_toggled.emit)
        self.addWidget(self.bold_btn)

        # Italic
        self.italic_btn = QToolButton()
        self.italic_btn.setText("I")
        font_i = QFont("Segoe UI", 10)
        font_i.setItalic(True)
        self.italic_btn.setFont(font_i)
        self.italic_btn.setCheckable(True)
        self.italic_btn.setToolTip("Italic (Ctrl+I)")
        self.italic_btn.toggled.connect(self.italic_toggled.emit)
        self.addWidget(self.italic_btn)

        # Underline
        self.underline_btn = QToolButton()
        self.underline_btn.setText("U")
        font_u = QFont("Segoe UI", 10)
        font_u.setUnderline(True)
        self.underline_btn.setFont(font_u)
        self.underline_btn.setCheckable(True)
        self.underline_btn.setToolTip("Underline (Ctrl+U)")
        self.underline_btn.toggled.connect(self.underline_toggled.emit)
        self.addWidget(self.underline_btn)

        self.addSeparator()

        # Align Left
        self.align_left_btn = QToolButton()
        self.align_left_btn.setText("Align Left")
        self.align_left_btn.setToolTip("Align Text Left")
        self.align_left_btn.clicked.connect(lambda: self.align_changed.emit("left"))
        self.addWidget(self.align_left_btn)

        # Align Center
        self.align_center_btn = QToolButton()
        self.align_center_btn.setText("Center")
        self.align_center_btn.setToolTip("Center Text")
        self.align_center_btn.clicked.connect(lambda: self.align_changed.emit("center"))
        self.addWidget(self.align_center_btn)

        # Align Right
        self.align_right_btn = QToolButton()
        self.align_right_btn.setText("Align Right")
        self.align_right_btn.setToolTip("Align Text Right")
        self.align_right_btn.clicked.connect(lambda: self.align_changed.emit("right"))
        self.addWidget(self.align_right_btn)

        self.addSeparator()

        # Text Color
        self.text_color_btn = QToolButton()
        self.text_color_btn.setText("Text Color")
        self.text_color_btn.setToolTip("Set Text Color")
        self.text_color_btn.clicked.connect(self.pick_text_color)
        self.addWidget(self.text_color_btn)

        # Cell Fill Color
        self.bg_color_btn = QToolButton()
        self.bg_color_btn.setText("Fill Color")
        self.bg_color_btn.setToolTip("Set Cell Background Color")
        self.bg_color_btn.clicked.connect(self.pick_bg_color)
        self.addWidget(self.bg_color_btn)

        self.addSeparator()

        # Number Format
        self.num_format_combo = QComboBox()
        self.num_format_combo.addItems(["General", "Number", "Currency", "Percentage"])
        self.num_format_combo.currentTextChanged.connect(self.number_format_changed.emit)
        self.addWidget(self.num_format_combo)

        self.addSeparator()

        # Formula Menu
        self.formula_btn = QToolButton()
        self.formula_btn.setText("Fx Functions")
        self.formula_btn.setPopupMode(QToolButton.InstantPopup)
        formula_menu = QMenu(self)
        for fn in ["SUM", "AVERAGE", "COUNT", "MIN", "MAX"]:
            act = QAction(f"={fn}()", self)
            act.triggered.connect(lambda checked=False, f=fn: self.insert_formula_requested.emit(f"={f}()"))
            formula_menu.addAction(act)
        self.formula_btn.setMenu(formula_menu)
        self.addWidget(self.formula_btn)

    def pick_text_color(self):
        color = QColorDialog.getColor(Qt.black, self, "Select Text Color")
        if color.isValid():
            self.text_color_changed.emit(color.name())

    def pick_bg_color(self):
        color = QColorDialog.getColor(Qt.white, self, "Select Fill Color")
        if color.isValid():
            self.bg_color_changed.emit(color.name())

    def update_states(self, fmt: dict):
        self.blockSignals(True)
        self.font_combo.setCurrentText(fmt.get("font_family", "Segoe UI"))
        self.size_combo.setCurrentText(str(fmt.get("font_size", 10)))
        self.bold_btn.setChecked(fmt.get("bold", False))
        self.italic_btn.setChecked(fmt.get("italic", False))
        self.underline_btn.setChecked(fmt.get("underline", False))
        self.num_format_combo.setCurrentText(fmt.get("number_format", "General"))
        self.blockSignals(False)
