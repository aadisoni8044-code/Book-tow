"""
Spreadsheet Table Model for Book/Tow 1.1.
Implements PySide6 QAbstractTableModel with formula dependency tracking,
cell formatting, cell style management, and undo/redo capabilities.
"""

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QFont, QColor
from app.formula_engine import evaluate_formula, cell_name_to_coords, coords_to_cell_name


class CellStyle:
    def __init__(self):
        self.font_family = "Segoe UI"
        self.font_size = 10
        self.bold = False
        self.italic = False
        self.underline = False
        self.alignment = Qt.AlignLeft | Qt.AlignVCenter
        self.text_color = "#1F2937"
        self.bg_color = "#FFFFFF"
        self.border_top = False
        self.border_bottom = False
        self.border_left = False
        self.border_right = False
        self.number_format = "General"  # General, Number, Currency, Percentage, Plain Text

    def to_dict(self):
        return {
            "font_family": self.font_family,
            "font_size": self.font_size,
            "bold": self.bold,
            "italic": self.italic,
            "underline": self.underline,
            "align": int(self.alignment),
            "text_color": self.text_color,
            "bg_color": self.bg_color,
            "borders": {
                "top": self.border_top,
                "bottom": self.border_bottom,
                "left": self.border_left,
                "right": self.border_right
            },
            "num_format": self.number_format
        }

    @classmethod
    def from_dict(cls, d):
        s = cls()
        s.font_family = d.get("font_family", "Segoe UI")
        s.font_size = d.get("font_size", 10)
        s.bold = d.get("bold", False)
        s.italic = d.get("italic", False)
        s.underline = d.get("underline", False)
        s.alignment = Qt.AlignmentFlag(d.get("align", int(Qt.AlignLeft | Qt.AlignVCenter)))
        s.text_color = d.get("text_color", "#1F2937")
        s.bg_color = d.get("bg_color", "#FFFFFF")
        borders = d.get("borders", {})
        s.border_top = borders.get("top", False)
        s.border_bottom = borders.get("bottom", False)
        s.border_left = borders.get("left", False)
        s.border_right = borders.get("right", False)
        s.number_format = d.get("num_format", "General")
        return s


