"""Per-user Windows registration for the .booktow project file type."""

import os
import sys


FILE_EXTENSION = ".booktow"
PROGRAM_ID = "BookTow.Project"
DESCRIPTION = "Book/Tow Project"


def _application_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))


def _open_command(executable_path):
    executable = os.path.abspath(executable_path)
    if getattr(sys, "frozen", False):
        return '"{}" "%1"'.format(executable)
    application_root = _application_root()
    entry_point = os.path.join(application_root, "main.py")
    return '"{}" "{}" "%1"'.format(executable, entry_point)


def register_file_association(executable_path=None):
    if os.name != "nt":
        raise OSError("Book/Tow file association registration is only available on Windows.")

    import winreg

    executable_path = executable_path or sys.executable
    command = _open_command(executable_path)
    icon_path = (os.path.abspath(executable_path) if getattr(sys, "frozen", False)
                 else os.path.join(_application_root(), "assets", "book_tow.ico"))
    classes_root = r"Software\Classes"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, classes_root + "\\" + FILE_EXTENSION) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, PROGRAM_ID)
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, classes_root + "\\" + PROGRAM_ID) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, DESCRIPTION)
    with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            classes_root + "\\" + PROGRAM_ID + r"\DefaultIcon") as key:
        winreg.SetValueEx(
            key, "", 0, winreg.REG_SZ, '"{}",0'.format(icon_path))
    with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            classes_root + "\\" + PROGRAM_ID + r"\shell\open\command") as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
    with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            classes_root + "\\" + FILE_EXTENSION + r"\OpenWithProgids") as key:
        winreg.SetValueEx(key, PROGRAM_ID, 0, winreg.REG_NONE, b"")

    capabilities_path = r"Software\BookTow\Capabilities"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, capabilities_path) as key:
        winreg.SetValueEx(key, "ApplicationName", 0, winreg.REG_SZ, "Book/Tow")
        winreg.SetValueEx(
            key, "ApplicationDescription", 0, winreg.REG_SZ,
            "Open and edit Book/Tow project files.")
    with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, capabilities_path + r"\FileAssociations") as key:
        winreg.SetValueEx(key, FILE_EXTENSION, 0, winreg.REG_SZ, PROGRAM_ID)
    with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\RegisteredApplications") as key:
        winreg.SetValueEx(
            key, "Book/Tow", 0, winreg.REG_SZ, capabilities_path)
    import ctypes

    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, None, None)
