"""
Main Window Implementation for Book/Tow 1.1.
Integrates Menu Bar, Toolbar, Formula Bar, Tabbed Spreadsheet Views, and Status Bar.
"""

import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QTableView, QStatusBar, QFileDialog, QMessageBox,
    QMenu, QMenuBar, QHeaderView, QAbstractItemView, QDialog, QToolButton
)
from PySide6.QtGui import QIcon, QKeySequence, QAction, QColor, QPalette, QFont
from PySide6.QtCore import Qt, QModelIndex, ItemSelectionModel

from app.spreadsheet_model import SpreadsheetModel, CellStyle, coords_to_cell_name, cell_name_to_coords
from app.toolbar import SpreadsheetToolbar
from app.file_manager import FileManager
from app.theme import APP_STYLESHEET


class BookTowMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book/Tow 1.1")
        self.setMinimumSize(1000, 700)
        self.setWindowIcon(QIcon("assets/app_icon/icon.png"))

        self.current_filepath = None
        self.sheets = []

        self.setStyleSheet(APP_STYLESHEET)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._build_menu_bar()
        self._build_toolbar()
        self._build_formula_bar()
        self._build_tabbed_spreadsheet()
        self._build_status_bar()

        self.add_new_sheet("Sheet1")

    def _build_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        act_new = QAction("New Spreadsheet", self)
        act_new.setShortcut(QKeySequence.New)
        act_new.triggered.connect(self.action_new_file)
        file_menu.addAction(act_new)

        act_open = QAction("Open...", self)
        act_open.setShortcut(QKeySequence.Open)
        act_open.triggered.connect(self.action_open_file)
        file_menu.addAction(act_open)

        act_save = QAction("Save", self)
        act_save.setShortcut(QKeySequence.Save)
        act_save.triggered.connect(self.action_save_file)
        file_menu.addAction(act_save)

        act_save_as = QAction("Save As...", self)
        act_save_as.setShortcut(QKeySequence.SaveAs)
        act_save_as.triggered.connect(self.action_save_as_file)
        file_menu.addAction(act_save_as)

        file_menu.addSeparator()

        act_export_csv = QAction("Export to CSV...", self)
        act_export_csv.triggered.connect(self.action_export_csv)
        file_menu.addAction(act_export_csv)

        act_import_csv = QAction("Import from CSV...", self)
        act_import_csv.triggered.connect(self.action_import_csv)
        file_menu.addAction(act_import_csv)

        file_menu.addSeparator()

        act_exit = QAction("Exit", self)
        act_exit.setShortcut(QKeySequence.Quit)
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)

        edit_menu = menu_bar.addMenu("Edit")

        act_undo = QAction("Undo", self)
        act_undo.setShortcut(QKeySequence.Undo)
        act_undo.triggered.connect(self.action_undo)
        edit_menu.addAction(act_undo)

        act_redo = QAction("Redo", self)
        act_redo.setShortcut(QKeySequence.Redo)
        act_redo.triggered.connect(self.action_redo)
        edit_menu.addAction(act_redo)

        edit_menu.addSeparator()

        act_cut = QAction("Cut", self)
        act_cut.setShortcut(QKeySequence.Cut)
        act_cut.triggered.connect(self.action_cut)
        edit_menu.addAction(act_cut)

        act_copy = QAction("Copy", self)
        act_copy.setShortcut(QKeySequence.Copy)
        act_copy.triggered.connect(self.action_copy)
        edit_menu.addAction(act_copy)

        act_paste = QAction("Paste", self)
        act_paste.setShortcut(QKeySequence.Paste)
        act_paste.triggered.connect(self.action_paste)
        edit_menu.addAction(act_paste)

        view_menu = menu_bar.addMenu("View")
        act_expand = QAction("Expand Grid (+50 Rows, +10 Cols)", self)
        act_expand.triggered.connect(self.action_expand_grid)
        view_menu.addAction(act_expand)

        insert_menu = menu_bar.addMenu("Insert")
        act_add_sheet = QAction("New Worksheet", self)
        act_add_sheet.triggered.connect(lambda: self.add_new_sheet())
        insert_menu.addAction(act_add_sheet)

        format_menu = menu_bar.addMenu("Format")
        act_clear_fmt = QAction("Clear Formatting", self)
        act_clear_fmt.triggered.connect(self.action_clear_formatting)
        format_menu.addAction(act_clear_fmt)

        data_menu = menu_bar.addMenu("Data")
        act_recalc = QAction("Recalculate All Formulas", self)
        act_recalc.triggered.connect(self.action_recalculate)
        data_menu.addAction(act_recalc)

        help_menu = menu_bar.addMenu("Help")
        act_about = QAction("About Book/Tow 1.1", self)
        act_about.triggered.connect(self.action_about)
        help_menu.addAction(act_about)

    def _build_toolbar(self):
        self.toolbar_widget = SpreadsheetToolbar(self)
        self.main_layout.addWidget(self.toolbar_widget)

        self.toolbar_widget.newFileRequested.connect(self.action_new_file)
        self.toolbar_widget.openFileRequested.connect(self.action_open_file)
        self.toolbar_widget.saveFileRequested.connect(self.action_save_file)
        self.toolbar_widget.saveAsFileRequested.connect(self.action_save_as_file)
        self.toolbar_widget.undoRequested.connect(self.action_undo)
        self.toolbar_widget.redoRequested.connect(self.action_redo)

        self.toolbar_widget.fontFamilyChanged.connect(self.apply_font_family)
        self.toolbar_widget.fontSizeChanged.connect(self.apply_font_size)
        self.toolbar_widget.boldToggled.connect(self.apply_bold)
        self.toolbar_widget.italicToggled.connect(self.apply_italic)
        self.toolbar_widget.underlineToggled.connect(self.apply_underline)
        self.toolbar_widget.alignmentChanged.connect(self.apply_alignment)
        self.toolbar_widget.textColorSelected.connect(self.apply_text_color)
        self.toolbar_widget.bgColorSelected.connect(self.apply_bg_color)
        self.toolbar_widget.numFormatChanged.connect(self.apply_num_format)
        self.toolbar_widget.insertFormulaRequested.connect(self.insert_formula_into_cell)

    def _build_formula_bar(self):
        bar_widget = QWidget(self)
        bar_widget.setObjectName("FormulaBarContainer")
        layout = QHBoxLayout(bar_widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        self.lbl_cell_address = QLabel("A1", self)
        self.lbl_cell_address.setObjectName("CellAddressLabel")
        layout.addWidget(self.lbl_cell_address)

        lbl_fx = QLabel("<i><b>f(x)</b></i>", self)
        lbl_fx.setStyleSheet("color: #F28C28; font-size: 13px; font-weight: bold;")
        layout.addWidget(lbl_fx)

        self.formula_input = QLineEdit(self)
        self.formula_input.setPlaceholderText("Enter a value or formula starting with '='...")
        self.formula_input.returnPressed.connect(self.on_formula_submitted)
        layout.addWidget(self.formula_input)

        btn_confirm = QPushButton("✓", self)
        btn_confirm.setFixedSize(26, 26)
        btn_confirm.setToolTip("Accept Formula")
        btn_confirm.clicked.connect(self.on_formula_submitted)
        layout.addWidget(btn_confirm)

        btn_cancel = QPushButton("✕", self)
        btn_cancel.setFixedSize(26, 26)
        btn_cancel.setToolTip("Cancel Editing")
        btn_cancel.clicked.connect(self.on_formula_cancelled)
        layout.addWidget(btn_cancel)

        self.main_layout.addWidget(bar_widget)

    def _build_tabbed_spreadsheet(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.currentChanged.connect(self.on_active_tab_changed)

        btn_add_tab = QToolButton(self)
        btn_add_tab.setText("+")
        btn_add_tab.setToolTip("Add Worksheet")
        btn_add_tab.setStyleSheet("font-size: 16px; font-weight: bold; color: #F28C28;")
        btn_add_tab.clicked.connect(lambda: self.add_new_sheet())
        self.tab_widget.setCornerWidget(btn_add_tab, Qt.TopRightCorner)

        self.main_layout.addWidget(self.tab_widget)

    def current_model(self):
        idx = self.tab_widget.currentIndex()
        if idx >= 0 and idx < len(self.sheets):
            return self.sheets[idx]["model"]
        return None

    def current_table_view(self):
        idx = self.tab_widget.currentIndex()
        if idx >= 0 and idx < len(self.sheets):
            return self.sheets[idx]["view"]
        return None

    def add_new_sheet(self, sheet_name=None):
        if not sheet_name:
            sheet_name = f"Sheet{len(self.sheets) + 1}"

        model = SpreadsheetModel(rows=100, cols=26, parent=self)
        view = QTableView(self)
        view.setModel(model)
        view.setAlternatingRowColors(False)
        view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        view.setSelectionBehavior(QAbstractItemView.SelectItems)

        view.horizontalHeader().setDefaultSectionSize(90)
        view.verticalHeader().setDefaultSectionSize(26)
        view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        selection_model = view.selectionModel()
        selection_model.currentChanged.connect(self.on_current_cell_changed)
        selection_model.selectionChanged.connect(self.on_selection_changed)

        model.dataChangedSignal.connect(self.update_status_and_formula_bar)

        sheet_info = {
            "name": sheet_name,
            "model": model,
            "view": view
        }
        self.sheets.append(sheet_info)

        idx = self.tab_widget.addTab(view, sheet_name)
        self.tab_widget.setCurrentIndex(idx)

    def _build_status_bar(self):
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.lbl_status_msg = QLabel("Ready", self)
        self.lbl_status_stats = QLabel("SUM: 0 | AVERAGE: 0 | COUNT: 0", self)

        self.status_bar.addWidget(self.lbl_status_msg, 1)
        self.status_bar.addPermanentWidget(self.lbl_status_stats, 0)

    def on_active_tab_changed(self, index):
        self.update_status_and_formula_bar()

    def on_current_cell_changed(self, current, previous):
        if not current.isValid():
            return
        row, col = current.row(), current.column()
        cell_name = coords_to_cell_name(row, col)
        self.lbl_cell_address.setText(cell_name)

        model = self.current_model()
        if model:
            raw_val = model.get_raw_value(row, col)
            self.formula_input.blockSignals(True)
            self.formula_input.setText(str(raw_val))
            self.formula_input.blockSignals(False)

            style = model.get_cell_style(row, col)
            self.toolbar_widget.update_style_state(style)

    def on_selection_changed(self, selected, deselected):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        indexes = view.selectionModel().selectedIndexes()
        if not indexes:
            self.lbl_status_stats.setText("")
            return

        numeric_vals = []
        for idx in indexes:
            val = model.get_computed_value(idx.row(), idx.column())
            if val is not None and val != "":
                try:
                    num = float(val)
                    numeric_vals.append(num)
                except (ValueError, TypeError):
                    pass

        if numeric_vals:
            sum_v = sum(numeric_vals)
            avg_v = sum_v / len(numeric_vals)
            cnt_v = len(numeric_vals)
            sum_str = int(sum_v) if sum_v.is_integer() else f"{sum_v:.2f}"
            avg_str = int(avg_v) if avg_v.is_integer() else f"{avg_v:.2f}"
            self.lbl_status_stats.setText(f"SUM: {sum_str}  |  AVERAGE: {avg_str}  |  COUNT: {cnt_v}")
        else:
            self.lbl_status_stats.setText(f"Selected: {len(indexes)} cells")

    def update_status_and_formula_bar(self):
        view = self.current_table_view()
        if view and view.currentIndex().isValid():
            self.on_current_cell_changed(view.currentIndex(), QModelIndex())

    def on_formula_submitted(self):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        curr = view.currentIndex()
        if not curr.isValid():
            return

        new_val = self.formula_input.text()
        model.setData(curr, new_val)

    def on_formula_cancelled(self):
        view = self.current_table_view()
        if view and view.currentIndex().isValid():
            self.on_current_cell_changed(view.currentIndex(), QModelIndex())

    def insert_formula_into_cell(self, formula_text):
        self.formula_input.setText(formula_text)
        self.formula_input.setFocus()
        self.formula_input.setCursorPosition(len(formula_text) - 1)

    def apply_to_selection(self, modifier_fn):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        indexes = view.selectionModel().selectedIndexes()
        if not indexes and view.currentIndex().isValid():
            indexes = [view.currentIndex()]

        for idx in indexes:
            r, c = idx.row(), idx.column()
            style = model.get_cell_style(r, c)
            modifier_fn(style)
            model.set_cell_style(r, c, style)

    def apply_font_family(self, family):
        self.apply_to_selection(lambda s: setattr(s, "font_family", family))

    def apply_font_size(self, size):
        self.apply_to_selection(lambda s: setattr(s, "font_size", size))

    def apply_bold(self, bold):
        self.apply_to_selection(lambda s: setattr(s, "bold", bold))

    def apply_italic(self, italic):
        self.apply_to_selection(lambda s: setattr(s, "italic", italic))

    def apply_underline(self, underline):
        self.apply_to_selection(lambda s: setattr(s, "underline", underline))

    def apply_alignment(self, align):
        self.apply_to_selection(lambda s: setattr(s, "alignment", align))

    def apply_text_color(self, hex_color):
        self.apply_to_selection(lambda s: setattr(s, "text_color", hex_color))

    def apply_bg_color(self, hex_color):
        self.apply_to_selection(lambda s: setattr(s, "bg_color", hex_color))

    def apply_num_format(self, fmt_name):
        self.apply_to_selection(lambda s: setattr(s, "number_format", fmt_name))

    def action_clear_formatting(self):
        self.apply_to_selection(lambda s: s.__init__())

    def action_undo(self):
        model = self.current_model()
        if model:
            model.undo()

    def action_redo(self):
        model = self.current_model()
        if model:
            model.redo()

    def action_copy(self):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        indexes = view.selectionModel().selectedIndexes()
        if not indexes:
            return

        indexes = sorted(indexes, key=lambda x: (x.row(), x.column()))
        min_r = min(x.row() for x in indexes)
        max_r = max(x.row() for x in indexes)
        min_c = min(x.column() for x in indexes)
        max_c = max(x.column() for x in indexes)

        lines = []
        for r in range(min_r, max_r + 1):
            row_vals = []
            for c in range(min_c, max_c + 1):
                raw = model.get_raw_value(r, c)
                row_vals.append(str(raw))
            lines.append("\t".join(row_vals))

        tsv_str = "\n".join(lines)
        sys_clip = QWidget().clipboard()
        sys_clip.setText(tsv_str)
        self.lbl_status_msg.setText("Copied cell selection to clipboard.")

    def action_cut(self):
        self.action_copy()
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        for idx in view.selectionModel().selectedIndexes():
            model.setData(idx, "")
        self.lbl_status_msg.setText("Cut cell selection.")

    def action_paste(self):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        curr = view.currentIndex()
        if not curr.isValid():
            return

        sys_clip = QWidget().clipboard()
        text = sys_clip.text()
        if not text:
            return

        start_r, start_c = curr.row(), curr.column()
        lines = text.splitlines()

        for r_off, line in enumerate(lines):
            cols = line.split("\t")
            for c_off, val in enumerate(cols):
                target_r = start_r + r_off
                target_c = start_c + c_off
                if target_r < model.rowCount() and target_c < model.columnCount():
                    idx = model.index(target_r, target_c)
                    model.setData(idx, val)

        self.lbl_status_msg.setText("Pasted cell content.")

    def action_expand_grid(self):
        model = self.current_model()
        if model:
            model.expand_grid(additional_rows=50, additional_cols=10)
            self.lbl_status_msg.setText("Grid expanded (+50 rows, +10 columns).")

    def action_recalculate(self):
        model = self.current_model()
        if model:
            model.recalculate_all()
            self.lbl_status_msg.setText("All formulas recalculated.")

    def action_new_file(self):
        reply = QMessageBox.question(
            self, "New Spreadsheet",
            "Are you sure you want to create a new spreadsheet? Any unsaved changes will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.tab_widget.clear()
            self.sheets.clear()
            self.current_filepath = None
            self.add_new_sheet("Sheet1")
            self.setWindowTitle("Book/Tow 1.1 - New Spreadsheet")
            self.lbl_status_msg.setText("New spreadsheet created.")

    def action_save_file(self):
        if not self.current_filepath:
            self.action_save_as_file()
        else:
            self._save_to_path(self.current_filepath)

    def action_save_as_file(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Book/Tow Spreadsheet", "", "Book/Tow Spreadsheet (*.btow);;All Files (*)"
        )
        if filepath:
            if not filepath.endswith(".btow"):
                filepath += ".btow"
            self.current_filepath = filepath
            self._save_to_path(filepath)

    def _save_to_path(self, filepath):
        try:
            sheets_data = []
            for sheet in self.sheets:
                model = sheet["model"]
                cells_dict = {}
                for (r, c), raw in model._raw_data.items():
                    cell_name = coords_to_cell_name(r, c)
                    style = model.get_cell_style(r, c)
                    cells_dict[cell_name] = {
                        "raw": raw,
                        "style": style.to_dict()
                    }
                sheets_data.append({
                    "name": sheet["name"],
                    "rows": model.rowCount(),
                    "cols": model.columnCount(),
                    "cells": cells_dict
                })

            FileManager.save_btow(filepath, sheets_data)
            self.setWindowTitle(f"Book/Tow 1.1 - {os.path.basename(filepath)}")
            self.lbl_status_msg.setText(f"File saved: {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save file:\n{e}")

    def action_open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open Book/Tow Spreadsheet", "", "Book/Tow Files (*.btow);;CSV Files (*.csv);;All Files (*)"
        )
        if not filepath:
            return

        if filepath.endswith(".csv"):
            self.action_import_csv(filepath)
            return

        try:
            sheets_data = FileManager.load_btow(filepath)
            self.tab_widget.clear()
            self.sheets.clear()

            for s_data in sheets_data:
                name = s_data.get("name", "Sheet1")
                rows = s_data.get("rows", 100)
                cols = s_data.get("cols", 26)
                cells = s_data.get("cells", {})

                self.add_new_sheet(name)
                model = self.current_model()

                for cell_name, cell_info in cells.items():
                    try:
                        r, c = cell_name_to_coords(cell_name)
                        if isinstance(cell_info, dict):
                            raw = cell_info.get("raw", "")
                            style_dict = cell_info.get("style", None)
                            if raw:
                                model.setData(model.index(r, c), raw)
                            if style_dict:
                                model.set_cell_style(r, c, CellStyle.from_dict(style_dict))
                        else:
                            model.setData(model.index(r, c), str(cell_info))
                    except Exception:
                        pass

            self.current_filepath = filepath
            self.setWindowTitle(f"Book/Tow 1.1 - {os.path.basename(filepath)}")
            self.lbl_status_msg.setText(f"File loaded: {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Open Error", f"Could not open file:\n{e}")

    def action_export_csv(self):
        model = self.current_model()
        if not model:
            return
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        if filepath:
            try:
                FileManager.export_csv(filepath, model)
                self.lbl_status_msg.setText(f"Exported CSV: {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Could not export CSV:\n{e}")

    def action_import_csv(self, filepath=None):
        if not filepath:
            filepath, _ = QFileDialog.getOpenFileName(
                self, "Import CSV", "", "CSV Files (*.csv);;All Files (*)"
            )
        if filepath:
            try:
                model = self.current_model()
                if model:
                    FileManager.import_csv(filepath, model)
                    self.lbl_status_msg.setText(f"Imported CSV: {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Could not import CSV:\n{e}")

    def action_about(self):
        QMessageBox.about(
            self,
            "About Book/Tow 1.1",
            "<h2>Book/Tow 1.1</h2>"
            "<p>A professional, cross-platform desktop spreadsheet application with "
            "an original orange visual identity.</p>"
            "<p>Features include custom formula evaluation engine, range calculations, "
            "cell formatting, undo/redo history, CSV and .btow document format support.</p>"
            "<p>Version: 1.1</p>"
        )
