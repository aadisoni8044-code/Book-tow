"""Persistent, validated recovery snapshots for Book/Tow documents."""

import hashlib
import json
import os
import shutil
import tempfile
import time

from PySide6.QtCore import QStandardPaths

from book_tow.app.spreadsheet_document import SpreadsheetDocument


RECOVERY_VERSION = 1


def recovery_directory():
    return os.path.join(
        QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppLocalDataLocation),
        "recovery")


def project_id_for_path(path):
    normalized = os.path.normcase(os.path.abspath(path))
    return hashlib.sha256(os.fsencode(normalized)).hexdigest()


def file_fingerprint(path):
    if not path or not os.path.isfile(path):
        return None
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def document_fingerprint(document_data):
    serialized = json.dumps(
        document_data, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def _recovery_paths(directory, project_id):
    return (os.path.join(directory, project_id + ".json"),
            os.path.join(directory, project_id + ".previous"))


def _atomic_json_write(path, data):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="\n", dir=directory,
                prefix=".booktow-recovery-", suffix=".tmp", delete=False) as stream:
            temporary_path = stream.name
            json.dump(data, stream, ensure_ascii=False, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    except (OSError, TypeError, ValueError) as error:
        if temporary_path and os.path.exists(temporary_path):
            os.unlink(temporary_path)
        raise ValueError("Could not write recovery data: {}".format(
            type(error).__name__)) from error


def write_recovery(directory, project_id, document_data, source_path,
                   base_fingerprint, base_document_fingerprint=None):
    if not isinstance(project_id, str) or not project_id.isalnum():
        raise ValueError("The recovery project identifier is invalid.")
    if source_path and project_id_for_path(source_path) != project_id:
        raise ValueError("The recovery source does not match its project.")
    SpreadsheetDocument.from_dict(document_data)
    primary_path, previous_path = _recovery_paths(directory, project_id)
    payload = {
        "recovery_version": RECOVERY_VERSION,
        "project_id": project_id,
        "source_path": os.path.abspath(source_path) if source_path else None,
        "base_fingerprint": base_fingerprint,
        "base_document_fingerprint": base_document_fingerprint,
        "document_fingerprint": document_fingerprint(document_data),
        "updated_at": time.time(),
        "document": document_data,
    }
    os.makedirs(directory, exist_ok=True)
    if os.path.isfile(primary_path) and _load_candidate(primary_path) is not None:
        backup_temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                    dir=directory, prefix=".booktow-backup-", suffix=".tmp",
                    delete=False) as stream:
                backup_temporary = stream.name
                with open(primary_path, "rb") as previous:
                    shutil.copyfileobj(previous, stream)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(backup_temporary, previous_path)
        except OSError as error:
            if backup_temporary and os.path.exists(backup_temporary):
                os.unlink(backup_temporary)
            raise ValueError("Could not preserve the previous recovery copy: "
                             "{}".format(type(error).__name__)) from error
    _atomic_json_write(primary_path, payload)


def _load_candidate(path):
    try:
        with open(path, "r", encoding="utf-8") as stream:
            payload = json.load(stream)
        if (not isinstance(payload, dict)
                or payload.get("recovery_version") != RECOVERY_VERSION
                or not isinstance(payload.get("project_id"), str)
                or not payload["project_id"].isalnum()
                or not isinstance(payload.get("document"), dict)
                or not isinstance(payload.get("document_fingerprint"), str)
                or not isinstance(payload.get("updated_at"), (int, float))):
            return None
        document = SpreadsheetDocument.from_dict(payload["document"])
        if document_fingerprint(payload["document"]) != payload["document_fingerprint"]:
            return None
        source_path = payload.get("source_path")
        base_fingerprint = payload.get("base_fingerprint")
        base_document_fingerprint = payload.get("base_document_fingerprint")
        if source_path is not None and not isinstance(source_path, str):
            return None
        if source_path and project_id_for_path(source_path) != payload["project_id"]:
            return None
        if base_fingerprint is not None and not isinstance(base_fingerprint, str):
            return None
        if (base_document_fingerprint is not None
                and not isinstance(base_document_fingerprint, str)):
            return None
        payload["validated_document"] = document
        return payload
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError):
        return None


def recovery_candidates(directory):
    if not os.path.isdir(directory):
        return []
    newest_by_project = {}
    for filename in os.listdir(directory):
        if not filename.endswith((".json", ".previous")):
            continue
        candidate = _load_candidate(os.path.join(directory, filename))
        if candidate is None:
            continue
        project_id = candidate["project_id"]
        current = newest_by_project.get(project_id)
        if current is None or candidate["updated_at"] > current["updated_at"]:
            candidate["recovery_file"] = os.path.join(directory, filename)
            newest_by_project[project_id] = candidate
    return sorted(
        newest_by_project.values(), key=lambda candidate: candidate["updated_at"],
        reverse=True)


def discard_recovery(directory, project_id):
    for path in _recovery_paths(directory, project_id):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        except OSError as error:
            raise ValueError("Could not discard recovery data: {}".format(
                type(error).__name__)) from error
