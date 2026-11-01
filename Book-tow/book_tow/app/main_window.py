"""Main Book/Tow window and spreadsheet interactions."""

import copy
import os
import time
import uuid

from book_tow.app.error_logging import log_file_operation_error
from PySide6.QtCore import QSettings, QSize, Qt, QThreadPool, QTimer, Slot
from PySide6.QtGui import (
    QAction, QActionGroup, QColor, QFont, QIcon, QKeySequence, QPainter,
    QPainterPath, QPen, QPixmap, QUndoStack,
)
from PySide6.QtWidgets import (
    QApplication, QColorDialog, QComboBox, QFileDialog, QFontComboBox,
    QHBoxLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMenu, QMessageBox,
    QPushButton, QSpinBox, QTabBar, QStatusBar, QTableView, QToolBar,
    QToolButton, QVBoxLayout, QWidget,
)

from book_tow import __version__
from book_tow.app.autosave import AutoSaveTask
from book_tow.app.file_manager import (
    LEGACY_PROJECT_EXTENSION, PROJECT_EXTENSION, ensure_project_extension,
    load_document, save_document,
)
from book_tow.app.formula_engine import FormulaError
from book_tow.app.recovery import (
    discard_recovery, document_fingerprint, file_fingerprint,
    project_id_for_path, recovery_candidates, recovery_directory,
)
from book_tow.app.spreadsheet_document import SpreadsheetDocument
from book_tow.app.spreadsheet_model import (
    SpreadsheetDelegate, SpreadsheetModel, cell_address,
)
from book_tow.app.theme import (
    ORANGE, apply_theme, application_icon, load_saved_theme,
    save_theme_preference,
)


COLOR_PALETTE = (
    "#000000", "#434343", "#666666", "#999999", "#B7B7B7", "#D9D9D9",
    "#F3F3F3", "#FFFFFF", "#F4CCCC", "#FCE5CD", "#FFF2CC", "#D9EAD3",
    "#D0E0E3", "#C9DAF8", "#CFE2F3", "#D9D2E9", "#EAD1DC", "#EA9999",
    "#F9CB9C", "#FFE599", "#B6D7A8", "#A2C4C9", "#A4C2F4", "#9FC5E8",
    "#B4A7D6", "#D5A6BD", "#E06666", "#F6B26B", "#FFD966", "#93C47D",
    "#76A5AF", "#6D9EEB", "#6FA8DC", "#8E7CC3", "#C27BA0", "#CC0000",
    "#E69138", "#F1C232", "#6AA84F", "#45818E", "#3C78D8", "#3D85C6",
    "#674EA7", "#A64D79", ORANGE,
)


def _color_swatch(color_value):
    pixmap = QPixmap(20, 16)
    pixmap.fill(QColor("transparent"))
    painter = QPainter(pixmap)
    painter.setPen(QPen(QColor("#A7A29B"), 1))
    painter.setBrush(QColor(color_value))
    painter.drawRect(1, 1, 17, 12)
    painter.end()
    return QIcon(pixmap)