class SpreadsheetModel(QAbstractTableModel):
    dataChangedSignal = Signal()

    def __init__(self, rows=100, cols=26, parent=None):
        super().__init__(parent)
        self._rows = rows
        self._cols = cols

        # Storage structures
        self._raw_data = {}  # (row, col) -> raw input string / formula
        self._computed_data = {}  # (row, col) -> evaluated value
        self._styles = {}  # (row, col) -> CellStyle object

        # Undo / Redo history stacks
        self._undo_stack = []
        self._redo_stack = []

    def rowCount(self, parent=QModelIndex()):
        return self._rows

    def columnCount(self, parent=QModelIndex()):
        return self._cols

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return coords_to_cell_name(0, section)[:-1]
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        pos = (index.row(), index.column())

        if role in (Qt.DisplayRole, Qt.EditRole):
            if role == Qt.EditRole:
                return self._raw_data.get(pos, "")

            # DisplayRole - formatted value
            val = self._computed_data.get(pos, "")
            style = self._styles.get(pos, None)
            return self.format_value(val, style.number_format if style else "General")

        elif role == Qt.FontRole:
            style = self._styles.get(pos)
            if style:
                font = QFont(style.font_family, style.font_size)
                font.setBold(style.bold)
                font.setItalic(style.italic)
                font.setUnderline(style.underline)
                return font

        elif role == Qt.TextAlignmentRole:
            style = self._styles.get(pos)
            if style:
                return style.alignment
            return int(Qt.AlignLeft | Qt.AlignVCenter)

        elif role == Qt.ForegroundRole:
            style = self._styles.get(pos)
            if style and style.text_color:
                return QColor(style.text_color)

        elif role == Qt.BackgroundRole:
            style = self._styles.get(pos)
            if style and style.bg_color and style.bg_color.upper() != "#FFFFFF":
                return QColor(style.bg_color)

        return None

    def format_value(self, val, num_format):
        if val is None or val == "":
            return ""

        if str(val).startswith("#"):
            return str(val)  # Error string like #DIV/0!

        if num_format == "General" or num_format == "Plain Text":
            return str(val)

        try:
            num = float(val)
            if num_format == "Number":
                return f"{num:,.2f}"
            elif num_format == "Currency":
                return f"${num:,.2f}"
            elif num_format == "Percentage":
                return f"{num * 100:.2f}%"
        except (ValueError, TypeError):
            pass

        return str(val)

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False

        row, col = index.row(), index.column()
        pos = (row, col)
        old_val = self._raw_data.get(pos, "")
        new_val = str(value) if value is not None else ""

        if old_val == new_val:
            return False

        # Record undo
        self._push_undo({"type": "set_data", "pos": pos, "old": old_val, "new": new_val})

        self._set_cell_internal(pos, new_val)
        self.recalculate_all()

        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        self.dataChangedSignal.emit()
        return True

    def _set_cell_internal(self, pos, new_val):
        if new_val == "":
            self._raw_data.pop(pos, None)
            self._computed_data.pop(pos, None)
        else:
            self._raw_data[pos] = new_val

    def get_raw_value(self, row, col):
        return self._raw_data.get((row, col), "")

    def get_computed_value(self, row, col):
        return self._computed_data.get((row, col), "")

    def get_cell_style(self, row, col):
        pos = (row, col)
        if pos not in self._styles:
            self._styles[pos] = CellStyle()
        return self._styles[pos]

    def set_cell_style(self, row, col, style):
        pos = (row, col)
        old_style = self._styles.get(pos, CellStyle()).to_dict()
        new_style = style.to_dict()

        if old_style != new_style:
            self._push_undo({"type": "set_style", "pos": pos, "old": old_style, "new": new_style})
            self._styles[pos] = style
            idx = self.index(row, col)
            self.dataChanged.emit(idx, idx)
            self.dataChangedSignal.emit()

    def get_cell_value_by_ref(self, cell_ref, visiting=None):
        if visiting is None:
            visiting = set()

        try:
            row, col = cell_name_to_coords(cell_ref)
        except Exception:
            return "#REF!"

        cell_id = cell_ref.upper()
        if cell_id in visiting:
            return "#CIRCULAR!"

        visiting.add(cell_id)

        raw = self.get_raw_value(row, col)
        if not raw:
            visiting.remove(cell_id)
            return 0

        if raw.startswith('='):
            res = evaluate_formula(raw, lambda ref, v=visiting: self.get_cell_value_by_ref(ref, set(v)), set(visiting))
            visiting.remove(cell_id)
            return res

        visiting.remove(cell_id)
        try:
            return float(raw) if '.' in raw else int(raw)
        except ValueError:
            return raw

    def recalculate_all(self):
        for pos, raw in list(self._raw_data.items()):
            if raw.startswith('='):
                cell_name = coords_to_cell_name(pos[0], pos[1])
                val = evaluate_formula(raw, lambda ref, v=None: self.get_cell_value_by_ref(ref, v), {cell_name})
                self._computed_data[pos] = val
            else:
                try:
                    self._computed_data[pos] = float(raw) if '.' in raw else int(raw)
                except ValueError:
                    self._computed_data[pos] = raw

        top_left = self.index(0, 0)
        bottom_right = self.index(self._rows - 1, self._cols - 1)
        self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole])

    def _push_undo(self, cmd):
        self._undo_stack.append(cmd)
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            return
        cmd = self._undo_stack.pop()
        self._redo_stack.append(cmd)

        if cmd["type"] == "set_data":
            pos = cmd["pos"]
            self._set_cell_internal(pos, cmd["old"])
            self.recalculate_all()
            idx = self.index(pos[0], pos[1])
            self.dataChanged.emit(idx, idx)
            self.dataChangedSignal.emit()
        elif cmd["type"] == "set_style":
            pos = cmd["pos"]
            self._styles[pos] = CellStyle.from_dict(cmd["old"])
            idx = self.index(pos[0], pos[1])
            self.dataChanged.emit(idx, idx)
            self.dataChangedSignal.emit()

    def redo(self):
        if not self._redo_stack:
            return
        cmd = self._redo_stack.pop()
        self._undo_stack.append(cmd)

        if cmd["type"] == "set_data":
            pos = cmd["pos"]
            self._set_cell_internal(pos, cmd["new"])
            self.recalculate_all()
            idx = self.index(pos[0], pos[1])
            self.dataChanged.emit(idx, idx)
            self.dataChangedSignal.emit()
        elif cmd["type"] == "set_style":
            pos = cmd["pos"]
            self._styles[pos] = CellStyle.from_dict(cmd["new"])
            idx = self.index(pos[0], pos[1])
            self.dataChanged.emit(idx, idx)
            self.dataChangedSignal.emit()

    def clear_sheet(self):
        self.beginResetModel()
        self._raw_data.clear()
        self._computed_data.clear()
        self._styles.clear()
        self._undo_stack.clear()
        self._redo_stack.clear()
        self.endResetModel()

    def expand_grid(self, additional_rows=0, additional_cols=0):
        if additional_rows > 0:
            self.beginInsertRows(QModelIndex(), self._rows, self._rows + additional_rows - 1)
            self._rows += additional_rows
            self.endInsertRows()
        if additional_cols > 0:
            self.beginInsertColumns(QModelIndex(), self._cols, self._cols + additional_cols - 1)
            self._cols += additional_cols
            self.endInsertColumns()
