import os
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTableView, QTabWidget, QStatusBar, QFileDialog, QMessageBox, QMenu,
    QToolBar, QPushButton, QSplitter, QHeaderView, QAbstractItemView
)
from PySide6.QtGui import QAction, QKeySequence, QIcon, QFont, QPixmap
from PySide6.QtCore import Qt, QItemSelectionModel, QModelIndex

from app.spreadsheet_model import SpreadsheetModel, CellData
from app.file_manager import FileManager, FileManagerError
from app.toolbar import MainToolbar
from app.formula_engine import FormulaEngine
from app.theme import APP_QSS, PRIMARY_ORANGE, LIGHT_ORANGE_BG, DARK_ORANGE

class MainWindow(QMainWindow):
    """
    Main Application Window for Book/Tow 1.1 Spreadsheet Software.
    Provides Top Bar, Menu Bar, Formatting Toolbar, Formula Bar, Grid, Worksheet Tabs, and Status Bar.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book/Tow 1.1")
        self.resize(1150, 750)
        self.current_filepath = None

        # Load Icon
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "app_icon", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.sheets: list[SpreadsheetModel] = []
        self.init_ui()
        self.apply_theme()
        self.create_new_spreadsheet()

    def apply_theme(self):
        self.setStyleSheet(APP_QSS)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Custom Top Bar / Header
        top_bar = QWidget()
        top_bar.setObjectName("topBar")
        top_bar.setStyleSheet(f"background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0; padding: 6px 12px;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 6, 10, 6)

        # Logo and Title
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "app_icon", "icon.png")
        if os.path.exists(icon_path):
            logo_label = QLabel()
            pix = QPixmap(icon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pix)
            top_layout.addWidget(logo_label)

        title_label = QLabel("Book/Tow 1.1")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setStyleSheet(f"color: {PRIMARY_ORANGE}; margin-left: 4px; margin-right: 20px;")
        top_layout.addWidget(title_label)

        # Quick Action Buttons
        btn_new = QPushButton("New")
        btn_new.clicked.connect(self.create_new_spreadsheet)
        top_layout.addWidget(btn_new)

        btn_open = QPushButton("Open")
        btn_open.clicked.connect(self.open_file_dialog)
        top_layout.addWidget(btn_open)

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.save_file)
        top_layout.addWidget(btn_save)

        btn_save_as = QPushButton("Save As")
        btn_save_as.clicked.connect(self.save_file_as)
        top_layout.addWidget(btn_save_as)

        top_layout.addStretch()

        main_layout.addWidget(top_bar)

        # 2. Menu Bar
        self.create_menu_bar()

        # 3. Toolbar
        self.toolbar = MainToolbar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Connect Toolbar Signals
        self.toolbar.font_changed.connect(lambda f: self.apply_cell_format("font_family", f))
        self.toolbar.font_size_changed.connect(lambda s: self.apply_cell_format("font_size", s))
        self.toolbar.bold_toggled.connect(lambda b: self.apply_cell_format("bold", b))
        self.toolbar.italic_toggled.connect(lambda i: self.apply_cell_format("italic", i))
        self.toolbar.underline_toggled.connect(lambda u: self.apply_cell_format("underline", u))
        self.toolbar.align_changed.connect(lambda a: self.apply_cell_format("align", a))
        self.toolbar.text_color_changed.connect(lambda c: self.apply_cell_format("text_color", c))
        self.toolbar.bg_color_changed.connect(lambda c: self.apply_cell_format("bg_color", c))
        self.toolbar.number_format_changed.connect(lambda f: self.apply_cell_format("number_format", f))
        self.toolbar.insert_formula_requested.connect(self.insert_formula_to_cell)

        # 4. Formula Bar Widget
        formula_bar_widget = QWidget()
        formula_bar_widget.setStyleSheet("background-color: #F8FAFC; border-bottom: 1px solid #E2E8F0; padding: 4px 8px;")
        fb_layout = QHBoxLayout(formula_bar_widget)
        fb_layout.setContentsMargins(8, 4, 8, 4)

        self.cell_address_label = QLabel("A1")
        self.cell_address_label.setObjectName("formulaLabel")
        self.cell_address_label.setFixedWidth(55)
        self.cell_address_label.setAlignment(Qt.AlignCenter)
        fb_layout.addWidget(self.cell_address_label)

        fx_lbl = QLabel("fx")
        fx_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        fx_lbl.setStyleSheet(f"color: {DARK_ORANGE}; margin: 0 6px;")
        fb_layout.addWidget(fx_lbl)

        self.formula_input = QLineEdit()
        self.formula_input.setPlaceholderText("Enter a value or formula (e.g. =SUM(A1:B10))")
        self.formula_input.returnPressed.connect(self.commit_formula_input)
        fb_layout.addWidget(self.formula_input)

        main_layout.addWidget(formula_bar_widget)

        # 5. Worksheet Tab Widget & Grid TableView
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)

        # Add '+' button for adding sheets
        add_sheet_btn = QPushButton("+ Sheet")
        add_sheet_btn.setStyleSheet(f"background-color: transparent; color: {PRIMARY_ORANGE}; border: 1px solid {PRIMARY_ORANGE}; font-weight: bold; padding: 2px 8px;")
        add_sheet_btn.clicked.connect(self.add_new_sheet)
        self.tab_widget.setCornerWidget(add_sheet_btn, Qt.TopRightCorner)

        main_layout.addWidget(self.tab_widget)

        # 6. Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")

        act_new = QAction("New Spreadsheet", self)
        act_new.setShortcut(QKeySequence.New)
        act_new.triggered.connect(self.create_new_spreadsheet)
        file_menu.addAction(act_new)

        act_open = QAction("Open...", self)
        act_open.setShortcut(QKeySequence.Open)
        act_open.triggered.connect(self.open_file_dialog)
        file_menu.addAction(act_open)

        file_menu.addSeparator()

        act_save = QAction("Save", self)
        act_save.setShortcut(QKeySequence.Save)
        act_save.triggered.connect(self.save_file)
        file_menu.addAction(act_save)

        act_save_as = QAction("Save As...", self)
        act_save_as.setShortcut(QKeySequence.SaveAs)
        act_save_as.triggered.connect(self.save_file_as)
        file_menu.addAction(act_save_as)

        file_menu.addSeparator()

        act_imp_csv = QAction("Import CSV...", self)
        act_imp_csv.triggered.connect(self.import_csv_dialog)
        file_menu.addAction(act_imp_csv)

        act_exp_csv = QAction("Export CSV...", self)
        act_exp_csv.triggered.connect(self.export_csv_dialog)
        file_menu.addAction(act_exp_csv)

        file_menu.addSeparator()

        act_exit = QAction("Exit", self)
        act_exit.setShortcut(QKeySequence.Quit)
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)

        # Edit Menu
        edit_menu = menubar.addMenu("Edit")
        act_copy = QAction("Copy", self)
        act_copy.setShortcut(QKeySequence.Copy)
        act_copy.triggered.connect(self.copy_selection)
        edit_menu.addAction(act_copy)

        act_paste = QAction("Paste", self)
        act_paste.setShortcut(QKeySequence.Paste)
        act_paste.triggered.connect(self.paste_selection)
        edit_menu.addAction(act_paste)

        act_clear = QAction("Clear Contents", self)
        act_clear.setShortcut(QKeySequence.Delete)
        act_clear.triggered.connect(self.clear_selection)
        edit_menu.addAction(act_clear)

        # View Menu
        view_menu = menubar.addMenu("View")
        act_reset_zoom = QAction("Reset View", self)
        view_menu.addAction(act_reset_zoom)

        # Insert Menu
        insert_menu = menubar.addMenu("Insert")
        act_ins_sheet = QAction("New Worksheet", self)
        act_ins_sheet.triggered.connect(self.add_new_sheet)
        insert_menu.addAction(act_ins_sheet)

        # Format Menu
        format_menu = menubar.addMenu("Format")
        act_fmt_clear = QAction("Reset Formatting", self)
        format_menu.addAction(act_fmt_clear)

        # Data Menu
        data_menu = menubar.addMenu("Data")
        act_recalc = QAction("Recalculate All Formulas", self)
        act_recalc.triggered.connect(self.recalculate_current_sheet)
        data_menu.addAction(act_recalc)

        # Help Menu
        help_menu = menubar.addMenu("Help")
        act_about = QAction("About Book/Tow 1.1", self)
        act_about.triggered.connect(self.show_about_dialog)
        help_menu.addAction(act_about)

    def current_model(self) -> SpreadsheetModel | None:
        idx = self.tab_widget.currentIndex()
        if 0 <= idx < len(self.sheets):
            return self.sheets[idx]
        return None

    def current_table_view(self) -> QTableView | None:
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, QTableView):
            return widget
        return None

    def add_sheet_tab(self, model: SpreadsheetModel):
        self.sheets.append(model)
        table_view = QTableView()
        table_view.setModel(model)
        table_view.setSelectionMode(QAbstractItemView.ContiguousSelection)
        table_view.setAlternatingRowColors(False)

        # Header sizing
        table_view.horizontalHeader().setDefaultSectionSize(90)
        table_view.verticalHeader().setDefaultSectionSize(26)

        # Connect selection changes
        selection_model = table_view.selectionModel()
        selection_model.currentChanged.connect(self.on_cell_selected)

        tab_idx = self.tab_widget.addTab(table_view, model.sheet_name)
        self.tab_widget.setCurrentIndex(tab_idx)

    def add_new_sheet(self):
        sheet_count = len(self.sheets) + 1
        model = SpreadsheetModel(f"Sheet{sheet_count}")
        self.add_sheet_tab(model)

    def close_tab(self, index: int):
        if len(self.sheets) <= 1:
            QMessageBox.information(self, "Book/Tow", "Spreadsheet document must contain at least one worksheet.")
            return

        self.sheets.pop(index)
        self.tab_widget.removeTab(index)

    def tab_changed(self, index: int):
        view = self.current_table_view()
        if view:
            current_idx = view.currentIndex()
            if current_idx.isValid():
                self.on_cell_selected(current_idx)

    def on_cell_selected(self, current: QModelIndex):
        if not current.isValid():
            return

        r, c = current.row(), current.column()
        col_str = FormulaEngine.col_idx_to_str(c)
        cell_ref = f"{col_str}{r + 1}"
        self.cell_address_label.setText(cell_ref)

        model = self.current_model()
        if model:
            cell = model.get_cell_data(r, c)
            self.formula_input.blockSignals(True)
            self.formula_input.setText(cell.raw_value)
            self.formula_input.blockSignals(False)
            self.toolbar.update_states(cell.format)

            display_val = cell.evaluated_value
            self.status_bar.showMessage(f"Selected Cell: {cell_ref} | Raw: {cell.raw_value} | Value: {display_val}")

    def commit_formula_input(self):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        current_idx = view.currentIndex()
        if not current_idx.isValid():
            current_idx = model.index(0, 0)

        val = self.formula_input.text()
        model.setData(current_idx, val, Qt.EditRole)
        self.on_cell_selected(current_idx)

    def insert_formula_to_cell(self, formula_template: str):
        self.formula_input.setText(formula_template)
        self.formula_input.setFocus()

    def apply_cell_format(self, key: str, value: any):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        selection = view.selectionModel().selection()
        if selection.isEmpty():
            current = view.currentIndex()
            if current.isValid():
                model.format_range((current.row(), current.column()), (current.row(), current.column()), key, value)
        else:
            for range_ in selection:
                top_left = (range_.top(), range_.left())
                bottom_right = (range_.bottom(), range_.right())
                model.format_range(top_left, bottom_right, key, value)

    def copy_selection(self):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        selection = view.selectionModel().selection()
        if selection.isEmpty():
            return

        range_ = selection.first()
        lines = []
        for r in range(range_.top(), range_.bottom() + 1):
            row_vals = []
            for c in range(range_.left(), range_.right() + 1):
                cell = model.get_cell_data(r, c)
                row_vals.append(cell.raw_value)
            lines.append("\t".join(row_vals))

        text_to_copy = "\n".join(lines)
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(text_to_copy)
        self.status_bar.showMessage("Selection copied to clipboard.", 3000)

    def paste_selection(self):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        from PySide6.QtWidgets import QApplication
        text = QApplication.clipboard().text()
        if not text:
            return

        start_idx = view.currentIndex()
        if not start_idx.isValid():
            start_idx = model.index(0, 0)

        start_r, start_c = start_idx.row(), start_idx.column()
        rows = text.split("\n")

        for r_offset, row_str in enumerate(rows):
            cols = row_str.split("\t")
            for c_offset, val in enumerate(cols):
                target_r = start_r + r_offset
                target_c = start_c + c_offset
                if target_r < model.rowCount() and target_c < model.columnCount():
                    idx = model.index(target_r, target_c)
                    model.setData(idx, val, Qt.EditRole)

        self.status_bar.showMessage("Pasted clipboard contents.", 3000)

    def clear_selection(self):
        view = self.current_table_view()
        model = self.current_model()
        if not view or not model:
            return

        selection = view.selectionModel().selection()
        if selection.isEmpty():
            current = view.currentIndex()
            if current.isValid():
                model.clear_range((current.row(), current.column()), (current.row(), current.column()))
        else:
            for range_ in selection:
                model.clear_range((range_.top(), range_.left()), (range_.bottom(), range_.right()))

    def create_new_spreadsheet(self):
        if self.prompt_save_changes_if_needed():
            self.sheets.clear()
            self.tab_widget.clear()
            model = SpreadsheetModel("Sheet1")
            self.add_sheet_tab(model)
            self.current_filepath = None
            self.setWindowTitle("Book/Tow 1.1 - [Untitled]")
            self.status_bar.showMessage("New spreadsheet created.")

    def open_file_dialog(self):
        if not self.prompt_save_changes_if_needed():
            return

        path, _ = QFileDialog.getOpenFileName(
            self, "Open Spreadsheet", "", "Book/Tow Files (*.btow);;All Files (*)"
        )
        if path:
            try:
                models = FileManager.load_file(path)
                self.sheets.clear()
                self.tab_widget.clear()
                for m in models:
                    self.add_sheet_tab(m)
                self.current_filepath = path
                self.setWindowTitle(f"Book/Tow 1.1 - [{os.path.basename(path)}]")
                self.status_bar.showMessage(f"Opened file: {path}")
            except FileManagerError as fe:
                QMessageBox.critical(self, "File Error", str(fe))

    def save_file(self) -> bool:
        if not self.current_filepath:
            return self.save_file_as()

        try:
            FileManager.save_file(self.current_filepath, self.sheets)
            self.setWindowTitle(f"Book/Tow 1.1 - [{os.path.basename(self.current_filepath)}]")
            self.status_bar.showMessage("File saved successfully.")
            return True
        except FileManagerError as fe:
            QMessageBox.critical(self, "Save Error", str(fe))
            return False

    def save_file_as(self) -> bool:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Spreadsheet As", "", "Book/Tow Files (*.btow)"
        )
        if path:
            if not path.endswith(".btow"):
                path += ".btow"
            self.current_filepath = path
            return self.save_file()
        return False

    def import_csv_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if path:
            model = self.current_model()
            if model:
                try:
                    FileManager.import_csv(path, model)
                    self.status_bar.showMessage(f"Imported CSV from {path}")
                except FileManagerError as fe:
                    QMessageBox.critical(self, "Import Error", str(fe))

    def export_csv_dialog(self):
        model = self.current_model()
        if not model:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Export Worksheet to CSV", "", "CSV Files (*.csv)"
        )
        if path:
            try:
                FileManager.export_csv(path, model)
                self.status_bar.showMessage(f"Exported CSV to {path}")
            except FileManagerError as fe:
                QMessageBox.critical(self, "Export Error", str(fe))

    def recalculate_current_sheet(self):
        model = self.current_model()
        if model:
            model.recalculate_all()
            model.layoutChanged.emit()
            self.status_bar.showMessage("Recalculated all formulas.", 3000)

    def prompt_save_changes_if_needed(self) -> bool:
        any_modified = any(m.is_modified for m in self.sheets)
        if any_modified:
            res = QMessageBox.question(
                self, "Save Changes",
                "You have unsaved changes. Do you want to save before proceeding?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if res == QMessageBox.Save:
                return self.save_file()
            elif res == QMessageBox.Cancel:
                return False
        return True

    def closeEvent(self, event):
        if self.prompt_save_changes_if_needed():
            event.accept()
        else:
            event.ignore()

    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About Book/Tow 1.1",
            "<h2>Book/Tow 1.1</h2>"
            "<p>A professional, cross-platform spreadsheet software.</p>"
            "<p><b>Version:</b> 1.1</p>"
            "<p>Designed with original orange identity, multi-sheet capability, custom formula evaluation engine, and .btow document format.</p>"
        )
