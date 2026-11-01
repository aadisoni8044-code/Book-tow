"""Read and safely write the documented Book/Tow JSON format."""

import json
import os
import tempfile

from book_tow.app.spreadsheet_document import SpreadsheetDocument


PROJECT_EXTENSION = ".booktow"
LEGACY_PROJECT_EXTENSION = ".btow"


def ensure_project_extension(path):
    lowered_path = path.lower()
    while lowered_path.endswith(PROJECT_EXTENSION * 2):
        path = path[:-len(PROJECT_EXTENSION)]
        lowered_path = path.lower()
    if lowered_path.endswith((PROJECT_EXTENSION, LEGACY_PROJECT_EXTENSION)):
        return path
    return path + PROJECT_EXTENSION


def load_document(path):
    try:
        with open(path, "r", encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("Could not open this spreadsheet: {}".format(error)) from error
    try:
        return SpreadsheetDocument.from_dict(data)
    except ValueError as error:
        raise ValueError("Could not open this spreadsheet: {}".format(error)) from error


def save_document(document, path):
    directory = os.path.dirname(os.path.abspath(path))
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="\n", dir=directory,
                prefix=".booktow-", suffix=".tmp", delete=False) as stream:
            temporary_path = stream.name
            json.dump(document.to_dict(), stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    except (OSError, TypeError, ValueError) as error:
        if temporary_path and os.path.exists(temporary_path):
            os.unlink(temporary_path)
        raise ValueError("Could not save this spreadsheet: {}".format(error)) from error
