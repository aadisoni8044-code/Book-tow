import json
from typing import Dict, Any, Tuple, Optional, List
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QColor, QFont, QBrush

from app.formula_engine import FormulaEngine

DEFAULT_ROWS = 100
DEFAULT_COLS = 26

class CellData:
    def __init__(self, raw_value: str = "", format_dict: Optional[Dict[str, Any]] = None):
        self.raw_value: str = str(raw_value)
        self.evaluated_value: Any = ""
        self.format: Dict[str, Any] = format_dict if format_dict is not None else {
            "font_family": "Segoe UI",
            "font_size": 10,
            "bold": False,
            "italic": False,
            "underline": False,
            "align": "left",
            "text_color": "#1E293B",
            "bg_color": "#FFFFFF",
            "number_format": "General"
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_value": self.raw_value,
            "format": self.format
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CellData":
        return cls(
            raw_value=data.get("raw_value", ""),
            format_dict=data.get("format", {})
        )


class SpreadsheetModel(QAbstractTableModel):
    """
    QAbstractTableModel for Book/Tow spreadsheet grid.
    Supports formulas, cell formatting, recalculation, and copy/paste.
    """
    data_changed_signal = Signal()

    def __init__(self, name: str = "Sheet1", rows: int = DEFAULT_ROWS, cols: int = DEFAULT_COLS, parent=None):
        super().__init__(parent)
        self.sheet_name = name
        self._rows = rows
        self._cols = cols
        self.grid: Dict[Tuple[int, int], CellData] = {}
        self.formula_engine = FormulaEngine()
        self.is_modified = False

    def rowCount(self, parent=QModelIndex()) -> int:
        return self._rows

    def columnCount(self, parent=QModelIndex()) -> int:
        return self._cols

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return FormulaEngine.col_idx_to_str(section)
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None

    def get_cell_data(self, row: int, col: int) -> CellData:
        return self.grid.setdefault((row, col), CellData())

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None

        row, col = index.row(), index.column()
        cell = self.grid.get((row, col))
        if not cell:
            return None

        if role == Qt.DisplayRole:
            return self.get_formatted_display_value(cell)

        elif role == Qt.EditRole:
            return cell.raw_value

        elif role == Qt.FontRole:
            fmt = cell.format
            font = QFont(fmt.get("font_family", "Segoe UI"), fmt.get("font_size", 10))
            font.setBold(fmt.get("bold", False))
            font.setItalic(fmt.get("italic", False))
            font.setUnderline(fmt.get("underline", False))
            return font

        elif role == Qt.TextAlignmentRole:
            align_str = cell.format.get("align", "left")
            if align_str == "center":
                return Qt.AlignCenter
            elif align_str == "right":
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        elif role == Qt.ForegroundRole:
            color_hex = cell.format.get("text_color", "#1E293B")
            return QBrush(QColor(color_hex))

        elif role == Qt.BackgroundRole:
            bg_hex = cell.format.get("bg_color", "#FFFFFF")
            if bg_hex and bg_hex.upper() != "#FFFFFF":
                return QBrush(QColor(bg_hex))
            return None

        return None

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        if not index.isValid():
            return False

        if role == Qt.EditRole:
            row, col = index.row(), index.column()
            cell = self.get_cell_data(row, col)
            cell.raw_value = str(value)
            self.recalculate_all()
            self.is_modified = True
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
            self.data_changed_signal.emit()
            return True

        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    def recalculate_all(self):
        """Recalculates evaluated values for all cells containing formulas or values."""
        def cell_lookup(r: int, c: int) -> Any:
            cell = self.grid.get((r, c))
            if not cell:
                return ""
            if cell.raw_value.startswith("="):
                return cell.raw_value
            return cell.raw_value

        for (r, c), cell in list(self.grid.items()):
            if cell.raw_value.startswith("="):
                cell.evaluated_value = self.formula_engine.evaluate(cell.raw_value, cell_lookup)
            else:
                cell.evaluated_value = self.formula_engine.evaluate(cell.raw_value, cell_lookup)

    def get_formatted_display_value(self, cell: CellData) -> str:
        val = cell.evaluated_value
        if val is None or val == "":
            return ""

        num_fmt = cell.format.get("number_format", "General")

        if isinstance(val, (int, float)):
            if num_fmt == "Number":
                return f"{val:,.2f}"
            elif num_fmt == "Currency":
                return f"${val:,.2f}"
            elif num_fmt == "Percentage":
                return f"{val * 100:.2f}%"

        return str(val)

    def format_range(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], key: str, value: Any):
        """Applies format property to specified cell range."""
        r1, c1 = top_left
        r2, c2 = bottom_right

        min_r, max_r = min(r1, r2), max(r1, r2)
        min_c, max_c = min(c1, c2), max(c1, c2)

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                cell = self.get_cell_data(r, c)
                cell.format[key] = value

        self.is_modified = True
        top_idx = self.index(min_r, min_c)
        bot_idx = self.index(max_r, max_c)
        self.dataChanged.emit(top_idx, bot_idx, [Qt.FontRole, Qt.ForegroundRole, Qt.BackgroundRole, Qt.TextAlignmentRole])
        self.data_changed_signal.emit()

    def clear_range(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int]):
        """Clears contents of specified cell range."""
        r1, c1 = top_left
        r2, c2 = bottom_right

        min_r, max_r = min(r1, r2), max(r1, r2)
        min_c, max_c = min(c1, c2), max(c1, c2)

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if (r, c) in self.grid:
                    self.grid[(r, c)].raw_value = ""
                    self.grid[(r, c)].evaluated_value = ""

        self.recalculate_all()
        self.is_modified = True
        self.dataChanged.emit(self.index(min_r, min_c), self.index(max_r, max_c))
        self.data_changed_signal.emit()

    def to_dict(self) -> Dict[str, Any]:
        """Serializes sheet to dictionary representation."""
        cells_data = {}
        for (r, c), cell in self.grid.items():
            if cell.raw_value or cell.format != CellData().format:
                cells_data[f"{r},{c}"] = cell.to_dict()

        return {
            "name": self.sheet_name,
            "rows": self._rows,
            "cols": self._cols,
            "cells": cells_data
        }

    def from_dict(self, data: Dict[str, Any]):
        """Populates sheet from dictionary representation."""
        self.sheet_name = data.get("name", "Sheet1")
        self._rows = data.get("rows", DEFAULT_ROWS)
        self._cols = data.get("cols", DEFAULT_COLS)
        self.grid.clear()

        cells_data = data.get("cells", {})
        for key, cell_dict in cells_data.items():
            r_str, c_str = key.split(",")
            r, c = int(r_str), int(c_str)
            self.grid[(r, c)] = CellData.from_dict(cell_dict)

        self.recalculate_all()
        self.is_modified = False
        self.layoutChanged.emit()
