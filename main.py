"""
Main Application Entry Point for Book/Tow 1.1.
Launches the desktop spreadsheet application with orange brand theme and window metadata.
"""

import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from app.main_window import BookTowMainWindow


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("Book/Tow")
    app.setApplicationVersion("1.1")
    app.setOrganizationName("Book/Tow Software")

    icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = BookTowMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
