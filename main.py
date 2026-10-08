"""
JPS Script Studio Main Launcher
"""

import sys
import os

from PySide6.QtWidgets import QApplication
from jps_ide.ide.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    if "--test-init" in sys.argv:
        print("IDE initialized successfully for automated verification test.")
        sys.exit(0)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
