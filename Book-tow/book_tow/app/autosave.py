"""Background writer for project autosaves and recovery snapshots."""

from PySide6.QtCore import QObject, QRunnable, Signal

from book_tow.app.file_manager import save_document
from book_tow.app.recovery import (
    document_fingerprint, file_fingerprint, write_recovery,
)
from book_tow.app.spreadsheet_document import SpreadsheetDocument


class _SaveSignals(QObject):
    finished = Signal(object, object)


class AutoSaveTask(QRunnable):
    def __init__(self, snapshot, path, expected_fingerprint, recovery_directory,
                 project_id, source_path, base_fingerprint,
                 base_document_fingerprint, save_context):
        super().__init__()
        self.snapshot = snapshot
        self.path = path
        self.expected_fingerprint = expected_fingerprint
        self.recovery_directory = recovery_directory
        self.project_id = project_id
        self.source_path = source_path
        self.base_fingerprint = base_fingerprint
        self.base_document_fingerprint = base_document_fingerprint
        self.save_context = save_context
        self.signals = _SaveSignals()

    def run(self):
        project_saved = self.path is None
        project_error = None
        new_fingerprint = None
        if self.path:
            try:
                current_fingerprint = file_fingerprint(self.path)
                if current_fingerprint != self.expected_fingerprint:
                    raise ValueError(
                        "The spreadsheet file changed outside Book/Tow.")
                save_document(SpreadsheetDocument.from_dict(self.snapshot), self.path)
                new_fingerprint = file_fingerprint(self.path)
                project_saved = True
            except (OSError, TypeError, ValueError) as error:
                project_error = error

        recovery_saved = False
        recovery_error = None
        recovery_base_document_fingerprint = self.base_document_fingerprint
        recovery_base_fingerprint = self.base_fingerprint
        if project_saved and self.path:
            recovery_base_document_fingerprint = document_fingerprint(self.snapshot)
            recovery_base_fingerprint = new_fingerprint
        try:
            write_recovery(
                self.recovery_directory, self.project_id, self.snapshot,
                self.source_path, recovery_base_fingerprint,
                recovery_base_document_fingerprint)
            recovery_saved = True
        except (OSError, TypeError, ValueError) as error:
            recovery_error = error
        self.signals.finished.emit(self.save_context, {
            "project_id": self.project_id,
            "path": self.path,
            "project_saved": project_saved,
            "project_error": project_error,
            "new_fingerprint": new_fingerprint,
            "recovery_saved": recovery_saved,
            "recovery_error": recovery_error,
        })