def _toolbar_icon(name, theme, swatch=None):
    foreground = QColor("#FFD0A0" if theme == "dark" else "#68411F")
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(foreground, 1.8)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    def path(points, closed=False):
        shape = QPainterPath()
        shape.moveTo(*points[0])
        for point in points[1:]:
            shape.lineTo(*point)
        if closed:
            shape.closeSubpath()
        painter.drawPath(shape)

    def line(x1, y1, x2, y2):
        painter.drawLine(x1, y1, x2, y2)

    if name in {"new", "open", "save", "copy", "paste", "add_sheet"}:
        if name in {"new", "add_sheet"}:
            path([(6, 3), (13, 3), (17, 7), (17, 20), (6, 20), (6, 3)])
            line(13, 3, 13, 7)
            line(13, 7, 17, 7)
            if name == "new":
                line(8, 11, 15, 11)
                line(8, 14, 15, 14)
                line(8, 17, 15, 17)
            else:
                line(11.5, 11, 11.5, 17)
                line(8.5, 14, 14.5, 14)
        elif name == "open":
            path([(3, 7), (9, 7), (11, 9), (21, 9), (19, 19), (4, 19), (3, 7)])
            line(3, 7, 4, 5)
            line(4, 5, 10, 5)
            line(10, 5, 12, 7)
        elif name == "save":
            path([(4, 3), (17, 3), (20, 6), (20, 20), (4, 20), (4, 3)])
            painter.drawRect(8, 4, 8, 5)
            painter.drawRect(8, 13, 8, 7)
        elif name == "copy":
            painter.drawRoundedRect(8, 4, 12, 15, 1, 1)
            path([(5, 8), (4, 8), (4, 21), (16, 21)])
        else:
            painter.drawRoundedRect(5, 6, 14, 15, 1, 1)
            painter.drawRoundedRect(9, 3, 6, 5, 1, 1)
            line(8, 12, 16, 12)
            line(8, 16, 16, 16)
    elif name in {"undo", "redo"}:
        if name == "undo":
            path([(9, 6), (4, 10), (9, 14)])
            path([(5, 10), (12, 10), (16, 12), (18, 16)])
        else:
            path([(15, 6), (20, 10), (15, 14)])
            path([(19, 10), (12, 10), (8, 12), (6, 16)])
    elif name == "bold":
        painter.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "B")
    elif name == "italic":
        font = QFont("Segoe UI", 15)
        font.setItalic(True)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "I")
    elif name == "underline":
        painter.setFont(QFont("Segoe UI", 15))
        painter.drawText(pixmap.rect().adjusted(0, -2, 0, -2),
                         Qt.AlignmentFlag.AlignCenter, "U")
        line(7, 20, 17, 20)
    elif name in {"align_left", "align_center", "align_right"}:
        lengths = (14, 10, 14, 8)
        for index, length in enumerate(lengths):
            y = 5 + index * 4
            x = 5 if name != "align_right" else 19 - length
            if name == "align_center":
                x = round(12 - length / 2)
            line(x, y, x + length, y)
    elif name == "fill":
        path([(7, 4), (17, 14), (12, 19), (4, 11), (7, 4)])
        line(9, 6, 6, 9)
        painter.setPen(QPen(QColor(swatch or "#F1C232"), 3,
                            Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        line(6, 21, 18, 21)
    elif name == "font_color":
        painter.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        painter.drawText(pixmap.rect().adjusted(0, -3, 0, 1),
                         Qt.AlignmentFlag.AlignCenter, "A")
        painter.setPen(QPen(QColor(swatch or foreground), 3, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap))
        line(6, 20, 18, 20)
    elif name == "borders":
        painter.drawRect(4, 4, 16, 16)
        line(4, 10, 20, 10)
        line(4, 15, 20, 15)
        line(10, 4, 10, 20)
        line(15, 4, 15, 20)
    elif name == "sun":
        painter.drawEllipse(8, 8, 8, 8)
        for x1, y1, x2, y2 in (
                (12, 2, 12, 5), (12, 19, 12, 22), (2, 12, 5, 12),
                (19, 12, 22, 12), (5, 5, 7, 7), (17, 17, 19, 19),
                (17, 7, 19, 5), (5, 19, 7, 17)):
            line(x1, y1, x2, y2)
    elif name == "moon":
        painter.drawEllipse(5, 3, 15, 17)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#2D2F32" if theme == "dark" else "#FFFFFF"))
        painter.drawEllipse(2, 1, 14, 16)
    painter.end()
    return QIcon(pixmap)


class SpreadsheetView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        self.setEditTriggers(
            QTableView.EditTrigger.DoubleClicked
            | QTableView.EditTrigger.EditKeyPressed
            | QTableView.EditTrigger.AnyKeyPressed)
        self.horizontalHeader().setDefaultSectionSize(106)
        self.verticalHeader().setDefaultSectionSize(26)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection()
            return
        if event.matches(QKeySequence.StandardKey.Paste):
            self.paste_selection()
            return
        super().keyPressEvent(event)

    def copy_selection(self):
        indexes = self.selectedIndexes()
        if not indexes:
            return
        top = min(index.row() for index in indexes)
        bottom = max(index.row() for index in indexes)
        left = min(index.column() for index in indexes)
        right = max(index.column() for index in indexes)
        rows = []
        for row in range(top, bottom + 1):
            rows.append("\t".join(
                self.model().raw_value(row, column)
                for column in range(left, right + 1)))
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText("\n".join(rows))

    def paste_selection(self):
        from PySide6.QtWidgets import QApplication
        start = self.currentIndex()
        if not start.isValid():
            return
        data = QApplication.clipboard().text().splitlines()
        model = self.model()
        for row_offset, line in enumerate(data):
            row = start.row() + row_offset
            if row >= model.rowCount():
                break
            for column_offset, value in enumerate(line.split("\t")):
                column = start.column() + column_offset
                if column >= model.columnCount():
                    break
                model.setData(model.index(row, column), value)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme_settings = QSettings("Book/Tow", "Book/Tow")
        self.theme_mode = load_saved_theme(self.theme_settings)
        apply_theme(QApplication.instance(), self.theme_mode)
        self.document = SpreadsheetDocument()
        self.undo_stack = QUndoStack(self)
        self.model = SpreadsheetModel(self.document, self.undo_stack, self)
        self.current_path = None
        self.project_id = uuid.uuid4().hex
        self._base_fingerprint = None
        self._base_document_fingerprint = None
        self._change_revision = 0
        self._last_saved_revision = 0
        self._modified_without_undo = False
        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(750)
        self._save_timer.timeout.connect(self._start_background_save)
        self._save_thread_pool = QThreadPool(self)
        self._save_thread_pool.setMaxThreadCount(1)
        self._save_worker_active = False
        self._active_save_task = None
        self._pending_save = None
        self._closing = False
        self._allow_close = False
        self._recovery_directory = recovery_directory()
        self._building_tabs = False
        self.setWindowTitle("Book/Tow")
        self.setWindowIcon(application_icon())
        self.resize(1280, 800)
        self._create_actions()
        self._create_layout()
        self._create_brand_toolbar()
        self._create_toolbar()
        self._create_menus()
        self.save_status = QLabel("Saved")
        self.statusBar().addPermanentWidget(self.save_status)
        self._connect_signals()
        self._refresh_tabs()
        self.undo_stack.setClean()
        self._update_title()

    def _create_actions(self):
        self.new_action = self._action("New Spreadsheet", QKeySequence.StandardKey.New, self.new_file)
        self.open_action = self._action(
            "Open Project…", QKeySequence.StandardKey.Open, self.open_file)
        self.save_action = self._action(
            "Save Project", QKeySequence.StandardKey.Save, self.save_file)
        self.save_as_action = self._action(
            "Save Project As…", QKeySequence.StandardKey.SaveAs, self.save_file_as)
        self.undo_action = self.undo_stack.createUndoAction(self, "Undo")
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.setToolTip("Undo")
        self.undo_action.setStatusTip("Undo")
        self.redo_action = self.undo_stack.createRedoAction(self, "Redo")
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.setToolTip("Redo")
        self.redo_action.setStatusTip("Redo")
        self.copy_action = self._action(
            "Copy", QKeySequence.StandardKey.Copy,
            lambda: self.table.copy_selection())
        self.paste_action = self._action(
            "Paste", QKeySequence.StandardKey.Paste,
            lambda: self.table.paste_selection())
        self.add_sheet_action = self._action("New Worksheet", None, self.add_sheet)
        self.recovery_action = self._action(
            "Manage Recovery Data…", None, self.manage_recovery)
        self.about_action = self._action("About Book/Tow", None, self.show_about)
        for action, icon_name in (
                (self.new_action, "new"), (self.open_action, "open"),
                (self.save_action, "save"), (self.save_as_action, "save"),
                (self.undo_action, "undo"),
                (self.redo_action, "redo"), (self.copy_action, "copy"),
                (self.paste_action, "paste"), (self.add_sheet_action, "add_sheet")):
            action.setIcon(_toolbar_icon(icon_name, self.theme_mode))

    def _action(self, text, shortcut, callback):
        action = QAction(text, self)
        action.setToolTip(text)
        action.setStatusTip(text)
        if shortcut:
            action.setShortcut(shortcut)
        action.triggered.connect(callback)
        return action

    def _create_layout(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.formula_bar = QWidget()
        formula_layout = QHBoxLayout(self.formula_bar)
        formula_layout.setContentsMargins(12, 8, 12, 8)
        self.address_label = QLineEdit("A1")
        self.address_label.setReadOnly(True)
        self.address_label.setFixedWidth(78)
        self.formula_input = QLineEdit()
        self.formula_input.setPlaceholderText("Enter a value or formula")
        formula_layout.addWidget(self.address_label)
        formula_layout.addWidget(QLabel("fx"))
        formula_layout.addWidget(self.formula_input, 1)

        self.table = SpreadsheetView()
        self.table.setModel(self.model)
        self.table.setItemDelegate(SpreadsheetDelegate(self.table))
        self.tabs = QTabBar()
        self.tabs.setExpanding(False)
        self.tabs.setMovable(False)
        self.add_sheet_button = QPushButton("+")
        self.add_sheet_button.setIcon(_toolbar_icon("add_sheet", self.theme_mode))
        self.add_sheet_button.setToolTip("Add worksheet")
        self.add_sheet_button.setAccessibleName("Add worksheet")
        self.add_sheet_button.setFixedWidth(34)
        tab_row = QWidget()
        tab_layout = QHBoxLayout(tab_row)
        tab_layout.setContentsMargins(8, 4, 8, 4)
        tab_layout.addWidget(self.tabs)
        tab_layout.addWidget(self.add_sheet_button)
        tab_layout.addStretch(1)

        layout.addWidget(self.formula_bar)
        layout.addWidget(self.table, 1)
        layout.addWidget(tab_row)
        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

    def _create_toolbar(self):
        toolbar = QToolBar("Formatting")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setIconSize(QSize(18, 18))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.addToolBar(toolbar)
        self.font_family = QFontComboBox()
        self.font_family.setMaximumWidth(145)
        self.font_family.setToolTip("Font family")
        self.font_family.currentFontChanged.connect(
            lambda font: self._apply_style("font_family", font.family()))
        self.font_size = QSpinBox()
        self.font_size.setRange(6, 72)
        self.font_size.setValue(10)
        self.font_size.setSuffix(" pt")
        self.font_size.setToolTip("Font size (points)")
        self.font_size.valueChanged.connect(
            lambda size: self._apply_style("font_size", size))
        toolbar.addWidget(self.font_family)
        toolbar.addWidget(self.font_size)
        toolbar.addSeparator()

        self.bold_button = self._format_button("B", "Bold", "bold")
        self.bold_button.setIcon(_toolbar_icon("bold", self.theme_mode))
        self.bold_button.setStyleSheet("font-weight: bold;")
        self.italic_button = self._format_button("I", "Italic", "italic")
        self.italic_button.setIcon(_toolbar_icon("italic", self.theme_mode))
        self.italic_button.setStyleSheet("font-style: italic;")
        self.underline_button = self._format_button("U", "Underline", "underline")
        self.underline_button.setIcon(_toolbar_icon("underline", self.theme_mode))
        self.underline_button.setStyleSheet("text-decoration: underline;")
        for button in (self.bold_button, self.italic_button, self.underline_button):
            toolbar.addWidget(button)
        toolbar.addSeparator()

        self.alignment_buttons = {}
        for label, alignment in (("Left", "left"), ("Center", "center"), ("Right", "right")):
            button = QToolButton()
            button.setIcon(_toolbar_icon("align_{}".format(alignment), self.theme_mode))
            button.setToolTip("Align {}".format(label.lower()))
            button.setAccessibleName("Align {}".format(label.lower()))
            button.clicked.connect(lambda checked=False, value=alignment: self._apply_style("alignment", value))
            toolbar.addWidget(button)
            self.alignment_buttons[alignment] = button
        self.color_button = QToolButton()
        self.color_button.setToolTip("Choose the text color for the selected cells")
        self.color_button.setAccessibleName("Font color")
        self._add_color_palette(self.color_button, "color")
        toolbar.addWidget(self.color_button)
        self.fill_button = QToolButton()
        self.fill_button.setToolTip("Choose the background color for the selected cells")
        self.fill_button.setAccessibleName("Cell fill color")
        self._add_color_palette(self.fill_button, "background")
        toolbar.addWidget(self.fill_button)
        self.border_button = QToolButton()
        self.border_button.setIcon(_toolbar_icon("borders", self.theme_mode))
        self.border_button.setToolTip("Choose borders for the selected cells")
        self.border_button.setAccessibleName("Cell borders")
        self.border_menu = QMenu(self.border_button)
        for label, operation in (
                ("All Borders", "all"),
                ("Outside Borders", "outside"),
                ("Top Border", "top"),
                ("Bottom Border", "bottom"),
                ("Left Border", "left"),
                ("Right Border", "right"),
                ("Remove Borders", "remove")):
            action = self.border_menu.addAction(label)
            action.triggered.connect(
                lambda _checked=False, selected=operation: self._apply_borders(selected))
        self.border_button.setMenu(self.border_menu)
        self.border_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        toolbar.addWidget(self.border_button)
        toolbar.addSeparator()

        self.number_format = QComboBox()
        self.number_format.addItems(["General", "Number", "Percent"])
        self.number_format.setToolTip("Number format")
        self.number_format.currentTextChanged.connect(self._number_format_changed)
        toolbar.addWidget(self.number_format)
        formula_button = QToolButton()
        formula_button.setText("ƒx")
        formula_button.setToolTip("Insert a formula")
        formula_button.setAccessibleName("Insert a formula")
        formula_button.clicked.connect(self._insert_formula)
        toolbar.addWidget(formula_button)
        self._update_color_icons()

    def _create_brand_toolbar(self):
        toolbar = QToolBar("Book/Tow")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(toolbar)
        logo = QLabel()
        logo.setPixmap(application_icon().pixmap(28, 28))
        logo.setContentsMargins(4, 0, 3, 0)
        toolbar.addWidget(logo)
        name = QLabel("<b>Book/Tow</b>")
        name.setStyleSheet("font-size: 15px; color: #A64B00; padding-right: 10px;")
        toolbar.addWidget(name)
        toolbar.addSeparator()
        for action in (
                self.new_action, self.open_action, self.save_action,
                self.save_as_action, self.undo_action, self.redo_action,
                self.copy_action, self.paste_action):
            toolbar.addAction(action)
        toolbar.addSeparator()
        toolbar.addAction(self.add_sheet_action)
        self.settings_menu = QMenu(self)
        self.theme_action_group = QActionGroup(self)
        self.theme_action_group.setExclusive(True)
        self.light_mode_action = self._theme_action("Light Mode", "light")
        self.dark_mode_action = self._theme_action("Dark Mode", "dark")
        self.settings_button = QToolButton()
        self.settings_button.setText("Theme")
        self.settings_button.setToolTip("Switch theme; use the menu to choose Light or Dark Mode")
        self.settings_button.setAccessibleName("Toggle light or dark theme")
        self.settings_button.setMenu(self.settings_menu)
        self.settings_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.settings_button.clicked.connect(self._toggle_theme)
        toolbar.addWidget(self.settings_button)
        self._update_theme_actions()

    def _theme_action(self, text, mode):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setToolTip("Switch to {} mode".format(text.removesuffix(" Mode").lower()))
        self.theme_action_group.addAction(action)
        self.settings_menu.addAction(action)
        action.triggered.connect(lambda _checked=False, selected=mode: self._set_theme(selected))
        return action

    def _add_color_palette(self, button, style_key):
        menu = QMenu(button)
        custom = menu.addAction("Custom color…")
        custom.triggered.connect(lambda _checked=False: self._choose_color(style_key))
        menu.addSeparator()
        for color_value in COLOR_PALETTE:
            action = menu.addAction(color_value)
            action.setIcon(_color_swatch(color_value))
            action.setToolTip(color_value)
            action.triggered.connect(
                lambda _checked=False, selected=color_value: self._apply_style(
                    style_key, selected))
        menu.addSeparator()
        clear = menu.addAction(
            "No fill" if style_key == "background" else "Automatic text color")
        clear.triggered.connect(
            lambda _checked=False: self._apply_style(style_key, None))
        button.setMenu(menu)
        button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

    def _format_button(self, text, tooltip, style_key):
        button = QToolButton()
        button.setText(text)
        button.setToolTip(tooltip)
        button.setAccessibleName(tooltip)
        button.setCheckable(True)
        button.toggled.connect(lambda enabled: self._apply_style(style_key, enabled))
        return button

    def _connect_signals(self):
        self.table.selectionModel().currentChanged.connect(self._selection_changed)
        self.model.dataChanged.connect(self._model_changed)
        self.formula_input.returnPressed.connect(self._commit_formula_input)
        self.tabs.currentChanged.connect(self._tab_changed)
        self.add_sheet_button.clicked.connect(self.add_sheet)
        self.undo_stack.cleanChanged.connect(self._update_title)
        self.undo_stack.indexChanged.connect(self._update_title)

    def _create_menus(self):
        file_menu = self.menuBar().addMenu("&File")
        for action in (self.new_action, self.open_action, self.save_action, self.save_as_action):
            file_menu.addAction(action)
        file_menu.addSeparator()
        file_menu.addAction(self.recovery_action)
        file_menu.addSeparator()
        file_menu.addAction(self._action("Quit", QKeySequence.StandardKey.Quit, self.close))

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self._action("Focus Formula Bar", QKeySequence("Ctrl+L"), self.formula_input.setFocus))
        insert_menu = self.menuBar().addMenu("&Insert")
        insert_menu.addAction(self.add_sheet_action)
        format_menu = self.menuBar().addMenu("&Format")
        for label, button in (
                ("Bold", self.bold_button), ("Italic", self.italic_button),
                ("Underline", self.underline_button)):
            format_menu.addAction(self._action(label, None, button.click))
        format_borders = format_menu.addMenu("Borders")
        for label, operation in (
                ("All Borders", "all"),
                ("Outside Borders", "outside"),
                ("Top Border", "top"),
                ("Bottom Border", "bottom"),
                ("Left Border", "left"),
                ("Right Border", "right"),
                ("Remove Borders", "remove")):
            action = format_borders.addAction(label)
            action.triggered.connect(
                lambda _checked=False, selected=operation: self._apply_borders(selected))
        format_menu.addSeparator()
        for label, alignment in (("Align Left", "left"), ("Align Center", "center"),
                                 ("Align Right", "right")):
            format_menu.addAction(self._action(
                label, None, lambda value=alignment: self._apply_style("alignment", value)))
        data_menu = self.menuBar().addMenu("&Data")
        data_menu.addAction(self._action("Recalculate Formulas", None, self.model.refresh))
        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.about_action)

    def _refresh_tabs(self):
        self._building_tabs = True
        while self.tabs.count():
            self.tabs.removeTab(0)
        for sheet in self.document.sheets:
            self.tabs.addTab(sheet["name"])
        self.tabs.setCurrentIndex(self.model.active_sheet)
        self._building_tabs = False

    def _selection_changed(self, current, _previous):
        if not current.isValid():
            return
        address = cell_address(current.row(), current.column())
        self.address_label.setText(address)
        self.formula_input.setText(self.model.raw_value(current.row(), current.column()))
        self.statusBar().showMessage(
            "{}   |   {} rows × {} columns".format(
                address, self.model.rowCount(), self.model.columnCount()))
        cell = self.model.sheet["cells"].get(address, {})
        style = cell.get("style", {})
        for button, key in ((self.bold_button, "bold"),
                            (self.italic_button, "italic"),
                            (self.underline_button, "underline")):
            button.blockSignals(True)
            button.setChecked(style.get(key, False))
            button.blockSignals(False)
        self.font_size.blockSignals(True)
        self.font_size.setValue(style.get("font_size", 10))
        self.font_size.blockSignals(False)
        family = style.get("font_family")
        if family:
            self.font_family.blockSignals(True)
            self.font_family.setCurrentFont(QFont(family))
            self.font_family.blockSignals(False)
        self.number_format.blockSignals(True)
        self.number_format.setCurrentText(style.get("number_format", "General"))
        self.number_format.blockSignals(False)
        self._update_color_icons()

    def _commit_formula_input(self):
        index = self.table.currentIndex()
        if not index.isValid():
            return
        self.model.setData(index, self.formula_input.text())
        self.table.setFocus()
        self._show_formula_status(index.row(), index.column())

    def _model_changed(self, *_args):
        self._mark_document_changed()
        index = self.table.currentIndex()
        if index.isValid() and not self.formula_input.hasFocus():
            self.formula_input.setText(self.model.raw_value(index.row(), index.column()))
            if self.model.raw_value(index.row(), index.column()).startswith("="):
                self._show_formula_status(index.row(), index.column())

    def _mark_document_changed(self):
        self._change_revision += 1
        self._save_timer.start()
        self.save_status.setText("Saving...")
        self.save_status.setToolTip("")

    def _show_formula_status(self, row, column):
        address = cell_address(row, column)
        try:
            self.model._calculated_value(address, set())
            self.statusBar().showMessage("{}   |   Formula calculated".format(address), 3500)
        except FormulaError as error:
            self.statusBar().showMessage("{}   |   {}".format(address, error), 7000)

    def _apply_style(self, key, value):
        indexes = self.table.selectionModel().selectedIndexes()
        if not indexes and self.table.currentIndex().isValid():
            indexes = [self.table.currentIndex()]
        if indexes:
            self._modified_without_undo = True
        self.model.apply_style(indexes, key, value)
        if key in {"color", "background"}:
            self._update_color_icons()
        self._update_title()

    def _apply_borders(self, operation):
        indexes = self.table.selectionModel().selectedIndexes()
        if not indexes and self.table.currentIndex().isValid():
            indexes = [self.table.currentIndex()]
        if indexes:
            self._modified_without_undo = True
        self.model.apply_borders(indexes, operation)
        self._update_title()

    def _choose_color(self, key):
        current = self.table.currentIndex()
        style = {}
        if current.isValid():
            address = cell_address(current.row(), current.column())
            style = self.model.sheet["cells"].get(address, {}).get("style", {})
        fallback = "#FFF2CC" if key == "background" else (
            "#E8E4DE" if self.theme_mode == "dark" else "#302D2A")
        color = QColorDialog.getColor(QColor(style.get(key, fallback)), self)
        if color.isValid():
            self._apply_style(key, color.name())

    def _set_theme(self, mode):
        if mode == self.theme_mode:
            self._update_theme_actions()
            return
        try:
            save_theme_preference(mode, self.theme_settings)
        except OSError as error:
            QMessageBox.warning(
                self, "Appearance Not Saved",
                "{} The current appearance has not been changed.".format(error))
            self._update_theme_actions()
            return
        self.theme_mode = mode
        apply_theme(QApplication.instance(), mode)
        self._update_theme_actions()
        self._refresh_toolbar_icons()
        self.table.viewport().update()

    def _update_theme_actions(self):
        self.light_mode_action.setChecked(self.theme_mode == "light")
        self.dark_mode_action.setChecked(self.theme_mode == "dark")
        self.light_mode_action.setIcon(_toolbar_icon("sun", self.theme_mode))
        self.dark_mode_action.setIcon(_toolbar_icon("moon", self.theme_mode))
        target = "dark" if self.theme_mode == "light" else "light"
        self.settings_button.setIcon(
            _toolbar_icon("sun" if self.theme_mode == "light" else "moon",
                          self.theme_mode))
        self.settings_button.setToolTip(
            "Switch to {} Mode (currently {})".format(
                target.capitalize(), self.theme_mode.capitalize()))

    def _toggle_theme(self):
        self._set_theme("dark" if self.theme_mode == "light" else "light")

    def _update_color_icons(self):
        style = {}
        current = self.table.currentIndex()
        if current.isValid():
            address = cell_address(current.row(), current.column())
            style = self.model.sheet["cells"].get(address, {}).get("style", {})
        foreground = style.get("color")
        if foreground is None:
            foreground = "#E8E4DE" if self.theme_mode == "dark" else "#302D2A"
        self.color_button.setIcon(
            _toolbar_icon("font_color", self.theme_mode, foreground))
        self.color_button.setToolTip(
            "Font color: {}; choose a text color for the selected cells".format(
                foreground))
        background = style.get("background", "#F1C232")
        self.fill_button.setIcon(_toolbar_icon("fill", self.theme_mode, background))
        self.fill_button.setToolTip(
            "Cell fill color: {}; choose a background color for the selected cells".format(
                style.get("background", "default")))

    def _refresh_toolbar_icons(self):
        for action, icon_name in (
                (self.new_action, "new"), (self.open_action, "open"),
                (self.save_action, "save"), (self.save_as_action, "save"),
                (self.undo_action, "undo"),
                (self.redo_action, "redo"), (self.copy_action, "copy"),
                (self.paste_action, "paste"), (self.add_sheet_action, "add_sheet")):
            action.setIcon(_toolbar_icon(icon_name, self.theme_mode))
        for button, icon_name in (
                (self.bold_button, "bold"), (self.italic_button, "italic"),
                (self.underline_button, "underline"),
                (self.border_button, "borders")):
            button.setIcon(_toolbar_icon(icon_name, self.theme_mode))
        for alignment, button in self.alignment_buttons.items():
            button.setIcon(_toolbar_icon(
                "align_{}".format(alignment), self.theme_mode))
        self._update_color_icons()
        self.add_sheet_button.setIcon(_toolbar_icon("add_sheet", self.theme_mode))

    def _number_format_changed(self, value):
        self._apply_style("number_format", "" if value == "General" else value)

    def _insert_formula(self):
        if not self.formula_input.text().startswith("="):
            self.formula_input.setText("=")
        self.formula_input.setFocus()
        self.formula_input.setCursorPosition(len(self.formula_input.text()))

    def _tab_changed(self, index):
        if self._building_tabs or index < 0:
            return
        self.model.set_active_sheet(index)
        self.table.setCurrentIndex(self.model.index(0, 0))

    def add_sheet(self):
        base = "Sheet{}".format(len(self.document.sheets) + 1)
        name = base
        suffix = 2
        existing = {sheet["name"].casefold() for sheet in self.document.sheets}
        while name.casefold() in existing:
            name = "{} ({})".format(base, suffix)
            suffix += 1
        self.document.sheets.append({"name": name, "cells": {}})
        self._modified_without_undo = True
        self._refresh_tabs()
        self.tabs.setCurrentIndex(len(self.document.sheets) - 1)
        self.model.set_active_sheet(len(self.document.sheets) - 1)
        self._mark_document_changed()
        self._update_title()

    def new_file(self):
        if not self._confirm_discard():
            return
        self.document = SpreadsheetDocument()
        self.undo_stack.clear()
        self.model.document = self.document
        self.model.active_sheet = 0
        self.model.beginResetModel()
        self.model.endResetModel()
        self.current_path = None
        self.project_id = uuid.uuid4().hex
        self._base_fingerprint = None
        self._base_document_fingerprint = None
        self._modified_without_undo = False
        self._last_saved_revision = self._change_revision
        self._refresh_tabs()
        self.undo_stack.setClean()
        self.table.setCurrentIndex(self.model.index(0, 0))
        self._update_title()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "",
            "Book/Tow Project (*{});;Legacy Book/Tow Spreadsheet (*{});;"
            "All Files (*)".format(
                PROJECT_EXTENSION, LEGACY_PROJECT_EXTENSION))
        if not path:
            return
        self.open_project_path(path)

    def open_project_path(self, path):
        try:
            document = load_document(path)
        except ValueError as error:
            log_file_operation_error("open", error)
            QMessageBox.critical(self, "Unable to Open Project", str(error))
            return False
        if not self._confirm_discard():
            return False
        self._install_document(document, path)
        return True

    def _install_document(self, document, path):
        self._save_timer.stop()
        self._pending_save = None
        self.document = document
        self.undo_stack.clear()
        self.model.document = document
        self.model.active_sheet = 0
        self.model.beginResetModel()
        self.model.endResetModel()
        self.current_path = path
        self.project_id = project_id_for_path(path)
        self._base_fingerprint = file_fingerprint(path)
        self._base_document_fingerprint = document_fingerprint(document.to_dict())
        self._modified_without_undo = False
        self._last_saved_revision = self._change_revision
        self._refresh_tabs()
        self.undo_stack.setClean()
        self.table.setCurrentIndex(self.model.index(0, 0))
        self._update_title()
        self._offer_recovery(self.project_id)

    def save_file(self):
        if not self.current_path:
            self.save_file_as()
            return
        self._save_to_path(self.current_path)

    def save_file_as(self):
        dialog = QFileDialog(
            self, "Save Project As", "",
            "Book/Tow Project (*{});;Legacy Book/Tow Spreadsheet (*{})".format(
                PROJECT_EXTENSION, LEGACY_PROJECT_EXTENSION))
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setDefaultSuffix(PROJECT_EXTENSION.lstrip("."))
        dialog.setOption(QFileDialog.Option.DontConfirmOverwrite, True)
        if not dialog.exec():
            return
        selected_files = dialog.selectedFiles()
        if not selected_files:
            return
        path = ensure_project_extension(selected_files[0])
        if os.path.exists(path):
            answer = QMessageBox.question(
                self, "Confirm Overwrite",
                "A project named '{}' already exists. Replace it?".format(
                    os.path.basename(path)),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
            if answer != QMessageBox.StandardButton.Yes:
                return
        if self._save_to_path(path):
            self._update_title()

    def _save_to_path(self, path):
        self._save_timer.stop()
        self._pending_save = None
        self._save_thread_pool.waitForDone()
        self._save_worker_active = False
        try:
            save_document(self.document, path)
        except ValueError as error:
            log_file_operation_error("save", error)
            QMessageBox.critical(self, "Unable to Save Project", str(error))
            self.save_status.setText("Save failed")
            self.save_status.setToolTip(
                "The pending edits will be written to recovery data if possible.")
            self._save_timer.start()
            return False
        self.undo_stack.setClean()
        self._modified_without_undo = False
        previous_project_id = self.project_id
        self.current_path = path
        self.project_id = project_id_for_path(path)
        self._base_fingerprint = file_fingerprint(path)
        self._base_document_fingerprint = document_fingerprint(self.document.to_dict())
        self._last_saved_revision = self._change_revision
        try:
            discard_recovery(self._recovery_directory, previous_project_id)
        except ValueError as error:
            log_file_operation_error("recovery cleanup", error)
        self.statusBar().showMessage("Saved {}".format(os.path.basename(path)), 4000)
        self.save_status.setText("Saved")
        self.save_status.setToolTip("")
        return True

    def _confirm_discard(self):
        if self.undo_stack.isClean() and not self._modified_without_undo:
            return True
        answer = QMessageBox.question(
            self, "Unsaved Changes", "Save changes to this spreadsheet before continuing?",
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save)
        if answer == QMessageBox.StandardButton.Save:
            self.save_file()
            return self.undo_stack.isClean()
        return answer == QMessageBox.StandardButton.Discard

    def closeEvent(self, event):
        if self._allow_close:
            event.accept()
            return
        if not (self._save_worker_active or self._pending_save
                or not self.undo_stack.isClean()
                or self._modified_without_undo):
            self._save_timer.stop()
            event.accept()
            return
        event.ignore()
        self._closing = True
        self._save_timer.stop()
        self._start_background_save()

    def _start_background_save(self):
        snapshot = copy.deepcopy(self.document.to_dict())
        save = {
            "snapshot": snapshot,
            "path": self.current_path,
            "expected_fingerprint": self._base_fingerprint,
            "project_id": self.project_id,
            "source_path": self.current_path,
            "base_fingerprint": self._base_fingerprint,
            "base_document_fingerprint": self._base_document_fingerprint,
            "revision": self._change_revision,
        }
        if self._save_worker_active:
            self._pending_save = save
            return
        self._save_worker_active = True
        task = AutoSaveTask(
            save["snapshot"], save["path"], save["expected_fingerprint"],
            self._recovery_directory, save["project_id"], save["source_path"],
            save["base_fingerprint"], save["base_document_fingerprint"], save)
        self._active_save_task = task
        task.signals.finished.connect(self._background_save_finished)
        self._save_thread_pool.start(task)

    @Slot(object, object)
    def _background_save_finished(self, saved, result):
        self._save_worker_active = False
        self._active_save_task = None
        if result["project_error"] is not None:
            log_file_operation_error("automatic save", result["project_error"])
        if result["recovery_error"] is not None:
            log_file_operation_error("recovery write", result["recovery_error"])
        if saved["project_id"] == self.project_id and saved["path"] == self.current_path:
            if result["project_saved"] and saved["path"]:
                if saved["revision"] >= self._last_saved_revision:
                    self._base_fingerprint = result["new_fingerprint"]
                    self._base_document_fingerprint = document_fingerprint(
                        saved["snapshot"])
                    self._last_saved_revision = saved["revision"]
                if saved["revision"] == self._change_revision:
                    self.undo_stack.setClean()
                    self._modified_without_undo = False
                    self._update_title()
            if not result["project_saved"]:
                self.save_status.setText("Save failed")
                self.save_status.setToolTip(
                    "Automatic save failed; a recovery copy was {}.".format(
                        "updated" if result["recovery_saved"] else "not updated"))
            elif result["recovery_saved"]:
                self.save_status.setText(
                    "Saved" if saved["path"] else "Recovery backup updated")
                self.save_status.setToolTip("")
            else:
                self.save_status.setText("Save failed")
                self.save_status.setToolTip(
                    "The project may be saved, but its recovery copy could not be updated.")
        if self._pending_save:
            pending = self._pending_save
            self._pending_save = None
            if (pending["project_id"] == self.project_id
                    and pending["path"] == self.current_path):
                pending["expected_fingerprint"] = self._base_fingerprint
                pending["base_fingerprint"] = self._base_fingerprint
                pending["base_document_fingerprint"] = (
                    self._base_document_fingerprint)
            self.save_status.setText("Saving...")
            self._launch_background_save(pending)
        elif self._closing:
            self._allow_close = True
            self.close()

    def _launch_background_save(self, save):
        self._save_worker_active = True
        task = AutoSaveTask(
            save["snapshot"], save["path"], save["expected_fingerprint"],
            self._recovery_directory, save["project_id"], save["source_path"],
            save["base_fingerprint"], save["base_document_fingerprint"], save)
        self._active_save_task = task
        task.signals.finished.connect(self._background_save_finished)
        self._save_thread_pool.start(task)

    def check_for_recovery(self):
        self._offer_recovery()

    def _recovery_source_fingerprint(self, path):
        try:
            return file_fingerprint(path)
        except OSError as error:
            log_file_operation_error("recovery comparison", error)
            return None

    def _offer_recovery(self, project_id=None):
        try:
            candidates = recovery_candidates(self._recovery_directory)
        except OSError as error:
            log_file_operation_error("recovery scan", error)
            self.save_status.setText("Save failed")
            self.save_status.setToolTip("Recovery data could not be checked.")
            return
        if project_id:
            candidates = [candidate for candidate in candidates
                          if candidate["project_id"] == project_id]
        eligible = []
        for candidate in candidates:
            source_path = candidate.get("source_path")
            current_fingerprint = (
                self._recovery_source_fingerprint(source_path)
                if source_path else None)
            if (candidate.get("base_document_fingerprint") is not None
                    and candidate["document_fingerprint"]
                    == candidate["base_document_fingerprint"]):
                try:
                    discard_recovery(
                        self._recovery_directory, candidate["project_id"])
                except ValueError as error:
                    log_file_operation_error("recovery cleanup", error)
                continue
            candidate["saved_file_changed"] = bool(
                source_path and candidate.get("base_fingerprint")
                and current_fingerprint != candidate.get("base_fingerprint"))
            eligible.append(candidate)
        if not eligible:
            return
        labels = [
            "{} — {} ({})".format(
                os.path.basename(candidate.get("source_path") or "Unsaved spreadsheet"),
                time.strftime("%Y-%m-%d %H:%M", time.localtime(candidate["updated_at"])),
                candidate["project_id"][:6])
            for candidate in eligible
        ]
        selected = eligible[0]
        if len(eligible) > 1:
            choice, accepted = QInputDialog.getItem(
                self, "Available Recovery Data",
                "Choose a spreadsheet recovery copy:", labels, 0, False)
            if not accepted:
                return
            selected = eligible[labels.index(choice)]
        if selected["saved_file_changed"]:
            message = (
                "The saved spreadsheet has changed since this recovery copy was "
                "created. Restore it as a separate, unsaved spreadsheet?")
        else:
            message = (
                "Unsaved changes from your previous session are available. "
                "Restore them?")
        answer = QMessageBox.question(
            self, "Recover Spreadsheet", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes)
        if answer != QMessageBox.StandardButton.Yes:
            return
        self._restore_recovery(selected)

    def _restore_recovery(self, candidate):
        self.document = candidate["validated_document"]
        self.undo_stack.clear()
        self.model.document = self.document
        self.model.active_sheet = 0
        self.model.beginResetModel()
        self.model.endResetModel()
        source_path = candidate.get("source_path")
        current_fingerprint = (
            self._recovery_source_fingerprint(source_path) if source_path else None)
        if (source_path and not candidate["saved_file_changed"]
                and current_fingerprint is not None
                and current_fingerprint == candidate.get("base_fingerprint")):
            self.current_path = source_path
            self._base_fingerprint = current_fingerprint
            self._base_document_fingerprint = candidate.get(
                "base_document_fingerprint")
            self.project_id = candidate["project_id"]
        else:
            self.current_path = None
            self._base_fingerprint = None
            self._base_document_fingerprint = None
            self.project_id = candidate["project_id"]
        self._modified_without_undo = True
        self._last_saved_revision = self._change_revision
        self._refresh_tabs()
        self.undo_stack.setClean()
        self.table.setCurrentIndex(self.model.index(0, 0))
        self._update_title()
        self._mark_document_changed()
        self.statusBar().showMessage(
            "Recovered unsaved changes from your previous session.", 8000)

    def manage_recovery(self):
        try:
            candidates = recovery_candidates(self._recovery_directory)
        except OSError as error:
            log_file_operation_error("recovery scan", error)
            QMessageBox.warning(
                self, "Unable to Read Recovery Data",
                "Book/Tow could not check its recovery folder.")
            return
        if not candidates:
            QMessageBox.information(
                self, "Recovery Data", "There are no saved recovery copies.")
            return
        labels = [
            "{} — {} ({})".format(
                os.path.basename(candidate.get("source_path") or "Unsaved spreadsheet"),
                time.strftime("%Y-%m-%d %H:%M", time.localtime(candidate["updated_at"])),
                candidate["project_id"][:6])
            for candidate in candidates
        ]
        choice, accepted = QInputDialog.getItem(
            self, "Manage Recovery Data", "Choose a recovery copy to discard:",
            labels, 0, False)
        if not accepted:
            return
        candidate = candidates[labels.index(choice)]
        answer = QMessageBox.question(
            self, "Discard Recovery Data",
            "Discard this recovery copy? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if answer == QMessageBox.StandardButton.Yes:
            try:
                discard_recovery(
                    self._recovery_directory, candidate["project_id"])
            except ValueError as error:
                log_file_operation_error("recovery cleanup", error)
                QMessageBox.warning(self, "Unable to Discard Recovery Data", str(error))

    def show_about(self):
        QMessageBox.about(
            self, "About Book/Tow",
            "<h2>Book/Tow 1.1</h2><p>A thoughtful place for your numbers.</p>"
            "<p>Save and share projects in the documented .booktow format.</p>")

    def _update_title(self):
        suffix = " — {}".format(os.path.basename(self.current_path)) if self.current_path else ""
        dirty = "" if self.undo_stack.isClean() and not self._modified_without_undo else " •"
        self.setWindowTitle("Book/Tow{}{}".format(suffix, dirty))
