import json
import csv
import os
from typing import List, Dict, Any, Tuple
from app.spreadsheet_model import SpreadsheetModel, CellData

BOOK_TOW_FORMAT_VERSION = "1.1"

class FileManagerError(Exception):
    """Custom exception for file operations."""
    pass

class FileManager:
    """
    Handles saving and loading .btow spreadsheet files as well as CSV import/export.
    """

    @staticmethod
    def save_file(filepath: str, models: List[SpreadsheetModel]) -> bool:
        """Saves one or multiple spreadsheet tabs into a .btow document."""
        try:
            document_data = {
                "application": "Book/Tow",
                "version": BOOK_TOW_FORMAT_VERSION,
                "sheets": [model.to_dict() for model in models]
            }

            temp_filepath = filepath + ".tmp"
            with open(temp_filepath, "w", encoding="utf-8") as f:
                json.dump(document_data, f, indent=2)

            os.replace(temp_filepath, filepath)

            for model in models:
                model.is_modified = False

            return True

        except Exception as e:
            raise FileManagerError(f"Failed to save file: {e}")

    @staticmethod
    def load_file(filepath: str) -> List[SpreadsheetModel]:
        """Loads a .btow document into a list of SpreadsheetModel objects."""
        if not os.path.exists(filepath):
            raise FileManagerError(f"File not found: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict) or data.get("application") != "Book/Tow":
                raise FileManagerError("Invalid Book/Tow document file format.")

            sheets_data = data.get("sheets", [])
            if not sheets_data:
                raise FileManagerError("Document contains no worksheets.")

            models = []
            for sheet_dict in sheets_data:
                model = SpreadsheetModel(name=sheet_dict.get("name", "Sheet1"))
                model.from_dict(sheet_dict)
                models.append(model)

            return models

        except json.JSONDecodeError:
            raise FileManagerError("Corrupted or invalid JSON data in file.")
        except Exception as e:
            raise FileManagerError(f"Failed to open file: {e}")

    @staticmethod
    def export_csv(filepath: str, model: SpreadsheetModel):
        """Exports the current sheet to CSV format."""
        try:
            max_row = 0
            max_col = 0
            for (r, c), cell in model.grid.items():
                if cell.raw_value:
                    if r > max_row:
                        max_row = r
                    if c > max_col:
                        max_col = c

            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for r in range(max_row + 1):
                    row_vals = []
                    for c in range(max_col + 1):
                        cell = model.grid.get((r, c))
                        val = cell.evaluated_value if cell else ""
                        row_vals.append(val)
                    writer.writerow(row_vals)

        except Exception as e:
            raise FileManagerError(f"Failed to export CSV: {e}")

    @staticmethod
    def import_csv(filepath: str, model: SpreadsheetModel):
        """Imports CSV file content into the given spreadsheet model."""
        if not os.path.exists(filepath):
            raise FileManagerError(f"File not found: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                model.grid.clear()
                for r_idx, row in enumerate(reader):
                    for c_idx, val in enumerate(row):
                        if val.strip():
                            cell = model.get_cell_data(r_idx, c_idx)
                            cell.raw_value = val.strip()

            model.recalculate_all()
            model.is_modified = True
            model.layoutChanged.emit()

        except Exception as e:
            raise FileManagerError(f"Failed to import CSV: {e}")
