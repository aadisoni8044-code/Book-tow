"""
File Manager for Book/Tow 1.1.
Handles native .btow document format (JSON with versioning and validation)
and CSV import/export.
"""

import json
import csv
import os
import tempfile
from app.spreadsheet_model import CellStyle, coords_to_cell_name, cell_name_to_coords

FORMAT_VERSION = "1.1"


class FileManager:
    @staticmethod
    def save_btow(filepath, sheets_data):
        document = {
            "app": "Book/Tow",
            "version": FORMAT_VERSION,
            "sheets": sheets_data
        }

        dir_name = os.path.dirname(os.path.abspath(filepath))
        os.makedirs(dir_name, exist_ok=True)

        fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix=".btow_tmp_", suffix=".json")
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(document, f, indent=2, ensure_ascii=False)

            os.replace(temp_path, filepath)
            return True
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise IOError(f"Failed to save Book/Tow document: {e}")

    @staticmethod
    def load_btow(filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                document = json.load(f)
        except Exception as e:
            raise ValueError(f"Invalid or corrupted Book/Tow file: {e}")

        if not isinstance(document, dict) or document.get("app") != "Book/Tow":
            raise ValueError("File is not a valid Book/Tow document")

        sheets = document.get("sheets", [])
        if not isinstance(sheets, list) or not sheets:
            raise ValueError("Book/Tow document contains no valid worksheet data")

        return sheets

    @staticmethod
    def export_csv(filepath, model):
        dir_name = os.path.dirname(os.path.abspath(filepath))
        os.makedirs(dir_name, exist_ok=True)

        max_row = 0
        max_col = 0
        for (r, c), raw in model._raw_data.items():
            if raw:
                max_row = max(max_row, r)
                max_col = max(max_col, c)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for r in range(max_row + 1):
                row_vals = []
                for c in range(max_col + 1):
                    val = model.get_computed_value(r, c)
                    row_vals.append(val if val is not None else "")
                writer.writerow(row_vals)

    @staticmethod
    def import_csv(filepath, model):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        model.clear_sheet()

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, val in enumerate(row):
                    if val != "":
                        idx = model.index(r, c)
                        model.setData(idx, val)
