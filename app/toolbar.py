"""
Toolbar Component for Book/Tow 1.1.
Contains top brand header bar and formatting controls.
"""

from PySide6.QtWidgets import (
    QWidget, QToolBar, QToolButton, QComboBox, QFontComboBox,
    QColorDialog, QHBoxLayout, QLabel, QMenu, QFrame
)
from PySide6.QtGui import QIcon, QFont, QColor, QAction
from PySide6.QtCore import Qt, Signal, QSize


class SpreadsheetToolbar(QWidget):
    # Formatting Signals
    fontFamilyChanged = Signal(str)
    fontSizeChanged = Signal(int)
    boldToggled = Signal(bool)
    italicToggled = Signal(bool)
    underlineToggled = Signal(bool)
    alignmentChanged = Signal(object)
    textColorSelected = Signal(str)
    bgColorSelected = Signal(str)
    numFormatChanged = Signal(str)
    insertFormulaRequested = Signal(str)

    # Action Signals
    newFileRequested = Signal()
    openFileRequested = Signal()
    saveFileRequested = Signal()
    saveAsFileRequested = Signal()
    undoRequested = Signal()
    redoRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.toolbar = QToolBar(self)
        self.toolbar.setIconSize(QSize(20, 20))
        layout.addWidget(self.toolbar)

        self._build_top_brand_bar()
        self.toolbar.addSeparator()
        self._build_formatting_controls()

    def _build_top_brand_bar(self):
        logo_label = QLabel(self)
        logo_pixmap = QIcon("assets/app_icon/icon.png").pixmap(24, 24)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setContentsMargins(8, 0, 6, 0)

        title_label = QLabel("Book/Tow 1.1", self)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #F28C28; padding-right: 12px;")

        self.toolbar.addWidget(logo_label)
        self.toolbar.addWidget(title_label)

        btn_new = QToolButton(self)
        btn_new.setText("New")
        btn_new.setToolTip("New Spreadsheet (Ctrl+N)")
        btn_new.clicked.connect(self.newFileRequested.emit)
        self.toolbar.addWidget(btn_new)

        btn_open = QToolButton(self)
        btn_open.setText("Open")
        btn_open.setToolTip("Open Spreadsheet (Ctrl+O)")
        btn_open.clicked.connect(self.openFileRequested.emit)
        self.toolbar.addWidget(btn_open)

        btn_save = QToolButton(self)
        btn_save.setText("Save")
        btn_save.setToolTip("Save Spreadsheet (Ctrl+S)")
        btn_save.clicked.connect(self.saveFileRequested.emit)
        self.toolbar.addWidget(btn_save)

        btn_save_as = QToolButton(self)
        btn_save_as.setText("Save As")
        btn_save_as.setToolTip("Save As (Ctrl+Shift+S)")
        btn_save_as.clicked.connect(self.saveAsFileRequested.emit)
        self.toolbar.addWidget(btn_save_as)

        self.toolbar.addSeparator()

        btn_undo = QToolButton(self)
        btn_undo.setText("↶ Undo")
        btn_undo.setToolTip("Undo (Ctrl+Z)")
        btn_undo.clicked.connect(self.undoRequested.emit)
        self.toolbar.addWidget(btn_undo)

        btn_redo = QToolButton(self)
        btn_redo.setText("↷ Redo")
        btn_redo.setToolTip("Redo (Ctrl+Y)")
        btn_redo.clicked.connect(self.redoRequested.emit)
        self.toolbar.addWidget(btn_redo)

    def _build_formatting_controls(self):
        self.combo_font = QFontComboBox(self)
        self.combo_font.setCurrentFont(QFont("Segoe UI"))
        self.combo_font.currentFontChanged.connect(lambda f: self.fontFamilyChanged.emit(f.family()))
        self.toolbar.addWidget(self.combo_font)

        self.combo_size = QComboBox(self)
        for s in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]:
            self.combo_size.addItem(str(s), s)
        self.combo_size.setCurrentText("10")
        self.combo_size.currentTextChanged.connect(lambda s: self.fontSizeChanged.emit(int(s)))
        self.toolbar.addWidget(self.combo_size)

        self.toolbar.addSeparator()

        self.btn_bold = QToolButton(self)
        self.btn_bold.setText("B")
        self.btn_bold.setStyleSheet("font-weight: bold;")
        self.btn_bold.setCheckable(True)
        self.btn_bold.toggled.connect(self.boldToggled.emit)
        self.toolbar.addWidget(self.btn_bold)

        self.btn_italic = QToolButton(self)
        self.btn_italic.setText("I")
        self.btn_italic.setStyleSheet("font-style: italic;")
        self.btn_italic.setCheckable(True)
        self.btn_italic.toggled.connect(self.italicToggled.emit)
        self.toolbar.addWidget(self.btn_italic)

        self.btn_underline = QToolButton(self)
        self.btn_underline.setText("U")
        self.btn_underline.setStyleSheet("text-decoration: underline;")
        self.btn_underline.setCheckable(True)
        self.btn_underline.toggled.connect(self.underlineToggled.emit)
        self.toolbar.addWidget(self.btn_underline)

        self.toolbar.addSeparator()

        btn_left = QToolButton(self)
        btn_left.setText("Left")
        btn_left.clicked.connect(lambda: self.alignmentChanged.emit(Qt.AlignLeft | Qt.AlignVCenter))
        self.toolbar.addWidget(btn_left)

        btn_center = QToolButton(self)
        btn_center.setText("Center")
        btn_center.clicked.connect(lambda: self.alignmentChanged.emit(Qt.AlignCenter))
        self.toolbar.addWidget(btn_center)

        btn_right = QToolButton(self)
        btn_right.setText("Right")
        btn_right.clicked.connect(lambda: self.alignmentChanged.emit(Qt.AlignRight | Qt.AlignVCenter))
        self.toolbar.addWidget(btn_right)

        self.toolbar.addSeparator()

        btn_text_color = QToolButton(self)
        btn_text_color.setText("A 🎨")
        btn_text_color.setToolTip("Text Color")
        btn_text_color.clicked.connect(self._choose_text_color)
        self.toolbar.addWidget(btn_text_color)

        btn_bg_color = QToolButton(self)
        btn_bg_color.setText("Fill 🪣")
        btn_bg_color.setToolTip("Background Fill Color")
        btn_bg_color.clicked.connect(self._choose_bg_color)
        self.toolbar.addWidget(btn_bg_color)

        self.toolbar.addSeparator()

        self.combo_format = QComboBox(self)
        self.combo_format.addItems(["General", "Number", "Currency", "Percentage", "Plain Text"])
        self.combo_format.currentTextChanged.connect(self.numFormatChanged.emit)
        self.toolbar.addWidget(self.combo_format)

        self.toolbar.addSeparator()

        btn_fx = QToolButton(self)
        btn_fx.setText("<i>f(x)</i>")
        btn_fx.setToolTip("Quick Insert Formula")

        fx_menu = QMenu(self)
        for fx in ["SUM", "AVERAGE", "COUNT", "MIN", "MAX", "IF", "ROUND", "ABS"]:
            action = fx_menu.addAction(fx)
            action.triggered.connect(lambda checked, name=fx: self.insertFormulaRequested.emit(f"={name}()"))

        btn_fx.setMenu(fx_menu)
        btn_fx.setPopupMode(QToolButton.InstantPopup)
        self.toolbar.addWidget(btn_fx)

    def _choose_text_color(self):
        color = QColorDialog.getColor(QColor("#1F2937"), self, "Select Text Color")
        if color.isValid():
            self.textColorSelected.emit(color.name())

    def _choose_bg_color(self):
        color = QColorDialog.getColor(QColor("#FFFFFF"), self, "Select Background Fill Color")
        if color.isValid():
            self.bgColorSelected.emit(color.name())

    def update_style_state(self, style):
        self.combo_font.blockSignals(True)
        self.combo_font.setCurrentFont(QFont(style.font_family))
        self.combo_font.blockSignals(False)

        self.combo_size.blockSignals(True)
        self.combo_size.setCurrentText(str(style.font_size))
        self.combo_size.blockSignals(False)

        self.btn_bold.blockSignals(True)
        self.btn_bold.setChecked(style.bold)
        self.btn_bold.blockSignals(False)

        self.btn_italic.blockSignals(True)
        self.btn_italic.setChecked(style.italic)
        self.btn_italic.blockSignals(False)

        self.btn_underline.blockSignals(True)
        self.btn_underline.setChecked(style.underline)
        self.btn_underline.blockSignals(False)

        self.combo_format.blockSignals(True)
        self.combo_format.setCurrentText(style.number_format)
        self.combo_format.blockSignals(False)
