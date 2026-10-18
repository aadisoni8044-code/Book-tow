import sys
import os
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Book/Tow")
    app.setApplicationVersion("1.1")
    app.setOrganizationName("BookTow")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
