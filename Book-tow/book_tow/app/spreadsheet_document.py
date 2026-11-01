"""In-memory spreadsheet document and sheet data."""

import re


DEFAULT_ROWS = 100
DEFAULT_COLUMNS = 26
FORMAT_VERSION = 1
_ADDRESS_PATTERN = re.compile(r"^([A-Z]+)([1-9][0-9]*)$")


def new_sheet(name="Sheet1"):
    return {"name": name, "cells": {}}


class SpreadsheetDocument:
    def __init__(self):
        self.sheets = [new_sheet()]
        self.rows = DEFAULT_ROWS
        self.columns = DEFAULT_COLUMNS

    def to_dict(self):
        return {
            "format": "booktow",
            "format_version": FORMAT_VERSION,
            "grid": {"rows": self.rows, "columns": self.columns},
            "sheets": self.sheets,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or data.get("format") != "booktow":
            raise ValueError("This is not a Book/Tow spreadsheet.")
        if data.get("format_version") != FORMAT_VERSION:
            raise ValueError("This Book/Tow file version is not supported.")

        grid = data.get("grid")
        sheets = data.get("sheets")
        if not isinstance(grid, dict) or not isinstance(sheets, list) or not sheets:
            raise ValueError("The spreadsheet file structure is invalid.")
        rows = grid.get("rows")
        columns = grid.get("columns")
        if (type(rows) is not int or type(columns) is not int
                or rows < 1 or columns < 1 or rows > 10000 or columns > 1000):
            raise ValueError("The spreadsheet grid dimensions are invalid.")

        document = cls()
        document.rows = rows
        document.columns = columns
        document.sheets = []
        names = set()
        for sheet in sheets:
            if not isinstance(sheet, dict):
                raise ValueError("A worksheet in this file is invalid.")
            name = sheet.get("name")
            cells = sheet.get("cells")
            if not isinstance(name, str) or not name.strip() or len(name) > 31:
                raise ValueError("A worksheet name is invalid.")
            if name.casefold() in names:
                raise ValueError("Worksheet names must be unique.")
            names.add(name.casefold())
            if not isinstance(cells, dict):
                raise ValueError("Worksheet cell data is invalid.")
            validated_cells = {}
            for address, cell in cells.items():
                match = _ADDRESS_PATTERN.fullmatch(address) if isinstance(address, str) else None
                if not match or not isinstance(cell, dict):
                    raise ValueError("A cell entry in this file is invalid.")
                column = _column_number(match.group(1))
                row = int(match.group(2))
                if row > rows or column > columns:
                    raise ValueError("A cell is outside the declared grid.")
                value = cell.get("value", "")
                style = cell.get("style", {})
                if not isinstance(value, str) or not isinstance(style, dict):
                    raise ValueError("Cell contents or formatting are invalid.")
                allowed = {"bold", "italic", "underline", "color", "background",
                           "alignment", "font_family", "font_size", "number_format",
                           "border", "borders"}
                if any(key not in allowed for key in style):
                    raise ValueError("A cell uses unsupported formatting.")
                if any(type(style.get(key)) is not bool
                       for key in ("bold", "italic", "underline", "border") if key in style):
                    raise ValueError("Cell formatting values are invalid.")
                if "borders" in style:
                    borders = style["borders"]
                    if (not isinstance(borders, dict)
                            or any(side not in {"top", "right", "bottom", "left"}
                                   for side in borders)
                            or any(type(enabled) is not bool for enabled in borders.values())):
                        raise ValueError("Cell border formatting is invalid.")
                if any(not isinstance(style.get(key), str)
                       for key in ("color", "background", "alignment", "font_family",
                                   "number_format") if key in style):
                    raise ValueError("Cell formatting values are invalid.")
                if style.get("alignment", "left") not in {"left", "center", "right"}:
                    raise ValueError("A cell alignment is invalid.")
                if style.get("number_format", "General") not in {"General", "Number", "Percent"}:
                    raise ValueError("A cell number format is invalid.")
                if any(not re.fullmatch(r"#[0-9A-Fa-f]{6}", style[key])
                       for key in ("color", "background") if key in style):
                    raise ValueError("A cell color is invalid.")
                if "font_size" in style and (
                        type(style["font_size"]) is not int or not 6 <= style["font_size"] <= 72):
                    raise ValueError("A cell font size is invalid.")
                if "font_family" in style and len(style["font_family"]) > 128:
                    raise ValueError("A cell font family is invalid.")
                validated_cells[address] = {"value": value, "style": dict(style)}
            document.sheets.append({"name": name, "cells": validated_cells})
        return document


def _column_number(name):
    value = 0
    for character in name:
        value = value * 26 + ord(character) - ord("A") + 1
    return value
