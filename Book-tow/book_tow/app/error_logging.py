"""Privacy-conscious logging for unexpected application and file errors."""

import logging
import os
import sys
import traceback
from logging.handlers import RotatingFileHandler

from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import QMessageBox


LOGGER = logging.getLogger("booktow")


def configure_error_logging():
    data_directory = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppLocalDataLocation)
    log_path = os.path.join(data_directory, "logs", "booktow.log")
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        handler = RotatingFileHandler(
            log_path, maxBytes=1_000_000, backupCount=2, encoding="utf-8")
    except OSError as error:
        QMessageBox.warning(
            None, "Error Logging Unavailable",
            "Book/Tow could not create its error log ({}).".format(
                type(error).__name__))
        return

    LOGGER.setLevel(logging.ERROR)
    LOGGER.addHandler(handler)
    LOGGER.propagate = False
    default_exception_hook = sys.excepthook

    def handle_unhandled_exception(error_type, _error, error_traceback):
        if issubclass(error_type, KeyboardInterrupt):
            default_exception_hook(error_type, _error, error_traceback)
            return
        LOGGER.error("Unhandled application exception (%s)", error_type.__name__)
        for frame in traceback.extract_tb(error_traceback):
            LOGGER.error(
                "%s:%d in %s", os.path.basename(frame.filename),
                frame.lineno, frame.name)
        QMessageBox.critical(
            None, "Unexpected Error",
            "Book/Tow encountered an unexpected error. Diagnostic details "
            "were saved to:\n{}\n\nSpreadsheet contents and file paths are "
            "not included.".format(log_path))

    sys.excepthook = handle_unhandled_exception


def log_file_operation_error(operation, error):
    LOGGER.error(
        "Spreadsheet %s failed (%s)", operation, type(error).__name__)
