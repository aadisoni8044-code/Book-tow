"""Qt table model for the spreadsheet grid."""

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QUndoCommand
from PySide6.QtWidgets import QApplication, QStyledItemDelegate

from book_tow.app.formula_engine import FormulaError, column_name, evaluate_formula


def cell_address(row, column):
    return "{}{}".format(column_name(column + 1), row + 1)


class _CellEditCommand(QUndoCommand):
    def __init__(self, model, row, column, old_value, new_value):
        super().__init__("Edit cell")
        self.model = model
        self.row = row
        self.column = column
        self.sheet_index = model.active_sheet
        self.old_value = old_value
        self.new_value = new_value

    def redo(self):
        self.model.set_raw_value(
            self.row, self.column, self.new_value, self.sheet_index)

    def undo(self):
        self.model.set_raw_value(
            self.row, self.column, self.old_value, self.sheet_index)


class SpreadsheetDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        borders = index.data(Qt.ItemDataRole.UserRole) or {}
        if borders:
            painter.save()
            theme = QApplication.instance().property("bookTowTheme")
            color = QColor("#9B805F" if theme == "dark" else "#B7A58F")
            painter.setPen(QPen(color, 1))
            rect = option.rect.adjusted(0, 0, -1, -1)
            lines = {
                "top": (rect.topLeft(), rect.topRight()),
                "right": (rect.topRight(), rect.bottomRight()),
                "bottom": (rect.bottomLeft(), rect.bottomRight()),
                "left": (rect.topLeft(), rect.bottomLeft()),
            }
            for side, (start, end) in lines.items():
                if borders.get(side, False):
                    painter.drawLine(start, end)
            painter.restore()


class SpreadsheetModel(QAbstractTableModel):
    def __init__(self, document, undo_stack, parent=None):
        super().__init__(parent)
        self.document = document
        self.undo_stack = undo_stack
        self.active_sheet = 0

    @property
    def sheet(self):
        return self.document.sheets[self.active_sheet]

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else self.document.rows

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else self.document.columns

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return column_name(section + 1)
        return str(section + 1)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        address = cell_address(index.row(), index.column())
        cell = self.sheet["cells"].get(address, {"value": "", "style": {}})
        raw = cell.get("value", "")
        style = cell.get("style", {})

        if role == Qt.ItemDataRole.EditRole:
            return raw
        if role == Qt.ItemDataRole.DisplayRole:
            try:
                value = self._calculated_value(address, set())
            except FormulaError:
                return "#ERROR!" if raw.startswith("=") else raw
            if style.get("number_format") == "Percent" and isinstance(value, (int, float)):
                return "{:.0%}".format(value)
            if style.get("number_format") == "Number" and isinstance(value, (int, float)):
                return "{:,.2f}".format(value)
            return str(value) if raw.startswith("=") else raw
        if role == Qt.ItemDataRole.ToolTipRole and raw.startswith("="):
            try:
                self._calculated_value(address, set())
            except FormulaError as error:
                return str(error)
        if role == Qt.ItemDataRole.FontRole:
            font = QFont(style.get("font_family") or "Aptos")
            font.setPointSize(style.get("font_size", 10))
            font.setBold(style.get("bold", False))
            font.setItalic(style.get("italic", False))
            font.setUnderline(style.get("underline", False))
            return font
        if role == Qt.ItemDataRole.ForegroundRole and style.get("color"):
            color = QColor(style["color"])
            return color if color.isValid() else None
        if role == Qt.ItemDataRole.BackgroundRole and style.get("background"):
            color = QColor(style["background"])
            return color if color.isValid() else None
        if role == Qt.ItemDataRole.TextAlignmentRole:
            alignment = style.get("alignment", "left")
            horizontal = {
                "left": Qt.AlignmentFlag.AlignLeft,
                "center": Qt.AlignmentFlag.AlignHCenter,
                "right": Qt.AlignmentFlag.AlignRight,
            }.get(alignment, Qt.AlignmentFlag.AlignLeft)
            return int(horizontal | Qt.AlignmentFlag.AlignVCenter)
        if role == Qt.ItemDataRole.UserRole:
            borders = style.get("borders", {})
            if style.get("border", False):
                return {side: True for side in ("top", "right", "bottom", "left")}
            return borders
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return (Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsEditable)

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role != Qt.ItemDataRole.EditRole or not index.isValid():
            return False
        new_value = str(value)
        old_value = self.raw_value(index.row(), index.column())
        if old_value == new_value:
            return True
        if self.undo_stack is not None:
            self.undo_stack.push(
                _CellEditCommand(self, index.row(), index.column(), old_value, new_value))
        else:
            self.set_raw_value(index.row(), index.column(), new_value)
        return True

    def set_raw_value(self, row, column, value, sheet_index=None):
        address = cell_address(row, column)
        sheet_index = self.active_sheet if sheet_index is None else sheet_index
        cells = self.document.sheets[sheet_index]["cells"]
        cell = cells.setdefault(address, {"value": "", "style": {}})
        cell["value"] = value
        if not value and not cell["style"]:
            cells.pop(address)
        if sheet_index == self.active_sheet:
            self._emit_cell_and_formula_updates()

    def raw_value(self, row, column):
        return self.sheet["cells"].get(
            cell_address(row, column), {"value": ""}).get("value", "")

    def set_active_sheet(self, index):
        if index == self.active_sheet:
            return
        self.beginResetModel()
        self.active_sheet = index
        self.endResetModel()

    def refresh(self):
        self._emit_all_formulas()

    def apply_style(self, indexes, key, value):
        addresses = {cell_address(index.row(), index.column()) for index in indexes}
        for address in addresses:
            cell = self.sheet["cells"].setdefault(address, {"value": "", "style": {}})
            if value is None or (key == "number_format" and not value):
                cell["style"].pop(key, None)
            else:
                cell["style"][key] = value
            if not cell["value"] and not cell["style"]:
                self.sheet["cells"].pop(address)
        if addresses:
            self._emit_all_formulas()

    def apply_borders(self, indexes, operation):
        sides = {"top", "right", "bottom", "left"}
        if operation not in sides | {"all", "outside", "remove"}:
            raise ValueError("Unsupported cell border operation.")
        positions = {(index.row(), index.column()) for index in indexes}
        if not positions:
            return

        for row, column in positions:
            address = cell_address(row, column)
            cell = self.sheet["cells"].setdefault(address, {"value": "", "style": {}})
            style = cell["style"]
            borders = style.setdefault("borders", {})
            if style.pop("border", False):
                borders.update({side: True for side in sides})

            if operation == "remove":
                style.pop("borders", None)
            elif operation == "all":
                borders.update({side: True for side in sides})
            else:
                neighbors = {
                    "top": (row - 1, column),
                    "right": (row, column + 1),
                    "bottom": (row + 1, column),
                    "left": (row, column - 1),
                }
                selected_sides = sides if operation == "outside" else {operation}
                for side in selected_sides:
                    if neighbors[side] not in positions:
                        borders[side] = True

            if not style.get("borders"):
                style.pop("borders", None)
            if not style and not cell["value"]:
                self.sheet["cells"].pop(address)

        self._emit_all_formulas()

    def _calculated_value(self, address, visiting):
        if address in visiting:
            raise FormulaError("This formula creates a circular reference.")
        raw = self.sheet["cells"].get(address, {}).get("value", "")
        if not isinstance(raw, str) or not raw.startswith("="):
            return raw
        next_visiting = set(visiting)
        next_visiting.add(address)
        return evaluate_formula(
            raw, lambda reference: self._calculated_value(reference, next_visiting))

    def _emit_cell_and_formula_updates(self):
        top_left = self.index(0, 0)
        bottom_right = self.index(self.rowCount() - 1, self.columnCount() - 1)
        self.dataChanged.emit(
            top_left, bottom_right,
            [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole])

    def _emit_all_formulas(self):
        if self.rowCount() and self.columnCount():
            self.dataChanged.emit(
                self.index(0, 0), self.index(self.rowCount() - 1, self.columnCount() - 1))
